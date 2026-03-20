"""Agente Scraper — Descarga contenido de Instagram y TikTok."""

import os
import subprocess
import json
import instaloader
from datetime import datetime
from config.settings import DATA_DIR, DOWNLOADS_DIR, YT_DLP_PATH


class ScraperAgent:
    """Descarga videos y metadata de perfiles de Instagram y TikTok."""

    def __init__(self):
        self.loader = instaloader.Instaloader(
            download_videos=True,
            download_video_thumbnails=True,
            download_comments=False,
            save_metadata=True,
            compress_json=False,
            dirname_pattern=os.path.join(DOWNLOADS_DIR, "instagram", "{profile}"),
            filename_pattern="{date_utc}__{shortcode}",
        )
        os.makedirs(os.path.join(DOWNLOADS_DIR, "instagram"), exist_ok=True)
        os.makedirs(os.path.join(DOWNLOADS_DIR, "tiktok"), exist_ok=True)

    def scrape_instagram_profile(self, username, max_posts=5):
        """Descarga los últimos posts/reels de un perfil de Instagram."""
        print(f"[Scraper] Descargando perfil de Instagram: @{username}")
        results = []
        try:
            profile = instaloader.Profile.from_username(
                self.loader.context, username
            )
            profile_info = {
                "username": username,
                "full_name": profile.full_name,
                "followers": profile.followers,
                "following": profile.followees,
                "posts_count": profile.mediacount,
                "bio": profile.biography,
                "platform": "instagram",
            }

            count = 0
            for post in profile.get_posts():
                if count >= max_posts:
                    break
                post_data = {
                    "shortcode": post.shortcode,
                    "url": f"https://www.instagram.com/p/{post.shortcode}/",
                    "caption": post.caption or "",
                    "likes": post.likes,
                    "comments": post.comments,
                    "date": post.date_utc.isoformat(),
                    "is_video": post.is_video,
                    "video_url": post.video_url if post.is_video else None,
                    "typename": post.typename,
                    "hashtags": list(post.caption_hashtags) if post.caption_hashtags else [],
                }

                # Descargar el video si es video/reel
                if post.is_video and post.video_url:
                    video_dir = os.path.join(DOWNLOADS_DIR, "instagram", username)
                    os.makedirs(video_dir, exist_ok=True)
                    video_path = os.path.join(
                        video_dir, f"{post.shortcode}.mp4"
                    )
                    if not os.path.exists(video_path):
                        try:
                            self.loader.download_post(post, target=username)
                            post_data["local_video_path"] = video_path
                        except Exception as e:
                            print(f"  [!] Error descargando video {post.shortcode}: {e}")
                            post_data["local_video_path"] = None
                    else:
                        post_data["local_video_path"] = video_path

                results.append(post_data)
                count += 1
                print(f"  [+] Post {count}/{max_posts}: {post.shortcode} ({'video' if post.is_video else 'imagen'})")

            return {"profile": profile_info, "posts": results}

        except Exception as e:
            print(f"  [!] Error con perfil @{username}: {e}")
            return {"profile": {"username": username, "error": str(e)}, "posts": []}

    def scrape_tiktok_profile(self, username, max_videos=5):
        """Descarga los últimos videos de un perfil de TikTok usando yt-dlp."""
        print(f"[Scraper] Descargando perfil de TikTok: @{username}")
        results = []
        video_dir = os.path.join(DOWNLOADS_DIR, "tiktok", username)
        os.makedirs(video_dir, exist_ok=True)

        profile_url = f"https://www.tiktok.com/@{username}"

        try:
            # Obtener metadata de los videos del perfil
            cmd = [
                YT_DLP_PATH,
                "--dump-json",
                "--playlist-items", f"1-{max_videos}",
                "--no-download",
                "--sleep-interval", "3",      # 3s entre requests para evitar rate limiting
                "--retries", "3",             # reintentos ante fallos temporales
                "--fragment-retries", "3",
                "--extractor-retries", "3",
                "--no-warnings",              # suprimir warnings de impersonation (no críticos)
                profile_url,
            ]
            result = subprocess.run(
                cmd, capture_output=True, text=True, timeout=180
            )

            if result.returncode != 0:
                error_msg = result.stderr[:500]
                print(f"  [!] Error obteniendo metadata de TikTok @{username}:")
                print(f"      {error_msg}")
                # Intentar con cookies del navegador como fallback
                cmd_fallback = [
                    YT_DLP_PATH,
                    "--dump-json",
                    "--playlist-items", f"1-{max_videos}",
                    "--no-download",
                    "--cookies-from-browser", "safari",
                    "--sleep-interval", "3",
                    "--retries", "3",
                    "--no-warnings",
                    profile_url,
                ]
                print(f"  [~] Reintentando con cookies de Safari...")
                result = subprocess.run(
                    cmd_fallback, capture_output=True, text=True, timeout=180
                )
                if result.returncode != 0:
                    print(f"  [!] Fallback también falló: {result.stderr[:200]}")
                    return {"profile": {"username": username, "platform": "tiktok", "error": result.stderr[:200]}, "videos": []}

            # Parsear cada línea JSON (una por video)
            for line in result.stdout.strip().split("\n"):
                if not line.strip():
                    continue
                try:
                    video_data = json.loads(line)
                    video_info = {
                        "id": video_data.get("id"),
                        "url": video_data.get("webpage_url"),
                        "title": video_data.get("title", ""),
                        "description": video_data.get("description", ""),
                        "duration": video_data.get("duration"),
                        "view_count": video_data.get("view_count"),
                        "like_count": video_data.get("like_count"),
                        "comment_count": video_data.get("comment_count"),
                        "share_count": video_data.get("repost_count"),
                        "date": video_data.get("upload_date"),
                        "uploader": video_data.get("uploader"),
                        "platform": "tiktok",
                    }

                    # Descargar el video
                    video_path = os.path.join(video_dir, f"{video_data.get('id', 'unknown')}.mp4")
                    if not os.path.exists(video_path):
                        dl_cmd = [
                            YT_DLP_PATH,
                            "-o", video_path,
                            "--retries", "3",
                            "--sleep-interval", "2",
                            "--no-warnings",
                            video_data.get("webpage_url", profile_url),
                        ]
                        dl_result = subprocess.run(dl_cmd, capture_output=True, text=True, timeout=120)
                        if dl_result.returncode == 0:
                            video_info["local_video_path"] = video_path
                            print(f"  [+] Video descargado: {video_data.get('id')}")
                        else:
                            video_info["local_video_path"] = None
                            print(f"  [!] Error descargando {video_data.get('id')}: {dl_result.stderr[:150]}")
                    else:
                        video_info["local_video_path"] = video_path
                        print(f"  [=] Video ya descargado: {video_data.get('id')}")

                    results.append(video_info)
                except json.JSONDecodeError:
                    continue

            profile_info = {
                "username": username,
                "platform": "tiktok",
                "videos_found": len(results),
            }
            return {"profile": profile_info, "videos": results}

        except subprocess.TimeoutExpired:
            print(f"  [!] Timeout al procesar @{username}")
            return {"profile": {"username": username, "platform": "tiktok", "error": "timeout"}, "videos": []}
        except Exception as e:
            print(f"  [!] Error con perfil @{username}: {e}")
            return {"profile": {"username": username, "platform": "tiktok", "error": str(e)}, "videos": []}

    def scrape_profiles(self, profiles):
        """Procesa una lista de perfiles. Formato: {'platform': 'instagram'|'tiktok', 'username': '...'}"""
        all_results = []
        for p in profiles:
            platform = p["platform"]
            username = p["username"]
            if platform == "instagram":
                result = self.scrape_instagram_profile(username)
            elif platform == "tiktok":
                result = self.scrape_tiktok_profile(username)
            else:
                print(f"  [!] Plataforma no soportada: {platform}")
                continue
            all_results.append(result)

        # Guardar resultados en JSON
        output_path = os.path.join(DATA_DIR, f"scrape_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json")
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(all_results, f, ensure_ascii=False, indent=2)
        print(f"[Scraper] Resultados guardados en: {output_path}")
        return all_results

"""Pipeline principal — Orquesta todos los agentes de Proper MKT."""

import sys
import os
import json
import re
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from agents.scraper import ScraperAgent
from agents.viewer import ViewerAgent
from agents.organizer import OrganizerAgent
from agents.analyzer import AnalyzerAgent
from config.settings import MONITORED_PROFILES, DATA_DIR


def run_pipeline(profiles, max_posts=5):
    """Ejecuta el pipeline completo sin base de datos (modo local)."""
    print("=" * 60)
    print("  PROPER MKT — Pipeline de Análisis de Contenido")
    print("=" * 60)

    scraper = ScraperAgent()
    scraped_data = scraper.scrape_profiles(profiles)

    viewer = ViewerAgent()
    analyses = viewer.batch_analyze(scraped_data)

    organizer = OrganizerAgent()
    report_path, report = organizer.generate_markdown_report(scraped_data, analyses)
    organizer.save_full_analysis(scraped_data, analyses)

    analyzer = AnalyzerAgent()
    patterns = analyzer.analyze_patterns(analyses)
    competitive = analyzer.compare_profiles(scraped_data)

    print(f"\n  PIPELINE COMPLETADO — Reporte: {report_path}")
    return {
        "scraped_data": scraped_data,
        "analyses": analyses,
        "report_path": report_path,
        "patterns": patterns,
        "competitive": competitive,
    }


def run_pipeline_with_db(profiles, max_posts=5):
    """Ejecuta el pipeline completo guardando resultados en PostgreSQL."""
    from database import (
        init_db, upsert_profile, upsert_post, insert_analysis,
        insert_content_idea, log_pipeline_run, update_pipeline_run,
    )

    init_db()
    run_id = log_pipeline_run("running")
    errors = []
    profiles_scraped = 0
    posts_found = 0
    videos_analyzed = 0

    print("=" * 60)
    print("  PROPER MKT — Pipeline con DB")
    print(f"  Run ID: {run_id}")
    print("=" * 60)

    try:
        # PASO 1: Scraping
        print("\n[1/4] Scraping de contenido...")
        scraper = ScraperAgent()
        viewer = ViewerAgent()
        analyzer = AnalyzerAgent()

        all_analyses = []

        for profile_config in profiles:
            platform = profile_config["platform"]
            username = profile_config["username"]
            is_competitor = profile_config.get("is_competitor", True)

            try:
                if platform == "instagram":
                    data = scraper.scrape_instagram_profile(username, max_posts)
                    profile_info = data.get("profile", {})
                    items = data.get("posts", [])

                    # Save profile to DB
                    db_profile_id = upsert_profile({
                        "username": username,
                        "platform": platform,
                        "full_name": profile_info.get("full_name"),
                        "bio": profile_info.get("bio"),
                        "followers": profile_info.get("followers", 0),
                        "following": profile_info.get("following", 0),
                        "posts_count": profile_info.get("posts_count", 0),
                        "profile_url": f"https://www.instagram.com/{username}/",
                    })
                    profiles_scraped += 1

                    # Save posts
                    for item in items:
                        try:
                            published = None
                            if item.get("date"):
                                try:
                                    published = datetime.fromisoformat(item["date"])
                                except (ValueError, TypeError):
                                    pass

                            db_post_id = upsert_post({
                                "profile_id": db_profile_id,
                                "platform": platform,
                                "post_id": item.get("shortcode", ""),
                                "post_url": item.get("url", ""),
                                "post_type": item.get("typename", ""),
                                "caption": item.get("caption", ""),
                                "hashtags": item.get("hashtags", []),
                                "likes": item.get("likes", 0),
                                "comments": item.get("comments", 0),
                                "views": item.get("view_count", 0),
                                "shares": 0,
                                "saves": 0,
                                "duration_seconds": None,
                                "is_video": item.get("is_video", False),
                                "thumbnail_url": None,
                                "video_url": item.get("video_url"),
                                "published_at": published,
                            })
                            posts_found += 1

                            # Analyze with Gemini
                            analysis_result = _analyze_and_store(
                                viewer, db_post_id, item, platform
                            )
                            if analysis_result:
                                videos_analyzed += 1
                                all_analyses.append(analysis_result)

                        except Exception as e:
                            errors.append(f"Post {item.get('shortcode')}: {e}")

                elif platform == "tiktok":
                    data = scraper.scrape_tiktok_profile(username, max_posts)
                    profile_info = data.get("profile", {})
                    items = data.get("videos", [])

                    db_profile_id = upsert_profile({
                        "username": username,
                        "platform": platform,
                        "full_name": profile_info.get("uploader"),
                        "bio": None,
                        "followers": 0,
                        "following": 0,
                        "posts_count": profile_info.get("videos_found", 0),
                        "profile_url": f"https://www.tiktok.com/@{username}",
                    })
                    profiles_scraped += 1

                    for item in items:
                        try:
                            published = None
                            if item.get("date"):
                                try:
                                    published = datetime.strptime(item["date"], "%Y%m%d")
                                except (ValueError, TypeError):
                                    pass

                            db_post_id = upsert_post({
                                "profile_id": db_profile_id,
                                "platform": platform,
                                "post_id": item.get("id", ""),
                                "post_url": item.get("url", ""),
                                "post_type": "video",
                                "caption": item.get("description", ""),
                                "hashtags": [],
                                "likes": item.get("like_count", 0),
                                "comments": item.get("comment_count", 0),
                                "views": item.get("view_count", 0),
                                "shares": item.get("share_count", 0),
                                "saves": 0,
                                "duration_seconds": item.get("duration"),
                                "is_video": True,
                                "thumbnail_url": None,
                                "video_url": item.get("url"),
                                "published_at": published,
                            })
                            posts_found += 1

                            analysis_result = _analyze_and_store(
                                viewer, db_post_id, item, platform
                            )
                            if analysis_result:
                                videos_analyzed += 1
                                all_analyses.append(analysis_result)

                        except Exception as e:
                            errors.append(f"TikTok {item.get('id')}: {e}")

            except Exception as e:
                errors.append(f"Profile @{username}: {e}")

        # PASO 4: Generate content ideas from patterns
        print("\n[4/4] Generando ideas de contenido...")
        if all_analyses:
            try:
                patterns = analyzer.analyze_patterns(all_analyses)
                if patterns.get("status") == "success":
                    _extract_and_store_ideas(patterns.get("strategic_analysis", ""))
            except Exception as e:
                errors.append(f"Pattern analysis: {e}")

        # Update pipeline run
        update_pipeline_run(run_id, {
            "status": "completed",
            "profiles_scraped": profiles_scraped,
            "posts_found": posts_found,
            "videos_analyzed": videos_analyzed,
            "errors": "; ".join(errors[:5]) if errors else None,
            "summary": f"Scraped {profiles_scraped} profiles, {posts_found} posts, analyzed {videos_analyzed} items.",
        })

        print(f"\n  PIPELINE COMPLETADO")
        print(f"  Perfiles: {profiles_scraped} | Posts: {posts_found} | Analizados: {videos_analyzed}")
        if errors:
            print(f"  Errores: {len(errors)}")

    except Exception as e:
        update_pipeline_run(run_id, {
            "status": "error",
            "profiles_scraped": profiles_scraped,
            "posts_found": posts_found,
            "videos_analyzed": videos_analyzed,
            "errors": str(e),
            "summary": f"Pipeline failed: {e}",
        })
        raise


def _analyze_and_store(viewer, db_post_id, item, platform):
    """Analyze a post/video with Gemini and store the analysis. Skips if already analyzed."""
    from database import insert_analysis, has_analysis

    # Skip if already analyzed — avoids redundant Gemini API calls
    if has_analysis(db_post_id):
        print(f"  [=] Ya analizado (post_id={db_post_id}), omitiendo.")
        return None

    # Analyze metadata
    item_copy = dict(item)
    item_copy["platform"] = platform
    metadata = viewer.analyze_post_metadata(item_copy)

    # Analyze video if available
    video_path = item.get("local_video_path")
    video_analysis = None
    if video_path and os.path.exists(video_path):
        video_analysis = viewer.analyze_video(video_path)

    full_text = ""
    if metadata.get("status") == "success":
        full_text += metadata.get("analysis", "")
    if video_analysis and video_analysis.get("status") == "success":
        full_text += "\n\n" + video_analysis.get("analysis", "")

    if not full_text.strip():
        return None

    # Extract structured fields from analysis
    hook_type = _extract_field(full_text, r"(?:hook|gancho).*?:\s*(.+?)(?:\n|$)", "")
    main_topic = _extract_field(full_text, r"(?:tema principal|main topic).*?:\s*(.+?)(?:\n|$)", "")
    summary = full_text[:500] if full_text else ""

    try:
        insert_analysis({
            "post_id": db_post_id,
            "analysis_type": "full",
            "hook_type": hook_type[:100] if hook_type else None,
            "hook_text": None,
            "narrative_structure": None,
            "main_topic": main_topic[:255] if main_topic else None,
            "key_points": None,
            "visual_style": None,
            "production_quality": None,
            "audio_type": None,
            "cta_text": None,
            "cta_type": None,
            "engagement_score": None,
            "replicability_score": None,
            "full_analysis": full_text,
            "summary": summary,
        })
    except Exception as e:
        print(f"  [!] Error saving analysis: {e}")

    return {
        "source": item.get("url") or item.get("shortcode", "unknown"),
        "platform": platform,
        "video_analysis": video_analysis or {"status": "no_video"},
        "metadata_analysis": metadata,
    }


def _extract_field(text, pattern, default=""):
    """Extract a field from analysis text using regex."""
    match = re.search(pattern, text, re.IGNORECASE)
    return match.group(1).strip() if match else default


def _extract_and_store_ideas(strategic_text):
    """Extract content ideas from strategic analysis and store them."""
    from database import insert_content_idea

    # Try to extract numbered ideas from the plan section
    ideas_section = re.search(
        r"PLAN DE CONTENIDO.*?\n([\s\S]*?)(?:\n##|\Z)", strategic_text, re.IGNORECASE
    )
    if not ideas_section:
        return

    # Split by numbered items
    items = re.split(r"\n\d+[\.\)]\s+", ideas_section.group(1))
    for item_text in items:
        item_text = item_text.strip()
        if len(item_text) < 10:
            continue

        lines = item_text.split("\n")
        title = lines[0][:255]
        description = "\n".join(lines[1:])[:500] if len(lines) > 1 else ""

        hook = _extract_field(item_text, r"hook.*?:\s*(.+?)(?:\n|$)")
        cta = _extract_field(item_text, r"cta.*?:\s*(.+?)(?:\n|$)")
        plat = "instagram"
        if "tiktok" in item_text.lower():
            plat = "tiktok"

        try:
            insert_content_idea({
                "title": title,
                "description": description,
                "hook_suggestion": hook[:255] if hook else None,
                "structure": None,
                "cta_suggestion": cta[:255] if cta else None,
                "platform": plat,
                "content_type": "video",
                "priority": "medium",
                "tags": ["auto-generated"],
                "inspired_by": None,
            })
        except Exception:
            pass


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Proper MKT Pipeline")
    parser.add_argument("--db", action="store_true", help="Save results to PostgreSQL")
    parser.add_argument("--max-posts", type=int, default=3, help="Max posts per profile")
    args = parser.parse_args()

    profiles = MONITORED_PROFILES
    if args.db:
        run_pipeline_with_db(profiles, args.max_posts)
    else:
        run_pipeline(profiles, args.max_posts)

"""Script de validación — Verifica que podemos acceder a los perfiles y usar Gemini."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from config.settings import GEMINI_API_KEY, GEMINI_MODEL, YT_DLP_PATH


def validate_gemini():
    """Valida conexión con Gemini API."""
    print("[1/3] Validando Gemini API...")
    try:
        import google.generativeai as genai
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(GEMINI_MODEL)
        response = model.generate_content("Di 'OK' si estás funcionando correctamente.")
        print(f"  ✅ Gemini API OK — Respuesta: {response.text.strip()[:50]}")
        return True
    except Exception as e:
        print(f"  ❌ Gemini API FALLÓ: {e}")
        return False


def validate_instagram():
    """Valida acceso a perfiles de Instagram."""
    print("[2/3] Validando acceso a Instagram...")
    try:
        import instaloader
        loader = instaloader.Instaloader()
        profile = instaloader.Profile.from_username(loader.context, "100ladrillos")
        print(f"  ✅ Instagram OK — @{profile.username}: {profile.followers} seguidores, {profile.mediacount} posts")

        # Verificar que podemos ver posts
        count = 0
        for post in profile.get_posts():
            is_video = "VIDEO" if post.is_video else "IMAGEN"
            print(f"  📌 Post: {post.shortcode} | {is_video} | {post.likes} likes | {post.date_utc.strftime('%Y-%m-%d')}")
            count += 1
            if count >= 3:
                break
        return True
    except Exception as e:
        print(f"  ❌ Instagram FALLÓ: {e}")
        return False


def validate_tiktok():
    """Valida acceso a perfiles de TikTok."""
    print("[3/3] Validando acceso a TikTok...")
    try:
        import subprocess
        result = subprocess.run(
            [YT_DLP_PATH, "--dump-json", "--playlist-items", "1-2", "--no-download",
             "https://www.tiktok.com/@capitalizarme.com"],
            capture_output=True, text=True, timeout=60
        )
        if result.returncode == 0:
            import json
            lines = result.stdout.strip().split("\n")
            for line in lines:
                data = json.loads(line)
                print(f"  ✅ TikTok OK — Video: {data.get('id')} | {data.get('view_count', 'N/A')} vistas | {data.get('title', '')[:60]}")
            return True
        else:
            print(f"  ⚠️  TikTok con problemas: {result.stderr[:200]}")
            return False
    except Exception as e:
        print(f"  ❌ TikTok FALLÓ: {e}")
        return False


if __name__ == "__main__":
    print("=" * 50)
    print("  PROPER MKT — Validación del Sistema")
    print("=" * 50)
    print()

    results = {
        "gemini": validate_gemini(),
        "instagram": validate_instagram(),
        "tiktok": validate_tiktok(),
    }

    print()
    print("=" * 50)
    print("  RESUMEN")
    print("=" * 50)
    for service, ok in results.items():
        status = "✅ OK" if ok else "❌ FALLÓ"
        print(f"  {service.upper():12s} {status}")

    all_ok = all(results.values())
    print()
    if all_ok:
        print("🚀 Todo listo. Puedes ejecutar: python3 pipeline.py")
    else:
        print("⚠️  Algunos servicios fallaron. Revisa los errores arriba.")

    sys.exit(0 if all_ok else 1)

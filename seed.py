"""Seed script — Loads initial data into the database."""

import sys
import os
import json

sys.path.insert(0, os.path.dirname(__file__))

from database import init_db, get_connection
from config.settings import MONITORED_PROFILES, DATA_DIR


def seed_best_practices():
    """Load best practices from JSON into the database."""
    config_dir = os.path.join(os.path.dirname(__file__), "config")
    filepath = os.path.join(config_dir, "best_practices.json")
    if not os.path.exists(filepath):
        print("[Seed] No best_practices.json found, skipping.")
        return

    with open(filepath, "r", encoding="utf-8") as f:
        practices = json.load(f)

    conn = get_connection()
    cur = conn.cursor()

    for bp in practices:
        cur.execute("""
            INSERT INTO best_practices (category, title, description, platform, relevance_score)
            VALUES (%(category)s, %(title)s, %(description)s, %(platform)s, %(relevance_score)s)
            ON CONFLICT DO NOTHING;
        """, bp)

    conn.commit()
    cur.close()
    conn.close()
    print(f"[Seed] {len(practices)} best practices loaded.")


def seed_profiles():
    """Seed monitored profiles into the database."""
    from database import upsert_profile

    for p in MONITORED_PROFILES:
        upsert_profile({
            "username": p["username"],
            "platform": p["platform"],
            "full_name": None,
            "bio": None,
            "followers": 0,
            "following": 0,
            "posts_count": 0,
            "profile_url": f"https://www.instagram.com/{p['username']}/" if p["platform"] == "instagram"
                          else f"https://www.tiktok.com/@{p['username']}",
        })
    print(f"[Seed] {len(MONITORED_PROFILES)} profiles seeded.")


if __name__ == "__main__":
    init_db()
    seed_profiles()
    seed_best_practices()
    print("[Seed] Done.")

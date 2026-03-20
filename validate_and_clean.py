#!/usr/bin/env python3
"""Validate and Clean — scans generated_content in the database,
validates each entry against Proper's brand rules, and optionally
deletes or flags invalid content.

Usage:
    python validate_and_clean.py              # Report only (dry run)
    python validate_and_clean.py --fix        # Delete critical, flag warnings
    python validate_and_clean.py --delete-all # Delete ALL invalid content
"""

import argparse
import sys
import json
import psycopg2
from psycopg2.extras import RealDictCursor

# Allow running from project root or from any location
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from agents.content_validator import ContentValidator
from config.settings import DATABASE_URL


def get_connection():
    """Get a database connection."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def fetch_all_generated_content(conn):
    """Fetch all generated_content rows."""
    cur = conn.cursor()
    cur.execute("""
        SELECT id, content_type, title, platform, raw_text,
               script_json, carousel_json, status, difficulty,
               created_at
        FROM generated_content
        ORDER BY id;
    """)
    rows = cur.fetchall()
    cur.close()
    return rows


def validate_all(conn, validator):
    """Validate every generated_content row. Returns list of results."""
    rows = fetch_all_generated_content(conn)
    results = []

    for row in rows:
        content_dict = {
            "title": row.get("title", ""),
            "raw_text": row.get("raw_text", ""),
            "script_json": row.get("script_json"),
            "carousel_json": row.get("carousel_json"),
        }
        validation = validator.validate_content(content_dict)
        results.append({
            "id": row["id"],
            "title": row["title"],
            "content_type": row["content_type"],
            "validation": validation,
        })

    return results


def print_report(results):
    """Print a human-readable validation report."""
    total = len(results)
    clean = sum(1 for r in results if r["validation"]["severity"] == "clean")
    warnings = sum(1 for r in results if r["validation"]["severity"] == "warning")
    critical = sum(1 for r in results if r["validation"]["severity"] == "critical")

    print("=" * 70)
    print("  PROPER MKT — Content Validation Report")
    print("=" * 70)
    print(f"  Total entries:  {total}")
    print(f"  Clean:          {clean}")
    print(f"  Warnings:       {warnings}")
    print(f"  Critical:       {critical}")
    print("=" * 70)

    for r in results:
        v = r["validation"]
        if v["severity"] == "clean":
            status_icon = "[OK]"
        elif v["severity"] == "warning":
            status_icon = "[WARN]"
        else:
            status_icon = "[CRIT]"

        print(f"\n{status_icon} ID={r['id']} | {r['content_type']} | {r['title']}")

        if v["issues"]:
            for issue in v["issues"]:
                print(f"    - {issue}")

        if v["corrected_fields"]:
            print(f"    Suggested corrections: {v['corrected_fields']}")

    print("\n" + "=" * 70)


def delete_content(conn, content_id, title):
    """Delete a generated_content row by ID."""
    cur = conn.cursor()
    cur.execute("DELETE FROM generated_content WHERE id = %s;", (content_id,))
    conn.commit()
    cur.close()
    print(f"  DELETED: ID={content_id} — {title}")


def flag_content(conn, content_id, title):
    """Flag a generated_content row by setting status to 'flagged'."""
    cur = conn.cursor()
    cur.execute(
        "UPDATE generated_content SET status = 'flagged' WHERE id = %s;",
        (content_id,),
    )
    conn.commit()
    cur.close()
    print(f"  FLAGGED: ID={content_id} — {title}")


def apply_fixes(conn, results, delete_all_invalid=False):
    """Apply fixes based on validation results.

    - Critical issues: always deleted
    - Warnings: flagged (or deleted if --delete-all)
    """
    actions_taken = 0

    for r in results:
        v = r["validation"]
        if v["severity"] == "critical":
            delete_content(conn, r["id"], r["title"])
            actions_taken += 1
        elif v["severity"] == "warning":
            if delete_all_invalid:
                delete_content(conn, r["id"], r["title"])
            else:
                flag_content(conn, r["id"], r["title"])
            actions_taken += 1

    if actions_taken == 0:
        print("\n  No actions needed — all content is clean.")
    else:
        print(f"\n  Total actions taken: {actions_taken}")


def main():
    parser = argparse.ArgumentParser(
        description="Validate and clean generated content in Proper MKT database."
    )
    parser.add_argument(
        "--fix",
        action="store_true",
        help="Delete critical issues, flag warnings.",
    )
    parser.add_argument(
        "--delete-all",
        action="store_true",
        help="Delete ALL invalid content (critical + warnings).",
    )
    args = parser.parse_args()

    validator = ContentValidator()
    conn = get_connection()

    try:
        results = validate_all(conn, validator)
        print_report(results)

        if args.fix or args.delete_all:
            print("\n--- Applying fixes ---")
            apply_fixes(conn, results, delete_all_invalid=args.delete_all)
        else:
            # Check if there are issues
            has_issues = any(r["validation"]["severity"] != "clean" for r in results)
            if has_issues:
                print("\nRun with --fix to delete critical and flag warnings,")
                print("or --delete-all to remove all invalid content.")
    finally:
        conn.close()


if __name__ == "__main__":
    main()

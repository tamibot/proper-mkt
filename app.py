"""Flask Web Application — Proper MKT Dashboard."""

import sys
import os
import json
from datetime import datetime

sys.path.insert(0, os.path.dirname(__file__))

from flask import Flask, render_template, jsonify, request
from flask_cors import CORS
from config.settings import FLASK_PORT, FLASK_DEBUG
from database import (
    init_db, get_all_profiles, get_posts_with_analysis,
    get_content_ideas, get_pipeline_runs, get_dashboard_stats,
)

app = Flask(__name__, template_folder="templates", static_folder="static")
CORS(app)

# Start scheduler when app starts
_scheduler = None
def _start_scheduler_once():
    global _scheduler
    if _scheduler is None:
        try:
            from scheduler import start_scheduler
            _scheduler = start_scheduler()
        except Exception as e:
            print(f"[App] Scheduler warning: {e}")

_start_scheduler_once()


@app.before_request
def ensure_db():
    """Initialize DB on first request."""
    if not getattr(app, '_db_initialized', False):
        try:
            init_db()
            app._db_initialized = True
        except Exception as e:
            print(f"[DB] Warning: {e}")


# --- API Endpoints ---

@app.route("/api/stats")
def api_stats():
    try:
        stats = get_dashboard_stats()
        # Serialize datetime objects
        if stats.get("last_run"):
            for k, v in stats["last_run"].items():
                if isinstance(v, datetime):
                    stats["last_run"][k] = v.isoformat()
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profiles")
def api_profiles():
    try:
        profiles = get_all_profiles()
        result = []
        for p in profiles:
            row = dict(p)
            for k, v in row.items():
                if isinstance(v, datetime):
                    row[k] = v.isoformat()
            result.append(row)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/posts")
def api_posts():
    try:
        platform = request.args.get("platform")
        profile_id = request.args.get("profile_id")
        limit = int(request.args.get("limit", 50))
        posts = get_posts_with_analysis(limit=limit, platform=platform, profile_id=profile_id)
        result = []
        for p in posts:
            row = dict(p)
            for k, v in row.items():
                if isinstance(v, datetime):
                    row[k] = v.isoformat()
            result.append(row)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ideas")
def api_ideas():
    try:
        status = request.args.get("status")
        ideas = get_content_ideas(status=status)
        result = []
        for i in ideas:
            row = dict(i)
            for k, v in row.items():
                if isinstance(v, datetime):
                    row[k] = v.isoformat()
            result.append(row)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/runs")
def api_runs():
    try:
        runs = get_pipeline_runs()
        result = []
        for r in runs:
            row = dict(r)
            for k, v in row.items():
                if isinstance(v, datetime):
                    row[k] = v.isoformat()
            result.append(row)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/best-practices")
def api_best_practices():
    try:
        conn = __import__('database').get_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM best_practices ORDER BY relevance_score DESC;")
        rows = cur.fetchall()
        cur.close()
        conn.close()
        result = []
        for r in rows:
            row = dict(r)
            for k, v in row.items():
                if isinstance(v, datetime):
                    row[k] = v.isoformat()
            result.append(row)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/trigger-pipeline", methods=["POST"])
def api_trigger():
    """Manually trigger the pipeline."""
    try:
        from pipeline import run_pipeline_with_db
        from config.settings import MONITORED_PROFILES
        # Run in background thread
        import threading
        thread = threading.Thread(
            target=run_pipeline_with_db,
            args=(MONITORED_PROFILES, 5),
            daemon=True,
        )
        thread.start()
        return jsonify({"status": "Pipeline iniciado", "message": "El pipeline se está ejecutando en segundo plano."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Web Pages ---

@app.route("/")
def index():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)

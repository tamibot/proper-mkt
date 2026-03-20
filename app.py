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
    get_generated_content, get_analyses_for_generation,
    insert_generated_content, get_posts_with_analysis_datefilter,
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


def _serialize(rows):
    """Serialize query results, converting datetime objects."""
    result = []
    for r in rows:
        row = dict(r)
        for k, v in row.items():
            if isinstance(v, datetime):
                row[k] = v.isoformat()
        result.append(row)
    return result


# --- API Endpoints ---

@app.route("/api/stats")
def api_stats():
    try:
        stats = get_dashboard_stats()
        if stats.get("last_run"):
            for k, v in stats["last_run"].items():
                if isinstance(v, datetime):
                    stats["last_run"][k] = v.isoformat()
        # Add generated content count
        try:
            generated = get_generated_content(limit=1000)
            stats["total_scripts"] = sum(1 for g in generated if g.get("content_type") == "video_script")
            stats["total_carousels"] = sum(1 for g in generated if g.get("content_type") == "carousel_plan")
        except Exception:
            stats["total_scripts"] = 0
            stats["total_carousels"] = 0
        return jsonify(stats)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/profiles")
def api_profiles():
    try:
        return jsonify(_serialize(get_all_profiles()))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/posts")
def api_posts():
    try:
        platform = request.args.get("platform")
        profile_id = request.args.get("profile_id")
        date_from = request.args.get("date_from")
        date_to = request.args.get("date_to")
        limit = int(request.args.get("limit", 100))
        posts = get_posts_with_analysis_datefilter(
            limit=limit, platform=platform, profile_id=profile_id,
            date_from=date_from, date_to=date_to
        )
        return jsonify(_serialize(posts))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/ideas")
def api_ideas():
    try:
        status = request.args.get("status")
        return jsonify(_serialize(get_content_ideas(status=status)))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/runs")
def api_runs():
    try:
        return jsonify(_serialize(get_pipeline_runs()))
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
        return jsonify(_serialize(rows))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generated-content")
def api_generated_content():
    """Get all generated content (scripts + carousels)."""
    try:
        content_type = request.args.get("type")
        limit = int(request.args.get("limit", 50))
        content = get_generated_content(content_type=content_type, limit=limit)
        return jsonify(_serialize(content))
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/generate-content", methods=["POST"])
def api_generate_content():
    """Generate new content (video script or carousel) from existing analyses."""
    try:
        from agents.content_generator import ContentGeneratorAgent
        generator = ContentGeneratorAgent()

        req = request.get_json() or {}
        content_type = req.get("type", "both")
        topic = req.get("topic")
        limit = int(req.get("limit", 5))

        analyses = get_analyses_for_generation(limit=limit)
        if not analyses:
            return jsonify({"error": "No hay analisis disponibles. Ejecuta el pipeline primero."}), 400

        generated = []
        for analysis in analyses:
            analysis_dict = dict(analysis)
            analysis_text = analysis_dict.get("full_analysis") or analysis_dict.get("summary") or ""
            if len(analysis_text) < 50:
                continue

            # Generate video script
            if content_type in ("both", "video_script"):
                result = generator.generate_video_script(
                    analysis_text,
                    platform=analysis_dict.get("platform", "tiktok"),
                    topic=topic,
                )
                if result.get("status") == "success":
                    script = result.get("script") or {}
                    content_id = insert_generated_content({
                        "content_type": "video_script",
                        "title": script.get("titulo", f"Video basado en @{analysis_dict.get('username', 'unknown')}"),
                        "platform": script.get("plataforma", analysis_dict.get("platform", "tiktok")),
                        "source_post_id": analysis_dict.get("post_id"),
                        "script_json": json.dumps(script) if script else None,
                        "carousel_json": None,
                        "raw_text": result.get("raw", ""),
                        "difficulty": script.get("nivel_dificultad", "medio"),
                    })
                    generated.append({"id": content_id, "type": "video_script", "title": script.get("titulo", "")})

            # Generate carousel
            if content_type in ("both", "carousel_plan"):
                result = generator.generate_carousel_plan(
                    analysis_text,
                    platform="instagram",
                    topic=topic,
                )
                if result.get("status") == "success":
                    carousel = result.get("carousel") or {}
                    content_id = insert_generated_content({
                        "content_type": "carousel_plan",
                        "title": carousel.get("titulo", f"Carrusel basado en @{analysis_dict.get('username', 'unknown')}"),
                        "platform": "instagram",
                        "source_post_id": analysis_dict.get("post_id"),
                        "script_json": None,
                        "carousel_json": json.dumps(carousel) if carousel else None,
                        "raw_text": result.get("raw", ""),
                        "difficulty": carousel.get("nivel_dificultad", "medio"),
                    })
                    generated.append({"id": content_id, "type": "carousel_plan", "title": carousel.get("titulo", "")})

        return jsonify({
            "status": "success",
            "generated": generated,
            "message": f"Se generaron {len(generated)} piezas de contenido."
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route("/api/trigger-pipeline", methods=["POST"])
def api_trigger():
    """Manually trigger the pipeline."""
    try:
        from pipeline import run_pipeline_with_db
        from config.settings import MONITORED_PROFILES
        import threading
        thread = threading.Thread(
            target=run_pipeline_with_db,
            args=(MONITORED_PROFILES, 5),
            daemon=True,
        )
        thread.start()
        return jsonify({"status": "Pipeline iniciado", "message": "El pipeline se esta ejecutando en segundo plano."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# --- Web Pages ---

@app.route("/")
def index():
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=FLASK_PORT, debug=FLASK_DEBUG)

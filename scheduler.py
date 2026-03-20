"""Scheduler — Ejecuta el pipeline diariamente a las 7 AM."""

import sys
import os

sys.path.insert(0, os.path.dirname(__file__))

from apscheduler.schedulers.background import BackgroundScheduler
from config.settings import SCHEDULER_HOUR, SCHEDULER_MINUTE, MONITORED_PROFILES


def scheduled_pipeline():
    """Tarea programada que ejecuta el pipeline."""
    print(f"[Scheduler] Ejecutando pipeline programado...")
    try:
        from pipeline import run_pipeline_with_db
        run_pipeline_with_db(MONITORED_PROFILES, max_posts=5)
        print("[Scheduler] Pipeline completado.")
    except Exception as e:
        print(f"[Scheduler] Error en pipeline: {e}")


def scheduled_news_fetch():
    """Tarea programada que busca noticias del sector."""
    print(f"[Scheduler] Ejecutando búsqueda de noticias...")
    try:
        from agents.news_agent import fetch_news
        results = fetch_news()
        print(f"[Scheduler] Noticias encontradas: {len(results)}")
    except Exception as e:
        print(f"[Scheduler] Error en búsqueda de noticias: {e}")


def start_scheduler():
    """Inicia el scheduler con la tarea diaria."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(
        scheduled_pipeline,
        trigger="cron",
        hour=SCHEDULER_HOUR,
        minute=SCHEDULER_MINUTE,
        id="daily_pipeline",
        replace_existing=True,
    )
    scheduler.add_job(
        scheduled_news_fetch,
        trigger="interval",
        days=3,
        id="news_fetch",
        replace_existing=True,
    )
    scheduler.start()
    print(f"[Scheduler] Pipeline programado para las {SCHEDULER_HOUR:02d}:{SCHEDULER_MINUTE:02d} diariamente.")
    print(f"[Scheduler] Búsqueda de noticias programada cada 3 días.")
    return scheduler

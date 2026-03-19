"""Database module — PostgreSQL models and operations for Proper MKT."""

import os
import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
from config.settings import DATABASE_URL


def get_connection():
    """Get a database connection."""
    return psycopg2.connect(DATABASE_URL, cursor_factory=RealDictCursor)


def init_db():
    """Initialize all database tables."""
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS profiles (
            id SERIAL PRIMARY KEY,
            username VARCHAR(100) NOT NULL,
            platform VARCHAR(20) NOT NULL,
            full_name VARCHAR(255),
            bio TEXT,
            followers INTEGER DEFAULT 0,
            following INTEGER DEFAULT 0,
            posts_count INTEGER DEFAULT 0,
            profile_url VARCHAR(500),
            is_competitor BOOLEAN DEFAULT FALSE,
            is_reference BOOLEAN DEFAULT TRUE,
            created_at TIMESTAMP DEFAULT NOW(),
            updated_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(username, platform)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS posts (
            id SERIAL PRIMARY KEY,
            profile_id INTEGER REFERENCES profiles(id) ON DELETE CASCADE,
            platform VARCHAR(20) NOT NULL,
            post_id VARCHAR(100),
            post_url VARCHAR(500),
            post_type VARCHAR(50),
            caption TEXT,
            hashtags TEXT[],
            likes INTEGER DEFAULT 0,
            comments INTEGER DEFAULT 0,
            views INTEGER DEFAULT 0,
            shares INTEGER DEFAULT 0,
            saves INTEGER DEFAULT 0,
            duration_seconds INTEGER,
            is_video BOOLEAN DEFAULT FALSE,
            thumbnail_url VARCHAR(1000),
            video_url VARCHAR(1000),
            published_at TIMESTAMP,
            scraped_at TIMESTAMP DEFAULT NOW(),
            UNIQUE(post_id, platform)
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS analyses (
            id SERIAL PRIMARY KEY,
            post_id INTEGER REFERENCES posts(id) ON DELETE CASCADE,
            analysis_type VARCHAR(50) NOT NULL,
            hook_type VARCHAR(100),
            hook_text TEXT,
            narrative_structure TEXT,
            main_topic VARCHAR(255),
            key_points TEXT,
            visual_style VARCHAR(100),
            production_quality VARCHAR(50),
            audio_type VARCHAR(100),
            cta_text TEXT,
            cta_type VARCHAR(100),
            engagement_score FLOAT,
            replicability_score FLOAT,
            full_analysis TEXT,
            summary TEXT,
            analyzed_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS content_ideas (
            id SERIAL PRIMARY KEY,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            hook_suggestion TEXT,
            structure TEXT,
            cta_suggestion TEXT,
            platform VARCHAR(20),
            content_type VARCHAR(50),
            priority VARCHAR(20) DEFAULT 'medium',
            status VARCHAR(20) DEFAULT 'idea',
            inspired_by INTEGER REFERENCES posts(id),
            tags TEXT[],
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS pipeline_runs (
            id SERIAL PRIMARY KEY,
            started_at TIMESTAMP DEFAULT NOW(),
            completed_at TIMESTAMP,
            status VARCHAR(20) DEFAULT 'running',
            profiles_scraped INTEGER DEFAULT 0,
            posts_found INTEGER DEFAULT 0,
            videos_analyzed INTEGER DEFAULT 0,
            errors TEXT,
            summary TEXT
        );
    """)

    cur.execute("""
        CREATE TABLE IF NOT EXISTS best_practices (
            id SERIAL PRIMARY KEY,
            category VARCHAR(100) NOT NULL,
            title VARCHAR(255) NOT NULL,
            description TEXT,
            source VARCHAR(255),
            platform VARCHAR(20),
            relevance_score FLOAT DEFAULT 0.5,
            created_at TIMESTAMP DEFAULT NOW()
        );
    """)

    conn.commit()
    cur.close()
    conn.close()
    print("[DB] Tablas inicializadas correctamente.")


# --- CRUD Operations ---

def upsert_profile(data):
    """Insert or update a profile."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO profiles (username, platform, full_name, bio, followers, following, posts_count, profile_url)
        VALUES (%(username)s, %(platform)s, %(full_name)s, %(bio)s, %(followers)s, %(following)s, %(posts_count)s, %(profile_url)s)
        ON CONFLICT (username, platform) DO UPDATE SET
            full_name = EXCLUDED.full_name,
            bio = EXCLUDED.bio,
            followers = EXCLUDED.followers,
            following = EXCLUDED.following,
            posts_count = EXCLUDED.posts_count,
            updated_at = NOW()
        RETURNING id;
    """, data)
    profile_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return profile_id


def upsert_post(data):
    """Insert or update a post."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO posts (profile_id, platform, post_id, post_url, post_type, caption, hashtags,
                          likes, comments, views, shares, saves, duration_seconds, is_video,
                          thumbnail_url, video_url, published_at)
        VALUES (%(profile_id)s, %(platform)s, %(post_id)s, %(post_url)s, %(post_type)s, %(caption)s,
                %(hashtags)s, %(likes)s, %(comments)s, %(views)s, %(shares)s, %(saves)s,
                %(duration_seconds)s, %(is_video)s, %(thumbnail_url)s, %(video_url)s, %(published_at)s)
        ON CONFLICT (post_id, platform) DO UPDATE SET
            likes = EXCLUDED.likes,
            comments = EXCLUDED.comments,
            views = EXCLUDED.views,
            shares = EXCLUDED.shares,
            saves = EXCLUDED.saves,
            scraped_at = NOW()
        RETURNING id;
    """, data)
    post_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return post_id


def insert_analysis(data):
    """Insert an analysis record."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO analyses (post_id, analysis_type, hook_type, hook_text, narrative_structure,
                            main_topic, key_points, visual_style, production_quality, audio_type,
                            cta_text, cta_type, engagement_score, replicability_score,
                            full_analysis, summary)
        VALUES (%(post_id)s, %(analysis_type)s, %(hook_type)s, %(hook_text)s, %(narrative_structure)s,
                %(main_topic)s, %(key_points)s, %(visual_style)s, %(production_quality)s, %(audio_type)s,
                %(cta_text)s, %(cta_type)s, %(engagement_score)s, %(replicability_score)s,
                %(full_analysis)s, %(summary)s)
        RETURNING id;
    """, data)
    analysis_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return analysis_id


def insert_content_idea(data):
    """Insert a content idea."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO content_ideas (title, description, hook_suggestion, structure, cta_suggestion,
                                  platform, content_type, priority, tags, inspired_by)
        VALUES (%(title)s, %(description)s, %(hook_suggestion)s, %(structure)s, %(cta_suggestion)s,
                %(platform)s, %(content_type)s, %(priority)s, %(tags)s, %(inspired_by)s)
        RETURNING id;
    """, data)
    idea_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return idea_id


def log_pipeline_run(status="running"):
    """Start a pipeline run log."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        INSERT INTO pipeline_runs (status) VALUES (%s) RETURNING id;
    """, (status,))
    run_id = cur.fetchone()["id"]
    conn.commit()
    cur.close()
    conn.close()
    return run_id


def update_pipeline_run(run_id, data):
    """Update a pipeline run log."""
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("""
        UPDATE pipeline_runs SET
            completed_at = NOW(),
            status = %(status)s,
            profiles_scraped = %(profiles_scraped)s,
            posts_found = %(posts_found)s,
            videos_analyzed = %(videos_analyzed)s,
            errors = %(errors)s,
            summary = %(summary)s
        WHERE id = %(run_id)s;
    """, {**data, "run_id": run_id})
    conn.commit()
    cur.close()
    conn.close()


# --- Query Functions for Dashboard ---

def get_all_profiles():
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM profiles ORDER BY followers DESC;")
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_posts_with_analysis(limit=50, platform=None, profile_id=None):
    conn = get_connection()
    cur = conn.cursor()
    query = """
        SELECT p.*, pr.username, pr.platform as profile_platform,
               a.summary, a.hook_type, a.engagement_score, a.replicability_score,
               a.main_topic, a.cta_type
        FROM posts p
        JOIN profiles pr ON p.profile_id = pr.id
        LEFT JOIN analyses a ON a.post_id = p.id
        WHERE 1=1
    """
    params = []
    if platform:
        query += " AND p.platform = %s"
        params.append(platform)
    if profile_id:
        query += " AND p.profile_id = %s"
        params.append(profile_id)
    query += " ORDER BY p.scraped_at DESC LIMIT %s;"
    params.append(limit)

    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_content_ideas(status=None):
    conn = get_connection()
    cur = conn.cursor()
    query = "SELECT * FROM content_ideas"
    params = []
    if status:
        query += " WHERE status = %s"
        params.append(status)
    query += " ORDER BY created_at DESC;"
    cur.execute(query, params)
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_pipeline_runs(limit=10):
    conn = get_connection()
    cur = conn.cursor()
    cur.execute("SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT %s;", (limit,))
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return rows


def get_dashboard_stats():
    conn = get_connection()
    cur = conn.cursor()
    stats = {}
    cur.execute("SELECT COUNT(*) as count FROM profiles;")
    stats["total_profiles"] = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) as count FROM posts;")
    stats["total_posts"] = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) as count FROM analyses;")
    stats["total_analyses"] = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) as count FROM content_ideas;")
    stats["total_ideas"] = cur.fetchone()["count"]
    cur.execute("SELECT COUNT(*) as count FROM posts WHERE is_video = TRUE;")
    stats["total_videos"] = cur.fetchone()["count"]
    cur.execute("SELECT AVG(engagement_score) as avg FROM analyses WHERE engagement_score IS NOT NULL;")
    row = cur.fetchone()
    stats["avg_engagement"] = round(row["avg"], 2) if row["avg"] else 0
    cur.execute("SELECT * FROM pipeline_runs ORDER BY started_at DESC LIMIT 1;")
    stats["last_run"] = cur.fetchone()
    cur.close()
    conn.close()
    return stats

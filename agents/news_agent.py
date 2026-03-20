"""News Agent — Fetches real estate & investment sector news from multiple sources."""

import sys
import os
import re
import urllib.request
import urllib.parse
from datetime import datetime, timezone

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

try:
    import feedparser
except ImportError:
    feedparser = None
    print("[NewsAgent] Warning: feedparser not installed. Install with: pip install feedparser")

from database import insert_news


# ═══════════════════════════════════════════════════════════════
# SOURCE CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Google News search queries (Peru real estate + LATAM + global)
GOOGLE_NEWS_QUERIES = [
    # Peru-specific
    "inversión inmobiliaria Perú 2025",
    "mercado inmobiliario Lima departamentos",
    "crédito hipotecario Perú tasas",
    "proptech Perú startups",
    "sector construcción Perú crecimiento",
    "fondo inversión inmobiliario Perú",
    "mivivienda techo propio Perú",
    "AFP ahorro pensión Perú alternativas",
    # LATAM real estate
    "real estate investment Latin America",
    "proptech latinoamerica tendencias",
    "mercado inmobiliario latinoamerica 2025",
    # Global investment / consulting insights
    "McKinsey real estate trends",
    "Deloitte real estate predictions",
    "PwC emerging trends real estate",
    "BBVA Research inmobiliario",
    "real estate investment emerging markets",
    "proptech global trends 2025",
    "passive income real estate strategies",
    # Financial / economic context
    "economía peruana crecimiento PIB",
    "tasas interés Perú BCRP",
    "inflación Perú impacto inversiones",
]

# Direct RSS feeds from specific publications/organizations
DIRECT_RSS_FEEDS = [
    # McKinsey & Consulting
    {
        "url": "https://www.mckinsey.com/industries/real-estate/our-insights/rss",
        "source": "McKinsey",
        "category": "consultoría",
    },
    {
        "url": "https://www2.deloitte.com/us/en/insights/industry/financial-services/commercial-real-estate-outlook.rss.xml",
        "source": "Deloitte",
        "category": "consultoría",
    },
    # BBVA Research
    {
        "url": "https://www.bbvaresearch.com/en/category/real-estate/feed/",
        "source": "BBVA Research",
        "category": "financiamiento",
    },
    # Peru business news
    {
        "url": "https://gestion.pe/economia/rss",
        "source": "Gestión",
        "category": "mercado",
    },
    {
        "url": "https://semanaeconomica.com/feed",
        "source": "Semana Económica",
        "category": "mercado",
    },
    # International real estate
    {
        "url": "https://www.globalpropertyguide.com/feeds/rss",
        "source": "Global Property Guide",
        "category": "inversión",
    },
    # Forbes real estate
    {
        "url": "https://www.forbes.com/real-estate/feed/",
        "source": "Forbes Real Estate",
        "category": "inversión",
    },
    # TechCrunch proptech
    {
        "url": "https://techcrunch.com/tag/proptech/feed/",
        "source": "TechCrunch Proptech",
        "category": "proptech",
    },
]

# ═══════════════════════════════════════════════════════════════
# RELEVANCE SCORING
# ═══════════════════════════════════════════════════════════════

RELEVANCE_KEYWORDS = {
    "high": [
        "inversión", "inmobiliaria", "inmobiliario", "departamento", "hipotecario",
        "proptech", "bienes raíces", "real estate", "lima", "perú", "peru",
        "proper", "constructora", "edificio", "vivienda", "mivivienda",
        "crédito", "financiamiento", "rentabilidad", "plusvalía",
        "cap rate", "roi", "retorno", "ingreso pasivo", "passive income",
        "afp", "pensión", "ahorro", "patrimonio",
    ],
    "medium": [
        "construcción", "sector", "mercado", "precio", "venta",
        "alquiler", "renta", "proyecto", "desarrollo", "urbano",
        "economía", "crecimiento", "banco", "tasa", "interés",
        "mckinsey", "deloitte", "pwc", "bbva", "consulting",
        "tendencia", "trend", "forecast", "outlook", "prediction",
        "latam", "latin america", "emerging market",
        "millennials", "generación", "joven", "primer departamento",
    ],
    "low": [
        "negocio", "empresa", "tecnología", "digital", "app",
        "startup", "fintech", "capital", "fondo", "ahorro",
        "inflación", "pib", "gdp", "economic", "growth",
        "sustainability", "sostenible", "verde", "green building",
    ],
}

CATEGORY_KEYWORDS = {
    "mercado": ["mercado", "precio", "oferta", "demanda", "venta", "compra", "alquiler", "market", "supply", "demand"],
    "financiamiento": ["crédito", "hipotecario", "tasa", "banco", "financiamiento", "mivivienda", "mortgage", "lending", "interest rate"],
    "proptech": ["proptech", "tecnología", "app", "digital", "plataforma", "startup", "tech", "platform", "AI", "software"],
    "regulación": ["ley", "norma", "regulación", "gobierno", "municipalidad", "zonificación", "regulation", "policy", "law"],
    "inversión": ["inversión", "rentabilidad", "plusvalía", "fondo", "retorno", "roi", "investment", "return", "yield", "cap rate"],
    "construcción": ["construcción", "proyecto", "edificio", "obra", "desarrollo", "constructora", "construction", "building", "development"],
    "consultoría": ["mckinsey", "deloitte", "pwc", "bbva", "kpmg", "ernst", "consulting", "consultora", "research", "insights", "outlook"],
    "economía": ["economía", "inflación", "pib", "crecimiento", "bcrp", "gdp", "economy", "inflation", "growth", "forecast"],
}


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

def _build_google_news_rss_url(query):
    """Build a Google News RSS feed URL for a search query."""
    encoded_query = urllib.parse.quote(query)
    return f"https://news.google.com/rss/search?q={encoded_query}&hl=es-419&gl=PE&ceid=PE:es-419"


def _score_relevance(title, summary):
    """Score relevance of a news item based on keyword matching (0-1)."""
    text = f"{title} {summary}".lower()
    score = 0.0

    for keyword in RELEVANCE_KEYWORDS["high"]:
        if keyword in text:
            score += 0.12

    for keyword in RELEVANCE_KEYWORDS["medium"]:
        if keyword in text:
            score += 0.06

    for keyword in RELEVANCE_KEYWORDS["low"]:
        if keyword in text:
            score += 0.03

    return min(round(score, 2), 1.0)


def _detect_category(title, summary):
    """Detect the most likely category based on keyword frequency."""
    text = f"{title} {summary}".lower()
    category_scores = {}

    for category, keywords in CATEGORY_KEYWORDS.items():
        count = sum(1 for kw in keywords if kw in text)
        if count > 0:
            category_scores[category] = count

    if category_scores:
        return max(category_scores, key=category_scores.get)
    return "general"


def _generate_content_potential(title, category, source_name=""):
    """Generate suggestions on how this news could be turned into Proper content."""
    source_tag = f" (fuente: {source_name})" if source_name else ""

    templates = {
        "mercado": (
            f"📊 Crear reel con datos clave del mercado{source_tag}. "
            f"Conectar con: ¿Es buen momento para invertir? Proper te ayuda desde S/25,000."
        ),
        "financiamiento": (
            f"🏦 Video educativo sobre opciones de financiamiento{source_tag}. "
            f"Ideal para audiencia que compara: ¿AFP o inversión inmobiliaria? Simulador Proper."
        ),
        "proptech": (
            f"🤖 Contenido sobre innovación inmobiliaria{source_tag}. "
            f"Posiciona a Proper como plataforma tecnológica que democratiza la inversión."
        ),
        "regulación": (
            f"⚖️ Post informativo sobre cambios normativos{source_tag}. "
            f"Genera confianza mostrando que Proper está al día con regulaciones."
        ),
        "inversión": (
            f"💰 Carousel con insights de inversión{source_tag}. "
            f"Conectar con métricas Proper: Cap Rate 6.9%, TIR 21.8%, ROI 40.2%."
        ),
        "construcción": (
            f"🏗️ Actualización de proyectos{source_tag}. "
            f"Mostrar el respaldo de Proper con constructoras reales y proyectos en Lima."
        ),
        "consultoría": (
            f"📈 Compartir insights de {source_name or 'consultora global'} adaptados al contexto peruano. "
            f"Posiciona a Proper como marca que sigue tendencias globales."
        ),
        "economía": (
            f"🌍 Contexto económico{source_tag}. "
            f"¿Cómo afecta esto a tus inversiones? Proper protege tu patrimonio con bienes raíces."
        ),
        "general": (
            f"📱 Adaptar noticia{source_tag} a formato educativo corto para redes de Proper."
        ),
    }
    return templates.get(category, templates["general"])


def _parse_published_date(entry):
    """Try to parse the published date from a feed entry."""
    published = getattr(entry, "published_parsed", None)
    if published:
        try:
            return datetime(*published[:6])
        except Exception:
            pass
    published_str = getattr(entry, "published", None) or getattr(entry, "updated", None)
    if published_str:
        for fmt in ["%a, %d %b %Y %H:%M:%S %Z", "%Y-%m-%dT%H:%M:%S%z", "%a, %d %b %Y %H:%M:%S %z"]:
            try:
                return datetime.strptime(published_str, fmt).replace(tzinfo=None)
            except ValueError:
                continue
    return None


def _extract_source_name(entry):
    """Extract source name from feed entry."""
    source = getattr(entry, "source", None)
    if source and hasattr(source, "title"):
        return source.title
    title = getattr(entry, "title", "")
    if " - " in title:
        return title.rsplit(" - ", 1)[-1].strip()
    return None


def _clean_title(title):
    """Clean title by removing the source suffix that Google News adds."""
    if " - " in title:
        return title.rsplit(" - ", 1)[0].strip()
    return title.strip()


def _fetch_rss_feed(url, timeout=15):
    """Fetch and parse an RSS feed URL."""
    try:
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/rss+xml, application/xml, text/xml, */*",
            },
        )
        with urllib.request.urlopen(req, timeout=timeout) as response:
            return feedparser.parse(response.read())
    except Exception as e:
        print(f"[NewsAgent] Error fetching feed {url}: {e}")
        return None


# ═══════════════════════════════════════════════════════════════
# MAIN FETCH FUNCTION
# ═══════════════════════════════════════════════════════════════

def fetch_news():
    """Fetch real estate & investment news from multiple sources.

    Sources:
    1. Google News RSS (20+ search queries)
    2. Direct RSS feeds (McKinsey, Deloitte, BBVA, Forbes, Gestión, etc.)

    Returns:
        list: List of news items found and stored.
    """
    if feedparser is None:
        print("[NewsAgent] feedparser not available. Cannot fetch news.")
        return []

    all_news = []
    seen_urls = set()

    def _process_entry(entry, default_source=None, default_category=None):
        """Process a single feed entry and store if relevant."""
        link = getattr(entry, "link", None)
        if not link or link in seen_urls:
            return None
        seen_urls.add(link)

        raw_title = getattr(entry, "title", "Sin título")
        clean = _clean_title(raw_title)
        summary = getattr(entry, "summary", "") or getattr(entry, "description", "") or ""
        summary = re.sub(r"<[^>]+>", "", summary).strip()

        source_name = default_source or _extract_source_name(entry) or "Fuente desconocida"
        relevance = _score_relevance(clean, summary)
        category = default_category or _detect_category(clean, summary)
        content_potential = _generate_content_potential(clean, category, source_name)
        published_at = _parse_published_date(entry)

        news_item = {
            "title": clean[:500],
            "summary": summary[:2000] if summary else None,
            "source_name": source_name[:255],
            "source_url": link,
            "category": category,
            "relevance_score": relevance,
            "content_potential": content_potential,
            "published_at": published_at,
        }

        # Lower threshold for premium sources
        min_relevance = 0.05 if source_name in [
            "McKinsey", "Deloitte", "BBVA Research", "Forbes Real Estate",
            "PwC", "Gestión", "Semana Económica", "Global Property Guide"
        ] else 0.1

        if relevance >= min_relevance:
            try:
                news_id = insert_news(news_item)
                if news_id:
                    news_item["id"] = news_id
                    all_news.append(news_item)
            except Exception as e:
                print(f"[NewsAgent] Error inserting: {e}")
                all_news.append(news_item)

        return news_item

    # ── Phase 1: Google News RSS searches ──
    print(f"[NewsAgent] Phase 1: Google News ({len(GOOGLE_NEWS_QUERIES)} queries)...")
    for query in GOOGLE_NEWS_QUERIES:
        rss_url = _build_google_news_rss_url(query)
        print(f"  → {query}")
        feed = _fetch_rss_feed(rss_url)
        if feed:
            for entry in feed.entries[:8]:
                _process_entry(entry)

    # ── Phase 2: Direct RSS feeds from publications ──
    print(f"\n[NewsAgent] Phase 2: Direct feeds ({len(DIRECT_RSS_FEEDS)} sources)...")
    for feed_config in DIRECT_RSS_FEEDS:
        source = feed_config["source"]
        print(f"  → {source}")
        feed = _fetch_rss_feed(feed_config["url"])
        if feed:
            for entry in feed.entries[:10]:
                _process_entry(
                    entry,
                    default_source=source,
                    default_category=feed_config.get("category"),
                )

    print(f"\n[NewsAgent] ✅ Total news fetched and stored: {len(all_news)}")
    return all_news


if __name__ == "__main__":
    print("=" * 60)
    print("  Proper MKT — News Agent")
    print("=" * 60)
    results = fetch_news()
    print(f"\nResults: {len(results)} news items\n")
    for item in results[:10]:
        r = item.get("relevance_score", 0)
        print(f"  [{item.get('category', '?'):12s}] {r:.0%}  {item.get('source_name', '?'):20s}  {item.get('title', '?')[:60]}")
        if item.get("source_url"):
            print(f"                {'':12s}       {'':20s}  🔗 {item['source_url'][:80]}")

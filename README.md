# Proper MKT — Sistema de Inteligencia de Contenido

> Sistema automatizado de analisis y replicacion de contenido de TikTok e Instagram usando Gemini API para la marca **Proper** ([@proper.inversion](https://www.instagram.com/proper.inversion/)).

## Que es Proper MKT

Proper MKT es un sistema de agentes de marketing que:
1. **Scrapea** contenido de perfiles referentes en Instagram y TikTok
2. **Analiza** videos e imagenes con Gemini API (multimodal)
3. **Organiza** resultados en tablas con metricas de engagement
4. **Genera guiones de video** listos para grabar con hook, desarrollo, CTA y tomas necesarias
5. **Genera planes de carrusel** para Instagram con slides detallados
6. **Presenta** todo en un dashboard web interactivo con filtros de fecha

El pipeline se ejecuta **automaticamente todos los dias a las 7:00 AM**.

## Arquitectura

```
                    +------------------+
                    |    Scheduler     |  (7:00 AM diario)
                    +--------+---------+
                             |
                    +--------v---------+
                    |     Pipeline     |  (Orquestador)
                    +--------+---------+
                             |
          +------------------+------------------+------------------+
          |                  |                  |                  |
  +-------v------+  +-------v------+  +--------v-----+  +--------v---------+
  | Scraper Agent|  | Viewer Agent |  |Analyzer Agent|  |Content Generator |
  | (IG + TikTok)|  | (Gemini API) |  | (Patrones)   |  | (Guiones + Carr) |
  +-------+------+  +-------+------+  +--------+-----+  +--------+---------+
          |                  |                  |                  |
          +------------------+------------------+------------------+
                             |
                    +--------v---------+
                    |    PostgreSQL    |
                    +--------+---------+
                             |
                    +--------v---------+
                    |  Flask Dashboard |
                    +------------------+
```

### Agentes

| Agente | Archivo | Funcion |
|--------|---------|---------|
| **Scraper** | `agents/scraper.py` | Descarga videos + metadata de Instagram (instaloader) y TikTok (yt-dlp) |
| **Viewer** | `agents/viewer.py` | Sube videos a Gemini API y analiza hooks, estructura, CTA, visual, audio |
| **Organizer** | `agents/organizer.py` | Genera reportes Markdown, CSVs y tablas comparativas |
| **Analyzer** | `agents/analyzer.py` | Identifica patrones cruzados y genera plan de contenido |
| **Content Generator** | `agents/content_generator.py` | Genera guiones de video y planes de carrusel basados en analisis |

### Perfiles Monitoreados

| Perfil | Plataforma | Tipo |
|--------|-----------|------|
| @decatecainversion | Instagram | Competidor/Referencia |
| @capitalizarme | Instagram | Competidor/Referencia |
| @100ladrillos | Instagram | Competidor/Referencia |
| @capitalizarme.com | TikTok | Competidor/Referencia |
| @proper.inversion | Instagram | Propio |

## Stack Tecnologico

| Componente | Tecnologia |
|---|---|
| Analisis multimodal | Google Gemini API (gemini-2.5-pro + gemini-2.5-flash) |
| Scraping Instagram | instaloader |
| Scraping TikTok | yt-dlp |
| Backend/API | Flask + Gunicorn |
| Base de datos | PostgreSQL (Railway) |
| Scheduler | APScheduler (cron diario 7 AM) |
| Frontend | HTML + Tailwind CSS + Vanilla JS |
| Deployment | Railway |

## Estructura del Proyecto

```
proper-mkt/
├── app.py                  # Flask web app + API endpoints
├── pipeline.py             # Pipeline orquestador (local y con DB)
├── scheduler.py            # Scheduler diario (APScheduler)
├── database.py             # Modelos PostgreSQL y operaciones CRUD
├── validate.py             # Script de validacion de servicios
├── Procfile                # Railway deployment config
├── railway.json            # Railway service config
├── runtime.txt             # Python version for Railway
├── requirements.txt        # Dependencias Python
├── .env                    # Credenciales locales (NO versionado)
├── .env.example            # Template de credenciales
├── agents/
│   ├── scraper.py          # Agente de scraping (IG + TikTok)
│   ├── viewer.py           # Agente de vision con Gemini
│   ├── organizer.py        # Agente organizador de reportes
│   ├── analyzer.py         # Agente de analisis de patrones
│   ├── content_generator.py # Agente generador de guiones y carruseles
│   ├── organic/            # (futuro) Sub-agente contenido organico
│   └── ads/                # (futuro) Sub-agente contenido ads
├── config/
│   └── settings.py         # Configuracion centralizada
├── templates/
│   └── dashboard.html      # Dashboard interactivo
├── data/                   # Datos generados (no versionado)
└── downloads/              # Videos descargados (no versionado)
```

## Generacion de Contenido

El sistema genera automaticamente dos tipos de contenido listo para producir:

### Guiones de Video (TikTok / Reels)
- **Hook**: Texto exacto para los primeros 3 segundos + tipo de hook
- **Desarrollo**: Segmentado por tiempos con texto, visual y overlay
- **CTA**: Call to action con accion sugerida
- **Tomas necesarias**: Lista de tomas a grabar
- **Equipamiento**: Que se necesita para producir
- **Caption + Hashtags**: Listos para publicar

### Planes de Carrusel (Instagram)
- **Slides detallados**: Titulo, cuerpo, visual, iconos por cada slide
- **Portada**: Diseno y texto de enganche
- **Puntos clave**: Contenido educativo estructurado
- **CTA slide**: Accion final con indicaciones
- **Caption + Hashtags**: Listos para publicar
- **Mejor hora de publicacion**: Sugerencia basada en best practices

## Dashboard Web

El dashboard muestra:
- **Stats**: Resumen de perfiles, posts, videos, analisis, guiones y carruseles
- **Contenido Analizado**: Tabla con filtros de fecha, plataforma y perfil
- **Contenido Generado**: Guiones de video y carruseles con vista detallada
- **Perfiles**: Lista de perfiles monitoreados con metricas
- **Ideas de Contenido**: Tarjetas con ideas generadas por IA
- **Historial Pipeline**: Log de ejecuciones del pipeline
- **Best Practices**: Mejores practicas de marketing de contenido

## API Endpoints

| Endpoint | Metodo | Descripcion |
|----------|--------|-------------|
| `/` | GET | Dashboard web |
| `/api/stats` | GET | Estadisticas generales |
| `/api/profiles` | GET | Lista de perfiles |
| `/api/posts` | GET | Posts con analisis (filtros: platform, profile_id, date_from, date_to) |
| `/api/ideas` | GET | Ideas de contenido |
| `/api/runs` | GET | Historial de ejecuciones |
| `/api/generated-content` | GET | Guiones y carruseles generados (filtro: type) |
| `/api/generate-content` | POST | Generar nuevo contenido (body: type, topic, limit) |
| `/api/trigger-pipeline` | POST | Ejecutar pipeline manualmente |
| `/api/best-practices` | GET | Mejores practicas de marketing |

## Setup Local

```bash
# 1. Clonar el repositorio
git clone <repo-url>
cd proper-mkt

# 2. Configurar credenciales
cp .env.example .env
# Editar .env con tu GEMINI_API_KEY y DATABASE_URL

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Validar que todo funcione
python validate.py

# 5. Ejecutar pipeline manualmente
python pipeline.py --db --max-posts 3

# 6. Iniciar dashboard web
python app.py
# Abrir http://localhost:5000
```

## Deploy en Railway

### Variables de entorno necesarias en Railway:

| Variable | Descripcion |
|----------|-------------|
| `GEMINI_API_KEY` | API key de Google Gemini |
| `DATABASE_URL` | Auto-generada por Railway PostgreSQL |
| `PORT` | Auto-asignado por Railway |
| `SCHEDULER_HOUR` | Hora de ejecucion diaria (default: 7) |

### Pasos:
1. Crear proyecto en Railway
2. Agregar servicio PostgreSQL
3. Conectar repo de GitHub
4. Configurar variables de entorno
5. Deploy automatico

## Estado del Proyecto

| Fase | Estado |
|---|---|
| Repositorio y estructura | Completado |
| Cliente Gemini API | Completado |
| Agente Scraper (IG + TikTok) | Completado |
| Agente Viewer (Gemini multimodal) | Completado |
| Agente Organizer (reportes) | Completado |
| Agente Analyzer (patrones) | Completado |
| Agente Content Generator | Completado |
| Pipeline orquestador | Completado |
| Base de datos PostgreSQL | Completado |
| Dashboard web interactivo | Completado |
| Filtros de fecha | Completado |
| Generacion de guiones de video | Completado |
| Generacion de carruseles IG | Completado |
| Scheduler diario 7 AM | Completado |
| Railway deployment config | Completado |
| Sub-agente contenido organico | Pendiente |
| Sub-agente contenido ads | Pendiente |

---

*Ultima actualizacion: 2026-03-20*

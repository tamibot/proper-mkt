"""Agente Content Generator — Genera guiones de video y planes de carrusel para Proper."""

import json
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL


class ContentGeneratorAgent:
    """Genera contenido replicable basado en el analisis de competidores."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def generate_video_script(self, analysis_text, platform="tiktok", topic=None):
        """Genera un guion completo de video basado en un analisis de contenido exitoso."""
        prompt = f"""Eres un creador de contenido experto para la marca "Proper", una plataforma de inversion inmobiliaria en LATAM.

Basado en este analisis de contenido exitoso de un competidor/referente:

{analysis_text[:3000]}

Genera UN GUION COMPLETO DE VIDEO listo para grabar para {platform.upper()}.

IMPORTANTE: El contenido debe ser para la marca PROPER (inversion inmobiliaria accesible).
{f"Tema sugerido: {topic}" if topic else ""}

Responde en formato JSON valido con esta estructura exacta:
{{
    "titulo": "Titulo del video",
    "plataforma": "{platform}",
    "duracion_estimada": "30-60 segundos",
    "hook": {{
        "tipo": "pregunta|dato_impactante|historia|problema|contrarian",
        "texto_exacto": "Lo que dice el presentador en los primeros 3 segundos",
        "visual": "Que se ve en pantalla durante el hook"
    }},
    "desarrollo": [
        {{
            "segundo": "3-15",
            "texto": "Lo que dice el presentador",
            "visual": "Que se muestra en pantalla",
            "texto_overlay": "Texto que aparece sobreimpuesto"
        }},
        {{
            "segundo": "15-25",
            "texto": "...",
            "visual": "...",
            "texto_overlay": "..."
        }},
        {{
            "segundo": "25-35",
            "texto": "...",
            "visual": "...",
            "texto_overlay": "..."
        }}
    ],
    "cta": {{
        "texto": "Lo que dice para cerrar",
        "visual": "Que se muestra",
        "accion": "Seguir, comentar, guardar, etc."
    }},
    "caption": "Caption completo para publicar con emojis y hashtags",
    "hashtags": ["lista", "de", "hashtags"],
    "musica_sugerida": "Tipo de musica o cancion trending",
    "tomas_necesarias": [
        "Descripcion de toma 1",
        "Descripcion de toma 2",
        "Descripcion de toma 3"
    ],
    "equipamiento": "Que se necesita para grabar (celular, tripie, etc)",
    "tips_produccion": "Consejos de produccion",
    "nivel_dificultad": "facil|medio|avanzado"
}}"""
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            # Extract JSON from response (may be wrapped in ```json blocks)
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            script_data = json.loads(text)
            return {"status": "success", "script": script_data, "raw": response.text}
        except json.JSONDecodeError:
            return {"status": "success", "script": None, "raw": response.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def generate_carousel_plan(self, analysis_text, platform="instagram", topic=None):
        """Genera un plan de carrusel para Instagram basado en contenido exitoso."""
        prompt = f"""Eres un creador de contenido experto para la marca "Proper", una plataforma de inversion inmobiliaria en LATAM.

Basado en este analisis de contenido exitoso:

{analysis_text[:3000]}

Genera UN PLAN COMPLETO DE CARRUSEL para Instagram.

IMPORTANTE: El contenido debe ser para la marca PROPER (inversion inmobiliaria accesible).
{f"Tema sugerido: {topic}" if topic else ""}

Responde en formato JSON valido con esta estructura exacta:
{{
    "titulo": "Titulo del carrusel",
    "tema": "Tema principal",
    "objetivo": "Educar|Convertir|Engagement|Awareness",
    "total_slides": 8,
    "slides": [
        {{
            "numero": 1,
            "tipo": "portada",
            "titulo_principal": "Texto grande que engancha (maximo 8 palabras)",
            "subtitulo": "Texto secundario",
            "visual": "Descripcion del diseno: colores, iconos, layout",
            "colores": "Paleta de colores sugerida"
        }},
        {{
            "numero": 2,
            "tipo": "contexto",
            "titulo_principal": "...",
            "cuerpo": "Texto del cuerpo (maximo 40 palabras)",
            "visual": "...",
            "dato_clave": "Un dato o estadistica si aplica"
        }},
        {{
            "numero": 3,
            "tipo": "punto_1",
            "titulo_principal": "...",
            "cuerpo": "...",
            "visual": "...",
            "icono_sugerido": "Emoji o icono que acompana"
        }},
        {{
            "numero": 4,
            "tipo": "punto_2",
            "titulo_principal": "...",
            "cuerpo": "...",
            "visual": "...",
            "icono_sugerido": "..."
        }},
        {{
            "numero": 5,
            "tipo": "punto_3",
            "titulo_principal": "...",
            "cuerpo": "...",
            "visual": "...",
            "icono_sugerido": "..."
        }},
        {{
            "numero": 6,
            "tipo": "ejemplo",
            "titulo_principal": "...",
            "cuerpo": "Un ejemplo concreto o caso real",
            "visual": "...",
            "dato_clave": "..."
        }},
        {{
            "numero": 7,
            "tipo": "resumen",
            "titulo_principal": "...",
            "puntos_clave": ["Punto 1", "Punto 2", "Punto 3"],
            "visual": "..."
        }},
        {{
            "numero": 8,
            "tipo": "cta",
            "titulo_principal": "Texto del CTA principal",
            "subtitulo": "Texto secundario del CTA",
            "accion": "Seguir, guardar, comentar, link en bio",
            "visual": "..."
        }}
    ],
    "caption": "Caption completo para publicar con emojis y hashtags",
    "hashtags": ["lista", "de", "hashtags"],
    "mejor_hora": "Hora optima de publicacion",
    "tips_diseno": "Consejos de diseno para el carrusel",
    "nivel_dificultad": "facil|medio|avanzado"
}}"""
        try:
            response = self.model.generate_content(prompt)
            text = response.text.strip()
            if "```json" in text:
                text = text.split("```json")[1].split("```")[0].strip()
            elif "```" in text:
                text = text.split("```")[1].split("```")[0].strip()
            carousel_data = json.loads(text)
            return {"status": "success", "carousel": carousel_data, "raw": response.text}
        except json.JSONDecodeError:
            return {"status": "success", "carousel": None, "raw": response.text}
        except Exception as e:
            return {"status": "error", "error": str(e)}

    def generate_content_batch(self, analyses_from_db):
        """Genera contenido basado en los analisis almacenados en la DB."""
        results = []
        for analysis in analyses_from_db:
            analysis_text = analysis.get("full_analysis") or analysis.get("summary") or ""
            if not analysis_text or len(analysis_text) < 50:
                continue

            # Generate video script
            video_result = self.generate_video_script(
                analysis_text,
                platform=analysis.get("platform", "tiktok"),
            )
            if video_result.get("status") == "success":
                results.append({
                    "type": "video_script",
                    "source_post_id": analysis.get("post_id"),
                    "content": video_result,
                })

            # Generate carousel plan
            carousel_result = self.generate_carousel_plan(
                analysis_text,
                platform="instagram",
            )
            if carousel_result.get("status") == "success":
                results.append({
                    "type": "carousel_plan",
                    "source_post_id": analysis.get("post_id"),
                    "content": carousel_result,
                })

        return results

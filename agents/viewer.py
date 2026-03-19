"""Agente Viewer — Usa Gemini API para 'ver' y analizar contenido multimedia."""

import os
import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL, GEMINI_MODEL_FAST


class ViewerAgent:
    """Analiza videos e imágenes usando Gemini API (multimodal)."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)  # Pro for video analysis
        self.model_fast = genai.GenerativeModel(GEMINI_MODEL_FAST)  # Flash for metadata

    def analyze_video(self, video_path, context=""):
        """Analiza un video local usando Gemini multimodal."""
        if not video_path or not os.path.exists(video_path):
            return {"error": f"Video no encontrado: {video_path}"}

        print(f"[Viewer] Analizando video: {os.path.basename(video_path)}")

        try:
            # Subir video a Gemini
            video_file = genai.upload_file(video_path)

            # Esperar a que el archivo esté procesado
            import time
            while video_file.state.name == "PROCESSING":
                time.sleep(2)
                video_file = genai.get_file(video_file.name)

            if video_file.state.name == "FAILED":
                return {"error": f"Gemini no pudo procesar el video: {video_file.state.name}"}

            prompt = f"""Analiza este video de redes sociales en detalle. {context}

Responde en formato estructurado con estas secciones:

## HOOK (primeros 3 segundos)
- Qué dice/muestra exactamente al inicio para captar atención
- Tipo de hook: pregunta, dato impactante, historia, problema, etc.

## ESTRUCTURA NARRATIVA
- Cómo está organizado el contenido (inicio, desarrollo, cierre)
- Duración aproximada de cada sección
- Transiciones usadas

## CONTENIDO Y MENSAJE
- Tema principal
- Puntos clave mencionados
- Propuesta de valor o mensaje central

## ELEMENTOS VISUALES
- Estilo visual (coloring, encuadres, texto en pantalla)
- Uso de subtítulos o texto overlay
- Calidad de producción (casero, profesional, semi-profesional)

## AUDIO
- Tipo de audio: voz, música, efectos
- Tono de voz (si aplica): formal, casual, urgente, educativo
- Música de fondo (si hay)

## CTA (Call to Action)
- Qué pide que haga el espectador
- Cómo lo presenta

## ENGAGEMENT POTENCIAL
- Qué hace que este contenido funcione o no
- Elementos que generan interacción (controversia, educación, entretenimiento)

## REPLICABILIDAD
- Qué tan fácil es replicar este formato
- Qué elementos específicos se pueden adaptar para la marca Proper
- Sugerencia de contenido similar adaptado
"""
            response = self.model.generate_content([video_file, prompt])

            # Limpiar el archivo subido
            try:
                genai.delete_file(video_file.name)
            except Exception:
                pass

            return {
                "video_path": video_path,
                "analysis": response.text,
                "status": "success",
            }

        except Exception as e:
            print(f"  [!] Error analizando video: {e}")
            return {"video_path": video_path, "error": str(e)}

    def analyze_post_metadata(self, post_data):
        """Analiza la metadata de un post (caption, hashtags, métricas) con Gemini."""
        prompt = f"""Analiza este post de redes sociales:

Plataforma: {post_data.get('platform', 'desconocida')}
Caption: {post_data.get('caption') or post_data.get('description', 'Sin caption')}
Hashtags: {post_data.get('hashtags', [])}
Likes: {post_data.get('likes') or post_data.get('like_count', 'N/A')}
Comentarios: {post_data.get('comments') or post_data.get('comment_count', 'N/A')}
Vistas: {post_data.get('view_count', 'N/A')}
Fecha: {post_data.get('date', 'N/A')}

Analiza:
1. **Copy Analysis**: Calidad del copy, uso de emojis, longitud, estilo
2. **Hashtag Strategy**: Relevancia y estrategia de hashtags
3. **Engagement Rate**: Si los datos lo permiten, evalúa el ratio de engagement
4. **Timing**: Comentario sobre el momento de publicación
5. **Replicabilidad**: Cómo podría Proper adaptar este estilo de copy
"""
        try:
            response = self.model_fast.generate_content(prompt)
            return {"analysis": response.text, "status": "success"}
        except Exception as e:
            return {"error": str(e)}

    def batch_analyze(self, scraped_data):
        """Analiza un lote de contenido scrapeado."""
        analyses = []
        for profile_data in scraped_data:
            # Posts de Instagram
            posts = profile_data.get("posts", [])
            # Videos de TikTok
            videos = profile_data.get("videos", [])
            items = posts + videos

            for item in items:
                analysis_result = {
                    "source": item.get("url") or item.get("shortcode", "unknown"),
                    "platform": item.get("platform", "instagram"),
                }

                # Analizar video si hay archivo local
                video_path = item.get("local_video_path")
                if video_path and os.path.exists(video_path):
                    video_analysis = self.analyze_video(video_path)
                    analysis_result["video_analysis"] = video_analysis
                else:
                    analysis_result["video_analysis"] = {"status": "no_video_file"}

                # Analizar metadata del post
                metadata_analysis = self.analyze_post_metadata(item)
                analysis_result["metadata_analysis"] = metadata_analysis

                analyses.append(analysis_result)

        return analyses

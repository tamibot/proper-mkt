"""Agente Analyzer — Analiza patrones y genera insights replicables."""

import google.generativeai as genai
from config.settings import GEMINI_API_KEY, GEMINI_MODEL


class AnalyzerAgent:
    """Analiza patrones cruzados entre múltiples contenidos y genera insights."""

    def __init__(self):
        genai.configure(api_key=GEMINI_API_KEY)
        self.model = genai.GenerativeModel(GEMINI_MODEL)

    def analyze_patterns(self, analyses):
        """Identifica patrones comunes entre todos los contenidos analizados."""
        # Compilar todos los análisis en un solo texto
        all_analyses_text = ""
        for i, item in enumerate(analyses, 1):
            all_analyses_text += f"\n--- CONTENIDO {i} ({item.get('platform', '')}) ---\n"
            all_analyses_text += f"Fuente: {item.get('source', 'unknown')}\n"

            va = item.get("video_analysis", {})
            if va.get("status") == "success":
                all_analyses_text += f"Análisis de video:\n{va.get('analysis', '')}\n"

            ma = item.get("metadata_analysis", {})
            if ma.get("status") == "success":
                all_analyses_text += f"Análisis de metadata:\n{ma.get('analysis', '')}\n"

        prompt = f"""Eres un estratega de marketing digital experto. Analiza estos contenidos de diferentes perfiles de redes sociales y encuentra patrones replicables para la marca "Proper".

{all_analyses_text}

Genera un reporte estratégico con estas secciones:

## 1. PATRONES DE HOOKS
- Los tipos de hooks más utilizados y efectivos
- Fórmulas comunes de apertura
- Qué tienen en común los hooks que mejor funcionan

## 2. PATRONES DE ESTRUCTURA
- Estructuras narrativas más comunes
- Duración óptima de cada sección
- Flujo de información más efectivo

## 3. PATRONES VISUALES
- Estilos visuales dominantes
- Uso de texto en pantalla
- Niveles de producción

## 4. PATRONES DE COPY
- Estilos de copy más efectivos
- Longitud ideal de captions
- Uso de hashtags y CTAs

## 5. TEMAS QUE FUNCIONAN
- Los temas con mejor engagement
- Ángulos más atractivos para la audiencia
- Nichos o sub-temas con oportunidad

## 6. PLAN DE CONTENIDO PARA PROPER
Genera un plan de 10 piezas de contenido para la marca Proper, basado en los patrones identificados:
- Para cada pieza incluir: tema, hook sugerido, estructura, CTA, plataforma recomendada
- Adaptarlo al estilo y tono que mejor funciona según el análisis

## 7. QUICK WINS
- 5 cosas que Proper puede implementar inmediatamente
- Formatos de bajo esfuerzo y alto impacto
"""
        try:
            response = self.model.generate_content(prompt)
            return {"strategic_analysis": response.text, "status": "success"}
        except Exception as e:
            return {"error": str(e)}

    def compare_profiles(self, scraped_data):
        """Compara perfiles entre sí para identificar diferencias y oportunidades."""
        profiles_text = ""
        for data in scraped_data:
            profile = data.get("profile", {})
            posts = data.get("posts", []) + data.get("videos", [])
            profiles_text += f"\n--- @{profile.get('username', 'unknown')} ({profile.get('platform', '')}) ---\n"
            profiles_text += f"Seguidores: {profile.get('followers', 'N/A')}\n"
            profiles_text += f"Bio: {profile.get('bio', 'N/A')}\n"
            profiles_text += f"Posts analizados: {len(posts)}\n"

            for p in posts:
                profiles_text += f"  - Likes: {p.get('likes') or p.get('like_count', 'N/A')}, "
                profiles_text += f"Views: {p.get('view_count', 'N/A')}, "
                caption = (p.get('caption') or p.get('description') or '')[:100]
                profiles_text += f"Caption: {caption}...\n"

        prompt = f"""Compara estos perfiles de redes sociales y genera un análisis competitivo:

{profiles_text}

Responde con:

## COMPARATIVA DE PERFILES
| Métrica | Perfil 1 | Perfil 2 | ... |
(Tabla comparativa)

## FORTALEZAS POR PERFIL
Qué hace bien cada perfil

## OPORTUNIDADES PARA PROPER
Qué puede tomar Proper de cada perfil

## DIFERENCIACIÓN
Cómo Proper puede diferenciarse de estos competidores/referentes

## BENCHMARK
Métricas objetivo que Proper debería apuntar basado en estos perfiles
"""
        try:
            response = self.model.generate_content(prompt)
            return {"competitive_analysis": response.text, "status": "success"}
        except Exception as e:
            return {"error": str(e)}

"""Agente Analyzer — Analiza patrones y genera insights replicables.

Uses built-in text analysis (no Gemini). Gemini is reserved for viewing
video/image content only.
"""

import re
from collections import Counter


class AnalyzerAgent:
    """Analiza patrones cruzados entre múltiples contenidos y genera insights."""

    # Keywords used to detect hook types
    HOOK_KEYWORDS = {
        "pregunta": ["?", "sabías", "sabes", "conoces", "alguna vez"],
        "estadística": ["%", "datos", "estudio", "según", "cifras", "número"],
        "controversia": ["nadie te dice", "verdad", "mentira", "error", "mito", "cuidado"],
        "historia": ["storytime", "historia", "me pasó", "cuando", "un día"],
        "pov": ["pov", "imagina", "eres", "cuando eres"],
        "tutorial": ["cómo", "como", "paso a paso", "guía", "tutorial", "aprende"],
        "lista": ["top", "mejores", "peores", "razones", "tips", "consejos"],
        "shock": ["increíble", "no vas a creer", "impactante", "sorprendente"],
    }

    CONTENT_TYPE_KEYWORDS = {
        "educativo": ["aprende", "explica", "qué es", "cómo funciona", "guía", "tips"],
        "entretenimiento": ["meme", "humor", "challenge", "trend", "viral"],
        "testimonial": ["testimonio", "caso real", "experiencia", "cliente", "inversor"],
        "motivacional": ["logra", "sueño", "meta", "futuro", "éxito", "libertad"],
        "noticioso": ["noticia", "actualización", "novedad", "breaking", "última hora"],
        "comparación": ["vs", "comparación", "diferencia", "mejor", "peor"],
    }

    def analyze_patterns(self, analyses):
        """Identifica patrones comunes entre todos los contenidos analizados."""
        if not analyses:
            return {"error": "No hay análisis para procesar."}

        hook_counter = Counter()
        content_type_counter = Counter()
        topics = []
        cta_examples = []
        platforms = Counter()
        visual_styles = []
        caption_lengths = []
        total = len(analyses)

        for item in analyses:
            platform = item.get("platform", "unknown")
            platforms[platform] += 1

            va = item.get("video_analysis", {})
            ma = item.get("metadata_analysis", {})

            analysis_text = ""
            if va.get("status") == "success":
                analysis_text += va.get("analysis", "")
            if ma.get("status") == "success":
                analysis_text += " " + ma.get("analysis", "")

            text_lower = analysis_text.lower()

            # Detect hooks
            for hook_type, keywords in self.HOOK_KEYWORDS.items():
                if any(kw in text_lower for kw in keywords):
                    hook_counter[hook_type] += 1

            # Detect content types
            for ct, keywords in self.CONTENT_TYPE_KEYWORDS.items():
                if any(kw in text_lower for kw in keywords):
                    content_type_counter[ct] += 1

            # Extract topics
            topic_patterns = re.findall(
                r"(?:tema|topic|sobre|acerca de)[:\s]+([^\n.]{5,60})", text_lower
            )
            topics.extend(topic_patterns)

            # Extract CTAs
            cta_patterns = re.findall(
                r"(?:cta|call to action|llamada a la acción)[:\s]+([^\n.]{5,80})",
                text_lower,
            )
            cta_examples.extend(cta_patterns)

            # Visual style keywords
            for style in ["minimalista", "colorido", "profesional", "casual", "cinematic"]:
                if style in text_lower:
                    visual_styles.append(style)

            # Caption length
            caption = item.get("caption", "") or ""
            if caption:
                caption_lengths.append(len(caption))

        # Build report
        top_hooks = hook_counter.most_common(5)
        top_content_types = content_type_counter.most_common(5)
        top_topics = Counter(topics).most_common(5)
        avg_caption = (
            round(sum(caption_lengths) / len(caption_lengths))
            if caption_lengths
            else 0
        )
        visual_style_counter = Counter(visual_styles).most_common(3)

        report_lines = [
            "## 1. PATRONES DE HOOKS",
        ]
        if top_hooks:
            for hook, count in top_hooks:
                pct = round(count / total * 100)
                report_lines.append(f"- **{hook}**: {count}/{total} contenidos ({pct}%)")
        else:
            report_lines.append("- No se detectaron patrones de hooks claros.")

        report_lines.append("\n## 2. PATRONES DE ESTRUCTURA")
        report_lines.append(f"- Plataformas analizadas: {dict(platforms)}")
        report_lines.append(f"- Longitud promedio de caption: {avg_caption} caracteres")

        report_lines.append("\n## 3. PATRONES VISUALES")
        if visual_style_counter:
            for style, count in visual_style_counter:
                report_lines.append(f"- {style}: {count} contenidos")
        else:
            report_lines.append("- No se detectaron estilos visuales dominantes.")

        report_lines.append("\n## 4. PATRONES DE COPY")
        if cta_examples:
            report_lines.append("CTAs encontrados:")
            for cta in cta_examples[:5]:
                report_lines.append(f'  - "{cta.strip()}"')
        else:
            report_lines.append("- No se extrajeron CTAs específicos.")

        report_lines.append("\n## 5. TEMAS QUE FUNCIONAN")
        if top_content_types:
            for ct, count in top_content_types:
                report_lines.append(f"- {ct}: {count} contenidos")
        if top_topics:
            report_lines.append("Temas específicos detectados:")
            for topic, count in top_topics:
                report_lines.append(f'  - "{topic.strip()}" ({count}x)')

        report_lines.append("\n## 6. PLAN DE CONTENIDO PARA PROPER")
        # Generate plan from detected patterns
        plan_hooks = [h for h, _ in top_hooks[:3]] if top_hooks else ["pregunta", "estadística", "lista"]
        plan_types = [t for t, _ in top_content_types[:3]] if top_content_types else ["educativo", "testimonial"]
        plan_platforms = list(platforms.keys()) or ["tiktok", "instagram"]

        plan_items = [
            {"tema": "Inversión inmobiliaria desde S/25,000", "hook": plan_hooks[0] if plan_hooks else "pregunta", "plataforma": plan_platforms[0]},
            {"tema": "Cap Rate y TIR explicados", "hook": "tutorial", "plataforma": plan_platforms[0]},
            {"tema": "Mitos sobre invertir en departamentos", "hook": "controversia", "plataforma": plan_platforms[0]},
            {"tema": "Caso real de inversionista Proper", "hook": "historia", "plataforma": plan_platforms[0]},
            {"tema": "Comparativa: AFP vs inmuebles", "hook": plan_hooks[0] if plan_hooks else "estadística", "plataforma": plan_platforms[0]},
            {"tema": "Errores comunes al invertir", "hook": "lista", "plataforma": plan_platforms[-1]},
            {"tema": "Desembolso diferido explicado", "hook": "tutorial", "plataforma": plan_platforms[-1]},
            {"tema": "Renta pasiva con departamentos", "hook": "pregunta", "plataforma": plan_platforms[-1]},
            {"tema": "Por qué los jóvenes deberían invertir hoy", "hook": "estadística", "plataforma": plan_platforms[0]},
            {"tema": "Simulador hipotecario Proper", "hook": "tutorial", "plataforma": plan_platforms[-1]},
        ]
        for i, item in enumerate(plan_items, 1):
            report_lines.append(
                f"{i}. **{item['tema']}** — Hook: {item['hook']} | "
                f"CTA: Regístrate en proper.com.pe | Plataforma: {item['plataforma']}"
            )

        report_lines.append("\n## 7. QUICK WINS")
        report_lines.append("1. Usar hooks de pregunta en los primeros 3 segundos")
        report_lines.append("2. Incluir datos/estadísticas para credibilidad")
        report_lines.append("3. CTAs claros dirigiendo a proper.com.pe")
        report_lines.append("4. Contenido educativo corto (< 60 seg) en TikTok")
        report_lines.append("5. Carruseles comparativos en Instagram")

        strategic_report = "\n".join(report_lines)

        return {"strategic_analysis": strategic_report, "status": "success"}

    def compare_profiles(self, scraped_data):
        """Compara perfiles entre sí para identificar diferencias y oportunidades."""
        if not scraped_data:
            return {"error": "No hay datos de perfiles para comparar."}

        profiles_info = []
        for data in scraped_data:
            profile = data.get("profile", {})
            posts = data.get("posts", []) + data.get("videos", [])

            username = profile.get("username", "unknown")
            platform = profile.get("platform", "unknown")
            followers = profile.get("followers", 0) or 0
            bio = profile.get("bio", "")

            total_likes = 0
            total_views = 0
            total_comments = 0
            captions = []

            for p in posts:
                likes = p.get("likes") or p.get("like_count", 0) or 0
                views = p.get("view_count", 0) or 0
                comments = p.get("comments") or p.get("comment_count", 0) or 0
                total_likes += likes
                total_views += views
                total_comments += comments
                caption = p.get("caption") or p.get("description") or ""
                if caption:
                    captions.append(caption)

            post_count = len(posts) or 1
            avg_likes = round(total_likes / post_count)
            avg_views = round(total_views / post_count) if total_views else 0
            avg_comments = round(total_comments / post_count)
            engagement_rate = (
                round((total_likes + total_comments) / (followers * post_count) * 100, 2)
                if followers > 0
                else 0
            )

            # Detect common hashtags
            all_hashtags = []
            for cap in captions:
                all_hashtags.extend(re.findall(r"#(\w+)", cap.lower()))
            top_hashtags = Counter(all_hashtags).most_common(5)

            profiles_info.append({
                "username": username,
                "platform": platform,
                "followers": followers,
                "post_count": post_count,
                "avg_likes": avg_likes,
                "avg_views": avg_views,
                "avg_comments": avg_comments,
                "engagement_rate": engagement_rate,
                "bio": bio,
                "top_hashtags": top_hashtags,
            })

        # Sort by followers for ranking
        profiles_info.sort(key=lambda x: x["followers"], reverse=True)

        # Build report
        report_lines = ["## COMPARATIVA DE PERFILES\n"]
        report_lines.append("| Métrica | " + " | ".join(f"@{p['username']}" for p in profiles_info) + " |")
        report_lines.append("| --- | " + " | ".join("---" for _ in profiles_info) + " |")

        metrics = [
            ("Seguidores", "followers"),
            ("Posts analizados", "post_count"),
            ("Likes promedio", "avg_likes"),
            ("Views promedio", "avg_views"),
            ("Comentarios promedio", "avg_comments"),
            ("Engagement Rate", "engagement_rate"),
        ]
        for label, key in metrics:
            vals = []
            for p in profiles_info:
                v = p[key]
                if key == "engagement_rate":
                    vals.append(f"{v}%")
                elif isinstance(v, int) and v >= 1000:
                    vals.append(f"{v:,}")
                else:
                    vals.append(str(v))
            report_lines.append(f"| {label} | " + " | ".join(vals) + " |")

        report_lines.append("\n## FORTALEZAS POR PERFIL")
        for p in profiles_info:
            report_lines.append(f"\n**@{p['username']}** ({p['platform']})")
            if p["engagement_rate"] > 3:
                report_lines.append("- Alto engagement rate (>3%)")
            if p["avg_views"] > 10000:
                report_lines.append("- Alto alcance promedio por contenido")
            if p["followers"] > 50000:
                report_lines.append("- Audiencia grande y establecida")
            if p["top_hashtags"]:
                tags = ", ".join(f"#{h}" for h, _ in p["top_hashtags"][:3])
                report_lines.append(f"- Hashtags clave: {tags}")
            if not any([
                p["engagement_rate"] > 3,
                p["avg_views"] > 10000,
                p["followers"] > 50000,
            ]):
                report_lines.append("- Perfil en crecimiento con oportunidad de escalar")

        report_lines.append("\n## OPORTUNIDADES PARA PROPER")
        best_engagement = max(profiles_info, key=lambda x: x["engagement_rate"])
        most_followers = profiles_info[0]
        report_lines.append(
            f"- Aprender estrategias de engagement de @{best_engagement['username']} "
            f"(tasa: {best_engagement['engagement_rate']}%)"
        )
        report_lines.append(
            f"- Benchmark de alcance: @{most_followers['username']} con "
            f"{most_followers['followers']:,} seguidores"
        )
        report_lines.append("- Adaptar los formatos con mejor engagement al contexto inmobiliario peruano")
        report_lines.append("- Usar hashtags relevantes del nicho identificados en los perfiles analizados")

        report_lines.append("\n## DIFERENCIACIÓN")
        report_lines.append("- Proper puede diferenciarse enfocándose en educación financiera accesible")
        report_lines.append("- Mostrar casos reales con datos verificables (TIR, Cap Rate)")
        report_lines.append("- Posicionarse como la plataforma más transparente del sector")
        report_lines.append("- Usar lenguaje cercano (NSE B-C, 25-45 años) vs competidores más corporativos")

        report_lines.append("\n## BENCHMARK")
        avg_engagement = round(
            sum(p["engagement_rate"] for p in profiles_info) / len(profiles_info), 2
        )
        avg_followers = round(
            sum(p["followers"] for p in profiles_info) / len(profiles_info)
        )
        report_lines.append(f"- Engagement rate objetivo: >{avg_engagement}%")
        report_lines.append(f"- Seguidores objetivo (6 meses): {avg_followers:,}")
        report_lines.append(f"- Frecuencia recomendada: 4-5 posts/semana")
        report_lines.append(f"- Likes promedio objetivo: {max(p['avg_likes'] for p in profiles_info):,}")

        competitive_report = "\n".join(report_lines)

        return {"competitive_analysis": competitive_report, "status": "success"}

"""Agente Organizer — Organiza resultados en tablas y reportes estructurados."""

import os
import json
import csv
from datetime import datetime
from config.settings import DATA_DIR


class OrganizerAgent:
    """Organiza análisis en tablas, CSVs y reportes estructurados."""

    def __init__(self):
        self.reports_dir = os.path.join(DATA_DIR, "reports")
        os.makedirs(self.reports_dir, exist_ok=True)

    def create_content_table(self, analyses):
        """Crea una tabla resumen de todo el contenido analizado."""
        rows = []
        for item in analyses:
            row = {
                "source": item.get("source", ""),
                "platform": item.get("platform", ""),
                "has_video_analysis": item.get("video_analysis", {}).get("status") == "success",
                "has_metadata_analysis": item.get("metadata_analysis", {}).get("status") == "success",
            }
            rows.append(row)
        return rows

    def create_profile_summary(self, scraped_data):
        """Crea un resumen de perfiles analizados."""
        summaries = []
        for data in scraped_data:
            profile = data.get("profile", {})
            posts = data.get("posts", [])
            videos = data.get("videos", [])
            items = posts + videos

            total_likes = sum(
                (item.get("likes") or item.get("like_count") or 0) for item in items
            )
            total_comments = sum(
                (item.get("comments") or item.get("comment_count") or 0) for item in items
            )
            total_views = sum(
                (item.get("view_count") or 0) for item in items
            )
            video_count = sum(
                1 for item in items if item.get("is_video") or item.get("platform") == "tiktok"
            )

            summary = {
                "username": profile.get("username", "unknown"),
                "platform": profile.get("platform", "unknown"),
                "followers": profile.get("followers", "N/A"),
                "total_posts_analyzed": len(items),
                "videos": video_count,
                "total_likes": total_likes,
                "total_comments": total_comments,
                "total_views": total_views,
                "avg_likes": round(total_likes / len(items), 1) if items else 0,
                "avg_comments": round(total_comments / len(items), 1) if items else 0,
            }
            summaries.append(summary)
        return summaries

    def export_to_csv(self, data, filename):
        """Exporta datos a CSV."""
        if not data:
            return None
        filepath = os.path.join(self.reports_dir, filename)
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=data[0].keys())
            writer.writeheader()
            writer.writerows(data)
        print(f"[Organizer] CSV exportado: {filepath}")
        return filepath

    def generate_markdown_report(self, scraped_data, analyses):
        """Genera un reporte completo en Markdown."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
        report = f"# Proper MKT — Reporte de Análisis de Contenido\n\n"
        report += f"**Fecha:** {timestamp}\n\n"
        report += "---\n\n"

        # Resumen de perfiles
        summaries = self.create_profile_summary(scraped_data)
        report += "## Resumen de Perfiles\n\n"
        report += "| Perfil | Plataforma | Seguidores | Posts | Videos | Avg Likes | Avg Comments |\n"
        report += "|--------|-----------|------------|-------|--------|-----------|-------------|\n"
        for s in summaries:
            report += (
                f"| @{s['username']} | {s['platform']} | {s['followers']} | "
                f"{s['total_posts_analyzed']} | {s['videos']} | "
                f"{s['avg_likes']} | {s['avg_comments']} |\n"
            )
        report += "\n---\n\n"

        # Análisis detallado
        report += "## Análisis Detallado\n\n"
        for item in analyses:
            report += f"### {item.get('platform', '').upper()} — {item.get('source', '')}\n\n"

            # Análisis de video
            va = item.get("video_analysis", {})
            if va.get("status") == "success":
                report += "#### Análisis de Video\n\n"
                report += va.get("analysis", "Sin análisis") + "\n\n"

            # Análisis de metadata
            ma = item.get("metadata_analysis", {})
            if ma.get("status") == "success":
                report += "#### Análisis de Copy/Metadata\n\n"
                report += ma.get("analysis", "Sin análisis") + "\n\n"

            report += "---\n\n"

        # Guardar reporte
        report_path = os.path.join(
            self.reports_dir,
            f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.md",
        )
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report)
        print(f"[Organizer] Reporte generado: {report_path}")

        # También exportar resumen a CSV
        self.export_to_csv(
            summaries, f"profiles_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        return report_path, report

    def save_full_analysis(self, scraped_data, analyses):
        """Guarda todo el análisis en JSON para referencia futura."""
        output = {
            "timestamp": datetime.now().isoformat(),
            "scraped_data": scraped_data,
            "analyses": analyses,
        }
        path = os.path.join(
            DATA_DIR, f"full_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        )
        with open(path, "w", encoding="utf-8") as f:
            json.dump(output, f, ensure_ascii=False, indent=2, default=str)
        print(f"[Organizer] Análisis completo guardado: {path}")
        return path

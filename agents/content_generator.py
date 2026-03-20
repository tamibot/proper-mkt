"""Agente Content Generator — Genera guiones de video y planes de carrusel para Proper.

NOTA: Este agente genera contenido basado en el contexto de Proper y los analisis
de competidores almacenados en la DB. NO usa Gemini API para generar contenido,
Gemini se usa UNICAMENTE para ver/analizar videos e imagenes (ViewerAgent).
"""

import json
from datetime import datetime

# Contexto de marca Proper (del Brief oficial)
PROPER_CONTEXT = {
    "nombre": "Proper",
    "sector": "Bienes raices e inversion inmobiliaria",
    "pais": "Peru",
    "moneda": "Soles (S/)",
    "slogan": "Invertir en departamentos nunca fue tan simple.",
    "inversion_minima": "S/25,000",
    "tir_promedio": "25% anual",
    "ahorro_desembolso": "S/24,000 a S/60,000",
    "problema_principal": "7 de cada 10 peruanos no tendran acceso a un esquema de pension. Los que si, recibiran entre S/750 y S/1,100 al mes.",
    "propuesta_valor": [
        "Condiciones de compra preferentes con las mejores inmobiliarias",
        "Desembolso postergado - el depa se paga solo",
        "Asesoria 100% GRATUITA en todo el proceso",
        "Proper Rentas: gestion completa del inmueble",
        "Ventas privadas y propiedades off-market con TIR del 25%",
    ],
    "beneficios": [
        "Accesibilidad: Asesoria personalizada y gratuita",
        "Rentabilidad: Propiedades seleccionadas para maximizar ROI",
        "Ahorro de tiempo: Proper filtra propiedades con alto potencial",
        "Confianza: Equipo experto + mejores inmobiliarias del pais",
    ],
    "herramientas": [
        "Analyzer de inversiones (calculadora automatizada)",
        "Simulador hipotecario",
        "Perfil del inversionista",
    ],
    "educacion": [
        "Reuniones semanales: Lunes y miercoles",
        "Workshops trimestrales",
    ],
    "alianzas": ["Pro Innovate", "Startup Peru", "UTEC Ventures", "ASEI", "Peru Proptech"],
    "tono": "Cercano, confiable y profesional",
    "publico": "25-45 anos, NSE B y C, Peru",
    "cta_principal": "Registrate en proper.com.pe para asesoria gratuita",
    "metricas_clave": {
        "gross_yield": "7.4%",
        "cap_rate": "6.9%",
        "tir": "21.8%",
        "roi_5_anos": "40.2%",
    },
    "web": "proper.com.pe",
    "instagram": "@proper.inversion",
}


class ContentGeneratorAgent:
    """Genera contenido replicable basado en el analisis de competidores y el contexto de Proper.

    Este agente NO usa Gemini API. Genera contenido directamente basado en:
    1. El brief de marca de Proper
    2. Los analisis de competidores almacenados en la DB
    3. Mejores practicas de contenido para fintech/proptech en LATAM
    """

    def __init__(self):
        self.context = PROPER_CONTEXT

    def generate_video_script(self, analysis_text, platform="tiktok", topic=None):
        """Genera un guion de video basado en analisis de competidores + contexto Proper."""
        # Extraer insights clave del analisis
        insights = self._extract_insights(analysis_text)

        # Determinar el tipo de video basado en el analisis
        video_type = self._determine_video_type(insights, topic)

        # Generar el guion estructurado
        script = self._build_video_script(video_type, insights, platform, topic)

        return {"status": "success", "script": script, "raw": json.dumps(script, ensure_ascii=False, indent=2)}

    def generate_carousel_plan(self, analysis_text, platform="instagram", topic=None):
        """Genera un plan de carrusel basado en analisis + contexto Proper."""
        insights = self._extract_insights(analysis_text)
        carousel_type = self._determine_carousel_type(insights, topic)
        carousel = self._build_carousel_plan(carousel_type, insights, platform, topic)

        return {"status": "success", "carousel": carousel, "raw": json.dumps(carousel, ensure_ascii=False, indent=2)}

    def _extract_insights(self, analysis_text):
        """Extrae insights clave de un texto de analisis."""
        text_lower = analysis_text.lower() if analysis_text else ""

        insights = {
            "has_hook": any(w in text_lower for w in ["hook", "gancho", "apertura", "inicio"]),
            "has_education": any(w in text_lower for w in ["educa", "ensen", "explica", "aprend"]),
            "has_testimonial": any(w in text_lower for w in ["testimon", "caso", "historia", "experiencia"]),
            "has_data": any(w in text_lower for w in ["dato", "estadistic", "numero", "porcentaje", "%"]),
            "has_comparison": any(w in text_lower for w in ["compar", "vs", "versus", "diferencia"]),
            "has_process": any(w in text_lower for w in ["paso", "proceso", "como", "guia"]),
            "has_myth": any(w in text_lower for w in ["mito", "realidad", "falso", "verdad"]),
            "mentions_pension": any(w in text_lower for w in ["pension", "afp", "retiro", "jubila"]),
            "mentions_rent": any(w in text_lower for w in ["renta", "alquiler", "inquilino"]),
            "mentions_credit": any(w in text_lower for w in ["credito", "hipoteca", "banco", "financ"]),
            "raw_text": analysis_text[:500] if analysis_text else "",
        }
        return insights

    def _determine_video_type(self, insights, topic=None):
        """Determina el mejor tipo de video basado en insights."""
        if topic:
            topic_lower = topic.lower()
            if any(w in topic_lower for w in ["mito", "verdad"]): return "mito_realidad"
            if any(w in topic_lower for w in ["paso", "como", "proceso"]): return "paso_a_paso"
            if any(w in topic_lower for w in ["dato", "sabias"]): return "dato_impactante"
            if any(w in topic_lower for w in ["error", "no hagas"]): return "errores_comunes"

        if insights.get("has_myth"): return "mito_realidad"
        if insights.get("has_data") or insights.get("mentions_pension"): return "dato_impactante"
        if insights.get("has_process"): return "paso_a_paso"
        if insights.get("has_testimonial"): return "testimonio"
        if insights.get("has_education"): return "educacion"
        return "dato_impactante"

    def _determine_carousel_type(self, insights, topic=None):
        """Determina el mejor tipo de carrusel."""
        if topic:
            topic_lower = topic.lower()
            if any(w in topic_lower for w in ["compar", "vs"]): return "comparativo"
            if any(w in topic_lower for w in ["paso", "como"]): return "proceso"
            if any(w in topic_lower for w in ["dato", "estadist"]): return "data_driven"

        if insights.get("has_comparison"): return "comparativo"
        if insights.get("has_process"): return "proceso"
        if insights.get("has_data"): return "data_driven"
        if insights.get("has_education"): return "educativo"
        return "educativo"

    def _build_video_script(self, video_type, insights, platform, topic):
        """Construye un guion de video estructurado."""
        scripts_library = {
            "mito_realidad": {
                "titulo": "MITO: Necesitas ser millonario para invertir en departamentos",
                "plataforma": platform,
                "duracion_estimada": "30-45 segundos",
                "hook": {
                    "tipo": "contrarian",
                    "texto_exacto": "Te dijeron que necesitas ser millonario para invertir en departamentos? Eso es MENTIRA.",
                    "visual": "Presentador mirando a camara con expresion seria, texto 'MITO' tachado aparece en pantalla"
                },
                "desarrollo": [
                    {
                        "segundo": "3-12",
                        "texto": "La realidad es que con Proper puedes empezar a invertir en departamentos desde 25 mil soles. Si, leiste bien. Veinticinco mil soles de cuota inicial.",
                        "visual": "Transicion a pantalla con cifra S/25,000 animada. Imagenes de departamentos modernos.",
                        "texto_overlay": "Inversion desde S/25,000"
                    },
                    {
                        "segundo": "12-22",
                        "texto": "Y lo mejor: el banco compra el departamento, el inquilino le paga al banco, y tu haces crecer tu patrimonio. El depa se paga solo.",
                        "visual": "Infografia simple: Banco -> Depa -> Inquilino -> Banco. Ciclo virtuoso.",
                        "texto_overlay": "El depa se paga solo"
                    },
                    {
                        "segundo": "22-30",
                        "texto": "Ademas, con el desembolso postergado te ahorras entre 24 mil y 60 mil soles que pagarias en un proceso tradicional.",
                        "visual": "Comparacion visual: Proceso tradicional vs Proper. Numeros en pantalla.",
                        "texto_overlay": "Ahorra hasta S/60,000"
                    }
                ],
                "cta": {
                    "texto": "Registrate gratis en proper.com.pe y agenda tu asesoria. Nosotros te guiamos paso a paso.",
                    "visual": "Logo Proper + URL proper.com.pe en pantalla",
                    "accion": "Link en bio para registro gratuito"
                },
                "caption": "MITO: 'Necesitas mucho dinero para invertir en departamentos'\nREALIDAD: Con Proper empiezas desde S/25,000 y el depa se paga solo.\n\nDeja de creer que invertir en bienes raices es solo para ricos. Con asesoria GRATUITA y condiciones preferentes, tu futuro financiero empieza hoy.\n\nRegistrate GRATIS en proper.com.pe (link en bio)",
                "hashtags": ["InversionInmobiliaria", "Proper", "BienesRaices", "InversionSimple", "LibertadFinanciera", "DepartamentosPeru", "InvertirEnPeru"],
                "musica_sugerida": "Trending audio energetico o voz sin musica para formato educativo",
                "tomas_necesarias": [
                    "Presentador hablando a camara (plano medio, buena iluminacion)",
                    "B-roll de departamentos modernos en Lima",
                    "Graficos animados con cifras (se pueden hacer en Canva)",
                    "Pantalla final con logo Proper y URL"
                ],
                "equipamiento": "Celular con buena camara, tripie, aro de luz, microfono de solapa (opcional)",
                "tips_produccion": "Grabar en formato vertical 9:16. Usar subtitulos grandes. Cortes rapidos cada 3-5 segundos para mantener atencion.",
                "nivel_dificultad": "facil"
            },
            "dato_impactante": {
                "titulo": "7 de cada 10 peruanos NO tendran pension. Y los que si...",
                "plataforma": platform,
                "duracion_estimada": "35-45 segundos",
                "hook": {
                    "tipo": "dato_impactante",
                    "texto_exacto": "Sabias que 7 de cada 10 peruanos NO van a tener pension cuando se jubilen?",
                    "visual": "Numero '7/10' grande en pantalla, presentador con expresion preocupada"
                },
                "desarrollo": [
                    {
                        "segundo": "3-12",
                        "texto": "Y los que si tengan pension, van a recibir entre 750 y 1,100 soles al mes. Eso no alcanza ni para el mercado.",
                        "visual": "Cifras S/750 - S/1,100 en pantalla. Imagenes de supermercado con precios.",
                        "texto_overlay": "S/750 - S/1,100 al mes de pension"
                    },
                    {
                        "segundo": "12-22",
                        "texto": "Por eso cada vez mas peruanos estan invirtiendo en departamentos como su plan de retiro. Un departamento te genera rentas pasivas todos los meses, PARA SIEMPRE.",
                        "visual": "Calendario con pagos de renta entrando cada mes. Graficos de crecimiento.",
                        "texto_overlay": "Rentas pasivas mensuales"
                    },
                    {
                        "segundo": "22-35",
                        "texto": "Con Proper puedes empezar desde 25 mil soles de inicial. Te asesoramos GRATIS, te ayudamos con el credito hipotecario y hasta te conseguimos el inquilino.",
                        "visual": "Secuencia rapida: Asesoria -> Credito -> Inquilino -> Renta. Logo Proper.",
                        "texto_overlay": "Asesoria 100% GRATIS"
                    }
                ],
                "cta": {
                    "texto": "No esperes a los 65 para darte cuenta. Empieza hoy. Link en mi bio para tu asesoria gratuita.",
                    "visual": "Pantalla con proper.com.pe y boton 'Registrate Gratis'",
                    "accion": "Registro en proper.com.pe via link en bio"
                },
                "caption": "7 de cada 10 peruanos NO tendran pension.\nLos que si? Entre S/750 y S/1,100 al mes.\n\nLa mejor alternativa? Invertir en departamentos.\nCon Proper empiezas desde S/25,000 con asesoria GRATUITA.\n\nNo esperes a los 65. Tu futuro financiero se construye HOY.\n\nLink en bio para asesoria gratis.",
                "hashtags": ["Pension", "AFP", "InversionInmobiliaria", "Proper", "RetiroPeru", "LibertadFinanciera", "RentasPasivas"],
                "musica_sugerida": "Audio trending dramatico para la estadistica, luego transicion a algo esperanzador",
                "tomas_necesarias": [
                    "Presentador a camara con expresion seria (hook)",
                    "B-roll de personas mayores (representando jubilacion)",
                    "Imagenes de departamentos y rentas",
                    "Pantalla de la plataforma Proper (Analyzer)",
                    "Cierre con logo y URL"
                ],
                "equipamiento": "Celular, tripie, buena iluminacion natural o aro de luz",
                "tips_produccion": "Empezar con tono serio/preocupante, transicionar a esperanzador. Subtitulos obligatorios. Usar datos duros para generar impacto.",
                "nivel_dificultad": "facil"
            },
            "paso_a_paso": {
                "titulo": "Asi de SIMPLE es invertir en departamentos con Proper",
                "plataforma": platform,
                "duracion_estimada": "40-50 segundos",
                "hook": {
                    "tipo": "pregunta",
                    "texto_exacto": "Quieres invertir en departamentos pero no sabes por donde empezar? Te lo explico en 40 segundos.",
                    "visual": "Presentador con cara amigable, texto '40 seg' como countdown"
                },
                "desarrollo": [
                    {
                        "segundo": "3-15",
                        "texto": "Paso 1: Te registras GRATIS en proper.com.pe y un asesor experto te contacta. Paso 2: Analizan tu perfil de inversionista y te recomiendan las mejores propiedades.",
                        "visual": "Pantalla del registro en proper.com.pe, luego pantalla del Perfil del Inversionista",
                        "texto_overlay": "Paso 1: Registro GRATIS / Paso 2: Perfil de inversionista"
                    },
                    {
                        "segundo": "15-27",
                        "texto": "Paso 3: Proper te ayuda con todo el credito hipotecario y negocia condiciones preferentes. Paso 4: Firmas y listo. Y con el desembolso postergado, no pagas cuotas hasta que te entreguen el depa.",
                        "visual": "Graficos del Analyzer mostrando TIR, ROI. Luego firma de documentos.",
                        "texto_overlay": "Paso 3: Credito hipotecario / Paso 4: Firma con desembolso postergado"
                    },
                    {
                        "segundo": "27-38",
                        "texto": "Y cuando te entregan el departamento, Proper Rentas te consigue el inquilino, cobra la renta y administra todo. Tu solo disfrutas tus ingresos pasivos.",
                        "visual": "Dashboard de Proper Rentas, notificaciones de renta cobrada, persona relajada.",
                        "texto_overlay": "Proper Rentas: Tu depa se administra solo"
                    }
                ],
                "cta": {
                    "texto": "Invierte desde 25 mil soles. Asesoria 100% gratis. Link en bio.",
                    "visual": "Logo Proper + 'proper.com.pe' + 'Asesoria GRATIS'",
                    "accion": "Registro gratuito en proper.com.pe"
                },
                "caption": "Invertir en departamentos en 4 pasos:\n\n1. Registrate GRATIS en proper.com.pe\n2. Descubre tu perfil de inversionista\n3. Proper gestiona tu credito hipotecario\n4. Firma y el depa se paga solo\n\nY con Proper Rentas, nos encargamos de TODO: inquilino, cobro y administracion.\n\nEmpieza desde S/25,000. Link en bio.",
                "hashtags": ["Proper", "InversionSimple", "BienesRaices", "PasoAPaso", "DepartamentosPeru", "CreditoHipotecario", "RentasPasivas"],
                "musica_sugerida": "Musica positiva y energetica, tipo tutorial",
                "tomas_necesarias": [
                    "Presentador explicando (plano medio)",
                    "Screen recording de proper.com.pe y el Analyzer",
                    "B-roll de departamentos y firma de documentos",
                    "Pantalla de Proper Rentas",
                    "Cierre con logo"
                ],
                "equipamiento": "Celular, tripie, captura de pantalla de la plataforma",
                "tips_produccion": "Ritmo rapido, un paso cada 8-10 segundos. Usar numeracion visible en pantalla. Subtitulos grandes.",
                "nivel_dificultad": "facil"
            },
            "testimonio": {
                "titulo": "Invirtio S/25,000 y ahora gana rentas todos los meses",
                "plataforma": platform,
                "duracion_estimada": "35-45 segundos",
                "hook": {
                    "tipo": "historia",
                    "texto_exacto": "Con 25 mil soles de inicial, esta persona ya tiene un departamento que le genera rentas todos los meses.",
                    "visual": "Imagen de departamento moderno, cifra S/25,000 en pantalla"
                },
                "desarrollo": [
                    {
                        "segundo": "3-12",
                        "texto": "Hace un ano no sabia nada de inversiones inmobiliarias. Se registro en Proper, le asignaron un asesor experto GRATIS, y juntos encontraron el departamento perfecto.",
                        "visual": "Secuencia: persona en computadora -> reunion con asesor -> visitando departamento",
                        "texto_overlay": "Hace 1 ano: 'No se nada de inversiones'"
                    },
                    {
                        "segundo": "12-22",
                        "texto": "Proper le consiguio condiciones preferentes: desembolso postergado, precio de preventa, y le gestionaron todo el credito hipotecario. Ahorro mas de 30 mil soles.",
                        "visual": "Graficos de ahorro, comparacion proceso normal vs Proper",
                        "texto_overlay": "Ahorro: +S/30,000"
                    },
                    {
                        "segundo": "22-35",
                        "texto": "Hoy su departamento ya tiene inquilino, Proper Rentas le cobra y le deposita la renta cada mes. El depa se paga solo y encima le queda ganancia.",
                        "visual": "Notificacion de deposito en celular, persona sonriendo, dashboard de rentas",
                        "texto_overlay": "El depa se paga solo + ganancia"
                    }
                ],
                "cta": {
                    "texto": "Tu puedes ser el proximo. Registrate gratis en proper.com.pe. Link en bio.",
                    "visual": "Logo Proper + CTA 'Asesoria GRATIS'",
                    "accion": "Registro en proper.com.pe"
                },
                "caption": "De no saber NADA de inversiones a generar rentas pasivas cada mes.\n\nAsesoria GRATIS + condiciones preferentes + desembolso postergado = Inversion SIMPLE.\n\nRegistrate en proper.com.pe y empieza tu camino. Link en bio.",
                "hashtags": ["CasoDeExito", "Proper", "InversionInmobiliaria", "RentasPasivas", "Testimonio", "LibertadFinanciera"],
                "musica_sugerida": "Musica inspiracional, tipo storytelling",
                "tomas_necesarias": [
                    "Actor/persona real contando su experiencia (o voz en off con B-roll)",
                    "Imagenes de departamento real",
                    "Screenshots de la plataforma Proper",
                    "Cierre motivacional"
                ],
                "equipamiento": "Celular, microfono de solapa, buena iluminacion",
                "tips_produccion": "Formato storytelling. Si es posible usar persona real. Si no, usar voz en off con B-roll. Subtitulos obligatorios.",
                "nivel_dificultad": "medio"
            },
            "educacion": {
                "titulo": "Que es el Cap Rate y por que importa para tu inversion?",
                "plataforma": platform,
                "duracion_estimada": "30-40 segundos",
                "hook": {
                    "tipo": "pregunta",
                    "texto_exacto": "Sabes que es el Cap Rate? Si no, estas tomando decisiones de inversion A CIEGAS.",
                    "visual": "Texto 'CAP RATE' grande en pantalla, presentador senalando"
                },
                "desarrollo": [
                    {
                        "segundo": "3-12",
                        "texto": "El Cap Rate es una de las metricas mas importantes cuando inviertes en departamentos. Basicamente te dice cuanto porcentaje de retorno te genera la propiedad por ano, sin contar la deuda.",
                        "visual": "Formula simple: Cap Rate = Renta Anual / Precio del Inmueble. Ejemplo visual.",
                        "texto_overlay": "Cap Rate = Renta Anual / Precio Inmueble"
                    },
                    {
                        "segundo": "12-22",
                        "texto": "Un buen Cap Rate en Peru esta entre 5% y 8%. En Proper, las propiedades que seleccionamos tienen un Cap Rate promedio de 6.9%. Eso significa que tu dinero trabaja para ti.",
                        "visual": "Barra comparativa mostrando rangos. Screenshot del Analyzer de Proper.",
                        "texto_overlay": "Cap Rate promedio Proper: 6.9%"
                    },
                    {
                        "segundo": "22-30",
                        "texto": "Y eso es solo una de las metricas. En el Analyzer de Proper puedes ver TIR, ROI, Gross Yield y mucho mas. GRATIS.",
                        "visual": "Screenshots del Analyzer mostrando todas las metricas",
                        "texto_overlay": "TIR: 21.8% | ROI: 40.2% | Gross Yield: 7.4%"
                    }
                ],
                "cta": {
                    "texto": "Entra al Analyzer gratis en proper.com.pe y analiza cualquier propiedad. Link en bio.",
                    "visual": "Logo Proper + 'Analyzer GRATIS' + URL",
                    "accion": "Usar el Analyzer en proper.com.pe"
                },
                "caption": "Si no sabes que es el Cap Rate, estas invirtiendo a ciegas.\n\nCap Rate = Renta Anual / Precio del Inmueble\nUn buen Cap Rate en Peru: 5%-8%\nCap Rate promedio Proper: 6.9%\n\nUsa el Analyzer GRATIS en proper.com.pe y toma decisiones inteligentes.\n\nLink en bio.",
                "hashtags": ["CapRate", "EducacionFinanciera", "Proper", "InversionInmobiliaria", "Finanzas", "InvertirEnPeru"],
                "musica_sugerida": "Sin musica o musica suave de fondo tipo podcast",
                "tomas_necesarias": [
                    "Presentador explicando a camara",
                    "Graficos/animaciones simples de la formula",
                    "Screen recording del Analyzer de Proper",
                    "Cierre con CTA"
                ],
                "equipamiento": "Celular, tripie, pizarra o tablet para graficos (opcional)",
                "tips_produccion": "Tono educativo pero no aburrido. Usar analogias simples. Subtitulos con la formula destacada.",
                "nivel_dificultad": "facil"
            },
            "errores_comunes": {
                "titulo": "3 errores que cometen los inversionistas primerizos",
                "plataforma": platform,
                "duracion_estimada": "35-45 segundos",
                "hook": {
                    "tipo": "problema",
                    "texto_exacto": "Si estas pensando invertir en un departamento, NO cometas estos 3 errores.",
                    "visual": "Texto 'ERROR' rojo en pantalla, presentador con expresion seria"
                },
                "desarrollo": [
                    {
                        "segundo": "3-12",
                        "texto": "Error 1: Comprar un departamento para vivir pensando que es inversion. No es lo mismo. Una inversion inmobiliaria se analiza por rentabilidad, no por gustos personales.",
                        "visual": "Corazon vs Calculadora. Icono de error/check.",
                        "texto_overlay": "Error 1: Comprar por emocion, no por rentabilidad"
                    },
                    {
                        "segundo": "12-22",
                        "texto": "Error 2: No calcular TODOS los costos. Cuota hipotecaria, mantenimiento, seguros, periodos vacios... Si no haces los numeros completos, tu 'inversion' puede ser perdida.",
                        "visual": "Lista de costos apareciendo uno a uno. Screenshot del Analyzer.",
                        "texto_overlay": "Error 2: No calcular todos los costos"
                    },
                    {
                        "segundo": "22-35",
                        "texto": "Error 3: Hacerlo solo. Las mejores condiciones se consiguen negociando en volumen. En Proper, negociamos por ti con las mejores inmobiliarias y te asesoramos GRATIS.",
                        "visual": "Persona sola vs comunidad Proper. Logo de inmobiliarias aliadas.",
                        "texto_overlay": "Error 3: Invertir sin asesoria experta"
                    }
                ],
                "cta": {
                    "texto": "No cometas estos errores. Asesorate GRATIS con Proper. Link en bio.",
                    "visual": "Logo Proper + 'Evita estos errores' + URL",
                    "accion": "Registro gratuito en proper.com.pe"
                },
                "caption": "3 errores que arruinan tu primera inversion inmobiliaria:\n\n1. Comprar por emocion, no por rentabilidad\n2. No calcular TODOS los costos\n3. Invertir sin asesoria experta\n\nCon Proper te asesoras GRATIS y tomas decisiones inteligentes.\n\nLink en bio.",
                "hashtags": ["ErroresDeInversion", "Proper", "InversionInmobiliaria", "TipsFinancieros", "BienesRaices"],
                "musica_sugerida": "Audio trending tipo 'oh no' o dramatico",
                "tomas_necesarias": [
                    "Presentador enumerando errores",
                    "Graficos simples para cada error",
                    "Screenshot del Analyzer",
                    "Cierre positivo con solucion Proper"
                ],
                "equipamiento": "Celular, tripie, aro de luz",
                "tips_produccion": "Formato lista numerada. Cada error con corte rapido. El ultimo error debe conectar con la solucion de Proper.",
                "nivel_dificultad": "facil"
            },
        }

        # Select best matching script or use dato_impactante as default
        script = scripts_library.get(video_type, scripts_library["dato_impactante"])

        # If topic was provided, adjust the title
        if topic:
            script["titulo"] = f"{topic} | Proper"

        return script

    def _build_carousel_plan(self, carousel_type, insights, platform, topic):
        """Construye un plan de carrusel estructurado."""
        carousels_library = {
            "educativo": {
                "titulo": "Guia basica: Como invertir en departamentos en Peru",
                "tema": "Inversion inmobiliaria para principiantes",
                "objetivo": "Educar",
                "total_slides": 8,
                "slides": [
                    {"numero": 1, "tipo": "portada", "titulo_principal": "Como invertir en departamentos (sin ser millonario)", "subtitulo": "Guia para principiantes por Proper", "visual": "Fondo blanco limpio, icono de edificio, logo Proper naranja", "colores": "Blanco, naranja #FF7B0F, navy #1B2A4A"},
                    {"numero": 2, "tipo": "contexto", "titulo_principal": "El problema de las pensiones en Peru", "cuerpo": "7 de cada 10 peruanos no tendran pension. Los que si, recibiran entre S/750 y S/1,100 al mes. Invertir en inmuebles es una alternativa real.", "visual": "Infografia con estadistica, colores sobrios", "dato_clave": "7/10 peruanos sin pension"},
                    {"numero": 3, "tipo": "punto_1", "titulo_principal": "Paso 1: Define tu perfil de inversionista", "cuerpo": "Cuanto puedes invertir de inicial? Cuanto ganas? Cuanto debes? Con el Perfil del Inversionista de Proper, descubre tu capacidad real.", "visual": "Screenshot del Perfil del Inversionista de Proper", "icono_sugerido": "1"},
                    {"numero": 4, "tipo": "punto_2", "titulo_principal": "Paso 2: Analiza la rentabilidad", "cuerpo": "No compres por emocion. Usa metricas: Cap Rate (6.9%), TIR (21.8%), ROI (40.2%). El Analyzer de Proper calcula todo automaticamente.", "visual": "Screenshot del Analyzer con metricas reales", "icono_sugerido": "2"},
                    {"numero": 5, "tipo": "punto_3", "titulo_principal": "Paso 3: Aprovecha el desembolso postergado", "cuerpo": "Con Proper, no pagas cuotas hasta que te entreguen el depa. Eso te ahorra entre S/24,000 y S/60,000.", "visual": "Comparacion: Proceso tradicional vs Proper con cifras de ahorro", "icono_sugerido": "3"},
                    {"numero": 6, "tipo": "ejemplo", "titulo_principal": "Ejemplo real con numeros", "cuerpo": "Depa en Santa Beatriz: S/242,450. Inicial 10% (S/24,245). Cuota: S/1,692. Alquiler: S/1,500. Tu bolsillo: solo S/192/mes.", "visual": "Tabla limpia con numeros del Analyzer", "dato_clave": "Cuota neta: solo S/192/mes"},
                    {"numero": 7, "tipo": "resumen", "titulo_principal": "Resumen: Tu camino a la inversion", "puntos_clave": ["Invierte desde S/25,000 de inicial", "Asesoria 100% GRATIS con Proper", "El depa se paga solo con el alquiler", "Proper Rentas administra todo por ti"], "visual": "Checklist limpio con iconos verdes"},
                    {"numero": 8, "tipo": "cta", "titulo_principal": "Empieza HOY. Es GRATIS.", "subtitulo": "Registrate en proper.com.pe y un asesor experto te contacta.", "accion": "Guardar este post + Visitar proper.com.pe (link en bio)", "visual": "Logo Proper grande, URL, boton naranja 'Registrate Gratis'"}
                ],
                "caption": "GUARDA ESTE POST si quieres empezar a invertir en departamentos.\n\nResumen rapido:\n- Invierte desde S/25,000\n- Asesoria 100% GRATIS\n- El depa se paga solo\n- Proper administra todo por ti\n\nRegistrate en proper.com.pe (link en bio) y da el primer paso hacia tu libertad financiera.",
                "hashtags": ["InversionInmobiliaria", "Proper", "GuiaDeInversion", "BienesRaices", "FinanzasPersonales", "DepartamentosPeru", "LibertadFinanciera", "InvertirEnPeru"],
                "mejor_hora": "Martes o jueves, entre 12:00 PM y 2:00 PM o 6:00 PM - 9:00 PM",
                "tips_diseno": "Estilo limpio y profesional. Fondo blanco, texto navy #1B2A4A, acentos naranja #FF7B0F. Usar iconografia simple. Tipografia sans-serif moderna.",
                "nivel_dificultad": "medio"
            },
            "comparativo": {
                "titulo": "AFP vs Departamento de inversion: Cual gana?",
                "tema": "Comparacion de alternativas de retiro",
                "objetivo": "Educar",
                "total_slides": 8,
                "slides": [
                    {"numero": 1, "tipo": "portada", "titulo_principal": "AFP vs Departamento: Cual es MEJOR para tu retiro?", "subtitulo": "La comparacion que nadie te muestra", "visual": "Diseno dividido: lado izquierdo AFP (gris), lado derecho Departamento (naranja)", "colores": "Blanco, naranja, gris, navy"},
                    {"numero": 2, "tipo": "contexto", "titulo_principal": "La realidad de las AFP en Peru", "cuerpo": "Pension promedio AFP: S/750-1,100/mes. Comisiones anuales que reducen tu fondo. Acceso limitado a tu propio dinero.", "visual": "Datos de AFP con iconos negativos", "dato_clave": "Pension AFP: S/750-1,100/mes"},
                    {"numero": 3, "tipo": "punto_1", "titulo_principal": "Rentabilidad: Departamento gana", "cuerpo": "Un departamento bien seleccionado genera TIR del 21.8% anual. La AFP promedio rinde 6-8% anual (antes de comisiones).", "visual": "Grafico de barras comparativo", "icono_sugerido": "Trofeo"},
                    {"numero": 4, "tipo": "punto_2", "titulo_principal": "Ingresos mensuales: Departamento gana", "cuerpo": "Con un depa, recibes renta TODOS los meses. Con AFP, solo al jubilarte (y si alcanza). Ademas el inmueble se aprecia.", "visual": "Calendario con pagos de renta vs espera de jubilacion", "icono_sugerido": "Dinero"},
                    {"numero": 5, "tipo": "punto_3", "titulo_principal": "Control: Departamento gana", "cuerpo": "Tu depa es TUYO. Lo puedes vender, alquilar o heredar cuando quieras. La AFP tiene restricciones y reglas cambiantes.", "visual": "Llave de propiedad vs candado de AFP", "icono_sugerido": "Llave"},
                    {"numero": 6, "tipo": "ejemplo", "titulo_principal": "Ejemplo: S/25,000 en AFP vs Departamento", "cuerpo": "AFP en 20 anos: ~S/80,000 (con suerte). Departamento con Proper: patrimonio de S/300,000+ con rentas mensuales todo ese tiempo.", "visual": "Tabla comparativa lado a lado con numeros", "dato_clave": "AFP: S/80K vs Depa: S/300K+ con rentas"},
                    {"numero": 7, "tipo": "resumen", "titulo_principal": "El veredicto es claro", "puntos_clave": ["Mayor rentabilidad con departamentos", "Ingresos pasivos desde el dia 1 (con inquilino)", "Control total de tu patrimonio", "Proper te asesora GRATIS"], "visual": "Marcador final: AFP 0 - Departamento 4"},
                    {"numero": 8, "tipo": "cta", "titulo_principal": "Crea tu propio plan de retiro", "subtitulo": "Registrate GRATIS en proper.com.pe", "accion": "Guardar + Compartir con alguien que necesita ver esto", "visual": "Logo Proper + URL + 'Asesoria GRATIS'"}
                ],
                "caption": "AFP vs Departamento de inversion. Cual gana?\n\nRentabilidad: DEPARTAMENTO\nIngresos mensuales: DEPARTAMENTO\nControl: DEPARTAMENTO\nResultado: 4-0\n\nNo dejes tu futuro en manos de la AFP. Crea tu propio plan de retiro invirtiendo en departamentos con Proper.\n\nAsesoria 100% GRATIS. Link en bio.",
                "hashtags": ["AFP", "PlanDeRetiro", "InversionInmobiliaria", "Proper", "LibertadFinanciera", "DepartamentosPeru", "FinanzasPersonales"],
                "mejor_hora": "Lunes o miercoles, entre 7:00 PM y 9:00 PM",
                "tips_diseno": "Formato VS con dos columnas. AFP en gris/rojo, Departamento en verde/naranja. Numeros grandes y visibles. Estilo limpio.",
                "nivel_dificultad": "medio"
            },
            "proceso": {
                "titulo": "Como funciona Proper en 6 simples pasos",
                "tema": "Proceso de inversion con Proper",
                "objetivo": "Convertir",
                "total_slides": 8,
                "slides": [
                    {"numero": 1, "tipo": "portada", "titulo_principal": "Invertir en departamentos en 6 pasos", "subtitulo": "Asi de SIMPLE es con Proper", "visual": "Diseno minimalista, numeros 1-6 como path/timeline, logo Proper", "colores": "Blanco, naranja #FF7B0F, navy #1B2A4A"},
                    {"numero": 2, "tipo": "punto_1", "titulo_principal": "1. Registrate GRATIS", "cuerpo": "Entra a proper.com.pe, llena el formulario y un asesor experto te contacta en menos de 24 horas. Sin costo, sin compromiso.", "visual": "Mockup del formulario de registro", "icono_sugerido": "1"},
                    {"numero": 3, "tipo": "punto_2", "titulo_principal": "2. Descubre tu perfil", "cuerpo": "Con nuestro Perfil del Inversionista, analizamos tu capacidad de financiamiento y te recomendamos opciones ideales para ti.", "visual": "Screenshot de la herramienta Perfil del Inversionista", "icono_sugerido": "2"},
                    {"numero": 4, "tipo": "punto_3", "titulo_principal": "3. Analiza propiedades", "cuerpo": "Usa el Analyzer de Proper para ver Cap Rate, TIR, ROI de cada propiedad. Toma decisiones con DATA, no con intuicion.", "visual": "Screenshot del Analyzer con metricas reales", "icono_sugerido": "3"},
                    {"numero": 5, "tipo": "punto_1", "titulo_principal": "4. Credito hipotecario", "cuerpo": "Proper gestiona tu credito con el banco. Y con el desembolso postergado, no pagas cuotas hasta la entrega del depa.", "visual": "Icono de banco + ahorro S/24,000-60,000", "icono_sugerido": "4"},
                    {"numero": 6, "tipo": "punto_2", "titulo_principal": "5. Firma y recibe tu depa", "cuerpo": "Te acompanamos en la firma de la minuta y en la recepcion del inmueble. Todo supervisado por expertos.", "visual": "Icono de firma + llaves", "icono_sugerido": "5"},
                    {"numero": 7, "tipo": "punto_3", "titulo_principal": "6. Proper Rentas lo administra", "cuerpo": "Conseguimos inquilino, cobramos renta, administramos todo. Tu solo recibes depositos cada mes.", "visual": "Dashboard de Proper Rentas con notificacion de deposito", "icono_sugerido": "6"},
                    {"numero": 8, "tipo": "cta", "titulo_principal": "Empieza en el Paso 1 hoy", "subtitulo": "Registrate GRATIS en proper.com.pe", "accion": "Guardar este post + Click en link en bio", "visual": "Boton naranja 'Registrate Gratis' + Logo Proper"}
                ],
                "caption": "Asi de SIMPLE es invertir con Proper:\n\n1. Registrate GRATIS\n2. Descubre tu perfil de inversionista\n3. Analiza propiedades con DATA\n4. Credito hipotecario gestionado\n5. Firma y recibe tu depa\n6. Proper Rentas administra todo\n\nEmpieza desde S/25,000. Asesoria 100% gratuita.\nLink en bio.",
                "hashtags": ["Proper", "InversionSimple", "PasoAPaso", "BienesRaices", "InversionInmobiliaria", "ProperRentas"],
                "mejor_hora": "Jueves o viernes, entre 12:00 PM y 2:00 PM",
                "tips_diseno": "Estilo timeline/pasos numerados. Cada slide con numero grande y circulo naranja. Fondo blanco, iconografia consistente.",
                "nivel_dificultad": "facil"
            },
            "data_driven": {
                "titulo": "Los numeros que debes conocer antes de invertir",
                "tema": "Metricas de inversion inmobiliaria",
                "objetivo": "Educar",
                "total_slides": 8,
                "slides": [
                    {"numero": 1, "tipo": "portada", "titulo_principal": "4 metricas que todo inversionista debe conocer", "subtitulo": "Con datos reales del mercado peruano", "visual": "Graficos minimalistas, numeros destacados, logo Proper", "colores": "Blanco, naranja, navy"},
                    {"numero": 2, "tipo": "punto_1", "titulo_principal": "Gross Yield: 7.4%", "cuerpo": "Es la rentabilidad bruta anual. Se calcula dividiendo la renta anual entre el precio del inmueble. En Proper, el promedio es 7.4%.", "visual": "Circulo con 7.4% grande, formula abajo", "icono_sugerido": "Grafico"},
                    {"numero": 3, "tipo": "punto_2", "titulo_principal": "Cap Rate: 6.9%", "cuerpo": "Similar al Gross Yield pero descuenta gastos operativos. Un Cap Rate arriba de 5% es considerado bueno en Peru.", "visual": "Barra de progreso mostrando 6.9% vs benchmark 5%", "icono_sugerido": "Target"},
                    {"numero": 4, "tipo": "punto_3", "titulo_principal": "TIR: 21.8%", "cuerpo": "La Tasa Interna de Retorno considera la apreciacion del inmueble + rentas. 21.8% anual supera cualquier plazo fijo o fondo mutuo.", "visual": "Comparacion: TIR 21.8% vs Plazo Fijo 5% vs Fondo Mutuo 8%", "icono_sugerido": "Cohete"},
                    {"numero": 5, "tipo": "ejemplo", "titulo_principal": "ROI en 5 anos: 40.2%", "cuerpo": "Tu retorno total sobre la inversion en 5 anos. Eso significa que por cada S/100,000 invertidos, generas S/40,200 de ganancia.", "visual": "Grafico de crecimiento en 5 anos", "dato_clave": "S/100K -> S/140.2K en 5 anos"},
                    {"numero": 6, "tipo": "contexto", "titulo_principal": "De donde salen estos numeros?", "cuerpo": "Del Analyzer de Proper: herramienta GRATUITA que calcula automaticamente todas las metricas de cualquier propiedad. Datos reales, no estimaciones.", "visual": "Screenshot del Analyzer completo", "dato_clave": "Herramienta 100% GRATIS"},
                    {"numero": 7, "tipo": "resumen", "titulo_principal": "Resumen de metricas Proper", "puntos_clave": ["Gross Yield: 7.4%", "Cap Rate: 6.9%", "TIR: 21.8% anual", "ROI 5 anos: 40.2%"], "visual": "Dashboard resumen con las 4 metricas"},
                    {"numero": 8, "tipo": "cta", "titulo_principal": "Calcula TU rentabilidad", "subtitulo": "Usa el Analyzer GRATIS en proper.com.pe", "accion": "Guardar + Probar el Analyzer (link en bio)", "visual": "Logo Proper + 'Analyzer GRATIS' + URL"}
                ],
                "caption": "Los numeros no mienten. Metricas promedio de propiedades Proper:\n\nGross Yield: 7.4%\nCap Rate: 6.9%\nTIR: 21.8% anual\nROI 5 anos: 40.2%\n\nCalculalos tu mismo GRATIS con el Analyzer de Proper.\n\nLink en bio.",
                "hashtags": ["MetricasDeInversion", "CapRate", "TIR", "ROI", "Proper", "InversionInmobiliaria", "DataDriven", "FinanzasPersonales"],
                "mejor_hora": "Miercoles, entre 6:00 PM y 8:00 PM",
                "tips_diseno": "Estilo infografico con numeros grandes y destacados. Colores consistentes por metrica. Graficos simples y limpios.",
                "nivel_dificultad": "medio"
            },
        }

        carousel = carousels_library.get(carousel_type, carousels_library["educativo"])
        if topic:
            carousel["titulo"] = f"{topic} | Proper"
        return carousel

    def generate_linkedin_post(self, analysis_text, topic=None):
        """Genera un post de LinkedIn basado en analisis de competidores + contexto Proper."""
        insights = self._extract_insights(analysis_text)
        post_type = self._determine_linkedin_type(insights, topic)
        post = self._build_linkedin_post(post_type, insights, topic)

        return {"status": "success", "linkedin_post": post, "raw": json.dumps(post, ensure_ascii=False, indent=2)}

    def generate_blog_article(self, news_item=None, topic=None):
        """Genera un articulo de blog para el blog de Proper."""
        if news_item:
            text = news_item.get("summary") or news_item.get("title") or ""
            insights = self._extract_insights(text)
        else:
            insights = self._extract_insights(topic or "")
        article_type = self._determine_blog_type(insights, topic, news_item)
        article = self._build_blog_article(article_type, insights, topic, news_item)

        return {"status": "success", "blog_article": article, "raw": json.dumps(article, ensure_ascii=False, indent=2)}

    def _determine_linkedin_type(self, insights, topic=None):
        """Determina el mejor tipo de post de LinkedIn."""
        if topic:
            topic_lower = topic.lower()
            if any(w in topic_lower for w in ["mito", "realidad", "falso"]): return "myth_buster"
            if any(w in topic_lower for w in ["leccion", "aprendimos", "experiencia"]): return "lesson_learned"
            if any(w in topic_lower for w in ["dato", "estadist", "numero"]): return "data_insight"
            if any(w in topic_lower for w in ["mercado", "hoy", "actualiz"]): return "market_update"
            if any(w in topic_lower for w in ["caso", "historia", "logro"]): return "success_story"
        if insights.get("has_myth"): return "myth_buster"
        if insights.get("has_data"): return "data_insight"
        if insights.get("has_testimonial"): return "success_story"
        if insights.get("mentions_pension") or insights.get("mentions_rent"): return "market_update"
        return "thought_leadership"

    def _determine_blog_type(self, insights, topic=None, news_item=None):
        """Determina el mejor tipo de articulo de blog."""
        if news_item:
            return "news_analysis"
        if topic:
            topic_lower = topic.lower()
            if any(w in topic_lower for w in ["guia", "paso", "como", "principiante"]): return "guide"
            if any(w in topic_lower for w in ["mercado", "reporte", "mensual", "trimestral"]): return "market_report"
            if any(w in topic_lower for w in ["educa", "aprend", "que es"]): return "educational"
        if insights.get("has_process"): return "guide"
        if insights.get("has_data"): return "market_report"
        return "educational"

    def _build_linkedin_post(self, post_type, insights, topic):
        """Construye un post de LinkedIn estructurado."""
        linkedin_library = {
            "thought_leadership": {
                "tipo": "thought_leadership",
                "post_text": (
                    "El mercado inmobiliario peruano esta en un punto de inflexion.\n\n"
                    "Mientras muchos siguen viendo los bienes raices como algo exclusivo para grandes capitales, "
                    "la realidad es que el acceso a la inversion inmobiliaria se esta democratizando.\n\n"
                    "En Proper llevamos anos trabajando para que cualquier profesional con S/25,000 de ahorro "
                    "pueda convertirse en inversionista inmobiliario. Y no es un sueno: nuestros inversionistas "
                    "alcanzan un TIR promedio del 21.8% anual.\n\n"
                    "Lo que diferencia a quienes construyen patrimonio de quienes no:\n"
                    "- Toman decisiones basadas en DATA, no en emociones\n"
                    "- Se asesoran con expertos (nuestra asesoria es 100% gratuita)\n"
                    "- Aprovechan herramientas como el desembolso postergado para ahorrar hasta S/60,000\n\n"
                    "El Cap Rate promedio de las propiedades que seleccionamos es 6.9%. "
                    "Eso supera cualquier plazo fijo o fondo mutuo en el mercado peruano.\n\n"
                    "La pregunta no es si puedes invertir. La pregunta es: cuanto tiempo mas vas a esperar?\n\n"
                    "Agenda tu asesoria gratuita en proper.com.pe y da el primer paso."
                ),
                "hashtags": ["#InversionInmobiliaria", "#BienesRaicesPeru", "#Proper", "#LibertadFinanciera", "#InvertirEnPeru"],
                "best_time": "Martes a jueves, entre 7:00-8:30 AM o 12:00-1:00 PM",
                "engagement_tips": [
                    "Responde TODOS los comentarios en las primeras 2 horas",
                    "Haz una pregunta al final para generar conversacion",
                    "Tagea a profesionales del sector en los comentarios",
                    "Comparte en grupos relevantes de LinkedIn (inmobiliario, finanzas Peru)",
                ],
                "image_suggestion": "Infografia profesional con datos clave: TIR 21.8%, Cap Rate 6.9%, inversion desde S/25,000. Colores Proper (naranja #FF7B0F, navy #1B2A4A).",
            },
            "data_insight": {
                "tipo": "data_insight",
                "post_text": (
                    "Un dato que cambio mi perspectiva sobre inversion inmobiliaria en Peru:\n\n"
                    "El Gross Yield promedio de las propiedades seleccionadas por Proper es 7.4%.\n\n"
                    "Para ponerlo en contexto:\n"
                    "- Un plazo fijo en Peru rinde entre 3% y 5% anual\n"
                    "- Un fondo mutuo conservador rinde entre 5% y 8%\n"
                    "- Un departamento de inversion bien seleccionado: 7.4% de yield + apreciacion del inmueble\n\n"
                    "Pero eso no es todo. Cuando sumamos la apreciacion del inmueble a largo plazo, "
                    "la TIR (Tasa Interna de Retorno) alcanza el 21.8% anual. "
                    "El ROI total en 5 anos es de 40.2%.\n\n"
                    "Estos no son numeros teoricos. Son metricas reales calculadas con nuestro Analyzer, "
                    "una herramienta gratuita que cualquier persona puede usar en proper.com.pe.\n\n"
                    "La inversion inmobiliaria en Peru ya no es un privilegio de pocos. "
                    "Con asesoria experta y gratuita, puedes empezar desde S/25,000.\n\n"
                    "Los datos estan claros. La decision es tuya.\n\n"
                    "Conoce tu potencial de inversion en proper.com.pe"
                ),
                "hashtags": ["#DatosInmobiliarios", "#InversionInteligente", "#Proper", "#ROI", "#FinanzasPersonales"],
                "best_time": "Miercoles, entre 10:00-11:00 AM",
                "engagement_tips": [
                    "Incluye una grafica o tabla con los datos comparativos",
                    "Pregunta: 'Donde tienes tus ahorros hoy?'",
                    "Menciona fuentes de datos para mayor credibilidad",
                    "Invita a calcular su propia rentabilidad con el Analyzer",
                ],
                "image_suggestion": "Tabla comparativa limpia: Plazo Fijo vs Fondo Mutuo vs Departamento de Inversion. Destacar la columna de departamento en naranja Proper.",
            },
            "lesson_learned": {
                "tipo": "lesson_learned",
                "post_text": (
                    "3 lecciones que aprendimos asesorando a cientos de inversionistas inmobiliarios en Peru:\n\n"
                    "1. La emocion es el peor consejero.\n"
                    "El 80% de los inversionistas primerizos quieren comprar el departamento que MAS les gusta. "
                    "Pero un depa de inversion se elige con datos: Cap Rate, TIR, demanda de alquiler en la zona. "
                    "En Proper, nuestro Analyzer calcula todo automaticamente.\n\n"
                    "2. El desembolso postergado es un game changer.\n"
                    "La mayoria no sabe que puede ahorrarse entre S/24,000 y S/60,000 con condiciones de compra preferentes. "
                    "Nosotros negociamos estas condiciones directamente con las inmobiliarias.\n\n"
                    "3. La gestion del alquiler no deberia quitarte el sueno.\n"
                    "Conseguir inquilino, cobrar renta, resolver emergencias... "
                    "Con Proper Rentas nos encargamos de TODO. Tu solo recibes depositos cada mes.\n\n"
                    "Estas lecciones le han ahorrado miles de soles a nuestros inversionistas.\n\n"
                    "Si estas pensando en invertir, empieza con una asesoria gratuita en proper.com.pe"
                ),
                "hashtags": ["#LeccionesDeInversion", "#BienesRaices", "#Proper", "#InversionInmobiliaria", "#AprendizajeFinanciero"],
                "best_time": "Lunes, entre 8:00-9:00 AM",
                "engagement_tips": [
                    "Usa formato de lista numerada para facilitar la lectura",
                    "Pide en comentarios: 'Cual fue TU mayor leccion invirtiendo?'",
                    "Responde con datos especificos a cada comentario",
                    "Comparte anecdotas reales (sin nombres) para humanizar",
                ],
                "image_suggestion": "Diseno con los 3 puntos clave en formato de tarjeta. Cada leccion con icono representativo. Branding Proper.",
            },
            "market_update": {
                "tipo": "market_update",
                "post_text": (
                    "Lo que esta pasando en el sector inmobiliario en Lima HOY:\n\n"
                    "El mercado de departamentos de inversion en Peru esta experimentando cambios importantes. "
                    "La demanda de alquiler sigue creciendo, especialmente en distritos como Miraflores, "
                    "San Isidro, Jesus Maria y Magdalena.\n\n"
                    "Que significa esto para los inversionistas?\n\n"
                    "Mayor demanda de alquiler = menor tiempo de vacancia. "
                    "Los departamentos bien ubicados se alquilan en promedio en 2-3 semanas.\n\n"
                    "Los precios de preventa siguen siendo la mejor oportunidad. "
                    "Comprar en preventa con desembolso postergado te ahorra entre S/24,000 y S/60,000 "
                    "respecto a comprar un departamento entregado.\n\n"
                    "Las metricas del mercado se mantienen atractivas:\n"
                    "- Cap Rate promedio: 6.9%\n"
                    "- TIR proyectada: 21.8% anual\n"
                    "- ROI a 5 anos: 40.2%\n\n"
                    "El mejor momento para invertir siempre es antes de que suban los precios.\n\n"
                    "Analiza propiedades con datos reales en proper.com.pe"
                ),
                "hashtags": ["#MercadoInmobiliario", "#LimaInmobiliaria", "#Proper", "#InversionPeru", "#BienesRaices"],
                "best_time": "Martes, entre 7:30-8:30 AM",
                "engagement_tips": [
                    "Menciona distritos especificos para atraer busquedas locales",
                    "Pregunta: 'En que zona de Lima te gustaria invertir?'",
                    "Actualiza con datos frescos cada mes",
                    "Comparte en grupos de profesionales de Lima",
                ],
                "image_suggestion": "Mapa de Lima con zonas destacadas de inversion. Indicadores de precio y rentabilidad por distrito. Estilo profesional con colores Proper.",
            },
            "myth_buster": {
                "tipo": "myth_buster",
                "post_text": (
                    "Mito: Solo los ricos pueden invertir en departamentos.\n"
                    "Realidad: Con S/25,000 de inicial ya puedes empezar.\n\n"
                    "Este es probablemente el mito mas danino del mercado inmobiliario peruano. "
                    "Y es hora de romperlo con datos.\n\n"
                    "Un profesional con ingresos de S/4,000-6,000 mensuales puede acceder a un credito hipotecario "
                    "para comprar un departamento de inversion. Con el desembolso postergado que negociamos en Proper, "
                    "no pagas cuotas hasta que te entreguen el departamento.\n\n"
                    "Cuando el depa esta listo:\n"
                    "- Proper Rentas consigue el inquilino\n"
                    "- El inquilino paga la renta\n"
                    "- La renta cubre la mayor parte de la cuota del banco\n"
                    "- El depa se paga solo y tu patrimonio crece\n\n"
                    "Con un Cap Rate de 6.9% y una TIR del 21.8%, los numeros hablan por si solos.\n\n"
                    "No necesitas ser millonario. Necesitas tomar la decision correcta.\n\n"
                    "Descubre tu capacidad de inversion con una asesoria gratuita en proper.com.pe"
                ),
                "hashtags": ["#MitosInmobiliarios", "#InversionAccesible", "#Proper", "#BienesRaicesPeru", "#EducacionFinanciera"],
                "best_time": "Jueves, entre 12:00-1:00 PM",
                "engagement_tips": [
                    "El formato Mito/Realidad genera alto engagement en LinkedIn",
                    "Pregunta: 'Que otros mitos sobre inversion inmobiliaria has escuchado?'",
                    "Usa negritas y lineas cortas para facilitar el scroll",
                    "Menciona ejemplos concretos con numeros reales",
                ],
                "image_suggestion": "Diseno dividido: lado izquierdo 'MITO' en rojo tachado, lado derecho 'REALIDAD' en verde/naranja Proper. Datos clave destacados.",
            },
            "success_story": {
                "tipo": "success_story",
                "post_text": (
                    "Hace 1 ano, un joven profesional nos contacto con S/25,000 ahorrados.\n\n"
                    "No sabia nada de inversiones inmobiliarias. Tenia dudas, miedos y muchas preguntas. "
                    "Como la mayoria, creia que invertir en departamentos era solo para gente con mucho dinero.\n\n"
                    "Le asignamos un asesor experto (100% gratuito). Juntos analizaron su perfil de inversionista "
                    "y encontraron un departamento en preventa con condiciones preferentes.\n\n"
                    "Los numeros:\n"
                    "- Cuota inicial: S/25,000\n"
                    "- Desembolso postergado: ahorro de S/35,000\n"
                    "- Cap Rate del proyecto: 7.1%\n\n"
                    "Hoy, 12 meses despues, su departamento ya tiene inquilino. "
                    "Proper Rentas se encarga de cobrar la renta y administrar todo. "
                    "El depa se paga solo y su patrimonio crece cada mes.\n\n"
                    "Lo mas valioso que nos dijo: 'Deberia haberlo hecho antes.'\n\n"
                    "No dejes pasar mas tiempo. Tu historia puede empezar hoy.\n\n"
                    "Agenda tu asesoria gratuita en proper.com.pe"
                ),
                "hashtags": ["#CasoDeExito", "#InversionInmobiliaria", "#Proper", "#Patrimonio", "#HistoriaReal"],
                "best_time": "Viernes, entre 9:00-10:00 AM",
                "engagement_tips": [
                    "Las historias personales generan el mayor engagement en LinkedIn",
                    "Pide permiso para etiquetar al inversionista (si es posible)",
                    "Cierra con pregunta: 'Cual es el primer paso que TU darias?'",
                    "Agrega un comentario propio con mas detalles para el algoritmo",
                ],
                "image_suggestion": "Foto profesional de persona sonriente (con permiso) o imagen aspiracional de departamento moderno. Cita destacada del inversionista.",
            },
        }

        post = linkedin_library.get(post_type, linkedin_library["thought_leadership"])
        if topic:
            # Prepend custom topic hook if provided
            post = dict(post)  # shallow copy
            post["topic_personalizado"] = topic
        return post

    def _build_blog_article(self, article_type, insights, topic, news_item):
        """Construye un articulo de blog estructurado."""
        blog_library = {
            "news_analysis": {
                "tipo": "news_analysis",
                "title": "Analisis: Que significa para los inversionistas peruanos",
                "meta_description": "Analizamos las ultimas noticias del sector inmobiliario en Peru y como impactan las oportunidades de inversion en departamentos. Descubre que acciones tomar hoy.",
                "keywords": ["inversion inmobiliaria Peru", "mercado inmobiliario Lima", "analisis sector inmobiliario", "oportunidades inversion departamentos", "Proper inversion"],
                "content": (
                    "## El contexto: Que esta pasando en el mercado\n\n"
                    "El sector inmobiliario peruano continua mostrando senales de dinamismo. "
                    "Los recientes desarrollos en el mercado presentan tanto desafios como oportunidades "
                    "para inversionistas que buscan construir patrimonio a traves de bienes raices.\n\n"
                    "En este analisis, desglosamos los puntos clave y lo que significan para ti como inversionista.\n\n"
                    "## Los datos que importan\n\n"
                    "Para entender el impacto real de estos cambios, veamos las metricas actuales del mercado:\n\n"
                    "- **Cap Rate promedio en propiedades seleccionadas**: 6.9%\n"
                    "- **TIR proyectada a largo plazo**: 21.8% anual\n"
                    "- **ROI acumulado en 5 anos**: 40.2%\n"
                    "- **Gross Yield bruto**: 7.4%\n\n"
                    "Estas cifras demuestran que, a pesar de los movimientos del mercado, "
                    "las propiedades bien seleccionadas mantienen su atractivo como vehiculo de inversion.\n\n"
                    "## Como afecta esto tu estrategia de inversion\n\n"
                    "### Oportunidad en preventa\n\n"
                    "Los departamentos en preventa siguen ofreciendo las mejores condiciones de entrada. "
                    "Con el desembolso postergado, los inversionistas pueden ahorrarse entre S/24,000 y S/60,000 "
                    "comparado con un proceso de compra tradicional.\n\n"
                    "### La importancia de la asesoria experta\n\n"
                    "En un mercado en movimiento, tomar decisiones basadas en datos es mas importante que nunca. "
                    "El Analyzer de Proper permite evaluar cualquier propiedad con metricas reales: "
                    "Cap Rate, TIR, ROI y Gross Yield, todo calculado automaticamente.\n\n"
                    "### Rentas como escudo financiero\n\n"
                    "Un departamento de inversion genera ingresos pasivos mensuales. "
                    "Con Proper Rentas, la gestion del inquilino, cobro de renta y administracion "
                    "del inmueble esta completamente cubierta.\n\n"
                    "## Conclusion: Que hacer ahora\n\n"
                    "Los mejores inversionistas no esperan al momento perfecto. "
                    "Analizan los datos, se asesoran con expertos y toman accion. "
                    "Con una inversion desde S/25,000, el camino hacia tu primer departamento de inversion "
                    "es mas accesible de lo que crees.\n\n"
                ),
                "cta_section": (
                    "## Da el primer paso hoy\n\n"
                    "En Proper te asesoramos de forma **100% gratuita**. Nuestro equipo de expertos "
                    "te ayuda a encontrar la propiedad ideal segun tu perfil de inversionista.\n\n"
                    "**[Agenda tu asesoria gratuita en proper.com.pe](https://proper.com.pe)**\n\n"
                    "Invierte desde S/25,000 | Asesoria GRATIS | El depa se paga solo"
                ),
                "social_share_text": "Nuevo analisis en nuestro blog: que significan los ultimos cambios del mercado inmobiliario para los inversionistas en Peru. Datos reales + recomendaciones accionables. Lee el articulo completo en proper.com.pe/blog",
            },
            "educational": {
                "tipo": "educational",
                "title": "Guia completa: Todo lo que debes saber sobre inversion inmobiliaria en Peru",
                "meta_description": "Aprende los conceptos fundamentales de inversion inmobiliaria en Peru: Cap Rate, TIR, ROI y como elegir tu primer departamento de inversion. Guia gratuita de Proper.",
                "keywords": ["como invertir en departamentos Peru", "inversion inmobiliaria principiantes", "Cap Rate Peru", "TIR inversion departamentos", "Proper asesoria"],
                "content": (
                    "## Por que invertir en departamentos en Peru\n\n"
                    "La inversion inmobiliaria es una de las formas mas solidas de construir patrimonio a largo plazo. "
                    "En Peru, el mercado ofrece oportunidades unicas para inversionistas que buscan "
                    "generar ingresos pasivos y proteger su dinero de la inflacion.\n\n"
                    "Consideremos un dato importante: 7 de cada 10 peruanos no tendran acceso a un esquema de pension. "
                    "Los que si tendran pension, recibiran entre S/750 y S/1,100 al mes. "
                    "Invertir en departamentos es una alternativa real para asegurar tu futuro financiero.\n\n"
                    "## Las 4 metricas que todo inversionista debe conocer\n\n"
                    "### 1. Gross Yield (Rentabilidad Bruta)\n\n"
                    "Es el porcentaje de retorno bruto anual que genera una propiedad. "
                    "Se calcula dividiendo la renta anual entre el precio del inmueble. "
                    "Un buen Gross Yield en Peru esta arriba del 6%. "
                    "En Proper, el promedio es **7.4%**.\n\n"
                    "### 2. Cap Rate (Tasa de Capitalizacion)\n\n"
                    "Similar al Gross Yield pero descuenta los gastos operativos (mantenimiento, seguros, vacancia). "
                    "Es la metrica mas utilizada por inversionistas profesionales. "
                    "Un Cap Rate arriba de 5% es considerado bueno. En Proper, el promedio es **6.9%**.\n\n"
                    "### 3. TIR (Tasa Interna de Retorno)\n\n"
                    "Considera tanto las rentas como la apreciacion del inmueble a lo largo del tiempo. "
                    "Es la metrica mas completa para evaluar una inversion. "
                    "La TIR promedio en propiedades Proper es **21.8% anual**.\n\n"
                    "### 4. ROI (Retorno sobre la Inversion)\n\n"
                    "El porcentaje total de retorno sobre tu capital invertido en un periodo determinado. "
                    "En propiedades seleccionadas por Proper, el ROI a 5 anos es **40.2%**.\n\n"
                    "## Como empezar a invertir con poco capital\n\n"
                    "Contrario a lo que muchos creen, no necesitas ser millonario para invertir en departamentos. "
                    "Con Proper puedes comenzar desde **S/25,000 de cuota inicial**.\n\n"
                    "El proceso es simple:\n"
                    "1. Te registras gratuitamente en proper.com.pe\n"
                    "2. Un asesor experto analiza tu perfil de inversionista\n"
                    "3. Te recomiendan propiedades con las mejores metricas\n"
                    "4. Proper gestiona tu credito hipotecario con condiciones preferentes\n"
                    "5. Con el desembolso postergado, te ahorras entre S/24,000 y S/60,000\n\n"
                    "## El secreto: El depa se paga solo\n\n"
                    "Una vez que recibes tu departamento, Proper Rentas se encarga de todo: "
                    "encontrar inquilino, cobrar la renta y administrar el inmueble. "
                    "La renta del inquilino cubre la mayor parte de tu cuota hipotecaria, "
                    "haciendo que el departamento se pague solo mientras tu patrimonio crece.\n\n"
                ),
                "cta_section": (
                    "## Empieza tu camino como inversionista\n\n"
                    "La asesoria de Proper es **100% gratuita**. No importa si nunca has invertido antes, "
                    "nuestro equipo te guia paso a paso.\n\n"
                    "**[Registrate gratis en proper.com.pe](https://proper.com.pe)**\n\n"
                    "Inversion desde S/25,000 | Asesoria experta GRATIS | Proper Rentas administra todo"
                ),
                "social_share_text": "Publicamos una guia completa sobre inversion inmobiliaria en Peru: metricas clave, como empezar con poco capital y por que el depa se paga solo. Leela gratis en proper.com.pe/blog",
            },
            "market_report": {
                "tipo": "market_report",
                "title": "Reporte del mercado inmobiliario en Lima: metricas y oportunidades",
                "meta_description": "Reporte actualizado del mercado inmobiliario en Lima, Peru. Cap Rate, TIR, precios por distrito y las mejores oportunidades de inversion en departamentos.",
                "keywords": ["reporte inmobiliario Lima", "mercado departamentos Peru", "precios inmobiliarios Lima", "mejores distritos inversion", "Proper analisis"],
                "content": (
                    "## Panorama general del mercado\n\n"
                    "El mercado inmobiliario en Lima mantiene su dinamismo con una demanda sostenida "
                    "de departamentos tanto para vivienda como para inversion. "
                    "Los distritos con mayor potencial de inversion continuan siendo aquellos con alta "
                    "demanda de alquiler y buenos fundamentales economicos.\n\n"
                    "## Metricas clave del periodo\n\n"
                    "Las propiedades seleccionadas por Proper muestran las siguientes metricas promedio:\n\n"
                    "| Metrica | Valor |\n"
                    "|---|---|\n"
                    "| Gross Yield | 7.4% |\n"
                    "| Cap Rate | 6.9% |\n"
                    "| TIR proyectada | 21.8% anual |\n"
                    "| ROI a 5 anos | 40.2% |\n\n"
                    "Estas metricas se mantienen competitivas frente a otras alternativas de inversion "
                    "disponibles en el mercado peruano.\n\n"
                    "## Oportunidades destacadas\n\n"
                    "### Departamentos en preventa\n\n"
                    "La preventa sigue siendo la mejor ventana de oportunidad para inversionistas. "
                    "Los precios de preventa pueden ser entre 10% y 20% menores que los de entrega inmediata, "
                    "y con el desembolso postergado que negocia Proper, "
                    "el ahorro puede alcanzar entre S/24,000 y S/60,000.\n\n"
                    "### Distritos con mayor potencial\n\n"
                    "Los distritos con mejor relacion precio-renta para inversion incluyen zonas "
                    "con alta demanda de alquiler, buena conectividad y servicios. "
                    "El Analyzer de Proper permite comparar metricas por propiedad "
                    "para identificar las mejores oportunidades.\n\n"
                    "## Tendencias a observar\n\n"
                    "- La demanda de alquiler se mantiene fuerte en distritos bien conectados\n"
                    "- Los creditos hipotecarios mantienen tasas competitivas\n"
                    "- La apreciacion de inmuebles en zonas emergentes supera el promedio\n"
                    "- Los inversionistas priorizan data sobre intuicion al elegir propiedades\n\n"
                    "## Recomendaciones para inversionistas\n\n"
                    "1. **Analiza antes de comprar**: Usa el Analyzer gratuito de Proper para evaluar cualquier propiedad\n"
                    "2. **Aprovecha la preventa**: Las mejores condiciones estan en etapa de preventa\n"
                    "3. **Considera el desembolso postergado**: Ahorra miles de soles en el proceso\n"
                    "4. **Delega la gestion**: Proper Rentas administra tu propiedad de forma integral\n\n"
                ),
                "cta_section": (
                    "## Accede a oportunidades exclusivas\n\n"
                    "En Proper tenemos acceso a ventas privadas y propiedades off-market "
                    "con condiciones preferentes. La asesoria es **100% gratuita**.\n\n"
                    "**[Descubre tu proxima inversion en proper.com.pe](https://proper.com.pe)**\n\n"
                    "Inversion desde S/25,000 | Ventas privadas | Asesoria GRATIS"
                ),
                "social_share_text": "Nuevo reporte del mercado inmobiliario en Lima: metricas actualizadas, distritos con mayor potencial y oportunidades de inversion. Consultalo gratis en proper.com.pe/blog",
            },
            "guide": {
                "tipo": "guide",
                "title": "Paso a paso: Como comprar tu primer departamento de inversion en Peru",
                "meta_description": "Guia paso a paso para comprar tu primer departamento de inversion en Peru. Desde el ahorro inicial de S/25,000 hasta generar rentas pasivas. Asesoria gratuita con Proper.",
                "keywords": ["comprar departamento inversion Peru", "primer departamento inversion", "guia inversion inmobiliaria", "como invertir en departamentos", "Proper guia"],
                "content": (
                    "## Antes de empezar: Lo que necesitas saber\n\n"
                    "Comprar tu primer departamento de inversion puede parecer abrumador, "
                    "pero con la guia correcta es mas simple de lo que imaginas. "
                    "En esta guia te explicamos cada paso del proceso.\n\n"
                    "**Requisitos basicos:**\n"
                    "- Ahorro inicial desde S/25,000\n"
                    "- Ingresos mensuales estables (formal o independiente)\n"
                    "- Historial crediticio razonable\n"
                    "- Ganas de construir patrimonio a largo plazo\n\n"
                    "## Paso 1: Define tu perfil de inversionista\n\n"
                    "Antes de ver propiedades, necesitas saber cuanto puedes invertir realmente. "
                    "Proper ofrece una herramienta gratuita llamada Perfil del Inversionista "
                    "que analiza tu capacidad de financiamiento y te recomienda opciones ideales.\n\n"
                    "Registrate gratis en proper.com.pe para acceder a esta herramienta.\n\n"
                    "## Paso 2: Aprende a leer las metricas\n\n"
                    "No compres un departamento porque 'se ve bonito'. Aprende a evaluarlo con datos:\n\n"
                    "- **Cap Rate**: Rentabilidad neta anual (busca arriba de 5%, ideal 6.9%+)\n"
                    "- **TIR**: Retorno total incluyendo apreciacion (21.8% promedio en Proper)\n"
                    "- **Gross Yield**: Rentabilidad bruta (7.4% promedio)\n"
                    "- **ROI**: Retorno total en un periodo (40.2% en 5 anos)\n\n"
                    "El Analyzer de Proper calcula todo esto automaticamente. Es gratuito.\n\n"
                    "## Paso 3: Elige la propiedad correcta\n\n"
                    "Un asesor de Proper te presenta las propiedades que mejor se ajustan a tu perfil. "
                    "Estas son seleccionadas por su potencial de rentabilidad, "
                    "ubicacion y demanda de alquiler.\n\n"
                    "Las propiedades en preventa ofrecen las mejores condiciones: "
                    "precios mas bajos y acceso al desembolso postergado.\n\n"
                    "## Paso 4: Gestiona tu credito hipotecario\n\n"
                    "Proper te acompana en todo el proceso de credito hipotecario. "
                    "Negociamos condiciones preferentes con los bancos y te ayudamos "
                    "a aprovechar el desembolso postergado, que te ahorra entre S/24,000 y S/60,000.\n\n"
                    "## Paso 5: Firma y espera la entrega\n\n"
                    "Con el desembolso postergado, no empiezas a pagar cuotas del banco "
                    "hasta que te entreguen el departamento. Esto te da tiempo para prepararte "
                    "financieramente mientras la inmobiliaria construye.\n\n"
                    "## Paso 6: Pon tu depa a trabajar\n\n"
                    "Una vez recibido el departamento, Proper Rentas se encarga de:\n"
                    "- Encontrar el inquilino ideal\n"
                    "- Cobrar la renta mensual\n"
                    "- Administrar el mantenimiento\n"
                    "- Resolver cualquier incidencia\n\n"
                    "La renta del inquilino cubre la mayor parte de tu cuota del banco. "
                    "El depa se paga solo y tu patrimonio crece mes a mes.\n\n"
                ),
                "cta_section": (
                    "## Tu primer paso empieza aqui\n\n"
                    "No necesitas ser experto. No necesitas ser millonario. "
                    "Solo necesitas tomar la decision de empezar.\n\n"
                    "En Proper te asesoramos **100% gratis** en cada paso del camino.\n\n"
                    "**[Registrate gratis en proper.com.pe](https://proper.com.pe)**\n\n"
                    "Inversion desde S/25,000 | Asesoria experta GRATIS | El depa se paga solo"
                ),
                "social_share_text": "Publicamos la guia definitiva para comprar tu primer departamento de inversion en Peru: paso a paso, desde S/25,000 hasta generar rentas pasivas. Leela en proper.com.pe/blog",
            },
        }

        article = blog_library.get(article_type, blog_library["educational"])
        article = dict(article)  # shallow copy

        if topic:
            article["topic_personalizado"] = topic
        if news_item:
            article["news_source"] = {
                "title": news_item.get("title", ""),
                "source_name": news_item.get("source_name", ""),
                "source_url": news_item.get("source_url", ""),
            }
            # Customize title based on news
            news_title = news_item.get("title", "")
            if news_title:
                article["title"] = f"Analisis: {news_title[:80]} y su impacto en la inversion inmobiliaria"

        return article

    def generate_content_batch(self, analyses_from_db):
        """Genera contenido basado en los analisis almacenados en la DB."""
        results = []
        video_types_used = set()
        carousel_types_used = set()

        for analysis in analyses_from_db:
            analysis_text = analysis.get("full_analysis") or analysis.get("summary") or ""
            if not analysis_text or len(analysis_text) < 50:
                continue

            insights = self._extract_insights(analysis_text)

            # Generate video script (avoid duplicates)
            video_type = self._determine_video_type(insights)
            if video_type not in video_types_used:
                video_types_used.add(video_type)
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

            # Generate carousel plan (avoid duplicates)
            carousel_type = self._determine_carousel_type(insights)
            if carousel_type not in carousel_types_used:
                carousel_types_used.add(carousel_type)
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

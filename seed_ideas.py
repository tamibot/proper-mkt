"""Seed script — Insert 20 high-quality content ideas into the Proper MKT database."""

import sys
import os

# Ensure project root is on the path
sys.path.insert(0, os.path.dirname(__file__))

from database import insert_content_idea


# ──────────────────────────────────────────────
# TIKTOK / REELS — 10 ideas
# ──────────────────────────────────────────────

tiktok_ideas = [
    # --- Mito vs Realidad (2) ---
    {
        "title": "Mito vs Realidad: 'Necesitas ser millonario para invertir en inmuebles'",
        "description": "Video corto desmintiendo el mito de que invertir en departamentos es solo para ricos. Mostrar que con S/25,000 de cuota inicial y desembolso diferido puedes empezar. Usar datos reales del mercado peruano y cerrar con el simulador de Proper.",
        "hook_suggestion": "Te dijeron que necesitas ser millonario para invertir en departamentos... te mintieron.",
        "structure": "1. Hook impactante (3s) | 2. Presentar el mito con texto en pantalla (5s) | 3. Revelar la realidad con cifras: S/25,000 cuota inicial (8s) | 4. Explicar desembolso diferido y ahorro de S/24,000-60,000 (10s) | 5. CTA final (4s)",
        "cta_suggestion": "Regístrate gratis en proper.com.pe y agenda tu asesoría personalizada. Link en bio.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "high",
        "tags": [
            "mito_vs_realidad", "inversion_inmobiliaria", "educacion_financiera",
            "proper", "peru", "departamentos"
        ],
        "inspired_by": None,
    },
    {
        "title": "Mito vs Realidad: 'La AFP me va a salvar cuando me jubile'",
        "description": "Contrastar la expectativa vs la realidad de las pensiones AFP en Perú. Dato clave: 7 de 10 peruanos no tendrán acceso a pensión y los que sí, recibirán S/750-1,100 mensuales. Proponer inversión inmobiliaria como alternativa real de ingreso pasivo.",
        "hook_suggestion": "¿Confías en tu AFP para tu jubilación? Este dato te va a asustar.",
        "structure": "1. Hook con pregunta directa (3s) | 2. Dato impactante: 7/10 sin pensión (5s) | 3. Monto real AFP: S/750-1,100/mes (5s) | 4. Alternativa: renta de departamento genera ingresos pasivos reales (8s) | 5. Proper como solución con asesoría gratuita (5s) | 6. CTA (4s)",
        "cta_suggestion": "No esperes a los 65 para darte cuenta. Empieza hoy con asesoría gratuita en proper.com.pe.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "high",
        "tags": [
            "mito_vs_realidad", "AFP", "pensiones", "jubilacion",
            "inversion_inmobiliaria", "peru", "proper"
        ],
        "inspired_by": None,
    },

    # --- Dato Impactante (2) ---
    {
        "title": "7 de cada 10 peruanos NO tendrán pensión — ¿y tú?",
        "description": "Video con cifra impactante sobre la crisis de pensiones en Perú. Visualizar el dato con gráficos simples. Transicionar a la solución: invertir en inmuebles como plan de retiro alternativo. Mencionar TIR promedio del 25% anual.",
        "hook_suggestion": "7 de cada 10 peruanos se van a jubilar sin pensión. ¿Vas a ser uno de ellos?",
        "structure": "1. Dato impactante en pantalla con voz (4s) | 2. Contexto: los que sí tienen AFP reciben S/750-1,100 (5s) | 3. Pregunta: ¿Te alcanza para vivir? (3s) | 4. Solución: inversión inmobiliaria con TIR del 25% anual (8s) | 5. Proper como puente accesible (5s) | 6. CTA (5s)",
        "cta_suggestion": "Asegura tu futuro hoy. Entra a proper.com.pe y simula tu primera inversión gratis.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "high",
        "tags": [
            "dato_impactante", "pensiones", "AFP", "estadisticas",
            "peru", "jubilacion", "proper"
        ],
        "inspired_by": None,
    },
    {
        "title": "Con S/25,000 puedes empezar a generar ingresos pasivos en Perú",
        "description": "Revelar que la barrera de entrada a la inversión inmobiliaria es más baja de lo que la gente cree. Explicar el modelo de desembolso diferido de Proper y cómo puedes ahorrar entre S/24,000 y S/60,000 mientras tu departamento se construye.",
        "hook_suggestion": "¿Sabías que con S/25,000 ya puedes ser inversionista inmobiliario en Perú?",
        "structure": "1. Hook con cifra sorpresa (3s) | 2. Explicar cuota inicial accesible (5s) | 3. Desembolso diferido: qué es y cuánto ahorras (8s) | 4. Visualizar ahorro S/24,000-60,000 (5s) | 5. Proper Rentas gestiona tu propiedad (5s) | 6. CTA (4s)",
        "cta_suggestion": "Usa el simulador hipotecario en proper.com.pe y descubre cuánto puedes generar.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "high",
        "tags": [
            "dato_impactante", "inversion_inmobiliaria", "cuota_inicial",
            "desembolso_diferido", "peru", "proper"
        ],
        "inspired_by": None,
    },

    # --- Paso a Paso (2) ---
    {
        "title": "Cómo invertir en tu primer departamento con Proper en 4 pasos",
        "description": "Guía rápida paso a paso del proceso de inversión con Proper. Desde el registro gratuito hasta la administración con Proper Rentas. Hacer énfasis en la simplicidad del proceso y la asesoría personalizada gratuita.",
        "hook_suggestion": "Invertir en departamentos nunca fue tan simple. Te explico en 4 pasos.",
        "structure": "1. Hook con slogan (3s) | 2. Paso 1: Regístrate gratis y agenda asesoría (5s) | 3. Paso 2: Usa el Analyzer y Simulador para elegir tu inversión (6s) | 4. Paso 3: Separa con cuota inicial desde S/25,000 (5s) | 5. Paso 4: Proper Rentas administra tu propiedad (6s) | 6. CTA (5s)",
        "cta_suggestion": "Empieza el paso 1 ahora: regístrate gratis en proper.com.pe. Asesoría sin compromiso.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "high",
        "tags": [
            "paso_a_paso", "tutorial", "como_invertir",
            "proper", "departamentos", "peru"
        ],
        "inspired_by": None,
    },
    {
        "title": "Cómo usar el Simulador Hipotecario de Proper para planificar tu inversión",
        "description": "Tutorial corto mostrando pantalla del simulador hipotecario. Explicar cómo ingresar datos, interpretar resultados de TIR, Cap Rate y retorno. Mostrar que cualquier persona puede usarlo gratis sin compromiso.",
        "hook_suggestion": "Esta herramienta gratuita te dice exactamente cuánto vas a ganar invirtiendo en inmuebles.",
        "structure": "1. Hook mostrando la herramienta (3s) | 2. Screen recording del simulador (5s) | 3. Explicar inputs: monto, plazo, zona (5s) | 4. Mostrar resultados: TIR, rentabilidad, flujo mensual (8s) | 5. Es gratis y sin compromiso (3s) | 6. CTA (4s)",
        "cta_suggestion": "Prueba el simulador ahora en proper.com.pe. Es gratis y te toma 2 minutos.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "medium",
        "tags": [
            "paso_a_paso", "tutorial", "simulador",
            "herramientas", "proper", "hipotecario"
        ],
        "inspired_by": None,
    },

    # --- Testimonio / Caso (2) ---
    {
        "title": "María invirtió S/25,000 a los 28 años — hoy genera ingresos pasivos",
        "description": "Caso de inversión tipo storytelling. Presentar un escenario realista de una joven profesional que decidió invertir en un departamento en preventa con Proper. Mostrar los números, el proceso y el resultado con Proper Rentas administrando.",
        "hook_suggestion": "María tenía 28 años, ganaba S/4,500 al mes y tomó la mejor decisión de su vida.",
        "structure": "1. Hook storytelling (4s) | 2. Situación inicial: profesional joven, ahorrando sin rumbo (5s) | 3. Descubre Proper, asesores le explican el modelo (5s) | 4. Invierte S/25,000 cuota inicial en preventa (5s) | 5. Desembolso diferido le permite seguir ahorrando (5s) | 6. Hoy tiene un activo que genera renta mensual (5s) | 7. CTA (4s)",
        "cta_suggestion": "¿Quieres ser como María? Agenda tu asesoría gratuita en proper.com.pe.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "high",
        "tags": [
            "testimonio", "caso_exito", "storytelling",
            "inversion_joven", "proper", "peru"
        ],
        "inspired_by": None,
    },
    {
        "title": "De ahorrar en el banco al 4% a invertir con TIR del 25% anual",
        "description": "Caso comparativo mostrando un escenario real: persona que tenía S/30,000 en ahorro bancario ganando casi nada vs. la misma persona invirtiendo en un departamento con Proper. Contrastar rendimientos a 5 años.",
        "hook_suggestion": "Tu banco te da 4% anual. Con inversión inmobiliaria puedes lograr hasta 25%. Te explico.",
        "structure": "1. Hook comparativo (3s) | 2. Escenario 1: S/30,000 en banco = S/1,200 en intereses al año (5s) | 3. Escenario 2: S/30,000 como cuota inicial en departamento (5s) | 4. TIR promedio 25% anual con Proper (5s) | 5. Comparación visual a 5 años (6s) | 6. La diferencia es abismal (3s) | 7. CTA (3s)",
        "cta_suggestion": "Deja de perder plata en el banco. Simula tu inversión gratis en proper.com.pe.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "medium",
        "tags": [
            "testimonio", "caso_comparativo", "banco_vs_inmueble",
            "TIR", "rendimiento", "proper"
        ],
        "inspired_by": None,
    },

    # --- Educación Financiera (2) ---
    {
        "title": "¿Qué es el Cap Rate y por qué importa al invertir en inmuebles?",
        "description": "Explicación clara y simple del Cap Rate (tasa de capitalización) para audiencia que no tiene formación financiera. Usar ejemplo real con números del mercado peruano. Comparar un buen vs mal Cap Rate.",
        "hook_suggestion": "Si no sabes qué es el Cap Rate, podrías estar perdiendo plata sin saberlo.",
        "structure": "1. Hook de urgencia (3s) | 2. Definición simple: Cap Rate = ingreso neto / precio del inmueble (5s) | 3. Ejemplo real: depa de S/300,000 que renta S/2,000/mes (8s) | 4. Cálculo en pantalla = 8% Cap Rate (5s) | 5. ¿Es bueno? Contextualizar vs promedio Lima (5s) | 6. Proper te ayuda a encontrar los mejores (3s) | 7. CTA (3s)",
        "cta_suggestion": "Aprende más en nuestras reuniones gratuitas de lunes y miércoles. Regístrate en proper.com.pe.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "medium",
        "tags": [
            "educacion_financiera", "cap_rate", "conceptos",
            "inversion_inmobiliaria", "proper", "peru"
        ],
        "inspired_by": None,
    },
    {
        "title": "TIR vs ROI: ¿Cuál es la diferencia y cuál te importa más?",
        "description": "Video educativo comparando TIR (Tasa Interna de Retorno) y ROI (Retorno sobre inversión). Explicar cuándo usar cada una y por qué la TIR es más relevante para inversiones inmobiliarias a largo plazo. Usar ejemplo con números reales de Proper.",
        "hook_suggestion": "TIR y ROI NO son lo mismo. Si los confundes, estás analizando mal tu inversión.",
        "structure": "1. Hook directo (3s) | 2. Definición ROI: ganancia / inversión (5s) | 3. Definición TIR: retorno considerando el tiempo (5s) | 4. Ejemplo: mismo depa, ROI vs TIR dan números distintos (8s) | 5. ¿Cuál usar? TIR para inmuebles a largo plazo (5s) | 6. Proper calcula ambos en su Analyzer (3s) | 7. CTA (3s)",
        "cta_suggestion": "¿Quieres entender tus números? Ven a nuestros talleres gratuitos. Info en proper.com.pe.",
        "platform": "tiktok",
        "content_type": "video",
        "priority": "medium",
        "tags": [
            "educacion_financiera", "TIR", "ROI", "conceptos",
            "inversion_inmobiliaria", "proper"
        ],
        "inspired_by": None,
    },
]


# ──────────────────────────────────────────────
# INSTAGRAM CAROUSELS — 10 ideas
# ──────────────────────────────────────────────

instagram_ideas = [
    # --- Educativo (2) ---
    {
        "title": "Inversión inmobiliaria explicada en 7 slides para principiantes",
        "description": "Carrusel educativo que explica desde cero qué es la inversión inmobiliaria, tipos de inversión (preventa, renta, plusvalía), ventajas vs otros instrumentos y cómo empezar en Perú con montos accesibles. Diseño limpio con iconos y cifras grandes.",
        "hook_suggestion": "Todo lo que necesitas saber sobre inversión inmobiliaria en 7 slides. Guarda este post.",
        "structure": "Slide 1: Portada — '¿Qué es la inversión inmobiliaria?' (diseño llamativo) | Slide 2: Definición simple + tipos: preventa, renta, plusvalía | Slide 3: ¿Por qué inmuebles? Tangible, valorización, ingreso pasivo | Slide 4: Mitos comunes desmentidos | Slide 5: ¿Cuánto necesitas? Desde S/25,000 | Slide 6: Pasos para empezar con Proper | Slide 7: CTA — Asesoría gratuita",
        "cta_suggestion": "Guarda este post y compártelo con alguien que necesita verlo. Agenda tu asesoría en proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "high",
        "tags": [
            "educativo", "principiantes", "inversion_inmobiliaria",
            "guia", "carrusel", "proper"
        ],
        "inspired_by": None,
    },
    {
        "title": "Crédito hipotecario en Perú: lo que nadie te explica",
        "description": "Carrusel explicando cómo funciona el crédito hipotecario para inversión en Perú. Cubrir: requisitos, tasas promedio, cuota inicial, plazos, y el concepto de desembolso diferido. Hacer énfasis en que Proper asesora gratis en todo el proceso.",
        "hook_suggestion": "Vas a pedir un crédito hipotecario y no entiendes nada. Aquí te lo explico fácil.",
        "structure": "Slide 1: Portada — 'Crédito Hipotecario: Lo que nadie te dice' | Slide 2: ¿Qué es y cómo funciona? | Slide 3: Requisitos básicos en Perú (ingreso mínimo, historial) | Slide 4: Tasas de interés promedio 2024-2025 | Slide 5: Cuota inicial: ¿cuánto necesitas realmente? | Slide 6: Desembolso diferido: el secreto que te ahorra miles | Slide 7: Proper te acompaña gratis en todo el proceso | Slide 8: CTA",
        "cta_suggestion": "¿Tienes dudas? Agenda una asesoría gratuita con nuestro equipo en proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "high",
        "tags": [
            "educativo", "credito_hipotecario", "hipoteca",
            "peru", "bancos", "proper"
        ],
        "inspired_by": None,
    },

    # --- Comparativo (2) ---
    {
        "title": "AFP vs Inversión Inmobiliaria: ¿Dónde estará tu plata en 20 años?",
        "description": "Carrusel comparativo visual mostrando lado a lado qué pasa con tu dinero en AFP vs inversión inmobiliaria a 20 años. Usar cifras reales del mercado peruano. Incluir infografías con gráficos de barras simples.",
        "hook_suggestion": "AFP vs Inversión Inmobiliaria. La comparación que tu AFP no quiere que veas.",
        "structure": "Slide 1: Portada — 'AFP vs Inmuebles: ¿Cuál gana?' | Slide 2: AFP: ¿Qué recibes? S/750-1,100/mes | Slide 3: Inversión inmobiliaria: renta mensual + plusvalía | Slide 4: Comparación a 10 años (gráfico) | Slide 5: Comparación a 20 años (gráfico) | Slide 6: Ventajas adicionales: activo tangible, herencia | Slide 7: ¿Por qué no ambos? Diversifica | Slide 8: CTA — Calcula tu retorno con Proper",
        "cta_suggestion": "No dejes tu futuro solo en manos de la AFP. Simula tu inversión en proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "high",
        "tags": [
            "comparativo", "AFP", "inversion_inmobiliaria",
            "jubilacion", "pensiones", "proper"
        ],
        "inspired_by": None,
    },
    {
        "title": "Cuenta de ahorros vs Departamento en preventa: La verdad en números",
        "description": "Carrusel que compara tener S/30,000 en una cuenta de ahorros bancaria vs usar ese monto como cuota inicial de un departamento en preventa. Mostrar rendimientos reales a 1, 3 y 5 años. Incluir efecto de la inflación.",
        "hook_suggestion": "S/30,000 en el banco vs S/30,000 en un departamento. Mira la diferencia.",
        "structure": "Slide 1: Portada visual con los dos escenarios | Slide 2: Escenario banco: tasa 3-5% anual, tu plata pierde valor vs inflación | Slide 3: Escenario inmueble: plusvalía + renta mensual | Slide 4: Año 1 — comparación de ganancias | Slide 5: Año 3 — la brecha se agranda | Slide 6: Año 5 — resultado final | Slide 7: Factor inflación: el banco te hace perder | Slide 8: CTA — Proper te ayuda a dar el salto",
        "cta_suggestion": "Tu plata en el banco pierde valor cada día. Descubre cuánto puedes ganar en proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "medium",
        "tags": [
            "comparativo", "ahorro_vs_inversion", "banco",
            "preventa", "inflacion", "proper"
        ],
        "inspired_by": None,
    },

    # --- Proceso Proper (2) ---
    {
        "title": "Así funciona Proper: De tu primera consulta a tu primer departamento",
        "description": "Carrusel que muestra el journey completo del inversionista con Proper. Desde el registro gratuito, pasando por la asesoría, uso de herramientas (Analyzer, Simulador, Perfil del Inversionista), hasta Proper Rentas. Transmitir confianza y simplicidad.",
        "hook_suggestion": "Invertir en departamentos nunca fue tan simple. Te mostramos cómo funciona Proper paso a paso.",
        "structure": "Slide 1: Portada — 'Tu camino con Proper' | Slide 2: Paso 1: Regístrate gratis en proper.com.pe | Slide 3: Paso 2: Asesoría personalizada sin costo | Slide 4: Paso 3: Usa nuestras herramientas — Analyzer, Simulador, Perfil | Slide 5: Paso 4: Elige tu inversión ideal | Slide 6: Paso 5: Desembolso diferido = ahorras miles | Slide 7: Paso 6: Proper Rentas administra tu propiedad | Slide 8: CTA — Empieza hoy",
        "cta_suggestion": "Todo empieza con un registro gratuito. Entra a proper.com.pe y da el primer paso.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "high",
        "tags": [
            "proceso_proper", "como_funciona", "journey",
            "herramientas", "proper_rentas", "proper"
        ],
        "inspired_by": None,
    },
    {
        "title": "Proper Rentas: Cómo generamos ingresos pasivos por ti",
        "description": "Carrusel explicando el servicio de Proper Rentas — administración integral de propiedades. Cubrir: qué incluye, cómo funciona, beneficios para el inversionista, y por qué elimina el dolor de cabeza de ser propietario.",
        "hook_suggestion": "¿Invertir en un departamento sin tener que lidiar con inquilinos? Existe y se llama Proper Rentas.",
        "structure": "Slide 1: Portada — 'Proper Rentas: Ingresos pasivos de verdad' | Slide 2: El problema: ser propietario es un trabajo | Slide 3: La solución: Proper Rentas administra todo por ti | Slide 4: ¿Qué incluye? Búsqueda de inquilinos, contratos, cobranza | Slide 5: Mantenimiento, reportes mensuales, soporte legal | Slide 6: Tú solo recibes tu renta cada mes | Slide 7: Respaldado por partners: UTEC Ventures, ASEI, Peru Proptech | Slide 8: CTA",
        "cta_suggestion": "Conoce más sobre Proper Rentas y empieza a generar ingresos pasivos. Info en proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "medium",
        "tags": [
            "proceso_proper", "proper_rentas", "administracion",
            "ingresos_pasivos", "property_management", "proper"
        ],
        "inspired_by": None,
    },

    # --- Data Driven (2) ---
    {
        "title": "5 cifras del mercado inmobiliario peruano que todo inversionista debe conocer",
        "description": "Carrusel con datos duros y estadísticas relevantes del mercado inmobiliario en Perú. Incluir: déficit habitacional, crecimiento de precios, rentabilidad promedio, zonas con mayor plusvalía y tendencias 2025-2026.",
        "hook_suggestion": "5 datos del mercado inmobiliario peruano que pueden cambiar tu forma de pensar sobre inversión.",
        "structure": "Slide 1: Portada — '5 cifras clave del mercado inmobiliario peruano' | Slide 2: Dato 1: Déficit habitacional en Perú (demanda insatisfecha) | Slide 3: Dato 2: Crecimiento promedio de precios por m2 | Slide 4: Dato 3: TIR promedio del 25% en inversión con Proper | Slide 5: Dato 4: Zonas con mayor rentabilidad en Lima | Slide 6: Dato 5: Proyección de crecimiento del sector | Slide 7: ¿Qué significa esto para ti? Oportunidad real | Slide 8: CTA — Analiza tu inversión con Proper",
        "cta_suggestion": "Los datos no mienten. Empieza a invertir con información real. Visita proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "medium",
        "tags": [
            "data_driven", "estadisticas", "mercado_inmobiliario",
            "cifras", "peru", "tendencias", "proper"
        ],
        "inspired_by": None,
    },
    {
        "title": "Radiografía del inversionista inmobiliario peruano en 2025",
        "description": "Carrusel con datos sobre el perfil del inversionista inmobiliario en Perú: edad promedio, ingreso, motivaciones, zonas preferidas y tipo de inversión más popular. Hacer que la audiencia se identifique y se anime a dar el paso.",
        "hook_suggestion": "¿Cómo es el inversionista inmobiliario promedio en Perú? Te vas a sorprender.",
        "structure": "Slide 1: Portada — 'Perfil del inversionista inmobiliario peruano' | Slide 2: Edad: 25-45 años (más jóvenes de lo que crees) | Slide 3: NSE: B y C — no necesitas ser de NSE A | Slide 4: Motivación #1: plan de retiro alternativo a la AFP | Slide 5: Inversión promedio: desde S/25,000 cuota inicial | Slide 6: Zonas preferidas y tipos de inversión | Slide 7: ¿Te identificas? Tú también puedes ser inversionista | Slide 8: CTA — Descubre tu perfil con Proper",
        "cta_suggestion": "Descubre tu perfil de inversionista gratis con nuestra herramienta. Entra a proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "medium",
        "tags": [
            "data_driven", "perfil_inversionista", "estadisticas",
            "demografia", "peru", "NSE", "proper"
        ],
        "inspired_by": None,
    },

    # --- Lifestyle / Aspiracional (2) ---
    {
        "title": "Libertad financiera: Cómo los ingresos pasivos cambian tu vida",
        "description": "Carrusel aspiracional mostrando el impacto real de tener ingresos pasivos por renta de departamentos. No vender lujo inalcanzable sino tranquilidad financiera: pagar cuentas sin estrés, viajar, dedicar tiempo a lo que importa. Tono cercano y realista.",
        "hook_suggestion": "Imagina recibir una renta cada mes sin tener que trabajar por ella. Así se siente la libertad financiera.",
        "structure": "Slide 1: Portada — 'Libertad financiera no es ser rico. Es tener opciones.' | Slide 2: ¿Qué significa libertad financiera? (definición real, no fantasía) | Slide 3: Ingresos pasivos = tranquilidad (pagar cuentas, emergencias cubiertas) | Slide 4: Tiempo para lo que importa (familia, proyectos, viajes) | Slide 5: Un departamento puede ser tu primer paso | Slide 6: Desde S/25,000 puedes empezar — no necesitas millones | Slide 7: Proper te acompaña en cada paso | Slide 8: CTA",
        "cta_suggestion": "Tu libertad financiera empieza con una decisión. Da el primer paso en proper.com.pe.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "medium",
        "tags": [
            "lifestyle", "aspiracional", "libertad_financiera",
            "ingresos_pasivos", "motivacion", "proper"
        ],
        "inspired_by": None,
    },
    {
        "title": "A los 30 decidí invertir en lugar de solo ahorrar — mi plan a 10 años",
        "description": "Carrusel storytelling en primera persona (ficticio pero realista) mostrando el plan de inversión de alguien de 30 años. Proyección a 10 años: 1 departamento hoy, 2 a los 35, libertad financiera a los 40. Usar cifras reales y tono motivacional pero honesto.",
        "hook_suggestion": "Tengo 30 años y este es mi plan para alcanzar libertad financiera a los 40.",
        "structure": "Slide 1: Portada — 'Mi plan de inversión: de los 30 a los 40' | Slide 2: Año 0 (hoy): Primer departamento con S/25,000 de cuota inicial | Slide 3: Años 1-3: Desembolso diferido, ahorro acelerado | Slide 4: Año 3-5: Primer depa rentando + ahorro para el segundo | Slide 5: Año 5-7: Segundo departamento, dos fuentes de ingreso pasivo | Slide 6: Año 10: Dos propiedades generando renta, patrimonio sólido | Slide 7: No es fantasía — es matemática. TIR 25% anual | Slide 8: CTA — Arma tu plan con Proper",
        "cta_suggestion": "¿Cuál es tu plan? Arma el tuyo con asesoría gratuita en proper.com.pe. Reuniones lunes y miércoles.",
        "platform": "instagram",
        "content_type": "carousel",
        "priority": "high",
        "tags": [
            "lifestyle", "aspiracional", "plan_inversion",
            "storytelling", "largo_plazo", "proper"
        ],
        "inspired_by": None,
    },
]


def main():
    """Insert all 20 content ideas into the database."""
    all_ideas = tiktok_ideas + instagram_ideas
    inserted = 0
    errors = 0

    print(f"[SEED] Insertando {len(all_ideas)} ideas de contenido...")
    print("=" * 60)

    for idea in all_ideas:
        try:
            idea_id = insert_content_idea(idea)
            inserted += 1
            print(f"  [OK] #{idea_id} — {idea['title'][:70]}...")
        except Exception as e:
            errors += 1
            print(f"  [ERROR] {idea['title'][:50]}... — {e}")

    print("=" * 60)
    print(f"[SEED] Completado: {inserted} insertadas, {errors} errores.")


if __name__ == "__main__":
    main()

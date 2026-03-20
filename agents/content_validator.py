"""Content Validator Agent for Proper MKT.

Validates that generated content aligns with Proper's verified brand identity,
partnerships, and business model. Flags false claims, incorrect terminology,
and off-brand messaging.
"""

import re
import json
from typing import Optional


# ── Proper Brand Facts (verified from official brief) ────────────────────────

BRAND_FACTS = {
    "company_name": "Proper",
    "website": "proper.com.pe",
    "description": "Plataforma que ayuda a personas a invertir en departamentos de forma simple",
    "minimum_investment": "S/25,000 (cuota inicial)",
    "tir_promedio": "25% anual",
    "deferred_disbursement_savings": "S/24,000 - S/60,000",
    "model": "Banco compra departamento → Inquilino paga banco → Inversionista crece capital",
    "advisory_cost": "100% GRATIS",
    "target_age": "25-45 años",
    "target_nse": "B y C",
    "target_country": "Perú",
    "tone": "Cercano, confiable, profesional",
    "tools": [
        "Analyzer",
        "Simulador Hipotecario",
        "Perfil del Inversionista",
    ],
    "services": [
        "Proper Rentas (administración integral de propiedades)",
    ],
    "education": [
        "Reuniones gratuitas lunes y miércoles",
        "Talleres trimestrales",
    ],
    "cta": "Regístrate en proper.com.pe para asesoría gratuita",
}

# Real partners and allies
REAL_PARTNERS = [
    "Pro Innovate",
    "Startup Perú",
    "UTEC Ventures",
    "La Mezcladora",
    "Hub de Innovación",
    "Ministerio de la Producción",
    "ASEI",
    "Asociación de Empresas Inmobiliarias del Perú",
    "Perú Proptech",
]

# Key claims that must match brand
KEY_CLAIMS = {
    "investors_pay_nothing": True,       # Developers pay Proper, NOT investors
    "developers_are_commercial_force": True,
    "free_advisory": True,
    "deferred_disbursement": True,
}

# ── Blacklisted terms and false claims ────────────────────────────────────────

# Companies/brands that are NOT partners
FALSE_PARTNERS = [
    "mercado libre",
    "mercadolibre",
    "amazon",
    "falabella",
    "ripley",
    "aliexpress",
    "shopify",
    "rappi",
    "uber",
    "airbnb",
    "booking",
]

# Business models that do NOT describe Proper
FALSE_BUSINESS_MODELS = [
    "crowdfunding",
    "crowdsourcing",
    "financiamiento colectivo",
    "inversión fraccionada",
    "fractional investment",
    "tokenizado",
    "tokenized",
    "token",
    "blockchain",
    "crypto",
    "criptomoneda",
    "nft",
    "agencia inmobiliaria",   # Proper is NOT a real estate agency
    "agencia de bienes raíces",
    "real estate agency",
]

# Things Proper does NOT do
FALSE_CLAIMS_PATTERNS = [
    # Proper does not charge investors
    r"(?i)cobr(a|amos|ar)\s+(al\s+)?inversionista",
    r"(?i)comisi[oó]n\s+(del?\s+)?inversionista",
    r"(?i)el inversionista\s+paga",
    # Proper does not sell properties directly
    r"(?i)proper\s+vende\s+(departamento|propiedad|inmueble)",
    r"(?i)vendemos\s+(departamento|propiedad|inmueble)",
    # Proper is not a real estate agency
    r"(?i)somos\s+una?\s+(agencia|inmobiliaria)",
    r"(?i)proper\s+es\s+una?\s+(agencia|inmobiliaria)",
]


class ContentValidator:
    """Validates generated content against Proper's verified brand identity."""

    def __init__(self):
        self.brand = BRAND_FACTS
        self.real_partners = [p.lower() for p in REAL_PARTNERS]
        self.false_partners = [p.lower() for p in FALSE_PARTNERS]
        self.false_models = [m.lower() for m in FALSE_BUSINESS_MODELS]
        self.false_claim_patterns = [re.compile(p) for p in FALSE_CLAIMS_PATTERNS]

    def validate_content(self, content_dict: dict) -> dict:
        """Validate a content dictionary against brand rules.

        Args:
            content_dict: Dictionary with keys like 'title', 'raw_text',
                          'script_json', 'carousel_json', etc.

        Returns:
            dict with:
                - is_valid (bool): True if content passes all checks
                - issues (list[str]): Descriptions of each problem found
                - corrected_fields (dict): Suggested corrections where possible
                - severity (str): 'critical', 'warning', or 'clean'
        """
        issues = []
        corrected_fields = {}

        # Gather all text to check
        text_sources = self._extract_all_text(content_dict)
        full_text = " ".join(text_sources).lower()

        # ── Check 1: False partner claims ─────────────────────────────
        for partner in self.false_partners:
            if partner in full_text:
                issues.append(
                    f"FALSE PARTNER: Mentions '{partner}' — Proper has NO alliance "
                    f"with this company. Real partners: {', '.join(REAL_PARTNERS[:5])}"
                )

        # ── Check 2: Wrong business model ─────────────────────────────
        for model in self.false_models:
            if model in full_text:
                issues.append(
                    f"WRONG MODEL: Uses term '{model}' — Proper is NOT {model}. "
                    f"Proper is a platform that helps people invest in apartments simply."
                )

        # ── Check 3: False claim patterns ─────────────────────────────
        for pattern in self.false_claim_patterns:
            matches = pattern.findall(full_text)
            if matches:
                issues.append(
                    f"FALSE CLAIM: Pattern matched '{pattern.pattern}' — "
                    f"investors pay NOTHING; developers pay Proper."
                )

        # ── Check 4: Verify minimum investment amount ─────────────────
        wrong_amounts = re.findall(
            r"(?i)(?:desde|mínimo|inversión\s+mínima)\s*(?:de\s+)?s/?\.?\s*([\d,\.]+)",
            full_text,
        )
        for amount_str in wrong_amounts:
            amount_clean = amount_str.replace(",", "").replace(".", "")
            try:
                amount = int(amount_clean)
                if amount < 25000:
                    issues.append(
                        f"WRONG AMOUNT: States minimum of S/{amount_str} but "
                        f"actual minimum is S/25,000."
                    )
                    corrected_fields["minimum_investment"] = "S/25,000"
            except ValueError:
                pass

        # ── Check 5: TIR accuracy ─────────────────────────────────────
        tir_matches = re.findall(r"(?i)tir\s*(?:promedio|anual)?\s*(?:de|del|:)?\s*(\d+)", full_text)
        for tir_str in tir_matches:
            tir_val = int(tir_str)
            if tir_val != 25 and tir_val > 10:
                issues.append(
                    f"WRONG TIR: States TIR of {tir_val}% but Proper's average TIR "
                    f"is 25% annual."
                )
                corrected_fields["tir"] = "25% anual"

        # ── Check 6: Advisory is free ─────────────────────────────────
        paid_advisory_patterns = [
            r"(?i)asesor[ií]a\s+(paga|pagada|premium|de pago|con costo)",
            r"(?i)cobr(a|amos)\s+por\s+asesor[ií]a",
        ]
        for pattern_str in paid_advisory_patterns:
            if re.search(pattern_str, full_text):
                issues.append(
                    "FALSE CLAIM: Suggests advisory has a cost — "
                    "Proper advisory is 100% FREE (gratis)."
                )
                corrected_fields["advisory_cost"] = "100% GRATIS"

        # ── Check 7: Mentions non-existent tools or services ──────────
        fake_tools = ["calculadora", "app", "aplicación móvil", "marketplace"]
        for tool in fake_tools:
            if tool in full_text and tool not in [t.lower() for t in BRAND_FACTS["tools"]]:
                # Only flag if claiming Proper has this tool
                if re.search(rf"(?i)(?:proper|nuestr[oa])\s+{tool}", full_text):
                    issues.append(
                        f"UNVERIFIED TOOL: Mentions '{tool}' as a Proper tool. "
                        f"Verified tools: {', '.join(BRAND_FACTS['tools'])}"
                    )

        # ── Check 8: Title-level issues ───────────────────────────────
        title = content_dict.get("title", "")
        if title:
            title_lower = title.lower()
            for partner in self.false_partners:
                if partner in title_lower:
                    issues.append(
                        f"TITLE: Contains false partner '{partner}' in the title."
                    )
                    corrected_fields["title"] = self._suggest_title_fix(title, partner)

        # Determine severity
        if any("FALSE PARTNER" in i or "FALSE CLAIM" in i or "WRONG MODEL" in i for i in issues):
            severity = "critical"
        elif issues:
            severity = "warning"
        else:
            severity = "clean"

        return {
            "is_valid": len(issues) == 0,
            "issues": issues,
            "corrected_fields": corrected_fields,
            "severity": severity,
        }

    def validate_text(self, text: str) -> dict:
        """Convenience method to validate raw text content."""
        return self.validate_content({"raw_text": text})

    def _extract_all_text(self, content_dict: dict) -> list:
        """Extract all text fields from a content dictionary for validation."""
        texts = []

        # Direct text fields
        for key in ("title", "raw_text", "description"):
            val = content_dict.get(key)
            if val and isinstance(val, str):
                texts.append(val)

        # JSON fields (script_json, carousel_json)
        for json_key in ("script_json", "carousel_json"):
            val = content_dict.get(json_key)
            if val:
                if isinstance(val, str):
                    try:
                        val = json.loads(val)
                    except (json.JSONDecodeError, TypeError):
                        texts.append(val)
                        continue
                texts.append(self._flatten_json_text(val))

        return texts

    def _flatten_json_text(self, obj, depth: int = 0) -> str:
        """Recursively extract all string values from a JSON object."""
        if depth > 20:
            return ""
        parts = []
        if isinstance(obj, dict):
            for v in obj.values():
                parts.append(self._flatten_json_text(v, depth + 1))
        elif isinstance(obj, list):
            for item in obj:
                parts.append(self._flatten_json_text(item, depth + 1))
        elif isinstance(obj, str):
            parts.append(obj)
        return " ".join(parts)

    def _suggest_title_fix(self, title: str, offending_term: str) -> str:
        """Suggest a corrected title removing the offending term."""
        # Simple removal — human review recommended
        return re.sub(
            rf"(?i)\s*x\s*{re.escape(offending_term)}[:\-—]?\s*",
            ": ",
            title,
        ).strip(": -—")

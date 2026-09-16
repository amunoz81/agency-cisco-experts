"""Verticales de industria soportadas (etiquetas EN/ES).

Lista alineada a las industrias que Cisco atiende con arquitecturas validadas.
"""

from __future__ import annotations

# id -> {"en": ..., "es": ...}
VERTICALS: dict[str, dict[str, str]] = {
    "manufacturing": {"en": "Manufacturing", "es": "Manufactura"},
    "oil_gas": {"en": "Oil & Gas", "es": "Petróleo y Gas"},
    "utilities": {"en": "Utilities & Energy", "es": "Servicios Públicos y Energía"},
    "mining": {"en": "Mining", "es": "Minería"},
    "healthcare": {"en": "Healthcare", "es": "Salud"},
    "education": {"en": "Education", "es": "Educación"},
    "retail": {"en": "Retail", "es": "Retail / Comercio"},
    "financial": {"en": "Financial Services", "es": "Servicios Financieros"},
    "public_sector": {
        "en": "Public Sector / Government", "es": "Sector Público / Gobierno",
    },
    "defense": {"en": "Defense", "es": "Defensa"},
    "service_provider": {
        "en": "Service Provider / Telecom", "es": "Proveedor de Servicios / Telecom",
    },
    "transportation": {"en": "Transportation & Logistics", "es": "Transporte y Logística"},
    "hospitality": {"en": "Hospitality", "es": "Hotelería"},
    "media": {"en": "Media & Entertainment", "es": "Medios y Entretenimiento"},
    "sports": {"en": "Sports & Venues", "es": "Deportes y Recintos"},
    "smart_cities": {"en": "Smart Cities", "es": "Ciudades Inteligentes"},
    "agriculture": {"en": "Agriculture", "es": "Agricultura"},
    "real_estate": {
        "en": "Real Estate & Smart Buildings", "es": "Inmobiliario / Edificios Inteligentes",
    },
    "technology": {"en": "Technology & Software", "es": "Tecnología y Software"},
    "other": {"en": "Other", "es": "Otro"},
}


def verticals_list(lang: str = "en") -> list[dict[str, str]]:
    lang = "es" if lang.lower().startswith("es") else "en"
    return [{"id": vid, "label": labels[lang]} for vid, labels in VERTICALS.items()]


def vertical_label(vid: str | None, lang: str = "en") -> str | None:
    if not vid:
        return None
    lang = "es" if lang.lower().startswith("es") else "en"
    entry = VERTICALS.get(vid)
    return entry[lang] if entry else vid

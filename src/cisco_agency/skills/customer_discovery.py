"""Skill: Descubrimiento del cliente.

Entrada: dict libre (YAML/JSON de la oportunidad).
Decisión: normaliza a una `Opportunity` estructurada e infiere banderas de
alcance a partir de sedes/cargas/inventario.
Entrega: ficha de oportunidad con objetivos, sedes, cargas, inventario,
restricciones, presupuesto y datos pendientes.
"""

from __future__ import annotations

from ..schemas import Opportunity, Site


def build_opportunity(raw: dict) -> Opportunity:
    sites = [Site(**s) if isinstance(s, dict) else Site(name=str(s)) for s in raw.get("sites", [])]

    has_plants = any(s.kind == "planta" for s in sites)
    workloads_text = " ".join(raw.get("workloads", [])).lower()

    opp = Opportunity(
        customer=raw.get("customer", "Cliente sin nombre"),
        industry=raw.get("industry"),
        objectives=raw.get("objectives", []),
        sites=sites,
        workloads=raw.get("workloads", []),
        inventory=raw.get("inventory", []),
        constraints=raw.get("constraints", []),
        budget=raw.get("budget"),
        horizon_years=raw.get("horizon_years", 3),
        pending_data=raw.get("pending_data", []),
        it_ot_present=raw.get("it_ot_present", has_plants),
        needs_correlation_soc=raw.get(
            "needs_correlation_soc",
            any(k in workloads_text for k in ("soc", "siem", "correlaci", "splunk")),
        ),
        needs_datacenter_ai=raw.get(
            "needs_datacenter_ai",
            any(
                k in workloads_text
                for k in ("gpu", "ia", "ai", "datacenter", "cómputo", "computo")
            ),
        ),
    )
    return opp

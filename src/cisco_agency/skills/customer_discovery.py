"""Skill: Descubrimiento del cliente.

Entrada: dict libre (YAML/JSON de la oportunidad).
Decisión: normaliza a una `Opportunity` estructurada e infiere banderas de
alcance a partir de sedes/cargas/inventario.
Entrega: ficha de oportunidad con objetivos, sedes, cargas, inventario,
restricciones, presupuesto y datos pendientes.
"""

from __future__ import annotations

from ..schemas import Opportunity, Site


def _build_sites(raw: dict) -> list[Site]:
    """Sedes explícitas si existen; si no, se construyen desde los conteos
    (n_sites campus + n_datacenters) que entrega el formulario web."""
    explicit = raw.get("sites")
    if explicit:
        return [Site(**s) if isinstance(s, dict) else Site(name=str(s)) for s in explicit]

    sites: list[Site] = []
    n_sites = int(raw.get("n_sites") or 0)
    n_dc = int(raw.get("n_datacenters") or 0)
    for i in range(1, n_sites + 1):
        sites.append(Site(name=f"Sede {i}", kind="campus"))
    for i in range(1, n_dc + 1):
        sites.append(Site(name=f"Datacenter {i}", kind="datacenter"))
    return sites


def build_opportunity(raw: dict) -> Opportunity:
    sites = _build_sites(raw)

    has_plants = any(s.kind == "planta" for s in sites)
    has_datacenter = any(s.kind == "datacenter" for s in sites)
    remote_users = raw.get("remote_users")
    remote_users = int(remote_users) if remote_users else None
    cloud_providers = raw.get("cloud_providers", [])
    # Texto libre para inferir alcance: cargas + situación + problema + inventario
    # + productos actuales + objetivos + industria (soporta el formulario web).
    signal = " ".join(
        raw.get("workloads", [])
        + raw.get("objectives", [])
        + raw.get("inventory", [])
        + raw.get("current_products", [])
        + cloud_providers
        + [str(raw.get(k, "")) for k in ("situation", "problem", "industry")]
    ).lower()

    opp = Opportunity(
        customer=raw.get("customer", "Cliente sin nombre"),
        industry=raw.get("industry"),
        situation=raw.get("situation"),
        problem=raw.get("problem"),
        objectives=raw.get("objectives", []),
        sites=sites,
        workloads=raw.get("workloads", []),
        inventory=raw.get("inventory", []),
        current_products=raw.get("current_products", []),
        remote_users=remote_users,
        cloud_providers=cloud_providers,
        constraints=raw.get("constraints", []),
        budget=raw.get("budget"),
        horizon_years=raw.get("horizon_years", 3),
        pending_data=raw.get("pending_data", []),
        it_ot_present=raw.get(
            "it_ot_present",
            has_plants
            or any(k in signal for k in ("ot", "industrial", "planta", "scada", "manufactur")),
        ),
        needs_correlation_soc=raw.get(
            "needs_correlation_soc",
            any(
                k in signal
                for k in ("soc", "siem", "correlaci", "splunk", "observab", "thousandeyes")
            ),
        ),
        needs_datacenter_ai=raw.get(
            "needs_datacenter_ai",
            has_datacenter
            or any(
                k in signal
                for k in (
                    "gpu", " ia ", " ai", "datacenter", "data center",
                    "cómputo", "computo", "nexus", "ucs",
                )
            ),
        ),
        needs_collaboration=raw.get(
            "needs_collaboration",
            bool(remote_users)
            or any(
                k in signal
                for k in (
                    "colabora", "webex", "telefon", "voz", "video",
                    "reunion", "reunión", "contact center", "uc ", "pbx",
                )
            ),
        ),
    )
    return opp

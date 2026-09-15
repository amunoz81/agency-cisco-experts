"""Especialista en Secure Networking."""

from __future__ import annotations

from datetime import date

from ..schemas import (
    Architecture,
    Bom,
    BomLine,
    Evidence,
    EvidenceStatus,
    Opportunity,
    ScopeClassification,
    SpecialistFinding,
)
from .base import SpecialistAgent


class SecureNetworkingSpecialist(SpecialistAgent):
    architecture = Architecture.SECURE_NETWORKING
    prompt_file = "secure_networking.md"

    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        n_sites = max(len(opportunity.sites), 1)
        return SpecialistFinding(
            architecture=self.architecture,
            scope=ScopeClassification.NECESSARY,
            customer_need=(
                "Conectividad segura y consistente entre sedes, con acceso e "
                "identidad unificados y segmentación por rol/dispositivo."
            ),
            proposed_solution=(
                "Acceso: Catalyst 9000 + Meraki para campus/sucursal gestionados "
                "desde el dashboard. Identidad: Cisco ISE + DUO (MFA) e integración "
                "con Access Manager. Conectividad segura a nube y SaaS con Cisco "
                "Secure Access (SSE). Segmentación macro/micro con SGT/TrustSec. "
                "Operación asistida con AgenticOps/Cloud Control."
            ),
            dependencies=[
                "ISE como fuente de política de identidad para Security e IT/OT",
                "Secure Firewall para el perímetro y enforcement de segmentación",
            ],
            sizing=(
                f"{n_sites} sede(s). Dimensionar switches por número de puertos y PoE, "
                "APs por área/densidad, y ISE por endpoints concurrentes."
            ),
            licenses=[
                "Cisco DNA/Catalyst Advantage por switch",
                "Meraki Enterprise/Advanced por AP y appliance",
                "ISE Essentials/Advantage por endpoint",
                "DUO Essentials/Advantage por usuario",
                "Secure Access (SSE) por usuario",
            ],
            measurable_benefit=(
                "Reducción de tiempo de aprovisionamiento de sedes y de incidentes "
                "de acceso; base de Zero Trust en la red. (Supuesto: línea base de "
                "MTTR y volumen de tickets a confirmar con el cliente.)"
            ),
            evidence=[
                Evidence(
                    claim="Diseño de acceso e identidad basado en CVD de campus.",
                    source="Cisco Validated Design - Campus LAN & Wireless",
                    source_date=date(2025, 6, 1),
                    version="CVD 2025",
                    status=EvidenceStatus.CONDITIONED,
                )
            ],
            risks_pending=[
                "Inventario y versiones de equipos existentes por confirmar",
                "Modalidad de gestión (cloud vs on-prem) a acordar con el cliente",
            ],
            bom_contribution=Bom(
                lines=[
                    BomLine(
                        sku="C9300-48P",
                        description="Catalyst 9300 48p PoE+ (acceso campus)",
                        quantity=n_sites * 2,
                        architecture=self.architecture,
                        management="Catalyst Center / Meraki",
                        sizing_basis="2 switches de acceso por sede (ejemplo)",
                    ),
                    BomLine(
                        sku="ISE-VM-L",
                        description="Cisco ISE (nodo virtual)",
                        quantity=2,
                        architecture=self.architecture,
                        is_license=False,
                        management="on-prem",
                        sizing_basis="Par en HA para política de identidad",
                    ),
                    BomLine(
                        sku="DUO-ADV",
                        description="Cisco DUO Advantage (MFA por usuario)",
                        quantity=sum(s.users or 0 for s in opportunity.sites) or 100,
                        architecture=self.architecture,
                        is_license=True,
                        management="cloud",
                        sizing_basis="Por usuario",
                    ),
                ]
            ),
        )

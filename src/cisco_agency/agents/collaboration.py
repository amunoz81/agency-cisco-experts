"""Especialista en Collaboration (Webex y comunicaciones)."""

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


class CollaborationSpecialist(SpecialistAgent):
    architecture = Architecture.COLLABORATION
    prompt_file = "collaboration.md"

    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        total_users = (sum(s.users or 0 for s in opportunity.sites) or 100) + (
            opportunity.remote_users or 0
        )
        # Salas de reunión estimadas: ~1 por cada 40 usuarios (ejemplo).
        rooms = max(total_users // 40, len(opportunity.sites))
        scope = (
            ScopeClassification.NECESSARY
            if opportunity.needs_collaboration
            else ScopeClassification.OPTIONAL
        )
        return SpecialistFinding(
            architecture=self.architecture,
            scope=scope,
            customer_need=(
                "Comunicaciones unificadas seguras (voz, video, mensajería y "
                "reuniones) y experiencia consistente de colaboración híbrida entre "
                "sedes, con opción de contacto con clientes."
            ),
            proposed_solution=(
                "Webex Suite (Meetings, Messaging, Calling) gestionado desde Control "
                "Hub. Telefonía en la nube con Webex Calling (o Unified CM Cloud/"
                "on-prem según el caso) y conectividad PSTN vía CUBE/Cloud Connected "
                "PSTN. Salas con dispositivos Webex (Room/Desk + Room Navigator). "
                "Webex Contact Center si hay atención a clientes. Seguridad con SSO/"
                "DUO y monitoreo de experiencia con Control Hub + ThousandEyes."
            ),
            dependencies=[
                "QoS y conectividad segura desde Secure Networking (marcado DSCP, SD-WAN)",
                "Identidad/SSO (ISE/DUO) para acceso seguro a Webex",
                "ThousandEyes/Control Hub para experiencia; Splunk si hay correlación",
            ],
            sizing=(
                f"{total_users} usuario(s) y ~{rooms} sala(s) de reunión. Dimensionar "
                "licencias por usuario, dispositivos por sala y sesiones PSTN "
                "concurrentes; Contact Center por número de agentes."
            ),
            licenses=[
                "Webex Suite (por usuario)",
                "Webex Calling (por usuario/estación)",
                "Webex Contact Center (por agente, si aplica)",
                "Control Hub (gestión, incluido)",
                "Cloud Connected PSTN / CUBE (por sesión)",
            ],
            measurable_benefit=(
                "Consolidación de plataformas de comunicación, reducción de costos de "
                "telefonía y mejor experiencia híbrida. (Supuesto: costo actual de "
                "PBX/telefonía y número de reuniones a validar.)"
            ),
            evidence=[
                Evidence(
                    claim="Diseño de UC y salas basado en guías de Webex/Control Hub.",
                    source="Cisco Webex / Collaboration Design Guides",
                    source_date=date(2025, 4, 1),
                    version="2025",
                    status=EvidenceStatus.CONDITIONED,
                )
            ],
            risks_pending=[
                "Modalidad de telefonía (Calling cloud vs Unified CM) por definir",
                "Proveedor y sesiones PSTN concurrentes por confirmar",
                "Inventario de salas y dispositivos existentes por levantar",
            ],
            bom_contribution=Bom(
                lines=[
                    BomLine(
                        sku="WEBEX-SUITE",
                        description="Webex Suite (Meetings/Messaging/Calling) por usuario",
                        quantity=total_users,
                        architecture=self.architecture,
                        is_license=True,
                        management="Control Hub",
                        sizing_basis="Por usuario",
                    ),
                    BomLine(
                        sku="WEBEX-ROOM-BAR",
                        description="Cisco Room Bar + Room Navigator (sala de reunión)",
                        quantity=rooms,
                        architecture=self.architecture,
                        management="Control Hub",
                        sizing_basis="1 dispositivo por sala (ejemplo: 1 sala/40 usuarios)",
                    ),
                    BomLine(
                        sku="CCP-PSTN",
                        description="Cloud Connected PSTN (sesiones concurrentes)",
                        quantity=max(total_users // 10, 1),
                        unit="sesión",
                        architecture=self.architecture,
                        is_license=True,
                        management="Control Hub",
                        sizing_basis="~10% de usuarios concurrentes (estimado)",
                    ),
                ]
            ),
        )

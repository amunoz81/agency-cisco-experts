"""Especialista IT/OT (seguridad y visibilidad industrial)."""

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


class ItOtSpecialist(SpecialistAgent):
    architecture = Architecture.IT_OT
    prompt_file = "it_ot.md"

    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        plants = [s for s in opportunity.sites if s.kind == "planta"]
        scope = (
            ScopeClassification.NECESSARY
            if (opportunity.it_ot_present or plants)
            else ScopeClassification.OPTIONAL
        )
        return SpecialistFinding(
            architecture=self.architecture,
            scope=scope,
            customer_need=(
                "Visibilidad de activos industriales y definición de comunicaciones "
                "permitidas por zona sin afectar la producción."
            ),
            proposed_solution=(
                "Modelo de zonas y conductos según IEC 62443/Purdue. Visibilidad con "
                "Cisco Cyber Vision usando sensores embebidos en switches industriales "
                "(Catalyst IE3x00) y sensores dedicados donde no haya. Enforcement de "
                "comunicaciones con ISE/TrustSec y Secure Firewall en la frontera IT/OT."
            ),
            dependencies=[
                "ISE/TrustSec para políticas de segmentación",
                "Secure Firewall en la zona de conducción (IDMZ)",
                "Exportación de eventos a Splunk/SOC si hay correlación",
            ],
            sizing=(
                f"{len(plants) or 1} planta(s). Ubicar sensores por celda/VLAN "
                "industrial; dimensionar por número de activos y ancho de banda de "
                "captura."
            ),
            licenses=[
                "Cyber Vision Sensor (embebido/dedicado) por punto de captura",
                "Cyber Vision Center (on-prem/cloud)",
            ],
            measurable_benefit=(
                "Inventario OT automático y detección de comunicaciones anómalas sin "
                "downtime. (Supuesto: acceso a SPAN/mirroring en switches OT.)"
            ),
            evidence=[
                Evidence(
                    claim="Diseño de zonas y conductos según estándar industrial.",
                    source="IEC 62443 / Cisco Cyber Vision Design Guide",
                    source_date=date(2025, 3, 1),
                    version="Cyber Vision 5.x",
                    status=EvidenceStatus.CONDITIONED,
                )
            ],
            risks_pending=[
                "Capacidad de los switches OT para sensor embebido a confirmar",
                "Ventanas de mantenimiento para despliegue sin afectar producción",
            ],
            bom_contribution=Bom(
                lines=[
                    BomLine(
                        sku="IE-3400",
                        description="Catalyst IE3400 con sensor Cyber Vision embebido",
                        quantity=(len(plants) or 1) * 4,
                        architecture=self.architecture,
                        management="Cyber Vision Center",
                        sizing_basis="4 celdas por planta (ejemplo)",
                    ),
                    BomLine(
                        sku="CV-CENTER",
                        description="Cyber Vision Center (appliance/VM)",
                        quantity=1,
                        architecture=self.architecture,
                        is_license=True,
                        management="on-prem",
                        sizing_basis="Central de visibilidad OT",
                    ),
                ]
            ),
        )

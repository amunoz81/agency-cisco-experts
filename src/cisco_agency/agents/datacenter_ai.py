"""Especialista en Data Center y Cloud / AI Fabric."""

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


class DatacenterAISpecialist(SpecialistAgent):
    architecture = Architecture.DATACENTER_AI
    prompt_file = "datacenter_ai.md"

    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        scope = (
            ScopeClassification.NECESSARY
            if opportunity.needs_datacenter_ai
            else ScopeClassification.OPTIONAL
        )
        return SpecialistFinding(
            architecture=self.architecture,
            scope=scope,
            customer_need=(
                "Infraestructura de cómputo, almacenamiento y red de datacenter para "
                "cargas locales, incluyendo plataformas de IA con aceleración GPU."
            ),
            proposed_solution=(
                "Cómputo con UCS (serie X/C) y fabric Nexus 9000 (ACI o NX-OS). Para "
                "IA, Cisco AI PODs (diseño validado con GPU) y AI Fabric de baja "
                "latencia. Gestión con Intersight. Protección con Hypershield/Secure "
                "Workload en el datacenter."
            ),
            dependencies=[
                "Segmentación y política desde Security (Secure Workload/Hypershield)",
                "Conectividad y QoS desde Secure Networking",
            ],
            sizing=(
                "GPU por tipo de carga (entrenamiento vs inferencia); nodos UCS por "
                "vCPU/RAM; fabric por puertos 100/400G y oversubscription."
            ),
            licenses=[
                "Intersight (Essentials/Advantage) por nodo",
                "Nexus Dashboard / ACI por switch",
            ],
            measurable_benefit=(
                "Plataforma local para IA con rendimiento y seguridad integrados. "
                "(Supuesto: perfil de cargas de IA a caracterizar con el cliente.)"
            ),
            evidence=[
                Evidence(
                    claim="Diseño AI POD y fabric de datacenter validados.",
                    source="Cisco AI PODs / Data Center Networking Design Guides",
                    source_date=date(2025, 7, 1),
                    version="2025",
                    status=EvidenceStatus.CONDITIONED,
                )
            ],
            risks_pending=[
                "Disponibilidad y tipo de GPU requerida por confirmar",
                "Energía y refrigeración del datacenter a validar",
            ],
            bom_contribution=Bom(
                lines=[
                    BomLine(
                        sku="UCS-X210C",
                        description="UCS X210c (nodo de cómputo)",
                        quantity=4,
                        architecture=self.architecture,
                        management="Intersight",
                        sizing_basis="Bloque inicial de cómputo (ejemplo)",
                    ),
                    BomLine(
                        sku="N9K-C93600",
                        description="Nexus 9300 (fabric 100/400G)",
                        quantity=2,
                        architecture=self.architecture,
                        management="Nexus Dashboard",
                        sizing_basis="Par leaf/spine (ejemplo)",
                    ),
                    BomLine(
                        sku="AI-POD",
                        description="Cisco AI POD (referencia con GPU)",
                        quantity=1,
                        architecture=self.architecture,
                        management="Intersight",
                        sizing_basis="1 POD de referencia para IA",
                    ),
                ]
            ),
        )

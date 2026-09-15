"""Especialista en Observabilidad y SOC (Splunk, ThousandEyes)."""

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


class ObservabilitySocSpecialist(SpecialistAgent):
    architecture = Architecture.OBSERVABILITY_SOC
    prompt_file = "observability_soc.md"

    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        scope = (
            ScopeClassification.NECESSARY
            if opportunity.needs_correlation_soc
            else ScopeClassification.OPTIONAL
        )
        return SpecialistFinding(
            architecture=self.architecture,
            scope=scope,
            customer_need=(
                "Correlación de eventos entre dominios (red, seguridad, OT), "
                "experiencia digital y respuesta a incidentes centralizada."
            ),
            proposed_solution=(
                "Splunk Enterprise Security como SIEM/analítica y Splunk SOAR para "
                "automatización de respuesta. ThousandEyes para experiencia digital y "
                "monitoreo de rutas a SaaS/nube. Integración de telemetría de Secure "
                "Firewall, Secure Network Analytics, ISE y Cyber Vision."
            ),
            dependencies=[
                "Fuentes de log de Security, Secure Networking e IT/OT",
                "Definición de casos de uso y playbooks con el cliente",
            ],
            sizing=(
                "Splunk por GB/día de ingesta y por número de agentes ThousandEyes "
                "(cloud/enterprise/endpoint)."
            ),
            licenses=[
                "Splunk Enterprise Security (por ingesta o workload)",
                "Splunk SOAR",
                "ThousandEyes por unidades de agente",
            ],
            measurable_benefit=(
                "Menor MTTD/MTTR por correlación cross-domain y visibilidad de "
                "experiencia. (Supuesto: volumen de ingesta GB/día a estimar.)"
            ),
            evidence=[
                Evidence(
                    claim="Arquitectura SIEM/SOAR y de experiencia digital.",
                    source="Splunk Validated Architectures / ThousandEyes docs",
                    source_date=date(2025, 5, 1),
                    version="2025",
                    status=EvidenceStatus.CONDITIONED,
                )
            ],
            risks_pending=[
                "Volumen real de ingesta (GB/día) por medir",
                "Retención y cumplimiento normativo a definir",
            ],
            bom_contribution=Bom(
                lines=[
                    BomLine(
                        sku="SPLUNK-ES",
                        description="Splunk Enterprise Security (ingesta)",
                        quantity=50,
                        unit="GB/día",
                        architecture=self.architecture,
                        is_license=True,
                        management="cloud/on-prem",
                        sizing_basis="Estimado inicial de ingesta",
                    ),
                    BomLine(
                        sku="TE-ENT",
                        description="ThousandEyes Enterprise Agents",
                        quantity=10,
                        architecture=self.architecture,
                        is_license=True,
                        management="cloud",
                        sizing_basis="Puntos de monitoreo clave",
                    ),
                ]
            ),
        )

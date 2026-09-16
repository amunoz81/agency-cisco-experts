"""Especialista en Security (ciberseguridad de extremo a extremo)."""

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


class SecuritySpecialist(SpecialistAgent):
    architecture = Architecture.SECURITY
    prompt_file = "security.md"

    def _offline_finding(self, opportunity: Opportunity) -> SpecialistFinding:
        remote = opportunity.remote_users or 0
        endpoints = (sum(s.users or 0 for s in opportunity.sites) or 100) + remote
        clouds = ", ".join(opportunity.cloud_providers) if opportunity.cloud_providers else None
        return SpecialistFinding(
            architecture=self.architecture,
            scope=ScopeClassification.NECESSARY,
            customer_need=(
                "Protección de extremo a extremo alineada a NIST CSF y CISA Zero "
                "Trust: identidad segura, seguridad de nube, micro-segmentación de "
                "aplicaciones y detección/respuesta en red y endpoint."
            ),
            proposed_solution=(
                "Zero Trust con identidad (ISE/DUO) como pilar. Micro-segmentación "
                "de aplicaciones con Secure Workload; segmentación a nivel de kernel "
                "con Isovalent (eBPF/Cilium). Protección de datacenter/AI con "
                "Hypershield. Perímetro con Secure Firewall. NDR con Secure Network "
                "Analytics (Stealthwatch) y EDR con Cisco Secure Client (Secure "
                "Endpoint). Cloud security con Secure Access/Umbrella."
            ),
            dependencies=[
                "Telemetría de red desde Secure Networking (NetFlow/SGT)",
                "ISE como política de identidad compartida",
                "Correlación en Splunk si se activa Observability/SOC",
            ],
            sizing=(
                "Secure Workload por número de workloads/agentes; NDR por FPS/flujos; "
                "EDR por endpoints; firewalls por throughput e inspección TLS."
                + (
                    f" Micro-segmentación multi-nube (agentless) sobre: {clouds}."
                    if clouds
                    else ""
                )
            ),
            licenses=[
                "Secure Firewall Threat Defense (IPS/URL/Malware)",
                "Secure Workload (SaaS o on-prem) por workload",
                "Secure Network Analytics por flujos",
                "Secure Endpoint (Cisco Secure Client) por endpoint",
                "Isovalent Enterprise por nodo/clúster",
            ],
            measurable_benefit=(
                "Reducción de superficie de ataque por micro-segmentación y menor "
                "tiempo de detección/contención. (Supuesto: métricas base de MTTD/MTTR "
                "a validar.)"
            ),
            evidence=[
                Evidence(
                    claim="Marco Zero Trust alineado a NIST SP 800-207 y CISA ZTMM.",
                    source="NIST SP 800-207 / CISA Zero Trust Maturity Model v2.0",
                    source_date=date(2023, 4, 1),
                    version="ZTMM v2.0",
                    status=EvidenceStatus.VERIFIED,
                )
            ],
            risks_pending=[
                "Compatibilidad de Isovalent con las distros/versiones de Kubernetes del cliente",
                "Alcance de inspección TLS y su impacto en throughput por confirmar",
            ],
            bom_contribution=Bom(
                lines=[
                    BomLine(
                        sku="FPR-3120",
                        description="Secure Firewall 3120 (perímetro/DC)",
                        quantity=2,
                        architecture=self.architecture,
                        management="Firewall Management Center / Cloud",
                        sizing_basis="Par en HA (ejemplo)",
                    ),
                    BomLine(
                        sku="SW-WORKLOAD",
                        description="Cisco Secure Workload (micro-segmentación)",
                        quantity=200,
                        architecture=self.architecture,
                        is_license=True,
                        management="SaaS",
                        sizing_basis="Por workload (estimado)",
                    ),
                    BomLine(
                        sku="SEC-ENDPOINT",
                        description="Cisco Secure Client / Secure Endpoint",
                        quantity=endpoints,
                        architecture=self.architecture,
                        is_license=True,
                        management="cloud",
                        sizing_basis=f"Por endpoint (incl. {remote} remotos)",
                    ),
                ]
            ),
        )

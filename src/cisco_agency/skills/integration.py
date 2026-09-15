"""Skill: Integración entre arquitecturas.

Describe flujos de datos, puntos de aplicación de políticas, dependencias y
responsabilidades operativas que conectan las recomendaciones de los
especialistas en un diseño único.
"""

from __future__ import annotations

from ..schemas import SpecialistFinding


def integrate_architectures(findings: list[SpecialistFinding]) -> dict:
    present = {f.architecture.value for f in findings}

    flows: list[str] = []
    policy_points: list[str] = []
    dependencies: list[str] = []

    if "secure_networking" in present and "security" in present:
        policy_points.append(
            "ISE/TrustSec como punto único de política de identidad y segmentación, "
            "aplicada por Catalyst/Meraki y Secure Firewall."
        )
    if "security" in present and "observability_soc" in present:
        flows.append(
            "Telemetría de Secure Firewall, Secure Network Analytics e ISE hacia "
            "Splunk ES/SOAR para correlación y respuesta."
        )
    if "it_ot" in present:
        flows.append(
            "Eventos de Cyber Vision hacia el SOC; enforcement OT en la IDMZ con "
            "Secure Firewall e ISE."
        )
    if "datacenter_ai" in present and "security" in present:
        policy_points.append(
            "Micro-segmentación del datacenter con Secure Workload/Hypershield "
            "coherente con la política de identidad."
        )

    # Consolidar dependencias declaradas por los especialistas
    for f in findings:
        dependencies.extend(f.dependencies)

    return {
        "architectures": sorted(present),
        "data_flows": flows,
        "policy_enforcement_points": policy_points,
        "dependencies": sorted(set(dependencies)),
        "operational_responsibilities": [
            "NetOps: Secure Networking (Catalyst/Meraki, ISE)",
            "SecOps: Security (Firewall, Workload, NDR/EDR) y SOC (Splunk)",
            "OT/Planta: IT/OT (Cyber Vision) con SecOps",
            "DC/Cloud: Data Center y AI (UCS/Nexus/Intersight)",
        ],
    }

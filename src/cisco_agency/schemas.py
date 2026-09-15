"""Esquemas de datos compartidos (Pydantic v2).

Define el "formato común" que todo especialista debe devolver para que el
coordinador pueda comparar y reconciliar recomendaciones, y las estructuras
de oportunidad, BOM y caso financiero.
"""

from __future__ import annotations

from datetime import date
from enum import Enum

from pydantic import BaseModel, Field


# --------------------------------------------------------------------------
# Arquitecturas del portafolio y clasificación de alcance
# --------------------------------------------------------------------------
class Architecture(str, Enum):
    SECURE_NETWORKING = "secure_networking"
    SECURITY = "security"
    IT_OT = "it_ot"
    OBSERVABILITY_SOC = "observability_soc"
    DATACENTER_AI = "datacenter_ai"
    COLLABORATION = "collaboration"


class ScopeClassification(str, Enum):
    """Cada arquitectura se clasifica según las cuatro preguntas de valor."""

    NECESSARY = "necesaria"
    OPTIONAL = "opcional_justificada"
    OUT_OF_SCOPE = "fuera_de_alcance"


class EvidenceStatus(str, Enum):
    VERIFIED = "verificada"
    CONDITIONED = "condicionada"
    PENDING = "pendiente"


# --------------------------------------------------------------------------
# Evidencia: toda conclusión relevante lleva fuente, fecha, versión y estado
# --------------------------------------------------------------------------
class Evidence(BaseModel):
    claim: str = Field(description="Conclusión o afirmación que se sustenta.")
    source: str = Field(description="Documento/URL/cotización que la respalda.")
    source_date: date | None = Field(
        default=None, description="Fecha del documento fuente."
    )
    version: str | None = Field(
        default=None, description="Versión de SW/HW/guía referida, si aplica."
    )
    status: EvidenceStatus = EvidenceStatus.PENDING


# --------------------------------------------------------------------------
# BOM y licenciamiento
# --------------------------------------------------------------------------
class BomLine(BaseModel):
    sku: str | None = Field(default=None, description="SKU / part number Cisco.")
    description: str
    quantity: float = 1
    unit: str = "unidad"
    architecture: Architecture
    is_license: bool = False
    management: str | None = Field(
        default=None, description="Modalidad de gestión (Dashboard, on-prem, cloud)."
    )
    sizing_basis: str | None = Field(
        default=None, description="Criterio de dimensionamiento usado."
    )
    notes: str | None = None


class Bom(BaseModel):
    lines: list[BomLine] = Field(default_factory=list)

    def deduplicated(self) -> Bom:
        """Consolida líneas duplicadas (mismo SKU+descripción) sumando cantidades."""
        merged: dict[tuple, BomLine] = {}
        for line in self.lines:
            key = (line.sku, line.description, line.architecture, line.is_license)
            if key in merged:
                merged[key].quantity += line.quantity
            else:
                merged[key] = line.model_copy(deep=True)
        return Bom(lines=list(merged.values()))


# --------------------------------------------------------------------------
# Formato común de entrega de cada especialista
# --------------------------------------------------------------------------
class SpecialistFinding(BaseModel):
    """Necesidad → solución → dependencias → dimensionamiento → licencias →
    beneficio medible → evidencia → riesgos y pendientes."""

    architecture: Architecture
    scope: ScopeClassification = ScopeClassification.NECESSARY

    customer_need: str = Field(description="Necesidad concreta del cliente que resuelve.")
    proposed_solution: str = Field(description="Solución propuesta (productos/diseño).")
    dependencies: list[str] = Field(
        default_factory=list, description="Dependencias con otras arquitecturas/sistemas."
    )
    sizing: str = Field(default="", description="Dimensionamiento y su criterio.")
    licenses: list[str] = Field(
        default_factory=list, description="Licencias/suscripciones requeridas."
    )
    measurable_benefit: str = Field(
        default="", description="Beneficio medible (con supuestos identificados)."
    )
    evidence: list[Evidence] = Field(default_factory=list)
    risks_pending: list[str] = Field(
        default_factory=list, description="Riesgos y pendientes (información faltante)."
    )
    bom_contribution: Bom = Field(default_factory=Bom)


# --------------------------------------------------------------------------
# Oportunidad / ficha de descubrimiento
# --------------------------------------------------------------------------
class Site(BaseModel):
    name: str
    kind: str = Field(default="campus", description="campus | datacenter | planta | sucursal")
    users: int | None = None
    notes: str | None = None


class Opportunity(BaseModel):
    """Ficha de oportunidad producida por la skill de descubrimiento."""

    customer: str
    industry: str | None = None
    objectives: list[str] = Field(default_factory=list)
    sites: list[Site] = Field(default_factory=list)
    workloads: list[str] = Field(default_factory=list)
    inventory: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)
    budget: str | None = None
    horizon_years: int = 3
    pending_data: list[str] = Field(default_factory=list)
    it_ot_present: bool = False
    needs_correlation_soc: bool = False
    needs_datacenter_ai: bool = False
    needs_collaboration: bool = False


# --------------------------------------------------------------------------
# Caso financiero
# --------------------------------------------------------------------------
class FinancialScenario(BaseModel):
    name: str
    capex: float = 0.0
    annual_opex: float = 0.0
    annual_benefit: float = 0.0
    horizon_years: int = 3


class FinancialCase(BaseModel):
    currency: str = "USD"
    fiscal_year: str = "FY26"
    scenarios: list[FinancialScenario] = Field(default_factory=list)
    assumptions: list[str] = Field(default_factory=list)
    results: dict[str, dict[str, float]] = Field(default_factory=dict)


# --------------------------------------------------------------------------
# Revisión técnica independiente
# --------------------------------------------------------------------------
class ReviewIssue(BaseModel):
    severity: str = Field(default="info", description="info | warning | blocker")
    category: str = Field(
        description="compatibilidad | cantidades | licencias | financiero | coherencia"
    )
    detail: str


class ReviewResult(BaseModel):
    passed: bool = True
    issues: list[ReviewIssue] = Field(default_factory=list)

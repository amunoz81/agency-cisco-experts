# Agentes

Cada agente vive en `src/cisco_agency/agents/` y su prompt de sistema en
`src/cisco_agency/prompts/`.

## Coordinador (`coordinator.py`)

Conserva la responsabilidad del diseño completo. Aplica las **cuatro preguntas de
valor** para clasificar cada arquitectura como `necesaria`,
`opcional_justificada` o `fuera_de_alcance`:

1. ¿Qué necesidad concreta del cliente resuelve?
2. ¿Qué capacidad adicional aporta?
3. ¿Cómo se integra y quién la opera?
4. ¿Su beneficio justifica costo y complejidad?

Reglas base: Secure Networking y Security siempre necesarias; IT/OT si hay
plantas; Observabilidad/SOC si hay correlación; Data Center/AI si hay cargas que
lo requieran.

Además, `Coordinator.synthesize()` produce la **síntesis ejecutiva** (STAR,
resumen y contradicciones resueltas): determinista en offline, LLM en línea.

## Especialistas

Todos heredan de `SpecialistAgent` (`base.py`) y devuelven un `SpecialistFinding`.

| Especialista | Portafolio principal |
|--------------|----------------------|
| `SecureNetworkingSpecialist` | Meraki, Catalyst, ISE, DUO, Secure Access, Secure Firewall, AgenticOps |
| `SecuritySpecialist` | Secure Workload, Isovalent, Hypershield, Secure Firewall, Secure Network Analytics, Secure Client |
| `ItOtSpecialist` | Cyber Vision, Catalyst IE3x00, ISE/TrustSec, IDMZ |
| `ObservabilitySocSpecialist` | Splunk ES/SOAR, ThousandEyes |
| `DatacenterAISpecialist` | UCS, Nexus, Intersight, AI PODs |
| `CollaborationSpecialist` | Webex Suite/Calling, Contact Center, dispositivos Webex, Control Hub, PSTN/CUBE |

## Revisor técnico (`technical_reviewer.py`)

Comprobaciones deterministas y auditables:

- Duplicados y cantidades no válidas en el BOM.
- Licencias declaradas por cada especialista.
- Evidencia verificada vs condicionada/pendiente.
- Supuestos financieros y recuperación en el horizonte.
- Dependencias declaradas entre capas.

Clasifica hallazgos como `info`, `warning`, `blocker`. Una oferta con
`blocker` no se considera cerrada.

`TechnicalReviewer.critique()` añade el **crítico cualitativo** (capa LLM): puede
solicitar una revisión acotada (`MAX_REVISIONS`) devolviendo el diseño a las
arquitecturas objetivo. Las verificaciones deterministas nunca se reemplazan.

## Añadir un especialista nuevo

1. Crea `agents/mi_especialista.py` heredando de `SpecialistAgent`; define
   `architecture`, `prompt_file` y `_offline_finding()`.
2. Añade la arquitectura a `schemas.Architecture` si es nueva.
3. Crea `prompts/mi_especialista.md`.
4. Regístralo en `agents/__init__.py` (`SPECIALIST_REGISTRY`).
5. Ajusta `Coordinator.plan_scope()` para decidir cuándo convocarlo.
6. Añade una etiqueta en `reporting/pdf_builder.py::ARCH_LABELS`.
7. (Opcional) Añade su rol a `config/models.yaml` y a `routing.KNOWN_ROLES` para
   asignarle un modelo específico; si no, usa el `default` del YAML.

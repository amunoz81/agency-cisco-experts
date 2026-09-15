# Arquitectura

## Visión general

La agencia es un **sistema multiagente** orquestado con **LangGraph**. El estado
(`AgencyState`, ver `state.py`) fluye por un grafo de nodos. Cada nodo es una
función pura que recibe el estado y devuelve un delta.

```
raw_input
   │
   ▼
discovery ─► planning ─► scope_gate ─(HITL)─► specialists ─► integration ─► bom
   ─► finance ─► review ─► critic ─┬─(revisión acotada)─► specialists
                                   └─► synthesis ─► proposal
```

| Nodo | Skill / Agente | Entrada | Salida |
|------|----------------|---------|--------|
| `discovery` | `customer_discovery` | dict crudo | `Opportunity` |
| `planning` | `Coordinator` | `Opportunity` | `scope_plan`, `selected_specialists` |
| `scope_gate` | `Approver` (HITL) | `scope_plan` | alcance aprobado/editado |
| `specialists` | `SpecialistAgent`* | `Opportunity` + grounding | `findings[]` |
| `integration` | `integration` | `findings` | flujos, políticas, dependencias |
| `bom` | `bom_licensing` | `findings` | `Bom` consolidado |
| `finance` | `financial_case` | `Opportunity`, `Bom` | `FinancialCase` |
| `review` | `TechnicalReviewer.review` | `findings`, `Bom`, `FinancialCase` | `ReviewResult` |
| `critic` | `TechnicalReviewer.critique` | `findings`, `integration` | `CritiqueResult` + decisión de reflexión |
| `synthesis` | `Coordinator.synthesize` | `findings`, `integration` | `ExecutiveSynthesis` (STAR) |
| `proposal` | `executive_proposal` | todo | HTML + PDF |

## Capa LLM híbrida (coordinador + revisor)

El control de flujo y las verificaciones son deterministas; el **juicio** es LLM:

- **Coordinador (`synthesize`)**: mantiene el ruteo determinista de alcance y
  añade una síntesis LLM (narrativa STAR, resumen ejecutivo, contradicciones
  resueltas). En offline produce una síntesis determinista.
- **Revisor (`critique`)**: las verificaciones deterministas (`review`) son el
  guardrail y **no** se reemplazan; encima, un crítico LLM evalúa coherencia
  cualitativa y puede solicitar una **revisión acotada** (`MAX_REVISIONS`, por
  defecto 1) devolviendo el diseño a las arquitecturas objetivo. En offline el
  crítico no solicita revisión.

## Multi-proveedor de LLM

`llm.py` construye el `BaseChatModel` según el proveedor:

- `anthropic` → `langchain_anthropic.ChatAnthropic`
- `openai` → `langchain_openai.ChatOpenAI`
- `azure` → `langchain_openai.AzureChatOpenAI`

Los agentes usan `model.with_structured_output(SpecialistFinding)` para obtener
la salida ya validada por Pydantic.

## Enrutamiento de modelos por agente

Cada rol puede usar **su propio proveedor y modelo** para equilibrar calidad y
costo. Lo resuelve `ModelRouter` (`routing.py`) a partir de un YAML declarativo
(`config/models.yaml`), con este orden de precedencia:

```
rol específico  →  `default` del YAML  →  valores globales de .env
```

Ejemplo de estrategia costo-eficiente (la de por defecto):

| Rol | Modelo | Motivo |
|-----|--------|--------|
| coordinator | gpt-4o | Razonamiento de negocio y alcance |
| security | gpt-4o | Dominio crítico (Zero Trust) |
| technical_reviewer | gpt-4o | Revisión rigurosa |
| resto de especialistas | gpt-4o-mini | Volumen a bajo costo |

Se pueden **mezclar proveedores** por rol (p. ej. `security` en Anthropic y el
resto en OpenAI) siempre que existan las credenciales de cada proveedor en
`.env`. Un rol cuyo proveedor no tenga credenciales corre en **modo offline de
forma individual**; los demás siguen usando su LLM.

Inspección: `cisco-agency models` (o `python -m cisco_agency.run models`) imprime
la tabla rol → proveedor/modelo/modo. Cambia la ruta del YAML con `MODELS_CONFIG`.

## Modo offline

`Settings.effective_offline()` es `True` si `OFFLINE=true` **o** si faltan
credenciales para el proveedor elegido. En ese caso cada especialista devuelve un
`_offline_finding()` determinista. Esto permite:

- Correr la **demo** sin API keys (`make demo`).
- Ejecutar **CI** de forma reproducible.
- Depurar el pipeline sin costo de tokens.

## Generación de PDF

`reporting/pdf_builder.py` renderiza `templates/proposal.html.j2` con Jinja2 y
exporta a PDF con dos motores, en orden:

1. **WeasyPrint** (máxima fidelidad) — requiere libs de sistema:
   - macOS: `brew install pango gdk-pixbuf libffi`
   - Debian/Ubuntu: `apt-get install libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0`
   - Instala el extra: `pip install -e '.[pdf]'`
2. **xhtml2pdf** (pure-Python, sin libs de sistema) — viene en las dependencias
   base y es el fallback por defecto.

Si ninguno está disponible, se genera solo el HTML y se reporta el motivo.

## Grounding / evidencia (anti-alucinación)

Antes de responder, cada especialista se **fundamenta** en una base de
conocimiento (`knowledge/`): recupera documentos del corpus para su arquitectura
y la oportunidad, los inyecta en el prompt como contexto citable (modo LLM) y los
adjunta al hallazgo como `Evidence` con fuente/fecha/versión/estado.

- `KnowledgeBase` (`knowledge/base.py`): carga `knowledge/corpus/*.md` (frontmatter
  YAML + cuerpo) y hace recuperación por palabras clave, sin dependencias ni red.
- Corpus semilla: estándares reales verificados (NIST SP 800-207, CISA ZTMM,
  IEC 62443) y **plantillas** de producto (`TEMPLATE-*.md`) marcadas como
  `condicionada`, para que el equipo las reemplace con material oficial.
- Punto de extensión: sustituir el scorer por embeddings / vector store para RAG
  a escala, manteniendo la misma interfaz `search()` / `evidence_for()`.

Esto evita inventar afirmaciones: lo no respaldado queda como `pendiente` o
`condicionada`, y el revisor lo separa de lo `verificada`.

## Human-in-the-loop (aprobación de alcance)

Tras `planning` hay una compuerta `scope_gate` donde un humano aprueba o edita el
alcance **antes** de diseñar (lo costoso). Es conectable vía `approval.Approver`:

- `AutoApprover` — aprueba tal cual (desatendido / CI / pruebas; `--yes` en CLI).
- `CLIApprover` — pregunta por terminal y permite forzar incluir/excluir
  arquitecturas.

Si se rechaza, el grafo va directo a `END` sin generar propuesta. Para una UI
asíncrona, sustituye el approver por `langgraph.interrupt` manteniendo el mismo
contrato (`approve_scope`).

## Evaluación y observabilidad

- **Evals** (`evals.py` + `evals/cases/*.yaml`): corren el pipeline offline sobre
  un dataset dorado y verifican propiedades estructurales (alcance, BOM sin
  duplicados, cobertura de evidencia, revisión aprobada, propuesta generada).
  `cisco-agency eval` / `make eval`; también en `tests/test_evals.py` y CI.
- **Métricas de corrida** (`metrics.py`): cada `run` escribe un `run_report_*.json`
  (duración, arquitecturas, BOM, evidencia verificada/cobertura, revisiones) y
  muestra una tabla de métricas. Es observabilidad sin dependencias.
- **Trazas profundas**: exporta `LANGCHAIN_TRACING_V2=true` y `LANGSMITH_API_KEY`
  para enviar trazas por nodo, tokens y latencia a LangSmith (ver `.env.example`).

## Extender el grafo

Para ejecutar especialistas en **paralelo**, el reducer `operator.add` sobre
`findings` en `AgencyState` ya soporta fan-out: convierte cada especialista en su
propio nodo y usa aristas condicionales desde `planning`. La versión actual los
ejecuta en un solo nodo secuencial por simplicidad y determinismo.

## Persistencia / checkpoints

LangGraph permite añadir un `checkpointer` (p. ej. `MemorySaver` o SQLite) en
`build_graph` para reanudar ejecuciones o intervención humana (human-in-the-loop)
entre nodos. Es el punto natural para aprobar el alcance antes de diseñar.

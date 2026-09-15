# Arquitectura

## Visión general

La agencia es un **sistema multiagente** orquestado con **LangGraph**. El estado
(`AgencyState`, ver `state.py`) fluye por un grafo de nodos. Cada nodo es una
función pura que recibe el estado y devuelve un delta.

```
raw_input
   │
   ▼
discovery ─► planning ─► specialists ─► integration ─► bom ─► finance ─► review ─► proposal
```

| Nodo | Skill / Agente | Entrada | Salida |
|------|----------------|---------|--------|
| `discovery` | `customer_discovery` | dict crudo | `Opportunity` |
| `planning` | `Coordinator` | `Opportunity` | `scope_plan`, `selected_specialists` |
| `specialists` | `SpecialistAgent`* | `Opportunity` | `findings[]` |
| `integration` | `integration` | `findings` | flujos, políticas, dependencias |
| `bom` | `bom_licensing` | `findings` | `Bom` consolidado |
| `finance` | `financial_case` | `Opportunity`, `Bom` | `FinancialCase` |
| `review` | `TechnicalReviewer` | `findings`, `Bom`, `FinancialCase` | `ReviewResult` |
| `proposal` | `executive_proposal` | todo | HTML + PDF |

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

## Human-in-the-loop (aprobación de alcance)

Tras `planning` hay una compuerta `scope_gate` donde un humano aprueba o edita el
alcance **antes** de diseñar (lo costoso). Es conectable vía `approval.Approver`:

- `AutoApprover` — aprueba tal cual (desatendido / CI / pruebas; `--yes` en CLI).
- `CLIApprover` — pregunta por terminal y permite forzar incluir/excluir
  arquitecturas.

Si se rechaza, el grafo va directo a `END` sin generar propuesta. Para una UI
asíncrona, sustituye el approver por `langgraph.interrupt` manteniendo el mismo
contrato (`approve_scope`).

## Extender el grafo

Para ejecutar especialistas en **paralelo**, el reducer `operator.add` sobre
`findings` en `AgencyState` ya soporta fan-out: convierte cada especialista en su
propio nodo y usa aristas condicionales desde `planning`. La versión actual los
ejecuta en un solo nodo secuencial por simplicidad y determinismo.

## Persistencia / checkpoints

LangGraph permite añadir un `checkpointer` (p. ej. `MemorySaver` o SQLite) en
`build_graph` para reanudar ejecuciones o intervención humana (human-in-the-loop)
entre nodos. Es el punto natural para aprobar el alcance antes de diseñar.

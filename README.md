# Cisco Experts Agency 🛰️

Agencia **agéntica** de expertos Cisco que produce **propuestas técnicas y
comerciales** (HTML/PDF) para audiencias técnicas y ejecutivas C-Level, cubriendo
todo el portafolio: **Secure Networking, Security, Data Center & AI, Colaboración
y Observabilidad (Splunk)**.

Construida con **LangGraph + LangChain** (open source), multi-proveedor de LLM
(Anthropic · OpenAI · Azure OpenAI) y con un **modo offline** para correr demos
y CI sin credenciales.

> ⚠️ Este repositorio es **privado**. Contenido base para revisión humana antes
> de entregarse a un cliente. No incorpora precios reales ni logotipos de terceros:
> el año fiscal, los productos disponibles y las condiciones comerciales se
> consultan por oportunidad con información autorizada.

---

## ¿Qué hace?

A partir de una **ficha de oportunidad** (YAML/JSON), la agencia:

1. **Descubre** y normaliza la oportunidad del cliente.
2. El **coordinador** define el alcance y selecciona especialistas.
3. Cada **especialista** entrega su análisis en un **formato común**.
4. Se **integra** el diseño, se consolida el **BOM**, se calcula el **caso financiero**.
5. Un **revisor técnico independiente** valida coherencia, cantidades y licencias.
6. Se genera la **propuesta ejecutiva** (STAR, blueprint, casos de uso, hoja de
   ruta, métricas y anexos) en **HTML y PDF**.

## Arranque rápido

```bash
# 1. Instalar (crea .venv e instala dependencias)
make install

# 2. Ejecutar la DEMO en modo offline (sin API keys) sobre la oportunidad Fanalca
make demo

# 3. Ver el resultado
open output/propuesta_fanalca.pdf     # o el .html
```

Para usar un LLM real:

```bash
cp .env.example .env      # completa LLM_PROVIDER y la API key correspondiente
make run
```

### Un modelo distinto por agente

Cada rol puede usar su propio proveedor/modelo (calidad donde importa, costo en
el resto). Se configura en [`config/models.yaml`](config/models.yaml):

```bash
cisco-agency models       # muestra rol → proveedor/modelo/modo
```

Por defecto (económico + alta calidad, familia gpt-4.1): `coordinator`, `security`
y `technical_reviewer` usan **gpt-4.1**; el resto de especialistas **gpt-4.1-mini**.
Puedes mezclar proveedores por rol (OpenAI/Anthropic/Azure) si tienes sus
credenciales en `.env`. Un rol sin credenciales de su proveedor corre en offline
individual; los demás no se afectan.
Ver [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md#enrutamiento-de-modelos-por-agente).

### Aprendizaje de Cisco Validated Designs (CVDs)

Cada especialista se fundamenta en los **CVDs oficiales** de su arquitectura:

```bash
cisco-agency ingest-cvd     # genera el corpus desde knowledge/cvd_sources.yaml
```

El catálogo trae CVDs reales por arquitectura (Campus LAN/WLAN, SD-WAN, Zero
Trust, ACI, DC Blueprint for AI/ML, Industrial Automation, Collaboration PA…).
Amplíalo agregando entradas al YAML; para texto completo, descarga el PDF a
`knowledge/cvd_downloads/` e instala el extra `pip install -e '.[ingest]'`.

## Interfaz web (formulario → propuesta)

Un formulario moderno (EN/ES) captura el contexto del cliente, permite **subir la
base instalada** (Excel/PDF/CSV) y dispara a los agentes:

```bash
pip install -e '.[web]'
cisco-agency serve      # http://127.0.0.1:8000   (o: make web)
```

Para compartirla con el equipo, con **Docker**:

```bash
cp .env.example .env
docker compose up --build      # http://localhost:8000
```

Ver [docs/WEB.md](docs/WEB.md). El logotipo de Cisco (marca de terceros): coloca
el asset aprobado en `src/cisco_agency/web/static/logo.svg`.

## Roles de la agencia

| Rol | Responsabilidad |
|-----|-----------------|
| **Arquitecto coordinador** | Entiende el negocio, define alcance, selecciona especialistas, resuelve contradicciones y entrega una sola oferta. |
| **Secure Networking** | Conectividad segura, acceso e identidad, segmentación (Meraki, Catalyst, ISE, DUO, Secure Access, Secure Firewall, AgenticOps). |
| **Security** | Ciberseguridad end-to-end alineada a NIST/CISA: Zero Trust, Secure Workload, Isovalent, Hypershield, NDR/EDR. |
| **Especialista IT/OT** | Zonas industriales, comunicaciones permitidas, visibilidad con Cyber Vision, sin afectar producción. |
| **Observabilidad y SOC** | Splunk, ThousandEyes: correlación cross-domain, experiencia digital y respuesta. |
| **Data Center y AI** | Cómputo, red de DC, virtualización y AI Fabric (AI PODs con GPU). |
| **Collaboration** | Comunicaciones unificadas y colaboración híbrida (Webex Suite/Calling, Contact Center, dispositivos, Control Hub, PSTN). |
| **Revisor técnico independiente** | Compatibilidad, dimensionamiento, dependencias, licencias y coherencia. |

Ver [docs/AGENTS.md](docs/AGENTS.md).

## Skills

Descubrimiento del cliente · Diseño Secure Networking · Diseño de ciberseguridad ·
Verificación de portafolio y compatibilidad · Integración entre arquitecturas ·
BOM y licenciamiento · Caso financiero · Propuesta ejecutiva.

Ver [docs/SKILLS.md](docs/SKILLS.md).

## Formato común de los especialistas

Cada especialista devuelve un `SpecialistFinding`:

```
Necesidad → solución → dependencias → dimensionamiento → licencias →
beneficio medible → evidencia → riesgos y pendientes
```

Cada conclusión relevante lleva **fuente, fecha, versión y estado**
(`verificada` / `condicionada` / `pendiente`).

## Estructura del repositorio

```
src/cisco_agency/
├── config.py         # Ajustes (.env), selección de proveedor y modo offline
├── llm.py            # Fábrica multi-proveedor (Anthropic/OpenAI/Azure)
├── schemas.py        # Formato común, evidencia, BOM, oportunidad, finanzas
├── state.py          # Estado del grafo LangGraph
├── graph.py          # Pipeline: discovery→planning→specialists→…→proposal
├── run.py            # CLI (typer)
├── agents/           # Coordinador, especialistas, revisor técnico
├── skills/           # Descubrimiento, integración, BOM, caso financiero, verificación
├── prompts/          # Prompts de sistema (uno por agente)
├── finance/          # Cálculos reproducibles (NPV, ROI, payback, TCO)
├── reporting/        # Plantilla Jinja2 + generación HTML/PDF + paleta
└── knowledge/        # Base de evidencia (placeholder para docs oficiales)
```

## Arquitectura del flujo

```mermaid
flowchart LR
  A[Descubrimiento] --> B[Coordinador: alcance]
  B --> C[Especialistas]
  C --> D[Integración]
  D --> E[BOM y licencias]
  E --> F[Caso financiero]
  F --> G[Revisión técnica]
  G --> H[Propuesta HTML/PDF]
```

Ver [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md).

## Desarrollo

```bash
make test     # pruebas
make eval     # evaluaciones (dataset dorado, offline)
make lint     # ruff + mypy
make fmt      # formateo
```

Cada corrida escribe un `run_report_*.json` con métricas (duración, BOM, cobertura
de evidencia, revisiones). Para trazas por nodo/tokens/latencia, activa LangSmith
en `.env` (ver `.env.example`).

## Contribuir

Lee [docs/CONTRIBUTING.md](docs/CONTRIBUTING.md). Para añadir un especialista o una
skill nueva hay guías paso a paso.

## Aviso

Documento y diseños generados automáticamente como **base**. Requieren revisión de
un arquitecto humano y validación contra matrices de compatibilidad, notas de
versión y ciclo de vida oficiales antes de cotizar o entregar.

# Interfaz web

Formulario moderno (bilingüe EN/ES) para capturar la oportunidad del cliente,
subir la base instalada de Cisco (Excel/PDF/CSV) y disparar a los agentes para
generar la propuesta técnica y comercial.

## Ejecutar

```bash
pip install -e '.[web]'      # FastAPI, uvicorn, openpyxl, pypdf
cisco-agency serve           # http://127.0.0.1:8000   (o: make web)
```

En modo LLM (con `OPENAI_API_KEY` en `.env`) una propuesta tarda ~30s; en modo
offline (toggle en el formulario) es instantánea y sin costo.

## Qué captura el formulario

- **Nombre del cliente** (obligatorio)
- **Vertical de industria** (lista de verticales Cisco, localizada)
- **Situación del cliente**
- **Problema / necesidad** (obligatorio)
- **Productos Cisco actuales y vigentes** (uno por línea o coma-separados)
- **N.º de sedes / datacenters** y **usuarios remotos** (conteos rápidos)
- **Proveedores de nube existentes** (AWS/Azure/GCP/Oracle/IBM/privada)
- **Sedes detalladas (opcional)**: nombre, tipo (campus/planta/datacenter/sucursal)
  y usuarios por sede — tienen precedencia sobre los conteos y afinan el
  dimensionamiento por ubicación
- **Base instalada interna** (subida de `.xlsx`, `.csv` o `.pdf` — los agentes la
  leen como inventario; ver `web/parsing.py`)
- Toggle **offline** (sin costo de LLM)

El backend mapea el formulario a una `Opportunity`, infiere el alcance
(especialistas) a partir del texto libre y ejecuta el grafo. Devuelve métricas,
los especialistas convocados y la propuesta en **cuatro formatos** descargables:
**PDF**, **PowerPoint** (deck ejecutivo), **Word** (documento técnico) y **HTML**.

La exportación a Office la genera `reporting/office.py` (python-pptx / python-docx,
incluidos en el extra `web`/`office`). El PPTX es un deck ejecutivo (portada,
STAR, alcance, arquitecturas, integración, BOM, caso financiero, revisión); el
DOCX es el documento técnico completo (blueprint por arquitectura con el formato
común, tablas de BOM y financiero, evidencia y pendientes). Ambos usan la paleta
Cisco. También se generan al correr `cisco-agency run` (CLI).

## Despliegue con Docker (para compartir con el equipo)

```bash
cp .env.example .env         # opcional: OPENAI_API_KEY, LLM_PROVIDER, modelo…
docker compose up --build    # http://localhost:8000   (o: make docker-up)
```

- Sin `OPENAI_API_KEY` la web corre en **modo offline** (sin costo, plantillado).
- El puerto del host se cambia con `WEB_PORT` (`WEB_PORT=9000 docker compose up`).
- Las propuestas generadas se persisten en `./output` (volumen).
- La imagen usa `xhtml2pdf` (PDF pure-Python), por lo que **no requiere libs de
  sistema**. Para PDF de máxima fidelidad con WeasyPrint, añade al `Dockerfile`
  `apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libgdk-pixbuf2.0-0` y el
  extra `.[pdf]`.
- El contenedor arranca con `python -m cisco_agency.web`, que lee `HOST`/`PORT`
  del entorno.

Para un solo contenedor sin compose:

```bash
docker build -t cisco-experts-agency .
docker run -p 8000:8000 -e OPENAI_API_KEY=sk-... cisco-experts-agency
```

## Arquitectura

- `web/app.py` — FastAPI: `/` (form), `/api/config`, `/api/proposal`, `/files/*`.
- `web/verticals.py` — catálogo de verticales EN/ES.
- `web/parsing.py` — lectura de la base instalada (Excel/CSV/PDF).
- `web/static/` — `index.html`, `styles.css`, `app.js`, `i18n.js`, `logo.svg`.

## Branding (logo Cisco)

La paleta y la estructura usan la identidad ya definida (`reporting/assets/palette.py`).
El **logotipo de Cisco es una marca de un tercero y no se incluye en el repo**.
Coloca el logo aprobado por tu organización/partner en
`src/cisco_agency/web/static/logo.svg` (o `.png` y ajusta el `src` en `index.html`)
y reemplazará el placeholder automáticamente.

## Notas / límites de v1

- La ejecución es síncrona (con overlay de progreso). Para cargas altas, mover a
  una cola/-tarea en background y polling.
- Los archivos generados se guardan en `output/web/` y se sirven por `/files/`.

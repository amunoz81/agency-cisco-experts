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
los especialistas convocados y la propuesta (HTML embebido + descarga PDF/HTML).

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

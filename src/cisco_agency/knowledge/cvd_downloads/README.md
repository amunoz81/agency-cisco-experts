# CVDs descargados (enriquecimiento de texto completo)

cisco.com bloquea el scraping automático, así que el catálogo
(`../cvd_sources.yaml`) guarda título + URL + resumen. Para incorporar el
**texto completo** de un CVD:

1. Descarga el CVD oficial (PDF o HTML) desde su URL.
2. Guárdalo aquí con un nombre que coincida con el `slug` del título del CVD,
   por ejemplo `campus-lan-and-wlan-design-guide-cvd.pdf`, **o** referencia el
   archivo con `local_file:` en la entrada del catálogo.
3. Corre `cisco-agency ingest-cvd` (requiere el extra: `pip install -e '.[ingest]'`).

El texto extraído se añade al documento del corpus como "Extracto del documento".
Los archivos aquí NO se versionan (ver `.gitignore`).

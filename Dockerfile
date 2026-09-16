# Cisco Experts Agency — imagen de la interfaz web (formulario + agentes)
FROM python:3.12-slim

ENV PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    HOST=0.0.0.0 \
    PORT=8000

WORKDIR /app

# Dependencias del proyecto (el PDF usa xhtml2pdf pure-Python, sin libs de sistema).
COPY pyproject.toml README.md ./
COPY src ./src
COPY config ./config

RUN pip install --upgrade pip && pip install -e ".[web]"

# Directorio de salida de propuestas generadas.
RUN mkdir -p output/web

EXPOSE 8000

# Arranca el servidor leyendo HOST/PORT del entorno (ver web/__main__.py).
CMD ["python", "-m", "cisco_agency.web"]

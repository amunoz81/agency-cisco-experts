"""Arranque del servidor web usando el puerto asignado por el entorno.

Lee el puerto de la variable PORT (la inyecta el harness de preview / autoPort);
por defecto 8000. Así el servidor no fija un puerto y evita colisiones.
"""

from __future__ import annotations

import os

import uvicorn

from .app import app


def main() -> None:
    host = os.environ.get("HOST", "127.0.0.1")
    port = int(os.environ.get("PORT", "8000"))
    uvicorn.run(app, host=host, port=port)


if __name__ == "__main__":
    main()

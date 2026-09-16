"""Base de conocimiento con evidencia para grounding (anti-alucinación).

Carga un corpus de documentos con metadatos (fuente, fecha, versión, estado) y
ofrece recuperación ligera por palabras clave, sin dependencias pesadas ni red.
Cada documento se puede convertir en `Evidence` para citar en los hallazgos.
"""

from .base import KnowledgeBase, KnowledgeDoc  # noqa: F401
from .ingest import ensure_corpus, ingest  # noqa: F401

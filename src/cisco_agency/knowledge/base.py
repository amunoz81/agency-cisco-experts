"""Base de conocimiento y recuperación ligera (keyword scoring).

Diseño intencionalmente simple y sin dependencias externas para que funcione
offline y en CI. Es el punto de extensión natural para un RAG con embeddings
(OpenAI/local) o un vector store cuando el corpus crezca.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

import yaml

from ..schemas import Evidence, EvidenceStatus, Opportunity

CORPUS_DIR = Path(__file__).resolve().parent / "corpus"

_STOPWORDS = {
    "de", "la", "el", "los", "las", "y", "o", "en", "con", "para", "por", "del",
    "un", "una", "the", "of", "and", "to", "a", "su", "sus", "que",
}


def _tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-záéíóúñ0-9]+", text.lower()) if t not in _STOPWORDS]


@dataclass
class KnowledgeDoc:
    id: str
    title: str
    architecture: str | None
    source: str
    source_date: date | None
    version: str | None
    status: EvidenceStatus
    tags: list[str] = field(default_factory=list)
    text: str = ""

    def searchable(self) -> str:
        return " ".join([self.title, " ".join(self.tags), self.text])

    def to_evidence(self) -> Evidence:
        return Evidence(
            claim=self.title,
            source=self.source,
            source_date=self.source_date,
            version=self.version,
            status=self.status,
        )


def _parse_doc(path: Path) -> KnowledgeDoc | None:
    raw = path.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return None
    _, fm, *rest = raw.split("---", 2)
    meta = yaml.safe_load(fm) or {}
    body = rest[0].strip() if rest else ""

    src_date = meta.get("source_date")
    parsed_date: date | None = None
    if isinstance(src_date, date):
        parsed_date = src_date
    elif isinstance(src_date, str) and src_date:
        try:
            parsed_date = date.fromisoformat(src_date)
        except ValueError:
            parsed_date = None

    try:
        status = EvidenceStatus(meta.get("status", "pendiente"))
    except ValueError:
        status = EvidenceStatus.PENDING

    return KnowledgeDoc(
        id=meta.get("id", path.stem),
        title=meta.get("title", path.stem),
        architecture=meta.get("architecture"),
        source=meta.get("source", "fuente no especificada"),
        source_date=parsed_date,
        version=str(meta.get("version")) if meta.get("version") is not None else None,
        status=status,
        tags=list(meta.get("tags", [])),
        text=body,
    )


class KnowledgeBase:
    def __init__(self, corpus_dir: Path | str | None = None) -> None:
        self.corpus_dir = Path(corpus_dir) if corpus_dir else CORPUS_DIR
        self.docs: list[KnowledgeDoc] = self._load()

    def _load(self) -> list[KnowledgeDoc]:
        docs: list[KnowledgeDoc] = []
        if not self.corpus_dir.exists():
            return docs
        for path in sorted(self.corpus_dir.glob("*.md")):
            doc = _parse_doc(path)
            if doc:
                docs.append(doc)
        return docs

    def search(
        self,
        query: str,
        architecture: str | None = None,
        k: int = 3,
    ) -> list[KnowledgeDoc]:
        """Recupera hasta k documentos por solapamiento de palabras clave.

        Prioriza documentos de la arquitectura pedida (o generales) y ordena por
        puntaje de coincidencia.
        """
        q_tokens = set(_tokenize(query))
        scored: list[tuple[float, KnowledgeDoc]] = []
        for doc in self.docs:
            if architecture and doc.architecture not in (None, "general", architecture):
                continue
            d_tokens = set(_tokenize(doc.searchable()))
            overlap = len(q_tokens & d_tokens)
            if overlap == 0:
                continue
            # Bonus por coincidencia exacta de arquitectura.
            arch_bonus = 1.5 if doc.architecture == architecture else 0.0
            scored.append((overlap + arch_bonus, doc))
        scored.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored[:k]]

    def evidence_for(
        self,
        architecture: str,
        opportunity: Opportunity,
        k: int = 3,
    ) -> list[Evidence]:
        """Devuelve evidencia recuperada para un especialista/oportunidad."""
        query = " ".join(
            [architecture]
            + opportunity.objectives
            + opportunity.workloads
            + ([opportunity.industry] if opportunity.industry else [])
        )
        return [doc.to_evidence() for doc in self.search(query, architecture, k)]

# core/catalog.py
from __future__ import annotations

from core.entities.catalog_entry import CatalogEntry
from core.exceptions import CatalogEntryNotFoundError, CatalogUnavailableError
from core.interfaces.catalog_repository import CatalogRepository


class CatalogService:
    """
    Gerencia o catálogo de modelos disponíveis para download.
    Não conhece a fonte dos dados (DB, JSON, API remota).
    """

    def __init__(self, repository: CatalogRepository) -> None:
        self._repository = repository

    # ── consulta ───────────────────────────────────────────────────────────

    def get(self, entry_id: str) -> CatalogEntry:
        entry = self._repository.find_by_id(entry_id)
        if entry is None:
            raise CatalogEntryNotFoundError(entry_id)
        return entry

    def list_all(self) -> list[CatalogEntry]:
        try:
            return self._repository.find_all()
        except Exception as exc:
            raise CatalogUnavailableError(str(exc)) from exc

    def search(self, query: str) -> list[CatalogEntry]:
        if not query.strip():
            return self.list_all()
        try:
            return self._repository.search(query.strip())
        except Exception as exc:
            raise CatalogUnavailableError(str(exc)) from exc

    def list_by_tag(self, tag: str) -> list[CatalogEntry]:
        return [
            entry for entry in self.list_all()
            if tag.lower() in [t.lower() for t in entry.tags]
        ]

    # ── gerenciamento ──────────────────────────────────────────────────────

    def add(self, entry: CatalogEntry) -> None:
        self._repository.save(entry)

    def remove(self, entry_id: str) -> None:
        self.get(entry_id)  # garante que existe antes de deletar
        self._repository.delete(entry_id)
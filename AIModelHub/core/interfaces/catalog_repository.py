# core/interfaces/catalog_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from core.entities.catalog_entry import CatalogEntry


class CatalogRepository(ABC):

    @abstractmethod
    def save(self, entry: CatalogEntry) -> None: ...

    @abstractmethod
    def find_by_id(self, entry_id: str) -> Optional[CatalogEntry]: ...

    @abstractmethod
    def find_all(self) -> list[CatalogEntry]: ...

    @abstractmethod
    def search(self, query: str) -> list[CatalogEntry]: ...

    @abstractmethod
    def delete(self, entry_id: str) -> None: ...
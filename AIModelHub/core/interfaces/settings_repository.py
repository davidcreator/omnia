# core/interfaces/settings_repository.py
from abc import ABC, abstractmethod
from typing import Any, Optional


class SettingsRepository(ABC):

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any: ...

    @abstractmethod
    def set(self, key: str, value: Any) -> None: ...

    @abstractmethod
    def delete(self, key: str) -> None: ...

    @abstractmethod
    def exists(self, key: str) -> bool: ...

    @abstractmethod
    def all(self) -> dict[str, Any]: ...
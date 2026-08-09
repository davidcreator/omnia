# core/interfaces/model_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from core.entities.ai_model import AIModel, ModelStatus


class ModelRepository(ABC):

    @abstractmethod
    def save(self, model: AIModel) -> None: ...

    @abstractmethod
    def update(self, model: AIModel) -> None: ...

    @abstractmethod
    def delete(self, model_id: str) -> None: ...

    @abstractmethod
    def find_by_id(self, model_id: str) -> Optional[AIModel]: ...

    @abstractmethod
    def find_all(self) -> list[AIModel]: ...

    @abstractmethod
    def find_by_status(self, status: ModelStatus) -> list[AIModel]: ...

    @abstractmethod
    def exists(self, model_id: str) -> bool: ...
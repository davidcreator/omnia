# core/manager.py
from __future__ import annotations

from core.entities.ai_model import AIModel, ModelStatus
from core.exceptions import ModelNotFoundError, ModelAlreadyRegisteredError
from core.interfaces.model_repository import ModelRepository


class ModelManager:
    """
    Orquestra o ciclo de vida dos modelos registrados.
    Não conhece SQLite, Qt ou engines — só a interface do repositório.
    """

    def __init__(self, repository: ModelRepository) -> None:
        self._repository = repository

    # ── consulta ───────────────────────────────────────────────────────────

    def get(self, model_id: str) -> AIModel:
        model = self._repository.find_by_id(model_id)
        if model is None:
            raise ModelNotFoundError(model_id)
        return model

    def list_all(self) -> list[AIModel]:
        return self._repository.find_all()

    def list_ready(self) -> list[AIModel]:
        return self._repository.find_by_status(ModelStatus.READY)

    def exists(self, model_id: str) -> bool:
        return self._repository.exists(model_id)

    # ── registro ───────────────────────────────────────────────────────────

    def register(self, model: AIModel) -> None:
        if self._repository.exists(model.id):
            raise ModelAlreadyRegisteredError(model.id)
        self._repository.save(model)

    def unregister(self, model_id: str) -> None:
        if not self._repository.exists(model_id):
            raise ModelNotFoundError(model_id)
        self._repository.delete(model_id)

    # ── transições de estado ───────────────────────────────────────────────

    def mark_ready(self, model_id: str) -> AIModel:
        model = self.get(model_id)
        model.mark_ready()
        self._repository.update(model)
        return model

    def mark_error(self, model_id: str) -> AIModel:
        model = self.get(model_id)
        model.mark_error()
        self._repository.update(model)
        return model

    def mark_downloading(self, model_id: str) -> AIModel:
        model = self.get(model_id)
        model.mark_downloading()
        self._repository.update(model)
        return model
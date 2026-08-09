# core/downloader.py
from __future__ import annotations

from typing import Callable
from core.entities.download_task import DownloadTask, DownloadStatus
from core.exceptions import (
    DownloadAlreadyActiveError,
    DownloadNotFoundError,
    DownloadFailedError,
)
from core.interfaces.download_repository import DownloadRepository

ProgressCallback = Callable[[str, int, int], None]  # model_id, downloaded, total


class DownloadManager:
    """
    Gerencia o estado e o ciclo de vida dos downloads.
    Não executa I/O de rede — delega para um executor externo.
    Não conhece Qt, threads ou SQLite diretamente.
    """

    def __init__(self, repository: DownloadRepository) -> None:
        self._repository  = repository
        self._callbacks:  dict[str, list[ProgressCallback]] = {}

    # ── API pública ────────────────────────────────────────────────────────

    def enqueue(self, model_id: str, url: str, destination: str) -> DownloadTask:
        existing = self._repository.find_by_model_id(model_id)
        if existing and existing.is_active:
            raise DownloadAlreadyActiveError(model_id)

        task = DownloadTask(
            model_id=model_id,
            url=url,
            destination=destination,
            status=DownloadStatus.PENDING,
        )
        self._repository.save(task)
        return task

    def start(self, model_id: str) -> DownloadTask:
        task = self._get_task(model_id)
        task.status = DownloadStatus.ACTIVE
        task.updated_at = __import__("datetime").datetime.now()
        self._repository.update(task)
        return task

    def report_progress(
        self, model_id: str, downloaded: int, total: int
    ) -> None:
        task = self._get_task(model_id)
        task.update_progress(downloaded, total)
        self._repository.update(task)

        for cb in self._callbacks.get(model_id, []):
            cb(model_id, downloaded, total)

    def complete(self, model_id: str) -> DownloadTask:
        task = self._get_task(model_id)
        task.mark_completed()
        self._repository.update(task)
        return task

    def fail(self, model_id: str, reason: str = "") -> DownloadTask:
        task = self._get_task(model_id)
        task.mark_failed(reason)
        self._repository.update(task)
        return task

    def cancel(self, model_id: str) -> DownloadTask:
        task = self._get_task(model_id)
        task.mark_cancelled()
        self._repository.update(task)
        return task

    def get_status(self, model_id: str) -> DownloadStatus:
        return self._get_task(model_id).status

    def list_active(self) -> list[DownloadTask]:
        return self._repository.find_by_status(DownloadStatus.ACTIVE)

    def list_all(self) -> list[DownloadTask]:
        return self._repository.find_all()

    # ── callbacks de progresso ─────────────────────────────────────────────

    def subscribe(self, model_id: str, callback: ProgressCallback) -> None:
        self._callbacks.setdefault(model_id, []).append(callback)

    def unsubscribe(self, model_id: str, callback: ProgressCallback) -> None:
        callbacks = self._callbacks.get(model_id, [])
        if callback in callbacks:
            callbacks.remove(callback)

    # ── interno ────────────────────────────────────────────────────────────

    def _get_task(self, model_id: str) -> DownloadTask:
        task = self._repository.find_by_model_id(model_id)
        if task is None:
            raise DownloadNotFoundError(model_id)
        return task
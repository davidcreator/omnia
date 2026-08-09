# core/interfaces/download_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from core.entities.download_task import DownloadTask, DownloadStatus


class DownloadRepository(ABC):

    @abstractmethod
    def save(self, task: DownloadTask) -> None: ...

    @abstractmethod
    def update(self, task: DownloadTask) -> None: ...

    @abstractmethod
    def find_by_model_id(self, model_id: str) -> Optional[DownloadTask]: ...

    @abstractmethod
    def find_by_status(self, status: DownloadStatus) -> list[DownloadTask]: ...

    @abstractmethod
    def find_all(self) -> list[DownloadTask]: ...

    @abstractmethod
    def delete(self, model_id: str) -> None: ...
# core/entities/download_task.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum


class DownloadStatus(Enum):
    PENDING    = "pending"
    ACTIVE     = "active"
    PAUSED     = "paused"
    COMPLETED  = "completed"
    FAILED     = "failed"
    CANCELLED  = "cancelled"


@dataclass
class DownloadTask:
    model_id:        str
    url:             str
    destination:     str
    total_bytes:     int            = 0
    downloaded_bytes: int           = 0
    status:          DownloadStatus = DownloadStatus.PENDING
    error_message:   str            = ""
    created_at:      datetime       = field(default_factory=datetime.now)
    updated_at:      datetime       = field(default_factory=datetime.now)

    @property
    def progress_pct(self) -> float:
        if self.total_bytes <= 0:
            return 0.0
        return round((self.downloaded_bytes / self.total_bytes) * 100, 1)

    @property
    def is_active(self) -> bool:
        return self.status == DownloadStatus.ACTIVE

    @property
    def is_finished(self) -> bool:
        return self.status in (
            DownloadStatus.COMPLETED,
            DownloadStatus.FAILED,
            DownloadStatus.CANCELLED,
        )

    def update_progress(self, downloaded: int, total: int) -> None:
        self.downloaded_bytes = downloaded
        self.total_bytes      = total
        self.updated_at       = datetime.now()

    def mark_completed(self) -> None:
        self.status     = DownloadStatus.COMPLETED
        self.updated_at = datetime.now()

    def mark_failed(self, reason: str = "") -> None:
        self.status        = DownloadStatus.FAILED
        self.error_message = reason
        self.updated_at    = datetime.now()

    def mark_cancelled(self) -> None:
        self.status     = DownloadStatus.CANCELLED
        self.updated_at = datetime.now()
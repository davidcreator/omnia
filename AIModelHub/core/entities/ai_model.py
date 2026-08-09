# core/entities/ai_model.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path


class ModelFormat(Enum):
    GGUF        = "gguf"
    ONNX        = "onnx"
    SAFETENSORS = "safetensors"
    PYTORCH     = "pytorch"
    LLAMAFILE   = "llamafile"
    UNKNOWN     = "unknown"

    @classmethod
    def from_extension(cls, path: str | Path) -> "ModelFormat":
        suffix = Path(path).suffix.lower().lstrip(".")
        mapping = {
            "gguf":        cls.GGUF,
            "onnx":        cls.ONNX,
            "safetensors": cls.SAFETENSORS,
            "pt":          cls.PYTORCH,
            "pth":         cls.PYTORCH,
            "bin":         cls.PYTORCH,
        }
        return mapping.get(suffix, cls.UNKNOWN)


class ModelStatus(Enum):
    REGISTERED  = "registered"
    DOWNLOADING = "downloading"
    READY       = "ready"
    LOADING     = "loading"
    LOADED      = "loaded"
    ERROR       = "error"


@dataclass
class AIModel:
    id:         str
    name:       str
    path:       str
    format:     ModelFormat
    size_bytes: int
    status:     ModelStatus  = ModelStatus.REGISTERED
    created_at: datetime     = field(default_factory=datetime.now)
    updated_at: datetime     = field(default_factory=datetime.now)
    metadata:   dict         = field(default_factory=dict)

    # ── propriedades de conveniência ───────────────────────────────────────

    @property
    def size_mb(self) -> float:
        return round(self.size_bytes / (1024 ** 2), 2)

    @property
    def size_gb(self) -> float:
        return round(self.size_bytes / (1024 ** 3), 2)

    @property
    def filename(self) -> str:
        return Path(self.path).name

    @property
    def is_ready(self) -> bool:
        return self.status == ModelStatus.READY

    @property
    def is_loaded(self) -> bool:
        return self.status == ModelStatus.LOADED

    # ── transições de estado ───────────────────────────────────────────────

    def mark_ready(self) -> None:
        self.status = ModelStatus.READY
        self.updated_at = datetime.now()

    def mark_loading(self) -> None:
        self.status = ModelStatus.LOADING
        self.updated_at = datetime.now()

    def mark_loaded(self) -> None:
        self.status = ModelStatus.LOADED
        self.updated_at = datetime.now()

    def mark_error(self) -> None:
        self.status = ModelStatus.ERROR
        self.updated_at = datetime.now()

    def mark_downloading(self) -> None:
        self.status = ModelStatus.DOWNLOADING
        self.updated_at = datetime.now()
# core/entities/catalog_entry.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class CatalogEntry:
    id:           str
    name:         str
    description:  str
    url:          str
    format:       str
    size_bytes:   int
    tags:         list[str] = field(default_factory=list)
    is_available: bool      = True
    updated_at:   datetime  = field(default_factory=datetime.now)

    @property
    def size_gb(self) -> float:
        return round(self.size_bytes / (1024 ** 3), 2)
# core/entities/benchmark_result.py
from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime


@dataclass
class BenchmarkResult:
    id:               str
    model_id:         str
    prompt_tokens:    int
    completion_tokens: int
    elapsed_ms:       float
    tokens_per_second: float
    memory_mb:        float
    created_at:       datetime = field(default_factory=datetime.now)
    metadata:         dict     = field(default_factory=dict)

    @property
    def total_tokens(self) -> int:
        return self.prompt_tokens + self.completion_tokens

    @property
    def elapsed_seconds(self) -> float:
        return round(self.elapsed_ms / 1000, 3)
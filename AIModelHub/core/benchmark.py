# core/benchmark.py
from __future__ import annotations

import time
import uuid
from typing import Callable

from core.entities.benchmark_result import BenchmarkResult
from core.exceptions import BenchmarkFailedError, ModelNotFoundError
from core.interfaces.benchmark_repository import BenchmarkRepository
from core.interfaces.model_repository import ModelRepository

InferenceCallable = Callable[[str], tuple[int, int]]
# recebe prompt, retorna (prompt_tokens, completion_tokens)


class BenchmarkService:
    """
    Executa e persiste benchmarks de modelos.
    Não conhece a engine de inferência — recebe um callable.
    """

    def __init__(
        self,
        benchmark_repository: BenchmarkRepository,
        model_repository: ModelRepository,
    ) -> None:
        self._benchmarks = benchmark_repository
        self._models     = model_repository

    # ── API pública ────────────────────────────────────────────────────────

    def run(
        self,
        model_id: str,
        prompt: str,
        inference_fn: InferenceCallable,
        memory_mb: float = 0.0,
    ) -> BenchmarkResult:
        """
        Executa o benchmark e persiste o resultado.

        Args:
            model_id:     ID do modelo a ser benchmarkado.
            prompt:       Texto de entrada para o benchmark.
            inference_fn: Callable que executa a inferência e retorna
                          (prompt_tokens, completion_tokens).
            memory_mb:    Uso de memória durante o benchmark (opcional).
        """
        if not self._models.exists(model_id):
            raise ModelNotFoundError(model_id)

        try:
            start = time.perf_counter()
            prompt_tokens, completion_tokens = inference_fn(prompt)
            elapsed_ms = (time.perf_counter() - start) * 1000
        except ModelNotFoundError:
            raise
        except Exception as exc:
            raise BenchmarkFailedError(model_id, str(exc)) from exc

        total_tokens = prompt_tokens + completion_tokens
        tps = (total_tokens / (elapsed_ms / 1000)) if elapsed_ms > 0 else 0.0

        result = BenchmarkResult(
            id=uuid.uuid4().hex,
            model_id=model_id,
            prompt_tokens=prompt_tokens,
            completion_tokens=completion_tokens,
            elapsed_ms=elapsed_ms,
            tokens_per_second=round(tps, 2),
            memory_mb=memory_mb,
        )

        self._benchmarks.save(result)
        return result

    def history(self, model_id: str) -> list[BenchmarkResult]:
        return self._benchmarks.find_by_model_id(model_id)

    def all_results(self) -> list[BenchmarkResult]:
        return self._benchmarks.find_all()

    def clear_history(self, model_id: str) -> None:
        self._benchmarks.delete_by_model_id(model_id)
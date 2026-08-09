# core/interfaces/benchmark_repository.py
from abc import ABC, abstractmethod
from core.entities.benchmark_result import BenchmarkResult


class BenchmarkRepository(ABC):

    @abstractmethod
    def save(self, result: BenchmarkResult) -> None: ...

    @abstractmethod
    def find_by_model_id(self, model_id: str) -> list[BenchmarkResult]: ...

    @abstractmethod
    def find_all(self) -> list[BenchmarkResult]: ...

    @abstractmethod
    def delete_by_model_id(self, model_id: str) -> None: ...
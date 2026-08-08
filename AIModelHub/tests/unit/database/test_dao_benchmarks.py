"""
Testes unitários — database/dao_benchmarks.py
"""

import pytest
from database.dao_benchmarks import DAOBenchmarks


@pytest.mark.unit
class TestDAOBenchmarksCreate:
    """Testa criação de benchmarks."""

    def test_create_basic(self, dao_benchmarks, sample_model):
        benchmark_id = dao_benchmarks.create(
            model_id="llama3:8b",
            engine_id="ollama",
        )
        assert benchmark_id is not None
        assert benchmark_id > 0

    def test_create_with_all_metrics(self, dao_benchmarks, sample_model):
        benchmark_id = dao_benchmarks.create(
            model_id="llama3:8b",
            engine_id="ollama",
            load_time_ms=1200.5,
            tokens_per_sec=45.3,
            ram_usage_mb=4096.0,
            vram_usage_mb=3800.0,
            cpu_percent=25.5,
            gpu_percent=85.0,
            metadata={"prompt": "test"},
        )
        result = dao_benchmarks.get_by_id(benchmark_id)
        assert result["tokens_per_sec"] == pytest.approx(45.3)
        assert result["ram_usage_mb"] == pytest.approx(4096.0)


@pytest.mark.unit
class TestDAOBenchmarksRead:
    """Testa leitura de benchmarks."""

    def test_get_by_id(self, dao_benchmarks, sample_model):
        bid = dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=50.0)
        result = dao_benchmarks.get_by_id(bid)
        assert result is not None
        assert result["model_id"] == "llama3:8b"

    def test_get_by_id_nonexistent(self, dao_benchmarks):
        result = dao_benchmarks.get_by_id(99999)
        assert result is None

    def test_get_by_model(self, dao_benchmarks, sample_model):
        dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=40.0)
        dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=50.0)
        results = dao_benchmarks.get_by_model("llama3:8b")
        assert len(results) == 2

    def test_get_by_model_limit(self, dao_benchmarks, sample_model):
        for i in range(5):
            dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=float(i))
        results = dao_benchmarks.get_by_model("llama3:8b", limit=3)
        assert len(results) == 3

    def test_get_latest(self, dao_benchmarks, sample_model):
        dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=40.0)
        dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=55.0)
        result = dao_benchmarks.get_latest("llama3:8b", "ollama")
        assert result is not None

    def test_get_average_by_model(self, dao_benchmarks, sample_model):
        dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=40.0)
        dao_benchmarks.create("llama3:8b", "ollama", tokens_per_sec=60.0)
        result = dao_benchmarks.get_average_by_model("llama3:8b")
        assert result["avg_tokens_per_sec"] == pytest.approx(50.0)


@pytest.mark.unit
class TestDAOBenchmarksDelete:
    """Testa remoção de benchmarks."""

    def test_delete_existing(self, dao_benchmarks, sample_model):
        bid = dao_benchmarks.create("llama3:8b", "ollama")
        result = dao_benchmarks.delete(bid)
        assert result is True
        assert dao_benchmarks.get_by_id(bid) is None

    def test_delete_nonexistent(self, dao_benchmarks):
        result = dao_benchmarks.delete(99999)
        assert result is False

    def test_delete_by_model(self, dao_benchmarks, sample_model):
        dao_benchmarks.create("llama3:8b", "ollama")
        dao_benchmarks.create("llama3:8b", "ollama")
        count = dao_benchmarks.delete_by_model("llama3:8b")
        assert count == 2
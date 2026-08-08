"""
Testes de performance — DAOs com grandes volumes de dados.
"""

import time
import pytest
import uuid

from database.dao_models import DAOModels
from database.dao_history import DAOHistory


@pytest.mark.performance
@pytest.mark.slow
class TestDAOModelsPerformance:
    """Testa performance do DAOModels com volumes altos."""

    def test_insert_100_models(self, dao_models, benchmark):
        """Inserção de 100 modelos deve ser rápida."""

        def insert_models():
            # Usa UUID para garantir IDs únicos em cada rodada do benchmark
            run_id = uuid.uuid4().hex[:8]
            for i in range(100):
                dao_models.create(
                    model_id=f"model:{run_id}:{i}",
                    name=f"Model {run_id} {i}",
                    format="gguf",
                    path=f"/models/model_{run_id}_{i}.gguf",
                )

        benchmark(insert_models)

    def test_get_all_100_models(self, dao_models):
        """Leitura de 100 modelos deve ser concluída em menos de 1s."""
        for i in range(100):
            dao_models.create(
                model_id=f"perf_model:{i}",
                name=f"Perf Model {i}",
                format="gguf",
                path=f"/models/perf_{i}.gguf",
            )

        start   = time.perf_counter()
        results = dao_models.get_all()
        elapsed = time.perf_counter() - start

        assert len(results) == 100
        assert elapsed < 1.0, f"get_all() demorou {elapsed:.3f}s (limite: 1.0s)"

    def test_search_100_models(self, dao_models):
        """Busca em 100 modelos deve ser concluída em menos de 500ms."""
        for i in range(100):
            dao_models.create(
                model_id=f"search_model:{i}",
                name=f"Search Model {i}",
                format="gguf",
                path=f"/models/search_{i}.gguf",
                manufacturer="TestCorp" if i % 2 == 0 else "OtherCorp",
            )

        start   = time.perf_counter()
        results = dao_models.search("TestCorp")
        elapsed = time.perf_counter() - start

        assert len(results) == 50
        assert elapsed < 0.5, f"search() demorou {elapsed:.3f}s (limite: 0.5s)"


@pytest.mark.performance
@pytest.mark.slow
class TestDAOHistoryPerformance:
    """Testa performance do DAOHistory com volumes altos."""

    def test_insert_1000_history_records(self, dao_history):
        """Inserção de 1000 registros deve ser concluída em menos de 3s."""
        start = time.perf_counter()
        for i in range(1000):
            dao_history.add(
                action="inference",
                details={"tokens": i, "duration_ms": i * 10},
            )
        elapsed = time.perf_counter() - start
        assert elapsed < 3.0, f"Inserção demorou {elapsed:.3f}s (limite: 3.0s)"

    def test_get_recent_from_1000_records(self, dao_history):
        """Leitura dos 50 mais recentes de 1000 registros."""
        for i in range(1000):
            dao_history.add("inference")

        start   = time.perf_counter()
        results = dao_history.get_recent(limit=50)
        elapsed = time.perf_counter() - start

        assert len(results) == 50
        assert elapsed < 0.5, f"get_recent() demorou {elapsed:.3f}s (limite: 0.5s)"
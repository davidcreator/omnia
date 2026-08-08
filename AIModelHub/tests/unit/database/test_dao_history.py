"""
Testes unitários — database/dao_history.py
"""

import pytest
from datetime import datetime, timedelta, UTC
from database.dao_history import DAOHistory


@pytest.mark.unit
class TestDAOHistoryCreate:
    """Testa criação de registros de histórico."""

    def test_add_basic(self, dao_history):
        history_id = dao_history.add("load_model")
        assert history_id is not None
        assert history_id > 0

    def test_add_with_model(self, dao_history, sample_model):
        history_id = dao_history.add(
            action="load_model",
            model_id="llama3:8b",
        )
        result = dao_history.get_recent(limit=1)
        assert result[0]["model_id"] == "llama3:8b"

    def test_add_with_details(self, dao_history):
        dao_history.add(
            action="inference",
            details={"tokens": 128, "duration_ms": 500},
        )
        result = dao_history.get_recent(limit=1)
        assert result[0]["details"]["tokens"] == 128


@pytest.mark.unit
class TestDAOHistoryRead:
    """Testa leitura do histórico."""

    def test_get_recent_empty(self, dao_history):
        result = dao_history.get_recent()
        assert result == []

    def test_get_recent_limit(self, dao_history):
        for i in range(10):
            dao_history.add(f"action_{i}")
        result = dao_history.get_recent(limit=5)
        assert len(result) == 5

    def test_get_by_action(self, dao_history):
        dao_history.add("load_model")
        dao_history.add("load_model")
        dao_history.add("inference")
        result = dao_history.get_by_action("load_model")
        assert len(result) == 2
        assert all(r["action"] == "load_model" for r in result)

    def test_get_by_model(self, dao_history, sample_model):
        dao_history.add("load_model", model_id="llama3:8b")
        dao_history.add("inference", model_id="llama3:8b")
        dao_history.add("load_model")
        result = dao_history.get_by_model("llama3:8b")
        assert len(result) == 2

    def test_get_most_used_models(self, dao_history, sample_models):
        for _ in range(3):
            dao_history.add("inference", model_id="llama3:8b")
        dao_history.add("inference", model_id="mistral:7b")
        result = dao_history.get_most_used_models()
        assert result[0]["model_id"] == "llama3:8b"
        assert result[0]["usage_count"] == 3

    def test_count(self, dao_history):
        dao_history.add("action1")
        dao_history.add("action2")
        assert dao_history.count() == 2

    def test_count_by_action(self, dao_history):
        dao_history.add("load_model")
        dao_history.add("load_model")
        dao_history.add("inference")
        assert dao_history.count("load_model") == 2


@pytest.mark.unit
class TestDAOHistoryDelete:
    """Testa remoção do histórico."""

    def test_clear(self, dao_history):
        dao_history.add("action1")
        dao_history.add("action2")
        dao_history.clear()
        assert dao_history.count() == 0

    def test_clear_before_date(self, dao_history):
        dao_history.add("old_action")
        future = datetime.now(UTC) + timedelta(days=1)
        dao_history.clear_before(future)
        assert dao_history.count() == 0
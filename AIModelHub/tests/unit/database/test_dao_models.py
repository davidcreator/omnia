"""
Testes unitários — database/dao_models.py
"""

import pytest
from database.dao_models import DAOModels


@pytest.mark.unit
class TestDAOModelsCreate:
    """Testa criação de modelos."""

    def test_create_model(self, dao_models):
        dao_models.create(
            model_id="test:model",
            name="Test Model",
            format="gguf",
            path="/models/test.gguf",
        )
        result = dao_models.get_by_id("test:model")
        assert result is not None
        assert result["name"] == "Test Model"

    def test_create_with_all_fields(self, dao_models):
        dao_models.create(
            model_id="full:model",
            name="Full Model",
            format="gguf",
            path="/models/full.gguf",
            architecture="llama",
            quantization="q4_0",
            size_bytes=1_000_000,
            manufacturer="Test Corp",
            description="A test model",
            metadata={"key": "value"},
        )
        result = dao_models.get_by_id("full:model")
        assert result["architecture"] == "llama"
        assert result["quantization"] == "q4_0"
        assert result["size_bytes"] == 1_000_000
        assert result["manufacturer"] == "Test Corp"
        assert result["metadata"]["key"] == "value"

    def test_create_model_default_not_favorite(self, dao_models):
        dao_models.create(
            model_id="new:model",
            name="New Model",
            format="gguf",
            path="/models/new.gguf",
        )
        result = dao_models.get_by_id("new:model")
        assert result["is_favorite"] == 0


@pytest.mark.unit
class TestDAOModelsRead:
    """Testa leitura de modelos."""

    def test_get_by_id_existing(self, sample_model):
        assert sample_model is not None
        assert sample_model["id"] == "llama3:8b"

    def test_get_by_id_nonexistent(self, dao_models):
        result = dao_models.get_by_id("nonexistent:model")
        assert result is None

    def test_get_all_returns_list(self, dao_models):
        result = dao_models.get_all()
        assert isinstance(result, list)

    def test_get_all_returns_all_models(self, sample_models, dao_models):
        result = dao_models.get_all()
        assert len(result) == 3

    def test_get_by_format(self, sample_models, dao_models):
        result = dao_models.get_by_format("gguf")
        assert all(m["format"] == "gguf" for m in result)

    def test_get_by_format_empty(self, dao_models):
        result = dao_models.get_by_format("tensorrt")
        assert result == []

    def test_get_favorites_empty(self, sample_models, dao_models):
        result = dao_models.get_favorites()
        assert result == []

    def test_search_by_name(self, sample_models, dao_models):
        result = dao_models.search("Llama")
        assert len(result) >= 1
        assert any("Llama" in m["name"] for m in result)

    def test_search_by_manufacturer(self, sample_models, dao_models):
        result = dao_models.search("Meta")
        assert len(result) >= 1

    def test_search_with_format_filter(self, sample_models, dao_models):
        result = dao_models.search("", format="huggingface")
        assert all(m["format"] == "huggingface" for m in result)

    def test_search_no_results(self, dao_models):
        result = dao_models.search("xyznotexistent")
        assert result == []


@pytest.mark.unit
class TestDAOModelsUpdate:
    """Testa atualização de modelos."""

    def test_update_name(self, sample_model, dao_models):
        dao_models.update("llama3:8b", name="Llama 3 8B Updated")
        result = dao_models.get_by_id("llama3:8b")
        assert result["name"] == "Llama 3 8B Updated"

    def test_update_multiple_fields(self, sample_model, dao_models):
        dao_models.update(
            "llama3:8b",
            description="Updated description",
            manufacturer="Updated Corp",
        )
        result = dao_models.get_by_id("llama3:8b")
        assert result["description"] == "Updated description"
        assert result["manufacturer"] == "Updated Corp"

    def test_update_nonexistent_returns_false(self, dao_models):
        result = dao_models.update("nonexistent:model", name="Test")
        assert result is False

    def test_mark_as_favorite(self, sample_model, dao_models):
        dao_models.mark_as_favorite("llama3:8b", True)
        result = dao_models.get_by_id("llama3:8b")
        assert result["is_favorite"] == 1

    def test_unmark_as_favorite(self, sample_model, dao_models):
        dao_models.mark_as_favorite("llama3:8b", True)
        dao_models.mark_as_favorite("llama3:8b", False)
        result = dao_models.get_by_id("llama3:8b")
        assert result["is_favorite"] == 0

    def test_mark_as_used_updates_timestamp(self, sample_model, dao_models):
        dao_models.mark_as_used("llama3:8b")
        result = dao_models.get_by_id("llama3:8b")
        assert result["last_used_at"] is not None


@pytest.mark.unit
class TestDAOModelsDelete:
    """Testa remoção de modelos."""

    def test_delete_existing(self, sample_model, dao_models):
        result = dao_models.delete("llama3:8b")
        assert result is True
        assert dao_models.get_by_id("llama3:8b") is None

    def test_delete_nonexistent(self, dao_models):
        result = dao_models.delete("nonexistent:model")
        assert result is False


@pytest.mark.unit
class TestDAOModelsCount:
    """Testa contagens."""

    def test_count_empty(self, dao_models):
        assert dao_models.count() == 0

    def test_count_with_models(self, sample_models, dao_models):
        assert dao_models.count() == 3

    def test_count_favorites_empty(self, sample_models, dao_models):
        assert dao_models.count_favorites() == 0

    def test_count_favorites_after_mark(self, sample_model, dao_models):
        dao_models.mark_as_favorite("llama3:8b", True)
        assert dao_models.count_favorites() == 1

    def test_exists_true(self, sample_model, dao_models):
        assert dao_models.exists("llama3:8b") is True

    def test_exists_false(self, dao_models):
        assert dao_models.exists("nonexistent:model") is False
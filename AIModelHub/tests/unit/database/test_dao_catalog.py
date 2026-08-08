"""
Testes unitários — database/dao_catalog.py
"""

import pytest
from database.dao_catalog import DAOCatalog


@pytest.mark.unit
class TestDAOCatalogTags:
    """Testa operações com tags."""

    def test_create_tag(self, dao_catalog):
        tag_id = dao_catalog.create_tag("chatbot")
        assert tag_id is not None
        assert isinstance(tag_id, int)

    def test_create_tag_idempotent(self, dao_catalog):
        id1 = dao_catalog.create_tag("chatbot")
        id2 = dao_catalog.create_tag("chatbot")
        assert id1 == id2

    def test_get_all_tags_empty(self, dao_catalog):
        result = dao_catalog.get_all_tags()
        assert result == []

    def test_get_all_tags(self, dao_catalog):
        dao_catalog.create_tag("chatbot")
        dao_catalog.create_tag("code")
        tags = dao_catalog.get_all_tags()
        assert "chatbot" in tags
        assert "code" in tags

    def test_get_tag_id_existing(self, dao_catalog):
        dao_catalog.create_tag("vision")
        tag_id = dao_catalog.get_tag_id("vision")
        assert tag_id is not None

    def test_get_tag_id_nonexistent(self, dao_catalog):
        result = dao_catalog.get_tag_id("nonexistent")
        assert result is None

    def test_delete_tag(self, dao_catalog):
        tag_id = dao_catalog.create_tag("to_delete")
        result = dao_catalog.delete_tag(tag_id)
        assert result is True
        assert dao_catalog.get_tag_id("to_delete") is None


@pytest.mark.unit
class TestDAOCatalogModelTags:
    """Testa relação modelo ↔ tags."""

    def test_add_tag_to_model(self, dao_catalog, sample_model):
        result = dao_catalog.add_tag_to_model("llama3:8b", "chatbot")
        assert result is True

    def test_get_model_tags(self, dao_catalog, sample_model):
        dao_catalog.add_tag_to_model("llama3:8b", "chatbot")
        dao_catalog.add_tag_to_model("llama3:8b", "english")
        tags = dao_catalog.get_model_tags("llama3:8b")
        assert "chatbot" in tags
        assert "english" in tags

    def test_get_model_tags_empty(self, dao_catalog, sample_model):
        tags = dao_catalog.get_model_tags("llama3:8b")
        assert tags == []

    def test_add_tags_to_model(self, dao_catalog, sample_model):
        count = dao_catalog.add_tags_to_model(
            "llama3:8b",
            ["chatbot", "english", "instruct"],
        )
        assert count == 3

    def test_remove_tag_from_model(self, dao_catalog, sample_model):
        dao_catalog.add_tag_to_model("llama3:8b", "chatbot")
        result = dao_catalog.remove_tag_from_model("llama3:8b", "chatbot")
        assert result is True
        tags = dao_catalog.get_model_tags("llama3:8b")
        assert "chatbot" not in tags

    def test_clear_model_tags(self, dao_catalog, sample_model):
        dao_catalog.add_tags_to_model("llama3:8b", ["a", "b", "c"])
        dao_catalog.clear_model_tags("llama3:8b")
        assert dao_catalog.get_model_tags("llama3:8b") == []

    def test_get_models_by_tag(self, dao_catalog, sample_models, dao_models):
        dao_catalog.add_tag_to_model("llama3:8b", "open-source")
        dao_catalog.add_tag_to_model("mistral:7b", "open-source")
        models = dao_catalog.get_models_by_tag("open-source")
        assert "llama3:8b" in models
        assert "mistral:7b" in models


@pytest.mark.unit
class TestDAOCatalogSearch:
    """Testa busca combinada por tags."""

    def test_search_by_single_tag(self, dao_catalog, sample_models):
        dao_catalog.add_tag_to_model("llama3:8b", "english")
        dao_catalog.add_tag_to_model("mistral:7b", "english")
        result = dao_catalog.search_by_tags(["english"])
        assert "llama3:8b" in result
        assert "mistral:7b" in result

    def test_search_by_tags_match_all(self, dao_catalog, sample_models):
        dao_catalog.add_tags_to_model("llama3:8b", ["english", "instruct"])
        dao_catalog.add_tag_to_model("mistral:7b", "english")
        result = dao_catalog.search_by_tags(
            ["english", "instruct"],
            match_all=True,
        )
        assert "llama3:8b" in result
        assert "mistral:7b" not in result

    def test_search_by_tags_match_any(self, dao_catalog, sample_models):
        dao_catalog.add_tag_to_model("llama3:8b", "english")
        dao_catalog.add_tag_to_model("mistral:7b", "french")
        result = dao_catalog.search_by_tags(
            ["english", "french"],
            match_all=False,
        )
        assert "llama3:8b" in result
        assert "mistral:7b" in result

    def test_search_empty_tags(self, dao_catalog):
        result = dao_catalog.search_by_tags([])
        assert result == []
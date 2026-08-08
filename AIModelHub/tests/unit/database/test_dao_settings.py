"""
Testes unitários — database/dao_settings.py
"""

import pytest
from database.dao_settings import DAOSettings


@pytest.mark.unit
class TestDAOSettingsSetGet:
    """Testa set e get de configurações."""

    def test_set_and_get_string(self, dao_settings):
        dao_settings.set("workspace.path", "/AIModels")
        assert dao_settings.get("workspace.path") == "/AIModels"

    def test_set_and_get_bool_true(self, dao_settings):
        dao_settings.set("backup.enabled", True)
        assert dao_settings.get("backup.enabled") is True

    def test_set_and_get_bool_false(self, dao_settings):
        dao_settings.set("backup.enabled", False)
        assert dao_settings.get("backup.enabled") is False

    def test_set_and_get_int(self, dao_settings):
        dao_settings.set("ui.width", 1920)
        assert dao_settings.get("ui.width") == 1920

    def test_set_and_get_float(self, dao_settings):
        dao_settings.set("cache.ttl", 3.14)
        assert dao_settings.get("cache.ttl") == pytest.approx(3.14)

    def test_get_nonexistent_returns_default(self, dao_settings):
        result = dao_settings.get("nonexistent.key", "fallback")
        assert result == "fallback"

    def test_get_nonexistent_returns_none(self, dao_settings):
        result = dao_settings.get("nonexistent.key")
        assert result is None

    def test_upsert_updates_existing(self, dao_settings):
        dao_settings.set("general.theme", "dark")
        dao_settings.set("general.theme", "light")
        assert dao_settings.get("general.theme") == "light"


@pytest.mark.unit
class TestDAOSettingsGetAll:
    """Testa recuperação de todas as configurações."""

    def test_get_all_empty(self, dao_settings):
        result = dao_settings.get_all()
        assert isinstance(result, dict)

    def test_get_all_returns_all(self, dao_settings):
        dao_settings.set("key1", "value1")
        dao_settings.set("key2", "value2")
        result = dao_settings.get_all()
        assert "key1" in result
        assert "key2" in result

    def test_get_by_category(self, dao_settings):
        dao_settings.set("theme", "dark", category="ui")
        dao_settings.set("language", "pt-BR", category="general")
        result = dao_settings.get_by_category("ui")
        assert "theme" in result
        assert "language" not in result


@pytest.mark.unit
class TestDAOSettingsSetMany:
    """Testa definição de múltiplas configurações."""

    def test_set_many(self, dao_settings):
        dao_settings.set_many({
            "key1": "value1",
            "key2": "value2",
            "key3": 42,
        })
        assert dao_settings.get("key1") == "value1"
        assert dao_settings.get("key2") == "value2"
        assert dao_settings.get("key3") == 42


@pytest.mark.unit
class TestDAOSettingsDelete:
    """Testa remoção de configurações."""

    def test_delete_existing(self, dao_settings):
        dao_settings.set("to.delete", "value")
        result = dao_settings.delete("to.delete")
        assert result is True
        assert dao_settings.get("to.delete") is None

    def test_delete_nonexistent(self, dao_settings):
        result = dao_settings.delete("nonexistent.key")
        assert result is False

    def test_delete_category(self, dao_settings):
        dao_settings.set("key1", "v1", category="temp")
        dao_settings.set("key2", "v2", category="temp")
        count = dao_settings.delete_category("temp")
        assert count == 2
        assert dao_settings.get("key1") is None
"""
Testes unitários — shared/settings.py
"""

import pytest
from pathlib import Path
from shared.settings import Settings


@pytest.mark.unit
class TestSettingsSingleton:
    """Testa o comportamento Singleton."""

    def test_singleton_same_instance(self, clean_settings):
        s1 = Settings()
        s2 = Settings()
        assert s1 is s2

    def test_singleton_preserves_data(self, clean_settings):
        s1 = Settings()
        s1.set("test.key", "value")
        s2 = Settings()
        assert s2.get("test.key") == "value"


@pytest.mark.unit
class TestSettingsGetSet:
    """Testa get e set com notação de ponto."""

    def test_set_and_get_string(self, clean_settings):
        clean_settings.set("general.theme", "light")
        assert clean_settings.get("general.theme") == "light"

    def test_set_and_get_int(self, clean_settings):
        clean_settings.set("ui.width", 1920)
        assert clean_settings.get("ui.width") == 1920

    def test_set_and_get_bool(self, clean_settings):
        clean_settings.set("general.debug", True)
        assert clean_settings.get("general.debug") is True

    def test_get_nonexistent_returns_default(self, clean_settings):
        result = clean_settings.get("nonexistent.key", "fallback")
        assert result == "fallback"

    def test_get_nonexistent_returns_none(self, clean_settings):
        result = clean_settings.get("nonexistent.key")
        assert result is None

    def test_set_deep_nested(self, clean_settings):
        clean_settings.set("a.b.c.d", "deep")
        assert clean_settings.get("a.b.c.d") == "deep"


@pytest.mark.unit
class TestSettingsDefaults:
    """Testa carregamento de defaults."""

    def test_load_defaults_from_file(self, clean_settings, tmp_path):
        """Testa carregamento do default.json."""
        import json

        config_file = tmp_path / "default.json"
        config_file.write_text(
            json.dumps({"general": {"theme": "dark"}}),
            encoding="utf-8",
        )

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.CONFIG_DEFAULT_FILE", config_file)
            clean_settings.load_defaults()

        assert clean_settings.get("general.theme") == "dark"

    def test_load_defaults_missing_file(self, clean_settings, tmp_path):
        """Testa fallback quando default.json não existe."""
        missing_file = tmp_path / "missing.json"

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.CONFIG_DEFAULT_FILE", missing_file)
            clean_settings.load_defaults()

        # Deve usar hardcoded defaults
        assert clean_settings.get("general.theme") is not None

    def test_load_defaults_invalid_json(self, clean_settings, tmp_path):
        """Testa fallback quando default.json tem JSON inválido."""
        bad_file = tmp_path / "default.json"
        bad_file.write_text("{ invalid json }", encoding="utf-8")

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.CONFIG_DEFAULT_FILE", bad_file)
            clean_settings.load_defaults()

        # Deve usar hardcoded defaults
        assert clean_settings.get("general.theme") is not None


@pytest.mark.unit
class TestSettingsProperties:
    """Testa as propriedades tipadas."""

    def test_workspace_path_returns_path(self, clean_settings):
        assert isinstance(clean_settings.workspace_path, Path)

    def test_theme_returns_string(self, clean_settings):
        assert isinstance(clean_settings.theme, str)

    def test_language_returns_string(self, clean_settings):
        assert isinstance(clean_settings.language, str)

    def test_workspace_path_expanduser(self, clean_settings):
        clean_settings.set("workspace.path", "~/AIModels")
        path = clean_settings.workspace_path
        assert "~" not in str(path)


@pytest.mark.unit
class TestSettingsPriority:
    """Testa a hierarquia de prioridade."""

    def test_runtime_overrides_defaults(self, clean_settings):
        """Runtime deve ter prioridade sobre defaults."""
        clean_settings._defaults = {"general": {"theme": "light"}}
        clean_settings.set("general.theme", "dark")
        assert clean_settings.get("general.theme") == "dark"

    def test_defaults_used_when_no_runtime(self, clean_settings):
        """Defaults são usados quando não há valor em runtime."""
        clean_settings._defaults = {"general": {"theme": "light"}}
        assert clean_settings.get("general.theme") == "light"
"""
Testes unitários — shared/constants.py
"""

import pytest
from pathlib import Path
from shared.constants import (
    APP_NAME,
    APP_VERSION,
    APP_AUTHOR,
    APP_ROOT,
    CONFIG_DIR,
    CONFIG_DEFAULT_FILE,
    USER_DATA_DIR,
    DATABASE_FILE,
    LOG_FILE,
    DEFAULT_WORKSPACE,
    WORKSPACE_SUBDIRS,
    SUPPORTED_FORMATS,
    FORMAT_EXTENSIONS,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
    LOG_LEVEL,
)


@pytest.mark.unit
class TestAppInfo:
    """Testa as constantes de informação da aplicação."""

    def test_app_name_not_empty(self):
        assert APP_NAME != ""

    def test_app_version_format(self):
        """Versão deve seguir o padrão semântico X.Y.Z"""
        parts = APP_VERSION.split(".")
        assert len(parts) == 3
        assert all(part.isdigit() for part in parts)

    def test_app_author_not_empty(self):
        assert APP_AUTHOR != ""


@pytest.mark.unit
class TestPaths:
    """Testa as constantes de paths."""

    def test_app_root_is_path(self):
        assert isinstance(APP_ROOT, Path)

    def test_app_root_exists(self):
        assert APP_ROOT.exists()

    def test_config_dir_inside_app_root(self):
        assert str(APP_ROOT) in str(CONFIG_DIR)

    def test_config_default_file_is_json(self):
        assert CONFIG_DEFAULT_FILE.suffix == ".json"

    def test_user_data_dir_is_path(self):
        assert isinstance(USER_DATA_DIR, Path)

    def test_database_file_is_db(self):
        assert DATABASE_FILE.suffix == ".db"

    def test_log_file_is_log(self):
        assert LOG_FILE.suffix == ".log"

    def test_default_workspace_is_path(self):
        assert isinstance(DEFAULT_WORKSPACE, Path)


@pytest.mark.unit
class TestWorkspace:
    """Testa as constantes do workspace."""

    def test_workspace_subdirs_not_empty(self):
        assert len(WORKSPACE_SUBDIRS) > 0

    def test_workspace_subdirs_are_strings(self):
        assert all(isinstance(d, str) for d in WORKSPACE_SUBDIRS)

    def test_workspace_contains_models(self):
        assert any("Models" in d for d in WORKSPACE_SUBDIRS)

    def test_workspace_contains_temp(self):
        assert any("Temp" in d for d in WORKSPACE_SUBDIRS)

    def test_workspace_contains_backups(self):
        assert any("Backups" in d for d in WORKSPACE_SUBDIRS)


@pytest.mark.unit
class TestFormats:
    """Testa as constantes de formatos."""

    def test_supported_formats_not_empty(self):
        assert len(SUPPORTED_FORMATS) > 0

    def test_gguf_in_supported_formats(self):
        assert "gguf" in SUPPORTED_FORMATS

    def test_huggingface_in_supported_formats(self):
        assert "huggingface" in SUPPORTED_FORMATS

    def test_format_extensions_is_dict(self):
        assert isinstance(FORMAT_EXTENSIONS, dict)

    def test_gguf_extension_correct(self):
        assert ".gguf" in FORMAT_EXTENSIONS["gguf"]


@pytest.mark.unit
class TestUIConstants:
    """Testa as constantes de interface."""

    def test_min_width_positive(self):
        assert WINDOW_MIN_WIDTH > 0

    def test_min_height_positive(self):
        assert WINDOW_MIN_HEIGHT > 0

    def test_default_larger_than_min(self):
        assert WINDOW_DEFAULT_WIDTH >= WINDOW_MIN_WIDTH
        assert WINDOW_DEFAULT_HEIGHT >= WINDOW_MIN_HEIGHT


@pytest.mark.unit
class TestLogConstants:
    """Testa as constantes de log."""

    def test_log_level_valid(self):
        valid_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        assert LOG_LEVEL in valid_levels
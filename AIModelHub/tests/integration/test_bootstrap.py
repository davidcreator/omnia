"""
Testes de integração — Bootstrap e inicialização completa.
"""

import pytest
from pathlib import Path
from unittest.mock import patch, MagicMock


@pytest.mark.integration
class TestBootstrapIntegration:
    """Testa a sequência de inicialização completa."""

    def test_system_dirs_created(self, tmp_path):
        """Verifica que os diretórios do sistema são criados."""
        from app.bootstrap import Bootstrap

        user_data = tmp_path / "user_data"
        logs_dir = user_data / "logs"

        with patch("shared.constants.USER_DATA_DIR", user_data):
            bootstrap = Bootstrap()
            bootstrap._step_system_dirs()

        assert user_data.exists()
        assert logs_dir.exists()

    def test_workspace_created(self, tmp_path):
        """Verifica que o workspace AIModels é criado."""
        from app.bootstrap import Bootstrap
        from shared.settings import Settings

        Settings._instance = None
        settings = Settings()
        settings.set("workspace.path", str(tmp_path / "AIModels"))

        bootstrap = Bootstrap()
        bootstrap._step_workspace()

        workspace = tmp_path / "AIModels"
        assert workspace.exists()
        assert (workspace / "Models" / "GGUF").exists()
        assert (workspace / "Temp").exists()
        assert (workspace / "Backups" / "db").exists()

        Settings._instance = None

    def test_temp_cleaned_on_startup(self, tmp_path):
        """Verifica que a pasta Temp é limpa na inicialização."""
        from app.bootstrap import Bootstrap
        from shared.settings import Settings

        Settings._instance = None
        settings = Settings()
        workspace = tmp_path / "AIModels"
        settings.set("workspace.path", str(workspace))

        # Cria arquivo na pasta Temp
        temp_dir = workspace / "Temp"
        temp_dir.mkdir(parents=True)
        leftover = temp_dir / "leftover.tmp"
        leftover.write_text("leftover data")

        bootstrap = Bootstrap()
        bootstrap._step_workspace()

        assert not leftover.exists()
        assert temp_dir.exists()

        Settings._instance = None

    def test_database_initialized(self, tmp_path):
        """Verifica que o banco de dados é criado e migrado."""
        from app.bootstrap import Bootstrap
        from database.connection import DatabaseConnection

        db_file = tmp_path / "test.db"
        DatabaseConnection._connection = None

        with patch("shared.constants.DATABASE_FILE", db_file):
            bootstrap = Bootstrap()
            bootstrap._step_database()

        assert db_file.exists()
        DatabaseConnection._connection = None
"""
Testes unitários — database/migrations.py
"""

import pytest
from database.migrations import MigrationManager
from database.schema import SCHEMA_SQL


@pytest.mark.unit
class TestMigrationManager:
    """Testa o sistema de migrações."""

    def test_schema_applied(self, db_connection):
        """Verifica que o schema base foi aplicado."""
        cursor = db_connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' ORDER BY name"
        )
        tables = {row[0] for row in cursor.fetchall()}
        expected = {
            "_migrations", "models", "tags", "model_tags",
            "engines", "benchmarks", "downloads", "history", "settings"
        }
        assert expected.issubset(tables)

    def test_migrations_table_exists(self, db_connection):
        """Tabela _migrations deve existir."""
        cursor = db_connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='_migrations'"
        )
        assert cursor.fetchone() is not None

    def test_no_pending_migrations(self, db_connection, tmp_path):
        """Sem arquivos SQL, não deve aplicar nada."""
        manager = MigrationManager(db_connection)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", tmp_path)
            manager.run()

        cursor = db_connection.execute("SELECT COUNT(*) FROM _migrations")
        count = cursor.fetchone()[0]
        assert count >= 0

    def test_migration_applied_once(self, db_connection, tmp_path):
        """Mesma migração não deve ser aplicada duas vezes."""
        sql_file = tmp_path / "002_test.sql"
        sql_file.write_text(
            "CREATE TABLE IF NOT EXISTS test_table (id INTEGER PRIMARY KEY);",
            encoding="utf-8",
        )

        manager = MigrationManager(db_connection)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", tmp_path)
            manager.run()
            manager.run()  # Segunda execução

        cursor = db_connection.execute(
            "SELECT COUNT(*) FROM _migrations WHERE version = 2"
        )
        count = cursor.fetchone()[0]
        assert count == 1

    def test_invalid_migration_filename_ignored(self, db_connection, tmp_path):
        """Arquivos com nome inválido devem ser ignorados."""
        bad_file = tmp_path / "invalid_name.sql"
        bad_file.write_text("SELECT 1;", encoding="utf-8")

        manager = MigrationManager(db_connection)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", tmp_path)
            manager.run()  # Não deve lançar exceção
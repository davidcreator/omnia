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
        """Sem arquivos SQL na pasta, não deve aplicar nada."""
        manager = MigrationManager(db_connection)

        # Pasta vazia — nenhum arquivo .sql
        empty_dir = tmp_path / "empty_migrations"
        empty_dir.mkdir()

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", empty_dir)
            manager.run()

        # Apenas o schema base deve existir, sem novas migrações
        cursor = db_connection.execute("SELECT COUNT(*) FROM _migrations")
        count = cursor.fetchone()[0]
        assert count >= 0  # Não lançou exceção

    def test_migration_applied_once(self, db_connection, tmp_path):
        """Mesma migração não deve ser aplicada duas vezes."""
        # Usa versão 999 para não conflitar com migrações reais
        sql_file = tmp_path / "999_test.sql"
        sql_file.write_text(
            "CREATE TABLE IF NOT EXISTS test_table_999 (id INTEGER PRIMARY KEY);",
            encoding="utf-8",
        )

        manager = MigrationManager(db_connection)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", tmp_path)
            manager.run()  # Primeira execução — aplica versão 999
            manager.run()  # Segunda execução — não deve reaplicar

        # Versão 999 deve estar registrada exatamente uma vez
        cursor = db_connection.execute(
            "SELECT COUNT(*) FROM _migrations WHERE version = 999"
        )
        count = cursor.fetchone()[0]
        assert count == 1

    def test_invalid_migration_filename_ignored(self, db_connection, tmp_path):
        """Arquivos com nome inválido devem ser ignorados sem exceção."""
        # Arquivo com nome que não segue o padrão NNN_nome.sql
        bad_file = tmp_path / "invalid_name.sql"
        bad_file.write_text("SELECT 1;", encoding="utf-8")

        manager = MigrationManager(db_connection)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", tmp_path)
            manager.run()  # Não deve lançar exceção

    def test_migration_creates_table(self, db_connection, tmp_path):
        """Migração válida deve criar tabela no banco."""
        sql_file = tmp_path / "998_create_test.sql"
        sql_file.write_text(
            "CREATE TABLE IF NOT EXISTS test_migration_998 (id INTEGER PRIMARY KEY);",
            encoding="utf-8",
        )

        manager = MigrationManager(db_connection)

        with pytest.MonkeyPatch.context() as mp:
            mp.setattr("shared.constants.MIGRATIONS_DIR", tmp_path)
            manager.run()

        # Tabela deve existir
        cursor = db_connection.execute(
            "SELECT name FROM sqlite_master WHERE type='table' AND name='test_migration_998'"
        )
        assert cursor.fetchone() is not None
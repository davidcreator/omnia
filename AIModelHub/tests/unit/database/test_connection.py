"""
Testes unitários — database/connection.py
"""

import sqlite3
import pytest
from unittest.mock import patch
from database.connection import DatabaseConnection


@pytest.mark.unit
class TestDatabaseConnection:
    """Testa a conexão com o banco de dados."""

    def test_connection_is_not_none(self, db_connection):
        assert db_connection is not None

    def test_connection_is_sqlite(self, db_connection):
        assert isinstance(db_connection, sqlite3.Connection)

    def test_get_returns_connection(self, db_connection):
        conn = DatabaseConnection.get()
        assert conn is db_connection

    def test_get_raises_without_init(self):
        """Deve lançar RuntimeError se não inicializado."""
        original = DatabaseConnection._connection
        DatabaseConnection._connection = None
        try:
            with pytest.raises(RuntimeError, match="não inicializado"):
                DatabaseConnection.get()
        finally:
            DatabaseConnection._connection = original

    def test_wal_mode_enabled_file_db(self, tmp_path):
        """
        WAL mode só funciona em banco em arquivo, não em memória.
        Este teste cria sua própria conexão isolada em arquivo temporário.
        """
        db_file    = tmp_path / "test_wal.db"
        original   = DatabaseConnection._connection
        mode       = None

        # Limpa o singleton antes de começar
        DatabaseConnection._connection = None

        try:
            with patch("database.connection.DATABASE_FILE", db_file):
                db = DatabaseConnection()
                db.initialize()

                # Lê o modo enquanto a conexão ainda está ativa
                # ``initialize`` mantém a conexão na instância criada.
                conn = db._connection
                cursor = conn.execute("PRAGMA journal_mode;")
                mode   = cursor.fetchone()[0]

        finally:
            # Fecha a conexão criada pelo teste
            if 'conn' in locals() and conn is not None:
                conn.close()

            # Restaura o singleton para o estado anterior
            DatabaseConnection._connection = original

        # Assert FORA do finally — executado apenas se não houve exceção
        assert mode == "wal", f"Esperado 'wal', recebido '{mode}'"

    def test_foreign_keys_enabled(self, db_connection):
        cursor = db_connection.execute("PRAGMA foreign_keys;")
        enabled = cursor.fetchone()[0]
        assert enabled == 1

    def test_close_sets_none(self, db_connection):
        DatabaseConnection.close()
        assert DatabaseConnection._connection is None

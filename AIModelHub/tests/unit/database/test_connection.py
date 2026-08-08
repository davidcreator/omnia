"""
Testes unitários — database/connection.py
"""

import sqlite3
import pytest
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
        DatabaseConnection._connection = None
        with pytest.raises(RuntimeError):
            DatabaseConnection.get()

    def test_wal_mode_enabled(self, db_connection):
        cursor = db_connection.execute("PRAGMA journal_mode;")
        mode = cursor.fetchone()[0]
        assert mode == "wal"

    def test_foreign_keys_enabled(self, db_connection):
        cursor = db_connection.execute("PRAGMA foreign_keys;")
        enabled = cursor.fetchone()[0]
        assert enabled == 1

    def test_close_sets_none(self, db_connection):
        DatabaseConnection.close()
        assert DatabaseConnection._connection is None
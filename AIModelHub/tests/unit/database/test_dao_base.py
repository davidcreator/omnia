# tests/unit/database/test_dao_base.py
"""
Testes unitários do DAOBase revisado.
Usa banco SQLite em memória injetado no singleton.
"""
from __future__ import annotations

import json
import sqlite3
import pytest

from database.connection import DatabaseConnection
from database.dao_base import DAOBase


# ── DAO concreto mínimo para testes ───────────────────────────────────────

class _TestDAO(DAOBase):
    """DAO concreto mínimo usado exclusivamente nos testes."""

    def setup(self) -> None:
        """Cria tabela auxiliar para os testes."""
        self._conn.execute(
            """
            CREATE TABLE IF NOT EXISTS _dao_test (
                id      INTEGER PRIMARY KEY AUTOINCREMENT,
                name    TEXT NOT NULL,
                data    TEXT,
                value   INTEGER DEFAULT 0
            );
            """
        )
        self._conn.commit()

    def insert(self, name: str, data: str = None, value: int = 0) -> int:
        return self._execute_insert(
            "INSERT INTO _dao_test (name, data, value) VALUES (?, ?, ?);",
            (name, data, value),
        )

    def update_name(self, row_id: int, name: str) -> int:
        return self._execute(
            "UPDATE _dao_test SET name=? WHERE id=?;",
            (name, row_id),
        )

    def delete(self, row_id: int) -> int:
        return self._execute(
            "DELETE FROM _dao_test WHERE id=?;",
            (row_id,),
        )

    def get_one(self, row_id: int) -> dict | None:
        return self._fetch_one(
            "SELECT * FROM _dao_test WHERE id=?;",
            (row_id,),
        )

    def get_all(self) -> list[dict]:
        return self._fetch_all("SELECT * FROM _dao_test;")

    def count_all(self) -> int:
        return self._fetch_scalar("SELECT COUNT(*) FROM _dao_test;", default=0)

    def exists_by_name(self, name: str) -> bool:
        return self._exists("_dao_test", "name", name)

    def count_by_value(self, value: int) -> int:
        return self._count(
            "_dao_test", "WHERE value=?", (value,)
        )

    def insert_many(self, names: list[str]) -> int:
        return self._execute_many(
            "INSERT INTO _dao_test (name) VALUES (?);",
            [(n,) for n in names],
        )


# ── fixtures ───────────────────────────────────────────────────────────────

@pytest.fixture(autouse=True)
def reset_singleton():
    """Garante que o singleton é resetado entre os testes."""
    DatabaseConnection._connection = None
    yield
    DatabaseConnection._connection = None


@pytest.fixture
def db() -> sqlite3.Connection:
    """Banco SQLite em memória injetado no singleton."""
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys=ON;")
    DatabaseConnection._connection = conn
    yield conn
    DatabaseConnection._connection = None
    conn.close()


@pytest.fixture
def dao(db: sqlite3.Connection) -> _TestDAO:
    """DAO concreto com tabela auxiliar criada."""
    d = _TestDAO()
    d.setup()
    return d


# ── inicialização ──────────────────────────────────────────────────────────

class TestDAOBaseInit:
    def test_init_stores_connection(self, db):
        dao = _TestDAO()
        assert dao._conn is db

    def test_init_raises_without_connection(self):
        DatabaseConnection._connection = None
        with pytest.raises(RuntimeError):
            _TestDAO()

    def test_conn_is_sqlite_connection(self, db):
        dao = _TestDAO()
        assert isinstance(dao._conn, sqlite3.Connection)


# ── serialização JSON ─────────────────────────────────────────────────────

class TestSerializeJSON:
    def test_serializes_dict(self, dao):
        result = dao._serialize_json({"key": "value"})
        assert isinstance(result, str)
        assert json.loads(result) == {"key": "value"}

    def test_returns_none_for_empty_dict(self, dao):
        assert dao._serialize_json({}) is None

    def test_returns_none_for_none(self, dao):
        assert dao._serialize_json(None) is None

    def test_serializes_nested_dict(self, dao):
        data = {"a": {"b": [1, 2, 3]}, "c": True}
        result = dao._serialize_json(data)
        assert json.loads(result) == data

    def test_preserves_unicode(self, dao):
        data = {"nome": "Modelão", "desc": "Português"}
        result = dao._serialize_json(data)
        assert "Modelão" in result

    def test_uses_compact_separators(self, dao):
        result = dao._serialize_json({"a": 1})
        assert " " not in result  # sem espaços extras


class TestDeserializeJSON:
    def test_deserializes_valid_json(self, dao):
        result = dao._deserialize_json('{"key": "value"}')
        assert result == {"key": "value"}

    def test_returns_empty_dict_for_none(self, dao):
        assert dao._deserialize_json(None) == {}

    def test_returns_empty_dict_for_empty_string(self, dao):
        assert dao._deserialize_json("") == {}

    def test_returns_empty_dict_for_invalid_json(self, dao):
        assert dao._deserialize_json("{invalid}") == {}

    def test_returns_empty_dict_for_non_dict_json(self, dao):
        assert dao._deserialize_json("[1, 2, 3]") == {}

    def test_returns_empty_dict_for_null_json(self, dao):
        assert dao._deserialize_json("null") == {}

    def test_roundtrip_preserves_data(self, dao):
        original = {
            "engine": "llama_cpp",
            "threads": 4,
            "tags": ["llm", "chat"],
            "nested": {"a": 1},
        }
        serialized = dao._serialize_json(original)
        restored = dao._deserialize_json(serialized)
        assert restored == original

    def test_roundtrip_preserves_unicode(self, dao):
        original = {"name": "Modelão 3", "desc": "Português"}
        restored = dao._deserialize_json(dao._serialize_json(original))
        assert restored == original


# ── conversão de rows ─────────────────────────────────────────────────────

class TestRowConversion:
    def test_row_to_dict_has_correct_keys(self, dao):
        dao.insert("row_test")
        result = dao.get_one(1)
        assert set(result.keys()) == {"id", "name", "data", "value"}

    def test_row_to_dict_has_correct_values(self, dao):
        dao.insert("alice", data="payload", value=42)
        result = dao.get_one(1)
        assert result["name"] == "alice"
        assert result["data"] == "payload"
        assert result["value"] == 42

    def test_fetch_all_returns_list_of_dicts(self, dao):
        dao.insert("a")
        dao.insert("b")
        results = dao.get_all()
        assert all(isinstance(r, dict) for r in results)

    def test_no_global_row_factory_side_effect(self, dao, db):
        """
        Garante que _fetch_one e _fetch_all não alteram
        a row_factory global da conexão.
        """
        original_factory = db.row_factory
        dao.insert("test")
        dao.get_one(1)
        dao.get_all()
        assert db.row_factory == original_factory


# ── _execute ──────────────────────────────────────────────────────────────

class TestExecute:
    def test_execute_update_returns_rowcount(self, dao):
        dao.insert("a")
        dao.insert("b")
        affected = dao._execute(
            "UPDATE _dao_test SET value=1;"
        )
        assert affected == 2

    def test_execute_delete_removes_row(self, dao, db):
        dao.insert("to_delete")
        dao.delete(1)
        row = db.execute(
            "SELECT * FROM _dao_test WHERE id=1;"
        ).fetchone()
        assert row is None

    def test_execute_commits_automatically(self, dao, db):
        dao.insert("committed")
        dao._execute(
            "UPDATE _dao_test SET name='updated' WHERE id=1;"
        )
        row = db.execute(
            "SELECT name FROM _dao_test WHERE id=1;"
        ).fetchone()
        assert row[0] == "updated"

    def test_execute_raises_on_invalid_sql(self, dao):
        with pytest.raises(Exception):
            dao._execute("INVALID SQL @@@@;")

    def test_execute_rollback_on_error(self, dao, db):
        dao.insert("safe")
        with pytest.raises(Exception):
            dao._execute(
                "UPDATE _dao_test SET name=? WHERE id=?;",
                ("ok",),  # params incorretos — causa erro
            )
        # linha original deve permanecer
        row = db.execute(
            "SELECT name FROM _dao_test WHERE id=1;"
        ).fetchone()
        assert row[0] == "safe"


# ── _execute_insert ───────────────────────────────────────────────────────

class TestExecuteInsert:
    def test_returns_lastrowid(self, dao):
        row_id = dao.insert("first")
        assert row_id == 1

    def test_increments_lastrowid(self, dao):
        id1 = dao.insert("first")
        id2 = dao.insert("second")
        assert id2 == id1 + 1

    def test_row_is_persisted(self, dao, db):
        dao.insert("persisted", data="payload")
        row = db.execute(
            "SELECT name, data FROM _dao_test WHERE id=1;"
        ).fetchone()
        assert row[0] == "persisted"
        assert row[1] == "payload"

    def test_raises_on_constraint_violation(self, dao):
        with pytest.raises(Exception):
            dao._execute_insert(
                "INSERT INTO _dao_test (name) VALUES (?);",
                (None,),  # NOT NULL violation
            )


# ── _execute_many ─────────────────────────────────────────────────────────

class TestExecuteMany:
    def test_inserts_multiple_rows(self, dao, db):
        dao.insert_many(["alpha", "beta", "gamma"])
        count = db.execute(
            "SELECT COUNT(*) FROM _dao_test;"
        ).fetchone()[0]
        assert count == 3

    def test_returns_rowcount(self, dao):
        affected = dao.insert_many(["a", "b", "c"])
        assert affected == 3

    def test_empty_list_returns_zero(self, dao):
        result = dao._execute_many(
            "INSERT INTO _dao_test (name) VALUES (?);", []
        )
        assert result == 0

    def test_rollback_on_partial_failure(self, dao, db):
        """
        Se qualquer linha falhar, nenhuma deve ser inserida.
        """
        with pytest.raises(Exception):
            dao._execute_many(
                "INSERT INTO _dao_test (name) VALUES (?);",
                [("valid",), (None,)],  # None viola NOT NULL
            )
        count = db.execute(
            "SELECT COUNT(*) FROM _dao_test;"
        ).fetchone()[0]
        assert count == 0


# ── _fetch_one ────────────────────────────────────────────────────────────

class TestFetchOne:
    def test_returns_dict_when_found(self, dao):
        dao.insert("found")
        result = dao.get_one(1)
        assert isinstance(result, dict)
        assert result["name"] == "found"

    def test_returns_none_when_not_found(self, dao):
        result = dao.get_one(9999)
        assert result is None

    def test_returns_correct_columns(self, dao):
        dao.insert("col_test", data="d", value=7)
        result = dao.get_one(1)
        assert result["id"] == 1
        assert result["name"] == "col_test"
        assert result["data"] == "d"
        assert result["value"] == 7

    def test_handles_null_fields(self, dao):
        dao.insert("with_null")  # data=None
        result = dao.get_one(1)
        assert result["data"] is None


# ── _fetch_all ────────────────────────────────────────────────────────────

class TestFetchAll:
    def test_returns_empty_list_when_no_rows(self, dao):
        assert dao.get_all() == []

    def test_returns_all_rows(self, dao):
        dao.insert("a")
        dao.insert("b")
        dao.insert("c")
        result = dao.get_all()
        assert len(result) == 3

    def test_all_items_are_dicts(self, dao):
        dao.insert("x")
        dao.insert("y")
        result = dao.get_all()
        assert all(isinstance(r, dict) for r in result)

    def test_filter_with_params(self, dao):
        dao.insert("match", value=1)
        dao.insert("match", value=1)
        dao.insert("no_match", value=2)
        result = dao._fetch_all(
            "SELECT * FROM _dao_test WHERE value=?;", (1,)
        )
        assert len(result) == 2
        assert all(r["value"] == 1 for r in result)


# ── _fetch_scalar ─────────────────────────────────────────────────────────

class TestFetchScalar:
    def test_count_empty_table(self, dao):
        result = dao.count_all()
        assert result == 0

    def test_count_with_rows(self, dao):
        dao.insert("a")
        dao.insert("b")
        assert dao.count_all() == 2

    def test_returns_default_when_aggregate_returns_null(self, dao):
        """
        SQLite retorna (None,) para MAX/MIN/SUM sem dados.
        _fetch_scalar deve tratar NULL como ausência e retornar default.
        """
        result = dao._fetch_scalar(
            "SELECT MAX(value) FROM _dao_test WHERE value > 9999;",
            default=-1,
        )
        assert result == -1

    def test_returns_default_when_no_rows(self, dao):
        """
        Queries não-agregadas sem resultado retornam None da row.
        _fetch_scalar deve retornar default neste caso.
        """
        result = dao._fetch_scalar(
            "SELECT value FROM _dao_test WHERE id = 9999;",
            default=-1,
        )
        assert result == -1

    def test_returns_none_as_default_when_not_specified(self, dao):
        """Default padrão é None quando não especificado."""
        result = dao._fetch_scalar(
            "SELECT MAX(value) FROM _dao_test WHERE value > 9999;"
        )
        assert result is None

    def test_returns_first_column_only(self, dao):
        dao.insert("scalar", value=42)
        result = dao._fetch_scalar(
            "SELECT value FROM _dao_test WHERE id=1;"
        )
        assert result == 42

    def test_sum_of_values(self, dao):
        dao.insert("a", value=10)
        dao.insert("b", value=20)
        dao.insert("c", value=30)
        result = dao._fetch_scalar(
            "SELECT SUM(value) FROM _dao_test;"
        )
        assert result == 60

    def test_sum_returns_default_when_no_rows(self, dao):
        """SUM de tabela vazia retorna NULL no SQLite."""
        result = dao._fetch_scalar(
            "SELECT SUM(value) FROM _dao_test;",
            default=0,
        )
        assert result == 0

    def test_count_returns_zero_not_default(self, dao):
        """
        COUNT(*) NUNCA retorna NULL — retorna 0 para tabela vazia.
        Neste caso o default NÃO deve ser usado.
        """
        result = dao._fetch_scalar(
            "SELECT COUNT(*) FROM _dao_test;",
            default=-1,
        )
        assert result == 0   # COUNT retornou 0, não NULL
        assert result != -1  # default não foi usado


# ── _exists ───────────────────────────────────────────────────────────────

class TestExists:
    def test_returns_true_when_exists(self, dao):
        dao.insert("alice")
        assert dao.exists_by_name("alice") is True

    def test_returns_false_when_not_exists(self, dao):
        assert dao.exists_by_name("ghost") is False

    def test_returns_false_after_delete(self, dao):
        dao.insert("temp")
        dao.delete(1)
        assert dao.exists_by_name("temp") is False

    def test_case_sensitive(self, dao):
        dao.insert("Alice")
        assert dao.exists_by_name("alice") is False
        assert dao.exists_by_name("Alice") is True


# ── _count ────────────────────────────────────────────────────────────────

class TestCount:
    def test_count_empty_table(self, dao):
        assert dao._count("_dao_test") == 0

    def test_count_all_rows(self, dao):
        dao.insert("a")
        dao.insert("b")
        assert dao._count("_dao_test") == 2

    def test_count_with_filter(self, dao):
        dao.insert("a", value=1)
        dao.insert("b", value=1)
        dao.insert("c", value=2)
        assert dao.count_by_value(1) == 2
        assert dao.count_by_value(2) == 1
        assert dao.count_by_value(99) == 0


# ── _transaction ──────────────────────────────────────────────────────────

class TestTransaction:
    def test_commits_on_success(self, dao, db):
        with dao._transaction():
            dao._conn.execute(
                "INSERT INTO _dao_test (name) VALUES ('tx_ok');"
            )
        row = db.execute(
            "SELECT name FROM _dao_test WHERE name='tx_ok';"
        ).fetchone()
        assert row is not None
        assert row[0] == "tx_ok"

    def test_rollback_on_exception(self, dao, db):
        with pytest.raises(RuntimeError):
            with dao._transaction():
                dao._conn.execute(
                    "INSERT INTO _dao_test (name) VALUES ('will_rollback');"
                )
                raise RuntimeError("Simulated failure")

        row = db.execute(
            "SELECT * FROM _dao_test WHERE name='will_rollback';"
        ).fetchone()
        assert row is None

    def test_multiple_inserts_atomic(self, dao, db):
        """Todas as inserções dentro da transação são atômicas."""
        with dao._transaction():
            dao._conn.execute(
                "INSERT INTO _dao_test (name) VALUES ('part1');"
            )
            dao._conn.execute(
                "INSERT INTO _dao_test (name) VALUES ('part2');"
            )
            dao._conn.execute(
                "INSERT INTO _dao_test (name) VALUES ('part3');"
            )

        count = db.execute(
            "SELECT COUNT(*) FROM _dao_test;"
        ).fetchone()[0]
        assert count == 3

    def test_partial_rollback_atomic(self, dao, db):
        """Se uma operação falhar, nenhuma deve persistir."""
        with pytest.raises(Exception):
            with dao._transaction():
                dao._conn.execute(
                    "INSERT INTO _dao_test (name) VALUES ('ok1');"
                )
                dao._conn.execute(
                    "INSERT INTO _dao_test (name) VALUES ('ok2');"
                )
                raise ValueError("Simulated mid-transaction failure")

        count = db.execute(
            "SELECT COUNT(*) FROM _dao_test;"
        ).fetchone()[0]
        assert count == 0

    def test_reraises_original_exception(self, dao):
        with pytest.raises(ValueError, match="original error"):
            with dao._transaction():
                raise ValueError("original error")
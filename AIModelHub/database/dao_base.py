# database/dao_base.py
"""
DAO Base — Classe abstrata que padroniza o acesso ao banco.

Todos os DAOs herdam desta classe para garantir consistência
de conexão, serialização, execução e tratamento de erros.

Correções em relação à versão anterior:
- self._conn usado em todos os métodos (sem chamar get() repetidamente)
- row_factory configurada por cursor, não na conexão global
- _execute_insert separado para retornar lastrowid
- Suporte a transações explícitas com rollback automático
- _fetch_one e _fetch_all consistentes e sem efeitos colaterais
"""

from __future__ import annotations

import json
from abc import ABC
from contextlib import contextmanager
from typing import Any, Generator, Optional

from loguru import logger

from database.connection import DatabaseConnection


class DAOBase(ABC):
    """
    Classe base para todos os Data Access Objects.

    Fornece:
    - Acesso à conexão singleton via self._conn
    - Helpers de serialização/deserialização JSON
    - Métodos padronizados de execução (escrita e leitura)
    - Gerenciamento de transações com rollback automático
    - Conversão de rows para dicts sem alterar row_factory global
    """

    def __init__(self) -> None:
        """Inicializa o DAO obtendo a conexão singleton."""
        self._conn = DatabaseConnection.get()

    # ──────────────────────────────────────────────────────────────────────
    # Helpers de JSON
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _serialize_json(data: dict[str, Any] | None) -> Optional[str]:
        """
        Serializa um dicionário para string JSON.

        Retorna None se o dicionário for vazio ou None,
        evitando armazenar '{}' ou 'null' no banco.
        """
        if not data:
            return None
        try:
            return json.dumps(data, ensure_ascii=False, separators=(",", ":"))
        except (TypeError, ValueError) as error:
            logger.error(f"Erro ao serializar JSON: {error}")
            return None

    @staticmethod
    def _deserialize_json(raw: Optional[str]) -> dict[str, Any]:
        """
        Deserializa uma string JSON para dicionário.

        Retorna {} se a string for None, vazia ou inválida.
        Nunca lança exceção — erros são logados e retornam {}.
        """
        if not raw:
            return {}
        try:
            result = json.loads(raw)
            if not isinstance(result, dict):
                logger.warning(
                    f"JSON deserializado não é um dict: {type(result).__name__}"
                )
                return {}
            return result
        except (json.JSONDecodeError, TypeError) as error:
            logger.error(f"Erro ao deserializar JSON: {error}")
            return {}

    # ──────────────────────────────────────────────────────────────────────
    # Helpers de conversão de rows
    # ──────────────────────────────────────────────────────────────────────

    @staticmethod
    def _row_to_dict(cursor, row: tuple) -> dict[str, Any]:
        """
        Converte uma row de resultado em dicionário.

        Usa os nomes das colunas do cursor sem alterar
        row_factory na conexão global.
        """
        columns = [description[0] for description in cursor.description]
        return dict(zip(columns, row))

    def _rows_to_dicts(
        self, cursor, rows: list[tuple]
    ) -> list[dict[str, Any]]:
        """Converte uma lista de rows em lista de dicionários."""
        if not rows:
            return []
        columns = [description[0] for description in cursor.description]
        return [dict(zip(columns, row)) for row in rows]

    # ──────────────────────────────────────────────────────────────────────
    # Execução — escrita
    # ──────────────────────────────────────────────────────────────────────

    def _execute(self, query: str, params: tuple = ()) -> int:
        """
        Executa uma query de escrita (UPDATE, DELETE).

        Retorna o número de linhas afetadas.
        Faz commit automático em caso de sucesso.
        Faz rollback automático em caso de erro.
        """
        try:
            cursor = self._conn.execute(query, params)
            self._conn.commit()
            return cursor.rowcount
        except Exception as error:
            self._conn.rollback()
            logger.error(f"Erro na execução: {error}")
            logger.debug(f"Query: {query!r}")
            logger.debug(f"Params: {params!r}")
            raise

    def _execute_insert(self, query: str, params: tuple = ()) -> int:
        """
        Executa uma query INSERT.

        Retorna o lastrowid (id da linha inserida).
        Útil para tabelas com INTEGER PRIMARY KEY AUTOINCREMENT.
        Faz rollback automático em caso de erro.
        """
        try:
            cursor = self._conn.execute(query, params)
            self._conn.commit()
            return cursor.lastrowid
        except Exception as error:
            self._conn.rollback()
            logger.error(f"Erro no INSERT: {error}")
            logger.debug(f"Query: {query!r}")
            logger.debug(f"Params: {params!r}")
            raise

    def _execute_many(
        self, query: str, params_list: list[tuple]
    ) -> int:
        """
        Executa a mesma query para múltiplos conjuntos de parâmetros.

        Retorna o número total de linhas afetadas.
        Usa executemany para melhor performance em batch.
        Faz rollback automático se qualquer linha falhar.
        """
        if not params_list:
            return 0
        try:
            cursor = self._conn.executemany(query, params_list)
            self._conn.commit()
            return cursor.rowcount
        except Exception as error:
            self._conn.rollback()
            logger.error(f"Erro no executemany: {error}")
            logger.debug(f"Query: {query!r}")
            logger.debug(f"Total params: {len(params_list)}")
            raise

    # ──────────────────────────────────────────────────────────────────────
    # Execução — leitura
    # ──────────────────────────────────────────────────────────────────────

    def _fetch_one(
        self, query: str, params: tuple = ()
    ) -> Optional[dict[str, Any]]:
        """
        Executa uma query de leitura e retorna uma linha como dict.

        Retorna None se nenhuma linha for encontrada.
        Não altera row_factory da conexão global.
        """
        try:
            cursor = self._conn.execute(query, params)
            row = cursor.fetchone()
            if row is None:
                return None
            return self._row_to_dict(cursor, row)
        except Exception as error:
            logger.error(f"Erro na consulta (fetch_one): {error}")
            logger.debug(f"Query: {query!r}")
            logger.debug(f"Params: {params!r}")
            raise

    def _fetch_all(
        self, query: str, params: tuple = ()
    ) -> list[dict[str, Any]]:
        """
        Executa uma query de leitura e retorna todas as linhas como dicts.

        Retorna lista vazia se nenhuma linha for encontrada.
        Não altera row_factory da conexão global.
        """
        try:
            cursor = self._conn.execute(query, params)
            rows = cursor.fetchall()
            return self._rows_to_dicts(cursor, rows)
        except Exception as error:
            logger.error(f"Erro na consulta (fetch_all): {error}")
            logger.debug(f"Query: {query!r}")
            logger.debug(f"Params: {params!r}")
            raise

    def _fetch_scalar(
        self, query: str, params: tuple = (), default: Any = None
    ) -> Any:
        """
        Executa uma query e retorna o valor da primeira coluna
        da primeira linha.

        Útil para COUNT(*), MAX(), SUM(), EXISTS(), etc.
        Retorna `default` se nenhuma linha for encontrada
        OU se o valor retornado for NULL.

        Nota sobre agregações SQLite:
            SELECT MAX(x) FROM t WHERE x > 9999  →  retorna (None,)
            SELECT COUNT(*) FROM t               →  retorna (0,)
            Ambos retornam uma linha — o NULL é tratado como ausência.

        Exemplo:
            count = self._fetch_scalar("SELECT COUNT(*) FROM models;")
            exists = bool(self._fetch_scalar(
                "SELECT COUNT(*) FROM models WHERE id=?;", (model_id,)
            ))
        """
        try:
            cursor = self._conn.execute(query, params)
            row = cursor.fetchone()

            # row is None  → nenhuma linha retornada (raro em agregações)
            # row[0] is None → linha retornada mas valor é NULL
            #                  (comum em MAX/MIN/SUM sem dados)
            if row is None or row[0] is None:
                return default

            return row[0]

        except Exception as error:
            logger.error(f"Erro na consulta (fetch_scalar): {error}")
            logger.debug(f"Query: {query!r}")
            logger.debug(f"Params: {params!r}")
            raise

    # ──────────────────────────────────────────────────────────────────────
    # Gerenciamento de transações
    # ──────────────────────────────────────────────────────────────────────

    @contextmanager
    def _transaction(self) -> Generator[None, None, None]:
        """
        Context manager para transações explícitas com rollback automático.

        Agrupa múltiplas operações em uma única transação atômica.
        Faz commit se todas as operações tiverem sucesso.
        Faz rollback se qualquer operação falhar.

        Uso:
            with self._transaction():
                self._execute("INSERT INTO models ...")
                self._execute("INSERT INTO model_tags ...")
                self._execute("INSERT INTO history ...")
            # commit automático aqui

        Nota: dentro do bloco, NÃO chame commit() manualmente.
        Os métodos _execute* fazem commit individual; use
        _transaction() quando precisar de atomicidade entre
        múltiplas operações.
        """
        try:
            self._conn.execute("BEGIN;")
            yield
            self._conn.commit()
            logger.debug("Transação concluída com sucesso.")
        except Exception as error:
            self._conn.rollback()
            logger.error(f"Transação revertida: {error}")
            raise

    # ──────────────────────────────────────────────────────────────────────
    # Helpers de validação
    # ──────────────────────────────────────────────────────────────────────

    def _exists(self, table: str, column: str, value: Any) -> bool:
        """
        Verifica se existe ao menos uma linha com o valor especificado.

        Uso:
            if self._exists("models", "id", model_id):
                ...
        """
        count = self._fetch_scalar(
            f"SELECT COUNT(*) FROM {table} WHERE {column} = ?;",
            (value,),
            default=0,
        )
        return count > 0

    def _count(self, table: str, where: str = "", params: tuple = ()) -> int:
        """
        Retorna a contagem de linhas de uma tabela.

        Uso:
            total = self._count("models")
            ready = self._count("models", "WHERE status='ready'")
        """
        clause = f" {where}" if where else ""
        result = self._fetch_scalar(
            f"SELECT COUNT(*) FROM {table}{clause};",
            params,
            default=0,
        )
        return int(result)
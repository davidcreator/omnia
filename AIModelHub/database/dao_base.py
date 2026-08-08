"""
DAO Base — Classe abstrata que padroniza o acesso ao banco.
Todos os DAOs herdam desta classe para garantir consistência.
"""

from __future__ import annotations

import json
from abc import ABC
from typing import Any, Optional

from loguru import logger
from database.connection import DatabaseConnection


class DAOBase(ABC):
    """
    Classe base para todos os Data Access Objects.
    Fornece helpers comuns para serialização e conexão.
    """

    def __init__(self) -> None:
        """Inicializa o DAO com a conexão singleton."""
        self._conn = DatabaseConnection.get()

    # ─────────────────────────────────────────
    # Helpers de JSON
    # ─────────────────────────────────────────

    @staticmethod
    def _serialize_json(data: dict[str, Any]) -> Optional[str]:
        """Serializa um dicionário para string JSON."""
        if not data:
            return None
        try:
            return json.dumps(data, ensure_ascii=False)
        except (TypeError, ValueError) as error:
            logger.error(f"Erro ao serializar JSON: {error}")
            return None

    @staticmethod
    def _deserialize_json(raw: Optional[str]) -> dict[str, Any]:
        """Deserializa uma string JSON para dicionário."""
        if not raw:
            return {}
        try:
            return json.loads(raw)
        except (json.JSONDecodeError, TypeError) as error:
            logger.error(f"Erro ao deserializar JSON: {error}")
            return {}

    # ─────────────────────────────────────────
    # Helpers de execução
    # ─────────────────────────────────────────

    @staticmethod
    def _execute(query: str, params: tuple = ()) -> int:
        """
        Executa uma query de escrita (INSERT, UPDATE, DELETE).
        Retorna o número de linhas afetadas.
        """
        try:
            cursor = DatabaseConnection.get().execute(query, params)
            DatabaseConnection.get().commit()
            return cursor.rowcount
        except Exception as error:
            logger.error(f"Erro na execução: {error}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise

    @staticmethod
    def _fetch_one(query: str, params: tuple = ()) -> Optional[dict[str, Any]]:
        """Executa uma query de leitura e retorna uma linha como dict."""
        try:
            DatabaseConnection.get().row_factory = None
            cursor = DatabaseConnection.get().execute(query, params)
            columns = [description[0] for description in cursor.description]
            row = cursor.fetchone()
            
            if row is None:
                return None
                
            return dict(zip(columns, row))
        except Exception as error:
            logger.error(f"Erro na consulta: {error}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise

    @staticmethod
    def _fetch_all(query: str, params: tuple = ()) -> list[dict[str, Any]]:
        """Executa uma query de leitura e retorna todas as linhas como dicts."""
        try:
            cursor = DatabaseConnection.get().execute(query, params)
            columns = [description[0] for description in cursor.description]
            rows = cursor.fetchall()
            
            return [dict(zip(columns, row)) for row in rows]
        except Exception as error:
            logger.error(f"Erro na consulta: {error}")
            logger.error(f"Query: {query}")
            logger.error(f"Params: {params}")
            raise
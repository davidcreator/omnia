"""
DAO de Histórico — Acesso à tabela `history`.
Registra e consulta ações do usuário no sistema.
"""

from __future__ import annotations

from datetime import datetime, timedelta, UTC
from typing import Any, Optional

from loguru import logger
from database.dao_base import DAOBase


class DAOHistory(DAOBase):
    """
    Data Access Object para a tabela `history`.
    
    Registra ações do usuário como carregar modelo,
    executar inferência, executar benchmark, etc.
    """

    TABLE = "history"

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def add(
        self,
        action: str,
        model_id: Optional[str] = None,
        engine_id: Optional[str] = None,
        details: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Adiciona um novo registro de histórico.
        
        Args:
            action: Tipo de ação (load, inference, benchmark, etc.)
            model_id: ID do modelo (opcional)
            engine_id: ID da engine (opcional)
            details: Dicionário com dados adicionais
        
        Returns:
            int: ID do registro criado
        """
        self._execute(
            f"""
            INSERT INTO {self.TABLE}
            (model_id, engine_id, action, details, created_at)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                model_id,
                engine_id,
                action,
                self._serialize_json(details),
                datetime.now(UTC).isoformat(),
            ),
        )

        row = self._fetch_one(
            f"SELECT id FROM {self.TABLE} ORDER BY id DESC LIMIT 1",
        )
        return row["id"] if row else 0

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_recent(self, limit: int = 50) -> list[dict[str, Any]]:
        """Retorna os registros mais recentes."""
        rows = self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (limit,),
        )
        return self._prepare_rows(rows)

    def get_by_action(self, action: str, limit: int = 50) -> list[dict[str, Any]]:
        """Retorna registros filtrados por ação."""
        rows = self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE action = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (action, limit),
        )
        return self._prepare_rows(rows)

    def get_by_model(self, model_id: str, limit: int = 50) -> list[dict[str, Any]]:
        """Retorna registros de um modelo específico."""
        rows = self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE model_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (model_id, limit),
        )
        return self._prepare_rows(rows)

    def get_by_date_range(
        self,
        start_date: datetime,
        end_date: datetime,
    ) -> list[dict[str, Any]]:
        """Retorna registros entre duas datas."""
        rows = self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE created_at BETWEEN ? AND ?
            ORDER BY created_at DESC
            """,
            (start_date.isoformat(), end_date.isoformat()),
        )
        return self._prepare_rows(rows)

    def get_by_days(self, days: int) -> list[dict[str, Any]]:
        """Retorna registros dos últimos N dias."""
        start_date = datetime.now(UTC) - timedelta(days=days)
        return self.get_by_date_range(start_date, datetime.now(UTC))

    # ─────────────────────────────────────────
    # Agregações
    # ─────────────────────────────────────────

    def count(self, action: Optional[str] = None) -> int:
        """Retorna o total de registros, opcionalmente filtrado por ação."""
        if action:
            row = self._fetch_one(
                f"SELECT COUNT(*) as total FROM {self.TABLE} WHERE action = ?",
                (action,),
            )
        else:
            row = self._fetch_one(f"SELECT COUNT(*) as total FROM {self.TABLE}")
        return row["total"] if row else 0

    def get_most_used_models(self, limit: int = 10) -> list[dict[str, Any]]:
        """Retorna os modelos mais usados."""
        return self._fetch_all(
            f"""
            SELECT model_id, COUNT(*) as usage_count
            FROM {self.TABLE}
            WHERE model_id IS NOT NULL
            GROUP BY model_id
            ORDER BY usage_count DESC
            LIMIT ?
            """,
            (limit,),
        )

    def get_most_frequent_actions(self, limit: int = 10) -> list[dict[str, Any]]:
        """Retorna as ações mais frequentes."""
        return self._fetch_all(
            f"""
            SELECT action, COUNT(*) as count
            FROM {self.TABLE}
            GROUP BY action
            ORDER BY count DESC
            LIMIT ?
            """,
            (limit,),
        )

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, history_id: int) -> bool:
        """Remove um registro pelo ID."""
        result = self._execute(
            f"DELETE FROM {self.TABLE} WHERE id = ?",
            (history_id,),
        )
        return result > 0

    def clear(self) -> None:
        """Remove todos os registros."""
        self._execute(f"DELETE FROM {self.TABLE}")
        logger.info("Histórico limpo.")

    def clear_before(self, date: datetime) -> int:
        """Remove registros anteriores a uma data."""
        return self._execute(
            f"DELETE FROM {self.TABLE} WHERE created_at < ?",
            (date.isoformat(),),
        )

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    def _prepare_rows(self, rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
        """Processa linhas para o formato de saída."""
        for row in rows:
            row["details"] = self._deserialize_json(row.get("details"))
        return rows
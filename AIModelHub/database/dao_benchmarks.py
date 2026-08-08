"""
DAO de Benchmarks — Acesso à tabela `benchmarks`.
Gerencia resultados de testes de performance.
"""

from __future__ import annotations

from datetime import datetime, UTC
from typing import Any, Optional

from loguru import logger
from database.dao_base import DAOBase


class DAOBenchmarks(DAOBase):
    """
    Data Access Object para a tabela `benchmarks`.
    
    Registra e consulta métricas de performance dos modelos
    executados em diferentes engines.
    """

    TABLE = "benchmarks"

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(
        self,
        model_id: str,
        engine_id: str,
        load_time_ms: Optional[float] = None,
        tokens_per_sec: Optional[float] = None,
        ram_usage_mb: Optional[float] = None,
        vram_usage_mb: Optional[float] = None,
        cpu_percent: Optional[float] = None,
        gpu_percent: Optional[float] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> int:
        """
        Cria um novo registro de benchmark.
        
        Returns:
            int: ID do benchmark criado
        """
        logger.debug(f"Criando benchmark: {model_id} / {engine_id}")

        self._execute(
            f"""
            INSERT INTO {self.TABLE}
            (model_id, engine_id, load_time_ms, tokens_per_sec,
             ram_usage_mb, vram_usage_mb, cpu_percent, gpu_percent,
             created_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                model_id, engine_id, load_time_ms, tokens_per_sec,
                ram_usage_mb, vram_usage_mb, cpu_percent, gpu_percent,
                datetime.now(UTC).isoformat(),
                self._serialize_json(metadata) if metadata else None,
            ),
        )

        # Retorna o ID do novo registro
        row = self._fetch_one(
            f"SELECT id FROM {self.TABLE} ORDER BY id DESC LIMIT 1",
        )
        return row["id"] if row else 0

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_by_id(self, benchmark_id: int) -> Optional[dict[str, Any]]:
        """Busca um benchmark pelo ID."""
        row = self._fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE id = ?",
            (benchmark_id,),
        )
        if row:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return row

    def get_by_model(self, model_id: str, limit: int = 20) -> list[dict[str, Any]]:
        """Retorna os benchmarks mais recentes de um modelo."""
        rows = self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE model_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (model_id, limit),
        )
        for row in rows:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return rows

    def get_by_engine(self, engine_id: str, limit: int = 20) -> list[dict[str, Any]]:
        """Retorna os benchmarks mais recentes de uma engine."""
        rows = self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE engine_id = ?
            ORDER BY created_at DESC
            LIMIT ?
            """,
            (engine_id, limit),
        )
        for row in rows:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return rows

    def get_latest(self, model_id: str, engine_id: str) -> Optional[dict[str, Any]]:
        """Retorna o benchmark mais recente para um modelo+engine."""
        row = self._fetch_one(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE model_id = ? AND engine_id = ?
            ORDER BY created_at DESC
            LIMIT 1
            """,
            (model_id, engine_id),
        )
        if row:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return row

    # ─────────────────────────────────────────
    # Métricas Agregadas
    # ─────────────────────────────────────────

    def get_average_by_model(self, model_id: str) -> dict[str, float]:
        """Retorna média das métricas para um modelo."""
        row = self._fetch_one(
            f"""
            SELECT 
                AVG(load_time_ms) as avg_load_time,
                AVG(tokens_per_sec) as avg_tokens_per_sec,
                AVG(ram_usage_mb) as avg_ram,
                AVG(vram_usage_mb) as avg_vram,
                AVG(cpu_percent) as avg_cpu,
                AVG(gpu_percent) as avg_gpu
            FROM {self.TABLE}
            WHERE model_id = ?
            """,
            (model_id,),
        )
        return row or {}

    def get_best_tokens_per_sec(self, model_id: str) -> Optional[dict[str, Any]]:
        """Retorna o melhor resultado de tokens/s para um modelo."""
        return self._fetch_one(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE model_id = ? AND tokens_per_sec = (
                SELECT MAX(tokens_per_sec) FROM {self.TABLE} WHERE model_id = ?
            )
            LIMIT 1
            """,
            (model_id, model_id),
        )

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, benchmark_id: int) -> bool:
        """Remove um benchmark pelo ID."""
        result = self._execute(
            f"DELETE FROM {self.TABLE} WHERE id = ?",
            (benchmark_id,),
        )
        return result > 0

    def delete_by_model(self, model_id: str) -> int:
        """Remove todos os benchmarks de um modelo."""
        return self._execute(
            f"DELETE FROM {self.TABLE} WHERE model_id = ?",
            (model_id,),
        )

    def count(self) -> int:
        """Retorna o total de benchmarks registrados."""
        row = self._fetch_one(f"SELECT COUNT(*) as total FROM {self.TABLE}")
        return row["total"] if row else 0
"""
DAO de Downloads — Acesso à tabela `downloads`.
Gerencia downloads de modelos em andamento e concluídos.
"""

from __future__ import annotations

from datetime import datetime
from typing import Any, Optional

from loguru import logger
from database.dao_base import DAOBase


class DAODownloads(DAOBase):
    """
    Data Access Object para a tabela `downloads`.
    
    Gerencia o ciclo de vida de downloads de modelos:
    - Fila de downloads pendentes
    - Progresso de downloads ativos
    - Histórico de downloads completos/falhos
    """

    TABLE = "downloads"

    STATUS_PENDING    = "pending"
    STATUS_ACTIVE     = "active"
    STATUS_COMPLETED  = "completed"
    STATUS_FAILED     = "failed"
    STATUS_CANCELLED  = "cancelled"

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(
        self,
        url: str,
        model_name: Optional[str] = None,
        size_bytes: Optional[int] = None,
    ) -> Optional[int]:
        """
        Cria um novo download na fila.
        
        Returns:
            int: ID do download criado, ou None em erro
        """
        self._execute(
            f"""
            INSERT INTO {self.TABLE}
            (url, model_name, status, progress, size_bytes, created_at)
            VALUES (?, ?, ?, 0, ?, ?)
            """,
            (
                url,
                model_name,
                self.STATUS_PENDING,
                size_bytes,
                datetime.utcnow().isoformat(),
            ),
        )

        row = self._fetch_one(
            f"SELECT id FROM {self.TABLE} ORDER BY id DESC LIMIT 1",
        )
        return row["id"] if row else None

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_by_id(self, download_id: int) -> Optional[dict[str, Any]]:
        """Retorna um download pelo ID."""
        row = self._fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE id = ?",
            (download_id,),
        )
        if row:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return row

    def get_by_status(self, status: str) -> list[dict[str, Any]]:
        """Retorna downloads por status."""
        return self._fetch_all(
            f"""
            SELECT * FROM {self.TABLE}
            WHERE status = ?
            ORDER BY created_at DESC
            """,
            (status,),
        )

    def get_pending(self) -> list[dict[str, Any]]:
        """Retorna downloads pendentes."""
        return self.get_by_status(self.STATUS_PENDING)

    def get_active(self) -> list[dict[str, Any]]:
        """Retorna downloads em andamento."""
        return self.get_by_status(self.STATUS_ACTIVE)

    def get_completed(self) -> list[dict[str, Any]]:
        """Retorna downloads concluídos."""
        return self.get_by_status(self.STATUS_COMPLETED)

    def get_failed(self) -> list[dict[str, Any]]:
        """Retorna downloads com falha."""
        return self.get_by_status(self.STATUS_FAILED)

    def get_all(self) -> list[dict[str, Any]]:
        """Retorna todos os downloads."""
        return self._fetch_all(
            f"SELECT * FROM {self.TABLE} ORDER BY created_at DESC"
        )

    # ─────────────────────────────────────────
    # UPDATE — Status
    # ─────────────────────────────────────────

    def update_status(self, download_id: int, status: str) -> bool:
        """Atualiza o status de um download."""
        self._execute(
            f"""
            UPDATE {self.TABLE}
            SET status = ?,
                completed_at = CASE WHEN ? IN ('completed', 'failed')
                    THEN ? ELSE completed_at END
            WHERE id = ?
            """,
            (status, status, datetime.utcnow().isoformat(), download_id),
        )

        logger.debug(f"Download {download_id} status → {status}")
        return True

    def mark_active(self, download_id: int) -> bool:
        """Marca um download como em andamento."""
        return self.update_status(download_id, self.STATUS_ACTIVE)

    def mark_completed(self, download_id: int) -> bool:
        """Marca um download como concluído."""
        return self.update_status(download_id, self.STATUS_COMPLETED)

    def mark_failed(self, download_id: int) -> bool:
        """Marca um download como falho."""
        return self.update_status(download_id, self.STATUS_FAILED)

    def mark_cancelled(self, download_id: int) -> bool:
        """Marca um download como cancelado."""
        return self.update_status(download_id, self.STATUS_CANCELLED)

    # ─────────────────────────────────────────
    # UPDATE — Progresso
    # ─────────────────────────────────────────

    def update_progress(self, download_id: int, progress: float) -> bool:
        """
        Atualiza o progresso de um download (0 a 100).
        
        Também atualiza o tamanho se houver mudanças.
        """
        progress = max(0.0, min(100.0, progress))

        self._execute(
            f"UPDATE {self.TABLE} SET progress = ? WHERE id = ?",
            (progress, download_id),
        )

        return True

    def update_size(self, download_id: int, size_bytes: int) -> bool:
        """Atualiza o tamanho total do download."""
        self._execute(
            f"UPDATE {self.TABLE} SET size_bytes = ? WHERE id = ?",
            (size_bytes, download_id),
        )
        return True

    # ─────────────────────────────────────────
    # Agregações
    # ─────────────────────────────────────────

    def count(self, status: Optional[str] = None) -> int:
        """Conta downloads, opcionalmente por status."""
        if status:
            row = self._fetch_one(
                f"SELECT COUNT(*) as total FROM {self.TABLE} WHERE status = ?",
                (status,),
            )
        else:
            row = self._fetch_one(f"SELECT COUNT(*) as total FROM {self.TABLE}")

        return row["total"] if row else 0

    def get_total_downloaded_bytes(self) -> int:
        """Retorna o total de bytes baixados."""
        row = self._fetch_one(
            f"""
            SELECT COALESCE(SUM(size_bytes), 0) as total
            FROM {self.TABLE}
            WHERE status = ?
            """,
            (self.STATUS_COMPLETED,),
        )
        return row["total"] if row else 0

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, download_id: int) -> bool:
        """Remove um download pelo ID."""
        result = self._execute(
            f"DELETE FROM {self.TABLE} WHERE id = ?",
            (download_id,),
        )
        return result > 0

    def clear_completed(self) -> int:
        """Remove todos os downloads concluídos."""
        return self._execute(
            f"DELETE FROM {self.TABLE} WHERE status = ?",
            (self.STATUS_COMPLETED,),
        )

    def clear_failed(self) -> int:
        """Remove todos os downloads falhos."""
        return self._execute(
            f"DELETE FROM {self.TABLE} WHERE status = ?",
            (self.STATUS_FAILED,),
        )
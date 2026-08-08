"""
DAO de Modelos — Acesso à tabela `models`.
Gerencia o CRUD completo dos modelos registrados.
"""

from __future__ import annotations

from datetime import datetime, UTC
from typing import Any, Optional

from loguru import logger
from database.dao_base import DAOBase


class DAOModels(DAOBase):
    """
    Data Access Object para a tabela `models`.

    Fornece operações CRUD completas para gerenciamento
    dos modelos de IA registrados no catálogo.
    """

    TABLE = "models"
    COLUMNS = [
        "id", "name", "format", "architecture", "quantization",
        "size_bytes", "path", "manufacturer", "description",
        "is_favorite", "created_at", "updated_at", "last_used_at",
        "metadata",
    ]

    # ─────────────────────────────────────────
    # CREATE
    # ─────────────────────────────────────────

    def create(
        self,
        model_id: str,
        name: str,
        format: str,
        path: str,
        architecture: Optional[str] = None,
        quantization: Optional[str] = None,
        size_bytes: Optional[int] = None,
        manufacturer: Optional[str] = None,
        description: Optional[str] = None,
        metadata: Optional[dict[str, Any]] = None,
    ) -> None:
        """
        Cria um novo registro de modelo no banco.

        Args:
            model_id    : ID único do modelo (ex: "llama3:8b")
            name        : Nome do modelo (ex: "Llama 3 8B")
            format      : Formato (huggingface, gguf, onnx, etc.)
            path        : Caminho completo do modelo
            architecture: Arquitetura (llama, mistral, etc.)
            quantization: Quantização (q4_0, q8_0, etc.)
            size_bytes  : Tamanho em bytes
            manufacturer: Fabricante/organização
            description : Descrição do modelo
            metadata    : Dicionário com dados extras
        """
        logger.debug(f"Criando modelo: {model_id} ({name})")

        now = datetime.now(UTC).isoformat()

        self._execute(
            f"""
            INSERT INTO {self.TABLE}
            (id, name, format, architecture, quantization,
             size_bytes, path, manufacturer, description,
             is_favorite, created_at, updated_at, last_used_at, metadata)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, 0, ?, ?, ?, ?)
            """,
            (
                model_id, name, format, architecture, quantization,
                size_bytes, path, manufacturer, description,
                now, now, None,
                self._serialize_json(metadata) if metadata else None,
            ),
        )
        logger.debug(f"Modelo criado com sucesso: {model_id}")

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get_by_id(self, model_id: str) -> Optional[dict[str, Any]]:
        """Busca um modelo pelo ID."""
        row = self._fetch_one(
            f"SELECT * FROM {self.TABLE} WHERE id = ?",
            (model_id,),
        )

        if row:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return row

    def get_all(self) -> list[dict[str, Any]]:
        """Retorna todos os modelos."""
        rows = self._fetch_all(
            f"SELECT * FROM {self.TABLE} ORDER BY name"
        )

        for row in rows:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return rows

    def get_by_format(self, format: str) -> list[dict[str, Any]]:
        """Retorna modelos filtrados por formato."""
        rows = self._fetch_all(
            f"SELECT * FROM {self.TABLE} WHERE format = ? ORDER BY name",
            (format,),
        )

        for row in rows:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return rows

    def get_favorites(self) -> list[dict[str, Any]]:
        """Retorna modelos marcados como favoritos."""
        rows = self._fetch_all(
            f"SELECT * FROM {self.TABLE} WHERE is_favorite = 1 ORDER BY name",
        )

        for row in rows:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return rows

    def search(
        self,
        query: str,
        format: Optional[str] = None,
        architecture: Optional[str] = None,
    ) -> list[dict[str, Any]]:
        """
        Busca modelos por nome, descrição ou fabricante.

        Args:
            query       : Texto para busca
            format      : Filtrar por formato (opcional)
            architecture: Filtrar por arquitetura (opcional)
        """
        sql = f"""
            SELECT * FROM {self.TABLE}
            WHERE (name LIKE ? OR description LIKE ? OR manufacturer LIKE ?)
        """
        params: list[Any] = [
            f"%{query}%", f"%{query}%", f"%{query}%",
        ]

        if format:
            sql += " AND format = ?"
            params.append(format)

        if architecture:
            sql += " AND architecture = ?"
            params.append(architecture)

        sql += " ORDER BY name"

        rows = self._fetch_all(sql, tuple(params))
        for row in rows:
            row["metadata"] = self._deserialize_json(row.get("metadata"))
        return rows

    # ─────────────────────────────────────────
    # UPDATE
    # ─────────────────────────────────────────

    def update(
        self,
        model_id: str,
        **changes: Any,
    ) -> bool:
        """
        Atualiza campos específicos de um modelo.

        Args:
            model_id: ID do modelo a atualizar
            **changes: Campos a serem atualizados

        Returns:
            bool: True se atualizado, False se não encontrado
        """
        if not changes:
            logger.warning(f"Nenhuma alteração fornecida para modelo {model_id}")
            return False

        allowed = set(self.COLUMNS) - {"id", "created_at"}
        updates = {k: v for k, v in changes.items() if k in allowed}

        if not updates:
            logger.warning(f"Nenhum campo válido para atualizar em {model_id}")
            return False

        # Metadados precisam serialização especial
        if "metadata" in updates and isinstance(updates["metadata"], dict):
            updates["metadata"] = self._serialize_json(updates["metadata"])

        # Sempre atualiza o timestamp
        updates["updated_at"] = datetime.now(UTC).isoformat()

        # Constrói a query dinamicamente
        set_clause = ", ".join(f"{key} = ?" for key in updates.keys())
        params     = list(updates.values()) + [model_id]

        result = self._execute(
            f"UPDATE {self.TABLE} SET {set_clause} WHERE id = ?",
            tuple(params),
        )

        return result > 0

    def mark_as_favorite(self, model_id: str, is_favorite: bool = True) -> bool:
        """Marca ou desmarca um modelo como favorito."""
        return self.update(model_id, is_favorite=1 if is_favorite else 0)

    def mark_as_used(self, model_id: str) -> None:
        """Registra o uso do modelo atualizando o timestamp."""
        now = datetime.now(UTC).isoformat()
        self._execute(
            f"UPDATE {self.TABLE} SET last_used_at = ?, updated_at = ? WHERE id = ?",
            (now, now, model_id),
        )

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, model_id: str) -> bool:
        """Remove um modelo pelo ID."""
        result = self._execute(
            f"DELETE FROM {self.TABLE} WHERE id = ?",
            (model_id,),
        )
        return result > 0

    # ─────────────────────────────────────────
    # CONTAGEM
    # ─────────────────────────────────────────

    def count(self) -> int:
        """Retorna o número total de modelos."""
        row = self._fetch_one(f"SELECT COUNT(*) as total FROM {self.TABLE}")
        return row["total"] if row else 0

    def count_favorites(self) -> int:
        """Retorna o número de modelos favoritos."""
        row = self._fetch_one(
            f"SELECT COUNT(*) as total FROM {self.TABLE} WHERE is_favorite = 1",
        )
        return row["total"] if row else 0

    def exists(self, model_id: str) -> bool:
        """Verifica se um modelo existe no banco."""
        row = self._fetch_one(
            f"SELECT id FROM {self.TABLE} WHERE id = ?",
            (model_id,),
        )
        return row is not None
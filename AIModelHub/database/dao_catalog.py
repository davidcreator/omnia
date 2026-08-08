"""
DAO do Catálogo — Gerencia a tabela `tags` e `model_tags`.
Operações de categorização e busca por tags.
"""

from __future__ import annotations

from typing import Any, Optional

from loguru import logger
from database.dao_base import DAOBase


class DAOCatalog(DAOBase):
    """
    Data Access Object para catálogo (tags e relações).
    
    Complementa o DAOModels focando na categorização
    através de tags e filtros combinados.
    """

    # ─────────────────────────────────────────
    # TAGS — CREATE / READ
    # ─────────────────────────────────────────

    def create_tag(self, name: str) -> Optional[int]:
        """
        Cria uma tag se não existir.
        Retorna o ID da tag (existente ou criada).
        """
        # Verifica se já existe
        existing = self._fetch_one(
            "SELECT id FROM tags WHERE name = ?",
            (name,),
        )
        if existing:
            return existing["id"]

        # Cria nova tag
        self._execute(
            "INSERT INTO tags (name) VALUES (?)",
            (name,),
        )

        # Retorna o ID da nova tag
        row = self._fetch_one(
            "SELECT id FROM tags WHERE name = ?",
            (name,),
        )
        return row["id"] if row else None

    def create_tags(self, names: list[str]) -> list[int]:
        """Cria várias tags de uma vez."""
        return [self.create_tag(name) for name in names]

    def get_all_tags(self) -> list[str]:
        """Retorna todas as tags."""
        rows = self._fetch_all("SELECT name FROM tags ORDER BY name")
        return [row["name"] for row in rows]

    def get_tag_id(self, name: str) -> Optional[int]:
        """Retorna o ID de uma tag pelo nome."""
        row = self._fetch_one(
            "SELECT id FROM tags WHERE name = ?",
            (name,),
        )
        return row["id"] if row else None

    def delete_tag(self, tag_id: int) -> bool:
        """Remove uma tag."""
        result = self._execute(
            "DELETE FROM tags WHERE id = ?",
            (tag_id,),
        )
        return result > 0

    # ─────────────────────────────────────────
    # MODEL_TAGS — Relação N:N
    # ─────────────────────────────────────────

    def add_tag_to_model(self, model_id: str, tag_name: str) -> bool:
        """
        Adiciona uma tag a um modelo.
        Cria a tag automaticamente se não existir.
        """
        # Garante que a tag existe
        tag_id = self.create_tag(tag_name)
        if not tag_id:
            return False

        try:
            self._execute(
                "INSERT OR IGNORE INTO model_tags (model_id, tag_id) VALUES (?, ?)",
                (model_id, tag_id),
            )
            return True
        except Exception as error:
            logger.error(f"Erro ao adicionar tag '{tag_name}' ao modelo {model_id}: {error}")
            return False

    def add_tags_to_model(self, model_id: str, tags: list[str]) -> int:
        """Adiciona várias tags a um modelo."""
        count = 0
        for tag in tags:
            if self.add_tag_to_model(model_id, tag):
                count += 1
        return count

    def remove_tag_from_model(self, model_id: str, tag_name: str) -> bool:
        """Remove uma tag de um modelo."""
        tag_id = self.get_tag_id(tag_name)
        if not tag_id:
            return False

        result = self._execute(
            "DELETE FROM model_tags WHERE model_id = ? AND tag_id = ?",
            (model_id, tag_id),
        )
        return result > 0

    def clear_model_tags(self, model_id: str) -> None:
        """Remove todas as tags de um modelo."""
        self._execute(
            "DELETE FROM model_tags WHERE model_id = ?",
            (model_id,),
        )

    def get_model_tags(self, model_id: str) -> list[str]:
        """Retorna todas as tags de um modelo."""
        rows = self._fetch_all(
            """
            SELECT t.name FROM tags t
            INNER JOIN model_tags mt ON t.id = mt.tag_id
            WHERE mt.model_id = ?
            ORDER BY t.name
            """,
            (model_id,),
        )
        return [row["name"] for row in rows]

    def get_models_by_tag(self, tag_name: str) -> list[str]:
        """Retorna IDs de modelos que possuem uma tag."""
        rows = self._fetch_all(
            """
            SELECT mt.model_id FROM model_tags mt
            INNER JOIN tags t ON t.id = mt.tag_id
            WHERE t.name = ?
            ORDER BY mt.model_id
            """,
            (tag_name,),
        )
        return [row["model_id"] for row in rows]

    # ─────────────────────────────────────────
    # BÚSQUEDA COMBINADA
    # ─────────────────────────────────────────

    def search_by_tags(self, tags: list[str], match_all: bool = True) -> list[str]:
        """
        Busca modelos que possuem as tags especificadas.
        
        Args:
            tags: Lista de tags para busca
            match_all: True para "AND" (todas as tags), False para "OR" (qualquer)
        
        Returns:
            Lista de IDs de modelos correspondentes
        """
        if not tags:
            return []

        if match_all:
            # Modelos que possuem TODAS as tags
            placeholders = ",".join("?" for _ in tags)
            rows = self._fetch_all(
                f"""
                SELECT mt.model_id
                FROM model_tags mt
                INNER JOIN tags t ON t.id = mt.tag_id
                WHERE t.name IN ({placeholders})
                GROUP BY mt.model_id
                HAVING COUNT(DISTINCT t.id) = ?
                """,
                (*tags, len(tags)),
            )
        else:
            # Modelos que possuem QUALQUER tag
            placeholders = ",".join("?" for _ in tags)
            rows = self._fetch_all(
                f"""
                SELECT DISTINCT mt.model_id
                FROM model_tags mt
                INNER JOIN tags t ON t.id = mt.tag_id
                WHERE t.name IN ({placeholders})
                """,
                tuple(tags),
            )

        return [row["model_id"] for row in rows]
"""
DAO de Configurações — Acesso à tabela `settings`.
Gerencia as configurações persistidas no banco.
"""

from __future__ import annotations

from datetime import datetime, UTC
from typing import Any, Optional

from loguru import logger
from database.dao_base import DAOBase


class DAOSettings(DAOBase):
    """
    Data Access Object para a tabela `settings`.
    
    Gerencia configurações persistidas que sobrescrevem
    os valores padrão do default.json.
    """

    TABLE = "settings"

    # ─────────────────────────────────────────
    # CREATE / UPDATE
    # ─────────────────────────────────────────

    def set(self, key: str, value: Any, category: str = "general") -> None:
        """
        Define/atualiza uma configuração.
        
        Args:
            key: Chave da configuração (ex: "workspace.path")
            value: Valor a ser armazenado
            category: Categoria da configuração
        """
        # Serializa valores complexos
        if isinstance(value, (dict, list, bool, int, float)):
            stored_value = self._serialize_json(value) if isinstance(value, dict) else str(value)
        else:
            stored_value = str(value)

        now = datetime.now(UTC).isoformat()

        # INSERT OR REPLACE (upsert)
        result = self._execute(
            f"""
            INSERT OR REPLACE INTO {self.TABLE}
            (key, value, category, updated_at)
            VALUES (?, ?, ?, ?)
            """,
            (key, stored_value, category, now),
        )
        logger.debug(f"Configuração salva: {key} = {value}")

    def set_many(self, settings: dict[str, Any], category: str = "general") -> None:
        """Define várias configurações de uma vez."""
        for key, value in settings.items():
            self.set(key, value, category)

    # ─────────────────────────────────────────
    # READ
    # ─────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retorna o valor de uma configuração.
        
        Args:
            key: Chave da configuração
            default: Valor padrão se a chave não existir
        """
        row = self._fetch_one(
            f"SELECT value FROM {self.TABLE} WHERE key = ?",
            (key,),
        )

        if row is None:
            return default

        raw_value = row["value"]

        # Tenta desserializar JSON
        parsed = self._deserialize_json(raw_value)
        if parsed:
            return parsed

        # Converte tipos básicos
        return self._convert_value(raw_value)

    def get_all(self) -> dict[str, Any]:
        """Retorna todas as configurações as um dicionário."""
        rows = self._fetch_all(
            f"SELECT key, value, category FROM {self.TABLE} ORDER BY category, key",
        )

        result: dict[str, Any] = {}
        for row in rows:
            result[row["key"]] = self._convert_value(row["value"])
        return result

    def get_by_category(self, category: str) -> dict[str, Any]:
        """Retorna configurações de uma categoria específica."""
        rows = self._fetch_all(
            f"SELECT key, value FROM {self.TABLE} WHERE category = ?",
            (category,),
        )

        return {
            row["key"]: self._convert_value(row["value"])
            for row in rows
        }

    # ─────────────────────────────────────────
    # DELETE
    # ─────────────────────────────────────────

    def delete(self, key: str) -> bool:
        """Remove uma configuração."""
        result = self._execute(
            f"DELETE FROM {self.TABLE} WHERE key = ?",
            (key,),
        )
        return result > 0

    def delete_category(self, category: str) -> int:
        """Remove todas as configurações de uma categoria."""
        result = self._execute(
            f"DELETE FROM {self.TABLE} WHERE category = ?",
            (category,),
        )
        return result

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    @staticmethod
    def _convert_value(raw: str) -> Any:
        """
        Converte uma string para o tipo mais apropriado.
        """
        # Booleano
        if raw.lower() == "true":
            return True
        if raw.lower() == "false":
            return False

        # Número
        try:
            if "." in raw:
                return float(raw)
            return int(raw) if raw.lstrip("-").isdigit() else raw
        except (ValueError, TypeError):
            return raw
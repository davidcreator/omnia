"""
Gerenciamento de configurações globais do AIModelHub.
Singleton — uma única instância durante toda a execução.
"""

import json
from pathlib import Path
from typing import Any

from loguru import logger
from shared.constants import CONFIG_DEFAULT_FILE, DEFAULT_WORKSPACE


class Settings:
    """
    Singleton que gerencia as configurações da aplicação.

    Hierarquia de prioridade (maior → menor):
    1. Runtime     — definidas em tempo de execução (banco de dados)
    2. Defaults    — carregadas do default.json
    3. Hardcoded   — fallback final embutido no código
    """

    _instance: "Settings | None" = None
    _defaults: dict[str, Any]   = {}
    _runtime:  dict[str, Any]   = {}

    def __new__(cls) -> "Settings":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    # ─────────────────────────────────────────
    # Inicialização
    # ─────────────────────────────────────────

    def load_defaults(self) -> None:
        """Carrega configurações padrão do default.json."""
        try:
            if CONFIG_DEFAULT_FILE.exists():
                with open(CONFIG_DEFAULT_FILE, encoding="utf-8") as f:
                    self._defaults = json.load(f)
                logger.debug(f"Configurações padrão carregadas → {CONFIG_DEFAULT_FILE}")
            else:
                logger.warning(
                    f"default.json não encontrado: {CONFIG_DEFAULT_FILE}. "
                    "Usando valores hardcoded."
                )
                self._defaults = self._hardcoded_defaults()

        except json.JSONDecodeError as error:
            logger.error(f"Erro ao ler default.json: {error}. Usando hardcoded.")
            self._defaults = self._hardcoded_defaults()

    def load_from_db(self, db_settings: dict[str, Any]) -> None:
        """
        Carrega configurações salvas no banco de dados.
        Chamado pelo bootstrap após inicialização do banco.
        """
        self._runtime = db_settings
        logger.debug(f"{len(db_settings)} configuração(ões) carregada(s) do banco.")

    # ─────────────────────────────────────────
    # API Pública
    # ─────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        """
        Retorna o valor de uma configuração.
        Suporta notação de ponto: get("workspace.path")
        """
        value = self._get_nested(self._runtime, key)
        if value is not None:
            return value

        value = self._get_nested(self._defaults, key)
        if value is not None:
            return value

        return default

    def set(self, key: str, value: Any) -> None:
        """
        Define um valor em runtime.
        Suporta notação de ponto: set("workspace.path", "/mnt/models")
        """
        self._set_nested(self._runtime, key, value)
        logger.debug(f"Configuração atualizada: {key} = {value}")

    # ─────────────────────────────────────────
    # Atalhos para configurações frequentes
    # ─────────────────────────────────────────

    @property
    def workspace_path(self) -> Path:
        """Caminho do workspace AIModels como Path."""
        raw = self.get("workspace.path", str(DEFAULT_WORKSPACE))
        return Path(raw).expanduser().resolve()

    @property
    def theme(self) -> str:
        """Tema atual da interface (dark/light)."""
        return self.get("general.theme", "dark")

    @property
    def language(self) -> str:
        """Idioma da interface."""
        return self.get("general.language", "pt-BR")

    # ─────────────────────────────────────────
    # Privado
    # ─────────────────────────────────────────

    def _hardcoded_defaults(self) -> dict[str, Any]:
        """Valores padrão mínimos como fallback final."""
        return {
            "general": {
                "theme"   : "dark",
                "language": "pt-BR",
            },
            "workspace": {
                "path": str(DEFAULT_WORKSPACE),
            },
            "database": {
                "backup_enabled"       : True,
                "backup_interval_hours": 24,
            },
            "ui": {
                "sidebar_collapsed": False,
            },
        }

    def _get_nested(self, data: dict, key: str) -> Any:
        """Acessa chaves aninhadas via notação de ponto."""
        keys    = key.split(".")
        current = data
        for k in keys:
            if not isinstance(current, dict) or k not in current:
                return None
            current = current[k]
        return current

    def _set_nested(self, data: dict, key: str, value: Any) -> None:
        """Define chaves aninhadas via notação de ponto."""
        keys    = key.split(".")
        current = data
        for k in keys[:-1]:
            current = current.setdefault(k, {})
        current[keys[-1]] = value
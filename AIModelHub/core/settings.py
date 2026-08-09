# core/settings.py
from __future__ import annotations

from typing import Any

from core.exceptions import InvalidSettingError, SettingNotFoundError
from core.interfaces.settings_repository import SettingsRepository


DEFAULTS: dict[str, Any] = {
    "workspace_path":      "",
    "default_engine":      "llama_cpp",
    "max_loaded_models":   1,
    "download_threads":    4,
    "log_level":           "INFO",
    "theme":               "system",
    "catalog_source":      "local",
    "auto_scan_on_start":  True,
}


class SettingsService:
    """
    Gerencia as configurações da aplicação.
    Valida os valores antes de persistir.
    Não conhece SQLite — depende de SettingsRepository.
    """

    def __init__(self, repository: SettingsRepository) -> None:
        self._repository = repository
        self._seed_defaults()

    # ── API pública ────────────────────────────────────────────────────────

    def get(self, key: str, default: Any = None) -> Any:
        if not self._repository.exists(key):
            if default is not None:
                return default
            if key in DEFAULTS:
                return DEFAULTS[key]
            raise SettingNotFoundError(key)
        return self._repository.get(key)

    def set(self, key: str, value: Any) -> None:
        self._validate(key, value)
        self._repository.set(key, value)

    def reset(self, key: str) -> None:
        if key not in DEFAULTS:
            raise SettingNotFoundError(key)
        self._repository.set(key, DEFAULTS[key])

    def reset_all(self) -> None:
        for key, value in DEFAULTS.items():
            self._repository.set(key, value)

    def all(self) -> dict[str, Any]:
        return self._repository.all()

    # ── validação ──────────────────────────────────────────────────────────

    def _validate(self, key: str, value: Any) -> None:
        validators = {
            "max_loaded_models": self._positive_int,
            "download_threads":  self._positive_int,
            "log_level":         self._valid_log_level,
            "theme":             self._valid_theme,
        }
        if key in validators:
            validators[key](key, value)

    @staticmethod
    def _positive_int(key: str, value: Any) -> None:
        if not isinstance(value, int) or value < 1:
            raise InvalidSettingError(key, "deve ser um inteiro maior que zero")

    @staticmethod
    def _valid_log_level(key: str, value: Any) -> None:
        valid = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
        if value not in valid:
            raise InvalidSettingError(key, f"deve ser um de: {', '.join(sorted(valid))}")

    @staticmethod
    def _valid_theme(key: str, value: Any) -> None:
        valid = {"system", "light", "dark"}
        if value not in valid:
            raise InvalidSettingError(key, f"deve ser um de: {', '.join(sorted(valid))}")

    # ── interno ────────────────────────────────────────────────────────────

    def _seed_defaults(self) -> None:
        """Insere defaults apenas se a chave ainda não existe."""
        for key, value in DEFAULTS.items():
            if not self._repository.exists(key):
                self._repository.set(key, value)
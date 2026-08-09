# core/exceptions.py


class OmniaError(Exception):
    """Exceção base do OMNIA. Todas as exceções de domínio herdam desta."""


# ── Modelo ─────────────────────────────────────────────────────────────────

class ModelNotFoundError(OmniaError):
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        super().__init__(f"Modelo não encontrado: '{model_id}'")


class ModelAlreadyRegisteredError(OmniaError):
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        super().__init__(f"Modelo já registrado: '{model_id}'")


class InvalidModelFileError(OmniaError):
    def __init__(self, path: str, reason: str = "") -> None:
        self.path = path
        detail = f" — {reason}" if reason else ""
        super().__init__(f"Arquivo de modelo inválido: '{path}'{detail}")


class UnsupportedModelFormatError(OmniaError):
    def __init__(self, fmt: str) -> None:
        self.format = fmt
        super().__init__(f"Formato de modelo não suportado: '{fmt}'")


# ── Download ────────────────────────────────────────────────────────────────

class DownloadAlreadyActiveError(OmniaError):
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        super().__init__(f"Download já em andamento para: '{model_id}'")


class DownloadNotFoundError(OmniaError):
    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        super().__init__(f"Nenhum download registrado para: '{model_id}'")


class DownloadFailedError(OmniaError):
    def __init__(self, model_id: str, reason: str = "") -> None:
        self.model_id = model_id
        detail = f" — {reason}" if reason else ""
        super().__init__(f"Download falhou para '{model_id}'{detail}")


# ── Scanner ─────────────────────────────────────────────────────────────────

class WorkspaceNotFoundError(OmniaError):
    def __init__(self, path: str) -> None:
        self.path = path
        super().__init__(f"Workspace não encontrado: '{path}'")


class ScanFailedError(OmniaError):
    def __init__(self, path: str, reason: str = "") -> None:
        self.path = path
        detail = f" — {reason}" if reason else ""
        super().__init__(f"Falha ao escanear '{path}'{detail}")


# ── Benchmark ───────────────────────────────────────────────────────────────

class BenchmarkFailedError(OmniaError):
    def __init__(self, model_id: str, reason: str = "") -> None:
        self.model_id = model_id
        detail = f" — {reason}" if reason else ""
        super().__init__(f"Benchmark falhou para '{model_id}'{detail}")


# ── Catálogo ────────────────────────────────────────────────────────────────

class CatalogUnavailableError(OmniaError):
    def __init__(self, reason: str = "") -> None:
        detail = f" — {reason}" if reason else ""
        super().__init__(f"Catálogo indisponível{detail}")


class CatalogEntryNotFoundError(OmniaError):
    def __init__(self, entry_id: str) -> None:
        self.entry_id = entry_id
        super().__init__(f"Entrada do catálogo não encontrada: '{entry_id}'")


# ── Configuração ────────────────────────────────────────────────────────────

class InvalidSettingError(OmniaError):
    def __init__(self, key: str, reason: str = "") -> None:
        self.key = key
        detail = f" — {reason}" if reason else ""
        super().__init__(f"Configuração inválida: '{key}'{detail}")


class SettingNotFoundError(OmniaError):
    def __init__(self, key: str) -> None:
        self.key = key
        super().__init__(f"Configuração não encontrada: '{key}'")
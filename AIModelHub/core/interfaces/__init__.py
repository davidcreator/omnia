# core/interfaces/__init__.py
from core.interfaces.model_repository     import ModelRepository
from core.interfaces.download_repository  import DownloadRepository
from core.interfaces.benchmark_repository import BenchmarkRepository
from core.interfaces.catalog_repository   import CatalogRepository
from core.interfaces.settings_repository  import SettingsRepository

__all__ = [
    "ModelRepository",
    "DownloadRepository",
    "BenchmarkRepository",
    "CatalogRepository",
    "SettingsRepository",
]
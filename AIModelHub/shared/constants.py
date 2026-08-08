"""
Constantes globais do AIModelHub.
Centraliza paths, versões e valores padrão do sistema.
"""

from pathlib import Path
import platformdirs

# ─────────────────────────────────────────
# Informações da Aplicação
# ─────────────────────────────────────────

APP_NAME         = "OMNIA AIModelHub"
APP_SHORT_NAME   = "AIModelHub"
APP_VERSION      = "0.1.0"
APP_AUTHOR       = "David Creator"
APP_LICENSE      = "GPL-2.0-or-later"

# ─────────────────────────────────────────
# Paths da Aplicação
# ─────────────────────────────────────────

# Raiz do AIModelHub (onde está o main.py)
APP_ROOT = Path(__file__).parent.parent.resolve()

# Pastas internas
CONFIG_DIR          = APP_ROOT / "config"
CONFIG_DEFAULT_FILE = CONFIG_DIR / "default.json"
RESOURCES_DIR       = APP_ROOT / "resources"
MIGRATIONS_DIR      = APP_ROOT / "database" / "migrations"

# ─────────────────────────────────────────
# Paths do Sistema Operacional
# ─────────────────────────────────────────

# Diretório de dados do usuário (por SO):
# Windows : C:/Users/<user>/AppData/Local/AIModelHub
# macOS   : ~/Library/Application Support/AIModelHub
# Linux   : ~/.local/share/AIModelHub
USER_DATA_DIR = Path(
    platformdirs.user_data_dir(
        appname=APP_SHORT_NAME,
        appauthor=APP_AUTHOR,
    )
)

# Banco de dados SQLite
DATABASE_FILE = USER_DATA_DIR / "omnia.db"

# Logs
LOG_FILE = USER_DATA_DIR / "logs" / "app.log"

# ─────────────────────────────────────────
# Workspace AIModels
# ─────────────────────────────────────────

DEFAULT_WORKSPACE = Path.home() / "AIModels"

WORKSPACE_SUBDIRS = [
    "Models/HuggingFace",
    "Models/GGUF",
    "Models/ONNX",
    "Models/TensorRT",
    "Models/MLX",
    "Models/Custom",
    "Catalog/metadata",
    "Engines",
    "Downloads/active",
    "Downloads/completed",
    "Downloads/failed",
    "Cache/inference",
    "Cache/embeddings",
    "Cache/thumbnails",
    "Logs",
    "Benchmarks",
    "Scripts/user_scripts",
    "Temp",
    "Exports",
    "Backups/db",
    "Backups/config",
]

# ─────────────────────────────────────────
# Banco de Dados
# ─────────────────────────────────────────

DATABASE_VERSION = 1

# ─────────────────────────────────────────
# Formatos de Modelo Suportados
# ─────────────────────────────────────────

SUPPORTED_FORMATS = [
    "huggingface",
    "gguf",
    "onnx",
    "tensorrt",
    "mlx",
    "custom",
]

FORMAT_EXTENSIONS = {
    "gguf"    : [".gguf"],
    "onnx"    : [".onnx"],
    "tensorrt": [".engine", ".trt"],
    "mlx"     : [".npz"],
}

# ─────────────────────────────────────────
# Interface Gráfica
# ─────────────────────────────────────────

WINDOW_MIN_WIDTH      = 1024
WINDOW_MIN_HEIGHT     = 768
WINDOW_DEFAULT_WIDTH  = 1280
WINDOW_DEFAULT_HEIGHT = 800

# ─────────────────────────────────────────
# Logs
# ─────────────────────────────────────────

LOG_MAX_SIZE  = "10 MB"
LOG_RETENTION = "30 days"
LOG_LEVEL     = "DEBUG"
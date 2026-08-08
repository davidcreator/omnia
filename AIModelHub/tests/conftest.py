"""
Fixtures globais compartilhadas entre todos os testes.
"""

import sqlite3
import pytest
import tempfile
import shutil

from pathlib import Path
from unittest.mock import patch

from loguru import logger


# ─────────────────────────────────────────
# Fixtures de Path
# ─────────────────────────────────────────

@pytest.fixture(scope="session")
def temp_dir():
    """
    Cria um diretório temporário para a sessão de testes.
    Removido automaticamente ao final.
    """
    path = Path(tempfile.mkdtemp(prefix="omnia_tests_"))
    yield path
    shutil.rmtree(path, ignore_errors=True)


@pytest.fixture(scope="function")
def temp_workspace(tmp_path):
    """
    Cria um workspace AIModels temporário para cada teste.
    """
    workspace = tmp_path / "AIModels"
    workspace.mkdir()
    return workspace


# ─────────────────────────────────────────
# Fixtures de Banco de Dados
# ─────────────────────────────────────────

@pytest.fixture(scope="function")
def db_connection():
    """
    Cria uma conexão SQLite em memória para cada teste.
    Garante isolamento total entre testes.
    """
    from database.schema import SCHEMA_SQL
    from database.connection import DatabaseConnection

    # Salva estado anterior do singleton
    previous_connection = DatabaseConnection._connection

    # Cria conexão em memória
    conn = sqlite3.connect(":memory:", check_same_thread=False)
    conn.execute("PRAGMA foreign_keys=ON;")
    conn.executescript(SCHEMA_SQL)
    conn.commit()

    # Injeta no singleton
    DatabaseConnection._connection = conn

    yield conn

    # Cleanup — fecha e restaura estado anterior
    conn.close()
    DatabaseConnection._connection = previous_connection


@pytest.fixture(scope="function")
def db_file(tmp_path):
    """
    Cria um banco SQLite em arquivo temporário.
    Útil para testes que precisam de persistência real.
    """
    from database.connection import DatabaseConnection

    db_path = tmp_path / "test_omnia.db"

    with patch("shared.constants.DATABASE_FILE", db_path):
        db = DatabaseConnection()
        db.initialize()
        yield DatabaseConnection._connection

    DatabaseConnection._connection = None


# ─────────────────────────────────────────
# Fixtures de DAOs
# ─────────────────────────────────────────

@pytest.fixture(scope="function")
def dao_models(db_connection):
    """DAO de modelos com banco em memória."""
    from database.dao_models import DAOModels
    return DAOModels()


@pytest.fixture(scope="function")
def dao_settings(db_connection):
    """DAO de configurações com banco em memória."""
    from database.dao_settings import DAOSettings
    return DAOSettings()


@pytest.fixture(scope="function")
def dao_catalog(db_connection):
    """DAO de catálogo com banco em memória."""
    from database.dao_catalog import DAOCatalog
    return DAOCatalog()


@pytest.fixture(scope="function")
def dao_benchmarks(db_connection):
    """DAO de benchmarks com banco em memória."""
    from database.dao_benchmarks import DAOBenchmarks
    return DAOBenchmarks()


@pytest.fixture(scope="function")
def dao_history(db_connection):
    """DAO de histórico com banco em memória."""
    from database.dao_history import DAOHistory
    return DAOHistory()


@pytest.fixture(scope="function")
def dao_downloads(db_connection):
    """DAO de downloads com banco em memória."""
    from database.dao_downloads import DAODownloads
    return DAODownloads()


# ─────────────────────────────────────────
# Fixtures de Dados
# ─────────────────────────────────────────

@pytest.fixture(scope="function")
def sample_model(dao_models):
    """
    Cria um modelo de exemplo no banco para uso nos testes.
    """
    dao_models.create(
        model_id="llama3:8b",
        name="Llama 3 8B",
        format="gguf",
        path="/AIModels/Models/GGUF/llama3_8b.gguf",
        architecture="llama",
        quantization="q4_0",
        size_bytes=4_500_000_000,
        manufacturer="Meta",
        description="Modelo Llama 3 8B quantizado Q4_0",
        metadata={"creator": "Meta", "license": "llama3"},
    )
    return dao_models.get_by_id("llama3:8b")


@pytest.fixture(scope="function")
def sample_models(dao_models):
    """
    Cria múltiplos modelos de exemplo no banco.
    """
    models_data = [
        {
            "model_id": "llama3:8b",
            "name": "Llama 3 8B",
            "format": "gguf",
            "path": "/AIModels/Models/GGUF/llama3_8b.gguf",
            "architecture": "llama",
            "quantization": "q4_0",
            "size_bytes": 4_500_000_000,
            "manufacturer": "Meta",
        },
        {
            "model_id": "mistral:7b",
            "name": "Mistral 7B",
            "format": "gguf",
            "path": "/AIModels/Models/GGUF/mistral_7b.gguf",
            "architecture": "mistral",
            "quantization": "q5_k_m",
            "size_bytes": 5_100_000_000,
            "manufacturer": "Mistral AI",
        },
        {
            "model_id": "gemma:2b",
            "name": "Gemma 2B",
            "format": "huggingface",
            "path": "/AIModels/Models/HuggingFace/google/gemma-2b",
            "architecture": "gemma",
            "quantization": None,
            "size_bytes": 2_000_000_000,
            "manufacturer": "Google",
        },
    ]

    for data in models_data:
        dao_models.create(**data)

    return dao_models.get_all()


# ─────────────────────────────────────────
# Fixtures de Settings
# ─────────────────────────────────────────

@pytest.fixture(scope="function")
def clean_settings():
    """
    Garante uma instância limpa do Settings para cada teste.
    """
    from shared.settings import Settings

    # Reseta o singleton
    Settings._instance = None
    Settings._defaults = {}
    Settings._runtime = {}

    settings = Settings()
    yield settings

    # Cleanup
    Settings._instance = None
    Settings._defaults = {}
    Settings._runtime = {}


# ─────────────────────────────────────────
# Configuração de Log para Testes
# ─────────────────────────────────────────

@pytest.fixture(scope="session", autouse=True)
def configure_test_logger():
    """
    Configura o logger para os testes.
    Desativa o log em arquivo durante os testes.
    """
    logger.remove()
    logger.add(
        sink=lambda msg: None,  # Descarta logs durante testes
        level="DEBUG",
    )
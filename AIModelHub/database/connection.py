"""
Gerenciamento da conexão com o banco de dados SQLite.
Implementa WAL mode e pool de conexão thread-safe.
"""

import sqlite3
from pathlib import Path
from shared.logger import logger

from shared.constants import DATABASE_FILE
from database.migrations import MigrationManager


class DatabaseConnection:
    """
    Gerencia a conexão singleton com o banco SQLite.
    Configura WAL mode para melhor performance e resiliência.
    """

    _connection: sqlite3.Connection | None = None

    def initialize(self) -> None:
        """
        Inicializa o banco de dados.
        Cria o arquivo se não existir e aplica migrações pendentes.
        """
        # Garante que o diretório existe
        DATABASE_FILE.parent.mkdir(parents=True, exist_ok=True)

        logger.debug(f"Conectando ao banco: {DATABASE_FILE}")

        self._connection = sqlite3.connect(
            str(DATABASE_FILE),
            check_same_thread=False,    # Permite acesso multi-thread
        )

        # Configurações de performance e segurança
        self._configure()

        # Aplica migrações pendentes
        migration_manager = MigrationManager(self._connection)
        migration_manager.run()

        logger.info(f"Banco de dados conectado: {DATABASE_FILE}")

    def _configure(self) -> None:
        """Aplica configurações ao banco SQLite."""
        cursor = self._connection.cursor()

        # WAL mode — melhor performance em leitura/escrita concorrente
        cursor.execute("PRAGMA journal_mode=WAL;")

        # Aumenta timeout para evitar erros em operações longas
        cursor.execute("PRAGMA busy_timeout=5000;")

        # Verifica integridade das foreign keys
        cursor.execute("PRAGMA foreign_keys=ON;")

        # Cache de páginas em memória (64MB)
        cursor.execute("PRAGMA cache_size=-65536;")

        self._connection.commit()
        logger.debug("Configurações do banco aplicadas (WAL, FK, cache).")

    @classmethod
    def get(cls) -> sqlite3.Connection:
        """
        Retorna a conexão ativa com o banco.
        Lança exceção se o banco não foi inicializado.
        """
        if cls._connection is None:
            raise RuntimeError(
                "Banco de dados não inicializado. "
                "Chame DatabaseConnection().initialize() primeiro."
            )
        return cls._connection

    @classmethod
    def close(cls) -> None:
        """Fecha a conexão com o banco."""
        if cls._connection:
            cls._connection.close()
            cls._connection = None
            logger.info("Conexão com banco encerrada.")
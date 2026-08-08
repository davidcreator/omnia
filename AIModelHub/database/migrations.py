"""
Sistema de migrações versionadas do banco de dados.
Aplica automaticamente migrações pendentes na ordem correta.
"""

import sqlite3
from pathlib import Path
from shared.logger import logger

from shared.constants import MIGRATIONS_DIR
from database.schema import SCHEMA_SQL


class MigrationManager:
    """
    Gerencia as migrações do banco de dados.
    
    - Aplica migrações pendentes em ordem sequencial.
    - Registra cada migração aplicada na tabela _migrations.
    - É idempotente: não aplica a mesma migração duas vezes.
    """

    def __init__(self, connection: sqlite3.Connection) -> None:
        self._conn = connection

    def run(self) -> None:
        """Executa todas as migrações pendentes."""
        logger.debug("Verificando migrações pendentes...")

        # Garante que o schema base existe
        self._apply_base_schema()

        # Descobre e aplica migrações pendentes
        pending = self._get_pending_migrations()

        if not pending:
            logger.debug("Nenhuma migração pendente.")
            return

        for version, name, sql in pending:
            self._apply_migration(version, name, sql)

        logger.info(f"{len(pending)} migração(ões) aplicada(s).")

    # ─────────────────────────────────────────
    # Privado
    # ─────────────────────────────────────────

    def _apply_base_schema(self) -> None:
        """Aplica o schema base (criação inicial das tabelas)."""
        try:
            self._conn.executescript(SCHEMA_SQL)
            self._conn.commit()
            logger.debug("Schema base verificado/aplicado.")
        except sqlite3.Error as error:
            logger.error(f"Erro ao aplicar schema base: {error}")
            raise

    def _get_applied_versions(self) -> set[int]:
        """Retorna os números de versão das migrações já aplicadas."""
        cursor = self._conn.execute(
            "SELECT version FROM _migrations ORDER BY version;"
        )
        return {row[0] for row in cursor.fetchall()}

    def _get_pending_migrations(self) -> list[tuple[int, str, str]]:
        """
        Descobre migrações pendentes nos arquivos .sql.
        
        Formato esperado: 001_nome_da_migracao.sql
        Retorna: [(versão, nome, sql), ...]
        """
        applied = self._get_applied_versions()
        pending = []

        if not MIGRATIONS_DIR.exists():
            logger.debug(f"Pasta de migrações não encontrada: {MIGRATIONS_DIR}")
            return pending

        for sql_file in sorted(MIGRATIONS_DIR.glob("*.sql")):
            try:
                # Extrai o número da versão do nome do arquivo
                version_str = sql_file.stem.split("_")[0]
                version = int(version_str)
                name = sql_file.stem

                if version not in applied:
                    sql = sql_file.read_text(encoding="utf-8")
                    pending.append((version, name, sql))

            except (ValueError, IndexError):
                logger.warning(
                    f"Arquivo de migração com nome inválido ignorado: {sql_file.name}. "
                    "Formato esperado: 001_nome.sql"
                )

        return pending

    def _apply_migration(self, version: int, name: str, sql: str) -> None:
        """Aplica uma migração específica e registra no banco."""
        logger.info(f"Aplicando migração {version:03d}: {name}...")

        try:
            self._conn.executescript(sql)
            self._conn.execute(
                "INSERT INTO _migrations (version, name) VALUES (?, ?);",
                (version, name),
            )
            self._conn.commit()
            logger.info(f"  ✓ Migração {version:03d} aplicada.")

        except sqlite3.Error as error:
            self._conn.rollback()
            logger.error(f"Erro na migração {version:03d} ({name}): {error}")
            raise
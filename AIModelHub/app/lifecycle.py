"""
Gerenciamento do ciclo de vida do AIModelHub.
Controla eventos de startup, shutdown e erro crítico.
"""

import sys
from loguru import logger

from database.connection import DatabaseConnection


class Lifecycle:
    """
    Gerencia os eventos do ciclo de vida do AIModelHub.
    """

    def on_startup(self) -> None:
        """Chamado após inicialização bem-sucedida."""
        logger.info("✅ AIModelHub iniciado com sucesso.")

    def on_shutdown(self) -> None:
        """Chamado quando a aplicação está encerrando."""
        logger.info("🔴 AIModelHub encerrando...")
        self._cleanup()
        logger.info("👋 AIModelHub encerrado.")

    def on_error(self, error: Exception) -> None:
        """Chamado quando ocorre um erro crítico na inicialização."""
        logger.critical(f"💥 Erro crítico: {error}")
        logger.exception(error)
        sys.exit(1)

    # ─────────────────────────────────────────
    # Privado
    # ─────────────────────────────────────────

    def _cleanup(self) -> None:
        """Executa tarefas de limpeza antes do encerramento."""
        try:
            DatabaseConnection.close()
            logger.debug("Limpeza concluída.")
        except Exception as error:
            logger.error(f"Erro durante limpeza: {error}")
"""
Sistema de log global do AIModelHub.
Deve ser o primeiro módulo inicializado no bootstrap.
"""

import sys
from pathlib import Path
from loguru import logger

from shared.constants import (
    LOG_FILE,
    LOG_LEVEL,
    LOG_MAX_SIZE,
    LOG_RETENTION,
)


def setup_logger() -> None:
    """
    Configura o sistema de log global.

    Handlers:
    - Console : logs coloridos para desenvolvimento.
    - Arquivo : logs rotativos em USER_DATA_DIR/logs/app.log.
    """

    # Remove o handler padrão do loguru
    logger.remove()

    # ── Console ────────────────────────────────────────
    logger.add(
        sink=sys.stdout,
        level=LOG_LEVEL,
        format=(
            "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | "
            "<level>{level: <8}</level> | "
            "<cyan>{name}</cyan>:<cyan>{line}</cyan> | "
            "<level>{message}</level>"
        ),
        colorize=True,
    )

    # ── Arquivo ────────────────────────────────────────
    log_path = Path(LOG_FILE)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger.add(
        sink=str(LOG_FILE),
        level=LOG_LEVEL,
        format=(
            "{time:YYYY-MM-DD HH:mm:ss} | "
            "{level: <8} | "
            "{name}:{line} | "
            "{message}"
        ),
        rotation=LOG_MAX_SIZE,
        retention=LOG_RETENTION,
        encoding="utf-8",
        enqueue=True,    # Thread-safe
        backtrace=True,  # Stack trace completo em erros
        diagnose=True,   # Diagnóstico detalhado
    )

    logger.info(f"Sistema de log iniciado → {LOG_FILE}")


# Exporta o logger para uso direto em qualquer módulo:
# from shared.logger import logger
__all__ = ["logger", "setup_logger"]
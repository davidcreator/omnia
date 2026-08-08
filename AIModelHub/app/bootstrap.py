"""
Sequência de inicialização do AIModelHub.
Orquestra todas as etapas de startup em ordem.
"""

import sys
import shutil

from shared.logger import logger
from PySide6.QtWidgets import QApplication
from PySide6.QtCore import Qt

from shared.logger import setup_logger
from shared.settings import Settings
from shared.constants import (
    APP_NAME,
    APP_VERSION,
    USER_DATA_DIR,
    WORKSPACE_SUBDIRS,
)
from database.connection import DatabaseConnection


class Bootstrap:
    """
    Executa a sequência de inicialização da aplicação.

    Ordem:
    1. Logger         — log disponível desde o início
    2. Diretórios     — pastas do sistema criadas
    3. Banco de dados — SQLite inicializado e migrado
    4. Configurações  — defaults + banco carregados
    5. Workspace      — AIModels/ verificado e criado
    6. Qt Application — instância Qt criada
    7. Interface      — janela principal exibida
    """

    def __init__(self) -> None:
        self._app: QApplication | None = None

    def initialize(self) -> QApplication:
        """
        Executa todas as etapas de inicialização.
        Retorna o QApplication pronto para execução.
        """
        self._step_logger()
        logger.info(f"🚀 Iniciando {APP_NAME} v{APP_VERSION}")

        self._step_system_dirs()
        self._step_database()
        self._step_settings()
        self._step_workspace()
        self._step_qt()
        self._step_ui()

        return self._app

    # ─────────────────────────────────────────
    # Etapas
    # ─────────────────────────────────────────

    def _step_logger(self) -> None:
        """Etapa 1 — Sistema de log."""
        setup_logger()

    def _step_system_dirs(self) -> None:
        """Etapa 2 — Diretórios internos do sistema."""
        logger.debug("Verificando diretórios do sistema...")

        dirs = [
            USER_DATA_DIR,
            USER_DATA_DIR / "logs",
        ]

        for directory in dirs:
            directory.mkdir(parents=True, exist_ok=True)
            logger.debug(f"  ✓ {directory}")

        logger.info("Diretórios do sistema verificados.")

    def _step_database(self) -> None:
        """Etapa 3 — Banco de dados SQLite."""
        logger.debug("Inicializando banco de dados...")
        db = DatabaseConnection()
        db.initialize()
        logger.info("Banco de dados inicializado.")

    def _step_settings(self) -> None:
        """Etapa 4 — Configurações."""
        logger.debug("Carregando configurações...")
        settings = Settings()
        settings.load_defaults()

        # Futuramente: carregar configurações salvas no banco
        # from database.dao_settings import DAOSettings
        # db_settings = DAOSettings().load_all()
        # settings.load_from_db(db_settings)

        logger.info(f"Workspace configurado → {settings.workspace_path}")

    def _step_workspace(self) -> None:
        """Etapa 5 — Workspace AIModels."""
        settings  = Settings()
        workspace = settings.workspace_path

        logger.debug(f"Verificando workspace: {workspace}")

        for subdir in WORKSPACE_SUBDIRS:
            path = workspace / subdir
            path.mkdir(parents=True, exist_ok=True)

        self._clean_temp(workspace)
        logger.info(f"Workspace verificado → {workspace}")

    def _step_qt(self) -> None:
        """Etapa 6 — Qt Application."""
        logger.debug("Inicializando Qt Application...")

        QApplication.setHighDpiScaleFactorRoundingPolicy(
            Qt.HighDpiScaleFactorRoundingPolicy.PassThrough
        )

        self._app = QApplication(sys.argv)
        self._app.setApplicationName(APP_NAME)
        self._app.setApplicationVersion(APP_VERSION)
        self._app.setOrganizationName("David Creator")

        logger.debug("Qt Application criada.")

    def _step_ui(self) -> None:
        """Etapa 7 — Interface gráfica."""
        logger.debug("Inicializando interface gráfica...")

        from ui.main_window import MainWindow
        self._window = MainWindow()
        self._window.show()

        logger.info("Interface gráfica iniciada.")

    # ─────────────────────────────────────────
    # Helpers
    # ─────────────────────────────────────────

    def _clean_temp(self, workspace) -> None:
        """Limpa o diretório Temp do workspace na inicialização."""
        temp_dir = workspace / "Temp"
        if temp_dir.exists():
            shutil.rmtree(temp_dir)
        temp_dir.mkdir(exist_ok=True)
        logger.debug("Pasta Temp limpa.")
"""
Janela principal do AIModelHub.
Versão inicial — estrutura base para a Fase 1.
"""

from PySide6.QtWidgets import (
    QMainWindow,
    QWidget,
    QLabel,
    QVBoxLayout,
)
from PySide6.QtCore import Qt

from shared.constants import (
    APP_NAME,
    APP_VERSION,
    WINDOW_MIN_WIDTH,
    WINDOW_MIN_HEIGHT,
    WINDOW_DEFAULT_WIDTH,
    WINDOW_DEFAULT_HEIGHT,
)
from shared.logger import logger


class MainWindow(QMainWindow):
    """
    Janela principal do AIModelHub.
    Fase 1: estrutura base — será expandida nas próximas fases.
    """

    def __init__(self) -> None:
        super().__init__()
        self._setup_window()
        self._setup_ui()
        logger.debug("MainWindow inicializada.")

    def _setup_window(self) -> None:
        """Configura propriedades da janela principal."""
        self.setWindowTitle(f"{APP_NAME} v{APP_VERSION}")
        self.setMinimumSize(WINDOW_MIN_WIDTH, WINDOW_MIN_HEIGHT)
        self.resize(WINDOW_DEFAULT_WIDTH, WINDOW_DEFAULT_HEIGHT)

    def _setup_ui(self) -> None:
        """Configura o layout inicial da interface."""
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        layout = QVBoxLayout(central_widget)
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Placeholder — será substituído na Fase 3
        label = QLabel(f"🚀 {APP_NAME}\nFase 1 — Fundação inicializada com sucesso!")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("font-size: 18px; color: #888;")

        layout.addWidget(label)
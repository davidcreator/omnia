"""
OMNIA — AIModelHub
Ponto de entrada da aplicação.
"""

import sys
from app.bootstrap import Bootstrap
from app.lifecycle import Lifecycle


def main() -> int:
    """
    Inicializa e executa o AIModelHub.
    Retorna o código de saída da aplicação.
    """
    lifecycle = Lifecycle()

    try:
        # Executa a sequência de inicialização
        bootstrap = Bootstrap()
        app = bootstrap.initialize()

        # Registra o shutdown ao encerrar
        app.aboutToQuit.connect(lifecycle.on_shutdown)

        # Inicia o loop de eventos Qt
        return app.exec()

    except Exception as error:
        lifecycle.on_error(error)
        return 1


if __name__ == "__main__":
    sys.exit(main())
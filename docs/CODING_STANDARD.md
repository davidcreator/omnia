# OMNIA

## Padrões de Código

**Versão:** 1.0  
**Linguagem:** Python 3.13+  
**Framework UI:** PySide6  
**Última atualização:** 2026

---

# 1. Visão Geral

Este documento define os padrões de código para o projeto OMNIA. Todos os contribuidores devem seguir estas convenções para manter a consistência, legibilidade e qualidade do código.

## Princípios Fundamentais

| Princípio | Descrição |
|-----------|-----------|
| **Legibilidade** | Código é lido mais vezes do que escrito. Priorize clareza. |
| **Consistência** | Siga os padrões existentes, mesmo que discorde. |
| **Simplicidade** | Prefira soluções simples. Evite over-engineering. |
| **Documentação** | Código sem documentação é código incompleto. |
| **Testabilidade** | Escreva código que possa ser testado facilmente. |

## Referências Base

* [PEP 8](https://peps.python.org/pep-0008/) — Style Guide for Python Code
* [PEP 257](https://peps.python.org/pep-0257/) — Docstring Conventions
* [PEP 484](https://peps.python.org/pep-0484/) — Type Hints
* [PEP 585](https://peps.python.org/pep-0585/) — Type Hinting Generics
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)

---

# 2. Estilo de Código

## 2.1 Formatação Básica

\`\`\`python
# ✅ Correto
def calculate_tokens_per_second(
    total_tokens: int,
    elapsed_time: float,
    *,
    precision: int = 2,
) -> float:
    """Calcula a taxa de tokens por segundo."""
    if elapsed_time <= 0:
        return 0.0
    return round(total_tokens / elapsed_time, precision)


# ❌ Incorreto
def calculate_tokens_per_second(total_tokens:int,elapsed_time:float,precision:int=2)->float:
    if elapsed_time<=0:return 0.0
    return round(total_tokens/elapsed_time,precision)
\`\`\`

## 2.2 Indentação

* **4 espaços** por nível de indentação
* **Nunca use tabs**
* Continuação de linha: alinhar com o delimitador de abertura

\`\`\`python
# ✅ Correto — alinhado com parêntese
result = some_function(argument_one, argument_two,
                       argument_three, argument_four)

# ✅ Correto — hanging indent
result = some_function(
    argument_one,
    argument_two,
    argument_three,
)

# ❌ Incorreto
result = some_function(argument_one, argument_two,
    argument_three, argument_four)
\`\`\`

## 2.3 Comprimento de Linha

* **Máximo: 100 caracteres** (preferível: 88 — padrão Black)
* Docstrings e comentários: máximo 79 caracteres
* URLs podem exceder o limite

## 2.4 Linhas em Branco

\`\`\`python
# Duas linhas em branco entre definições de top-level
class ModelManager:
    pass


class EngineManager:
    pass


# Uma linha em branco entre métodos
class ModelManager:
    def load(self) -> None:
        pass

    def unload(self) -> None:
        pass
\`\`\`

## 2.5 Strings

\`\`\`python
# ✅ Aspas duplas para strings (padrão do projeto)
message = "Model loaded successfully"

# ✅ Aspas simples quando a string contém aspas duplas
html = '<div class="container">Content</div>'

# ✅ f-strings para interpolação
log_message = f"Loaded model {model_name} in {elapsed:.2f}s"

# ✅ Strings longas com parênteses implícitos
long_message = (
    "This is a very long message that needs to be "
    "split across multiple lines for readability."
)

# ❌ Evite concatenação com +
message = "Model " + model_name + " loaded"  # Use f-string
\`\`\`

## 2.6 Trailing Commas

\`\`\`python
# ✅ Use trailing comma em estruturas multi-linha
config = {
    "model_path": "/path/to/model",
    "quantization": "q4_0",
    "context_length": 4096,  # <- trailing comma
}

engines = [
    "ollama",
    "transformers",
    "llama.cpp",  # <- trailing comma
]
\`\`\`

---

# 3. Nomenclatura

## 3.1 Convenções Gerais

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Módulos | snake_case | \`model_manager.py\` |
| Pacotes | snake_case | \`ai_engines\` |
| Classes | PascalCase | \`ModelManager\` |
| Funções | snake_case | \`load_model()\` |
| Métodos | snake_case | \`get_metrics()\` |
| Variáveis | snake_case | \`model_path\` |
| Constantes | UPPER_SNAKE_CASE | \`MAX_CONTEXT_LENGTH\` |
| Parâmetros | snake_case | \`context_length\` |
| Type Variables | PascalCase | \`ModelType\` |

## 3.2 Prefixos e Sufixos

\`\`\`python
# Variáveis privadas: prefixo _
class Model:
    def __init__(self):
        self._internal_state = {}  # Privado
        self.__mangled = None      # Name mangling (evite)

# Variáveis "dunder" são reservadas ao Python
__all__ = ["Model", "Engine"]

# Sufixos comuns
model_list: list[Model]       # _list para coleções
model_dict: dict[str, Model]  # _dict para dicionários
model_count: int              # _count para contagens
is_loaded: bool               # is_ para booleanos
has_gpu: bool                 # has_ para booleanos
can_inference: bool           # can_ para capacidades
\`\`\`

## 3.3 Nomes Descritivos

\`\`\`python
# ✅ Nomes claros e descritivos
def calculate_tokens_per_second(total_tokens: int, elapsed_time: float) -> float:
    pass

def get_model_by_architecture(architecture: str) -> list[Model]:
    pass

# ❌ Nomes vagos ou abreviados
def calc_tps(t: int, e: float) -> float:
    pass

def get_mdl(arch: str) -> list:
    pass
\`\`\`

## 3.4 Nomenclatura de Classes

\`\`\`python
# Classes base/abstratas: sufixo Base ou ABC
class EngineBase(ABC):
    pass

class AbstractModelLoader(ABC):
    pass

# Interfaces: prefixo I (opcional no Python)
class IModelProvider(Protocol):
    pass

# Exceções: sufixo Error ou Exception
class ModelNotFoundError(Exception):
    pass

class InvalidQuantizationError(ValueError):
    pass

# Mixins: sufixo Mixin
class LoggingMixin:
    pass

# Data classes: nome do domínio
@dataclass
class ModelMetadata:
    pass

@dataclass
class BenchmarkResult:
    pass
\`\`\`

---

# 4. Estrutura de Arquivos

## 4.1 Ordem dos Elementos

\`\`\`python
\"\"\"
Docstring do módulo.

Descrição mais detalhada do propósito do módulo.
\"\"\"

# 1. Future imports (se necessário)
from __future__ import annotations

# 2. Imports da biblioteca padrão
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

# 3. Imports de terceiros
from PySide6.QtWidgets import QWidget
from sqlalchemy import Column, String

# 4. Imports locais
from omnia.core.models import Model
from omnia.database.connection import get_session

# 5. Type checking imports
if TYPE_CHECKING:
    from omnia.engines.base import BaseEngine

# 6. Constantes do módulo
DEFAULT_CONTEXT_LENGTH = 4096
MAX_BATCH_SIZE = 32

# 7. Logger do módulo
logger = logging.getLogger(__name__)

# 8. Classes de exceção
class ModuleSpecificError(Exception):
    pass

# 9. Classes principais
class MainClass:
    pass

# 10. Funções auxiliares
def helper_function():
    pass

# 11. Bloco main (se aplicável)
if __name__ == "__main__":
    main()
\`\`\`

## 4.2 Tamanho de Arquivos

* **Máximo recomendado:** 500 linhas
* Se exceder, considere dividir em módulos menores
* Cada arquivo deve ter uma responsabilidade clara

## 4.3 Estrutura de Classes

\`\`\`python
class ModelManager:
    \"\"\"Gerencia o ciclo de vida dos modelos.\"\"\"

    # 1. Atributos de classe
    DEFAULT_FORMAT = "gguf"
    _instances: dict[str, "ModelManager"] = {}

    # 2. __init__
    def __init__(self, workspace_path: Path) -> None:
        self._workspace = workspace_path
        self._models: dict[str, Model] = {}
        self._current_model: Model | None = None

    # 3. Propriedades
    @property
    def current_model(self) -> Model | None:
        return self._current_model

    @current_model.setter
    def current_model(self, model: Model) -> None:
        self._current_model = model

    # 4. Métodos públicos
    def load_model(self, model_id: str) -> Model:
        pass

    def unload_model(self) -> None:
        pass

    # 5. Métodos privados
    def _validate_model(self, model: Model) -> bool:
        pass

    def _update_cache(self) -> None:
        pass

    # 6. Métodos estáticos e de classe
    @classmethod
    def get_instance(cls, workspace: Path) -> "ModelManager":
        pass

    @staticmethod
    def validate_path(path: Path) -> bool:
        pass

    # 7. Métodos mágicos (exceto __init__)
    def __repr__(self) -> str:
        return f"ModelManager(workspace={self._workspace})"

    def __len__(self) -> int:
        return len(self._models)
\`\`\`

---

# 5. Docstrings

## 5.1 Estilo Google (Padrão do Projeto)

\`\`\`python
def load_model(
    model_path: Path,
    *,
    quantization: str | None = None,
    context_length: int = 4096,
) -> Model:
    \"\"\"Carrega um modelo de IA do disco.

    Lê o arquivo de modelo especificado, valida seu formato e
    prepara-o para inferência. Suporta múltiplos formatos incluindo
    GGUF, HuggingFace e ONNX.

    Args:
        model_path: Caminho para o arquivo do modelo.
        quantization: Tipo de quantização (ex: 'q4_0', 'q8_0').
            Se None, usa o padrão do modelo.
        context_length: Tamanho máximo do contexto em tokens.
            Padrão é 4096.

    Returns:
        Instância do Model carregado e pronto para inferência.

    Raises:
        FileNotFoundError: Se o arquivo do modelo não existe.
        InvalidModelError: Se o formato do modelo é inválido.
        OutOfMemoryError: Se não há memória suficiente.

    Example:
        >>> model = load_model(Path("/models/llama.gguf"))
        >>> model.inference("Hello, world!")
        'Hello! How can I help you today?'

    Note:
        Modelos grandes podem demorar vários segundos para carregar.
        Considere usar load_model_async para operações não-bloqueantes.

    See Also:
        unload_model: Para descarregar o modelo da memória.
        get_model_info: Para obter metadados sem carregar.
    \"\"\"
    pass
\`\`\`

## 5.2 Docstrings de Classes

\`\`\`python
class EngineManager:
    \"\"\"Gerencia múltiplas engines de inferência.

    O EngineManager é responsável por descobrir, registrar e gerenciar
    diferentes backends de inferência (Ollama, Transformers, etc.).
    Implementa o padrão Singleton para garantir uma única instância.

    Attributes:
        engines: Dicionário de engines registradas.
        active_engine: Engine atualmente selecionada para inferência.
        supported_formats: Lista de formatos de modelo suportados.

    Example:
        >>> manager = EngineManager.get_instance()
        >>> manager.register_engine(OllamaEngine())
        >>> manager.select_engine("ollama")
        >>> result = manager.inference("Hello!")

    Note:
        Use get_instance() ao invés do construtor direto.
    \"\"\"

    def __init__(self) -> None:
        \"\"\"Inicializa o EngineManager.

        Warning:
            Não use diretamente. Use EngineManager.get_instance().
        \"\"\"
        pass
\`\`\`

## 5.3 Docstrings de Módulos

\`\`\`python
\"\"\"Motor de inferência para integração com Ollama.

Este módulo fornece a implementação do adaptador para o backend
Ollama, permitindo carregar e executar modelos GGUF através da
API REST do Ollama.

Principais componentes:
    - OllamaEngine: Classe principal do adaptador
    - OllamaConfig: Configurações específicas do Ollama
    - OllamaError: Exceções do módulo

Example:
    >>> from omnia.engines.ollama import OllamaEngine
    >>> engine = OllamaEngine()
    >>> if engine.is_available():
    ...     engine.load_model("llama2")
    ...     response = engine.inference("Hello!")

Requirements:
    - Ollama instalado e rodando (ollama serve)
    - Modelos baixados via 'ollama pull'

See Also:
    - https://ollama.ai/docs
    - omnia.engines.base.BaseEngine
\"\"\"
\`\`\`

---

# 6. Type Hints

## 6.1 Sintaxe Moderna (Python 3.10+)

\`\`\`python
# ✅ Sintaxe moderna
def process(items: list[str]) -> dict[str, int]:
    pass

def get_model(model_id: str) -> Model | None:
    pass

def load_models(paths: list[Path]) -> tuple[list[Model], list[str]]:
    pass

# ❌ Sintaxe antiga (evite)
from typing import List, Dict, Optional, Tuple

def process(items: List[str]) -> Dict[str, int]:
    pass

def get_model(model_id: str) -> Optional[Model]:
    pass
\`\`\`

## 6.2 Tipos Comuns

\`\`\`python
from collections.abc import Callable, Iterator, Sequence
from typing import Any, TypeVar, Generic, Protocol, TypeAlias

# Type aliases para tipos complexos
ModelDict: TypeAlias = dict[str, Model]
PathLike: TypeAlias = str | Path
JsonValue: TypeAlias = str | int | float | bool | None | list | dict

# TypeVar para genéricos
T = TypeVar("T")
ModelT = TypeVar("ModelT", bound=Model)

# Callable types
Callback: TypeAlias = Callable[[str], None]
ModelFactory: TypeAlias = Callable[[Path], Model]

# Protocol para duck typing estrutural
class SupportsInference(Protocol):
    def inference(self, prompt: str) -> str: ...
\`\`\`

## 6.3 Anotações de Retorno

\`\`\`python
# Sempre anote retornos, mesmo None
def save_model(model: Model) -> None:
    pass

# NoReturn para funções que nunca retornam
from typing import NoReturn

def fatal_error(message: str) -> NoReturn:
    raise SystemExit(message)

# Self para métodos que retornam a própria instância
from typing import Self

class Builder:
    def with_option(self, option: str) -> Self:
        return self
\`\`\`

---

# 7. Imports

## 7.1 Organização

\`\`\`python
# 1. Imports da biblioteca padrão
import os
import sys
from pathlib import Path
from typing import TYPE_CHECKING

# 2. Imports de terceiros (linha em branco antes)
import numpy as np
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QWidget

# 3. Imports locais (linha em branco antes)
from omnia.core import ModelManager
from omnia.database import Session
from omnia.utils.logging import get_logger

# 4. TYPE_CHECKING imports (evita imports circulares)
if TYPE_CHECKING:
    from omnia.engines.base import BaseEngine
\`\`\`

## 7.2 Boas Práticas

\`\`\`python
# ✅ Imports explícitos
from omnia.core.models import Model, ModelMetadata
from omnia.utils import calculate_hash

# ✅ Imports absolutos
from omnia.engines.ollama import OllamaEngine

# ❌ Evite wildcard imports
from omnia.core.models import *

# ❌ Evite imports relativos (exceto em pacotes internos)
from ..core import models  # Evite

# ✅ Renomeie para evitar conflitos
from PySide6.QtCore import Signal as QtSignal
from omnia.core.signals import Signal as OmniaSignal
\`\`\`

## 7.3 Imports Condicionais

\`\`\`python
# Para dependências opcionais
try:
    import torch
    HAS_TORCH = True
except ImportError:
    HAS_TORCH = False

# Para imports específicos de plataforma
import sys
if sys.platform == "win32":
    from omnia.platform.windows import get_gpu_info
else:
    from omnia.platform.unix import get_gpu_info
\`\`\`

---

# 8. Tratamento de Erros

## 8.1 Exceções Customizadas

\`\`\`python
# Defina no módulo omnia/core/exceptions.py
class OmniaError(Exception):
    \"\"\"Exceção base para todos os erros do OMNIA.\"\"\"
    pass


class ModelError(OmniaError):
    \"\"\"Erros relacionados a modelos.\"\"\"
    pass


class ModelNotFoundError(ModelError):
    \"\"\"Modelo não encontrado no catálogo.\"\"\"

    def __init__(self, model_id: str) -> None:
        self.model_id = model_id
        super().__init__(f"Model not found: {model_id}")


class EngineError(OmniaError):
    \"\"\"Erros relacionados a engines.\"\"\"
    pass


class EngineNotAvailableError(EngineError):
    \"\"\"Engine não está disponível no sistema.\"\"\"

    def __init__(self, engine_name: str, reason: str = "") -> None:
        self.engine_name = engine_name
        message = f"Engine '{engine_name}' is not available"
        if reason:
            message += f": {reason}"
        super().__init__(message)
\`\`\`

## 8.2 Boas Práticas

\`\`\`python
# ✅ Capture exceções específicas
try:
    model = load_model(path)
except FileNotFoundError:
    logger.error(f"Model file not found: {path}")
    raise ModelNotFoundError(str(path)) from None
except PermissionError as e:
    logger.error(f"Permission denied: {path}")
    raise ModelError(f"Cannot read model: {e}") from e

# ✅ Use context managers
with open(path, "r") as f:
    data = f.read()

# ✅ Re-raise com contexto
try:
    result = external_api_call()
except ExternalError as e:
    raise OmniaError("External API failed") from e

# ❌ Nunca silencie exceções sem motivo
try:
    risky_operation()
except Exception:
    pass  # NUNCA faça isso

# ❌ Evite bare except
try:
    operation()
except:  # Captura até KeyboardInterrupt!
    pass
\`\`\`

## 8.3 Padrão de Validação

\`\`\`python
def load_model(model_path: Path, *, validate: bool = True) -> Model:
    \"\"\"Carrega um modelo com validação opcional.\"\"\"
    # Validações no início
    if not model_path.exists():
        raise FileNotFoundError(f"Model not found: {model_path}")
    
    if not model_path.is_file():
        raise ValueError(f"Path is not a file: {model_path}")
    
    if validate and not _is_valid_model(model_path):
        raise InvalidModelError(f"Invalid model format: {model_path}")
    
    # Lógica principal após validações
    return _do_load_model(model_path)
\`\`\`

---

# 9. Logging

## 9.1 Configuração

\`\`\`python
# omnia/utils/logging.py
import logging
from pathlib import Path

def setup_logging(
    level: int = logging.INFO,
    log_file: Path | None = None,
) -> None:
    \"\"\"Configura o sistema de logging do OMNIA.\"\"\"
    format_string = (
        "%(asctime)s | %(levelname)-8s | "
        "%(name)s:%(funcName)s:%(lineno)d | %(message)s"
    )
    
    handlers: list[logging.Handler] = [logging.StreamHandler()]
    
    if log_file:
        handlers.append(logging.FileHandler(log_file))
    
    logging.basicConfig(
        level=level,
        format=format_string,
        handlers=handlers,
    )


def get_logger(name: str) -> logging.Logger:
    \"\"\"Obtém um logger configurado.\"\"\"
    return logging.getLogger(f"omnia.{name}")
\`\`\`

## 9.2 Uso Correto

\`\`\`python
# No topo do módulo
logger = get_logger(__name__)

# Níveis corretos
logger.debug("Detalhes para debugging: %s", details)
logger.info("Modelo carregado: %s", model_name)
logger.warning("Cache quase cheio: %d%%", usage)
logger.error("Falha ao carregar: %s", error)
logger.critical("Sistema em estado inconsistente")

# ✅ Use lazy formatting
logger.info("Processing %d items", len(items))

# ❌ Evite f-strings em logs (avalia mesmo se não logar)
logger.debug(f"Processing {len(expensive_operation())} items")

# ✅ Inclua exceções
try:
    risky_operation()
except Exception:
    logger.exception("Operation failed")  # Inclui traceback

# ✅ Use extra para dados estruturados
logger.info(
    "Model loaded",
    extra={
        "model_id": model.id,
        "format": model.format,
        "size_mb": model.size / 1024 / 1024,
    }
)
\`\`\`

---

# 10. Testes

## 10.1 Estrutura

\`\`\`
tests/
├── __init__.py
├── conftest.py              # Fixtures compartilhadas
├── unit/
│   ├── __init__.py
│   ├── test_models.py
│   ├── test_engines.py
│   └── test_database.py
├── integration/
│   ├── __init__.py
│   ├── test_model_loading.py
│   └── test_engine_inference.py
└── fixtures/
    ├── models/
    └── configs/
\`\`\`

## 10.2 Convenções de Nomenclatura

\`\`\`python
# Arquivos: test_<módulo>.py
# test_model_manager.py

# Classes: Test<Classe>
class TestModelManager:
    
    # Métodos: test_<método>_<cenário>_<resultado_esperado>
    def test_load_model_valid_path_returns_model(self):
        pass
    
    def test_load_model_invalid_path_raises_error(self):
        pass
    
    def test_load_model_corrupted_file_raises_invalid_model_error(self):
        pass
\`\`\`

## 10.3 Padrões de Teste

\`\`\`python
import pytest
from pathlib import Path
from omnia.core.models import ModelManager
from omnia.core.exceptions import ModelNotFoundError


class TestModelManager:
    \"\"\"Testes para ModelManager.\"\"\"

    @pytest.fixture
    def manager(self, tmp_path: Path) -> ModelManager:
        \"\"\"Fixture que fornece um ModelManager configurado.\"\"\"
        return ModelManager(workspace=tmp_path)

    @pytest.fixture
    def sample_model(self, tmp_path: Path) -> Path:
        \"\"\"Fixture que cria um modelo de teste.\"\"\"
        model_path = tmp_path / "test_model.gguf"
        model_path.write_bytes(b"fake model data")
        return model_path

    def test_load_model_success(
        self,
        manager: ModelManager,
        sample_model: Path,
    ) -> None:
        \"\"\"Testa carregamento bem-sucedido de modelo.\"\"\"
        # Arrange (já feito pelas fixtures)
        
        # Act
        model = manager.load_model(sample_model)
        
        # Assert
        assert model is not None
        assert model.path == sample_model
        assert manager.current_model == model

    def test_load_model_not_found_raises_error(
        self,
        manager: ModelManager,
    ) -> None:
        \"\"\"Testa erro quando modelo não existe.\"\"\"
        # Arrange
        fake_path = Path("/nonexistent/model.gguf")
        
        # Act & Assert
        with pytest.raises(ModelNotFoundError) as exc_info:
            manager.load_model(fake_path)
        
        assert str(fake_path) in str(exc_info.value)

    @pytest.mark.parametrize("format_type", ["gguf", "hf", "onnx"])
    def test_supports_multiple_formats(
        self,
        manager: ModelManager,
        format_type: str,
    ) -> None:
        \"\"\"Testa suporte a múltiplos formatos.\"\"\"
        assert format_type in manager.supported_formats
\`\`\`

## 10.4 Mocking

\`\`\`python
from unittest.mock import Mock, patch, MagicMock


def test_engine_inference_calls_backend(self) -> None:
    \"\"\"Testa se inference chama o backend corretamente.\"\"\"
    # Arrange
    mock_backend = Mock()
    mock_backend.generate.return_value = "Hello, World!"
    
    engine = OllamaEngine(backend=mock_backend)
    
    # Act
    result = engine.inference("Hello")
    
    # Assert
    mock_backend.generate.assert_called_once_with(
        prompt="Hello",
        model=engine.current_model,
    )
    assert result == "Hello, World!"


@patch("omnia.engines.ollama.requests.get")
def test_check_availability(self, mock_get: Mock) -> None:
    \"\"\"Testa verificação de disponibilidade.\"\"\"
    mock_get.return_value.status_code = 200
    
    engine = OllamaEngine()
    
    assert engine.is_available() is True
    mock_get.assert_called_with("http://localhost:11434/api/tags")
\`\`\`

---

# 11. Git & Commits

## 11.1 Conventional Commits

\`\`\`
<type>(<scope>): <description>

[optional body]

[optional footer(s)]
\`\`\`

### Types

| Type | Descrição |
|------|-----------|
| \`feat\` | Nova funcionalidade |
| \`fix\` | Correção de bug |
| \`docs\` | Alterações em documentação |
| \`style\` | Formatação (não afeta código) |
| \`refactor\` | Refatoração (sem feat/fix) |
| \`perf\` | Melhoria de performance |
| \`test\` | Adição/correção de testes |
| \`build\` | Build system ou dependências |
| \`ci\` | Configuração de CI |
| \`chore\` | Outras alterações |

### Exemplos

\`\`\`bash
# Feature
feat(engines): add support for vLLM backend

# Bug fix
fix(scanner): handle symlinks in model directory

# Documentation
docs(readme): update installation instructions

# Breaking change
feat(api)!: redesign model loading interface

BREAKING CHANGE: load_model now requires keyword arguments
\`\`\`

## 11.2 Branches

\`\`\`
main                    # Branch principal, sempre estável
├── develop             # Desenvolvimento ativo
├── feature/xxx         # Novas funcionalidades
├── fix/xxx             # Correções de bugs
├── docs/xxx            # Documentação
└── release/x.x.x       # Preparação de release
\`\`\`

## 11.3 Pull Requests

* **Título:** Segue Conventional Commits
* **Descrição:** Template com contexto, mudanças e testes
* **Tamanho:** Máximo ~400 linhas de código
* **Reviews:** Mínimo 1 aprovação

---

# 12. Ferramentas

## 12.1 Configuração Obrigatória

### pyproject.toml

\`\`\`toml
[project]
name = "omnia"
version = "1.0.0"
requires-python = ">=3.13"

[tool.black]
line-length = 88
target-version = ["py313"]
include = '\\.pyi?$'

[tool.ruff]
line-length = 88
target-version = "py313"
select = [
    "E",    # pycodestyle errors
    "W",    # pycodestyle warnings
    "F",    # Pyflakes
    "I",    # isort
    "B",    # flake8-bugbear
    "C4",   # flake8-comprehensions
    "UP",   # pyupgrade
    "SIM",  # flake8-simplify
]
ignore = ["E501"]  # line too long (handled by black)

[tool.ruff.isort]
known-first-party = ["omnia"]

[tool.mypy]
python_version = "3.13"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_functions = "test_*"
addopts = "-v --cov=omnia --cov-report=html"
\`\`\`

## 12.2 Pre-commit Hooks

\`\`\`yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.0
    hooks:
      - id: black

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.14
    hooks:
      - id: ruff
        args: [--fix]

  - repo: https://github.com/pre-commit/mirrors-mypy
    rev: v1.8.0
    hooks:
      - id: mypy
        additional_dependencies: [pyside6-stubs]
\`\`\`

## 12.3 Comandos do Dia a Dia

\`\`\`bash
# Formatar código
black .
ruff check --fix .

# Verificar tipos
mypy omnia/

# Rodar testes
pytest
pytest -x --pdb              # Para no primeiro erro, abre debugger
pytest -k "test_model"       # Filtra por nome
pytest --cov --cov-report=html  # Com cobertura

# Pre-commit
pre-commit install           # Instalar hooks
pre-commit run --all-files   # Rodar em tudo
\`\`\`

---

# 13. Segurança

## 13.1 Nunca Faça

\`\`\`python
# ❌ Nunca use eval/exec com input do usuário
eval(user_input)
exec(user_code)

# ❌ Nunca use pickle com dados não confiáveis
import pickle
data = pickle.loads(untrusted_data)

# ❌ Nunca construa SQL manualmente
query = f"SELECT * FROM models WHERE id = '{user_input}'"

# ❌ Nunca exponha secrets em logs
logger.info(f"API Key: {api_key}")

# ❌ Nunca desabilite verificação SSL
requests.get(url, verify=False)
\`\`\`

## 13.2 Boas Práticas

\`\`\`python
# ✅ Use queries parametrizadas
session.query(Model).filter(Model.id == user_input).first()

# ✅ Valide inputs
from pathlib import Path

def load_model(path: Path) -> Model:
    # Previne path traversal
    resolved = path.resolve()
    if not resolved.is_relative_to(MODELS_DIR):
        raise SecurityError("Path traversal detected")
    return _load(resolved)

# ✅ Use secrets seguros
import secrets
token = secrets.token_urlsafe(32)

# ✅ Sanitize output
from markupsafe import escape
safe_output = escape(user_content)
\`\`\`

---

# 14. Performance

## 14.1 Guidelines

\`\`\`python
# ✅ Use generators para grandes datasets
def iter_models(directory: Path) -> Iterator[Model]:
    for path in directory.glob("*.gguf"):
        yield load_model(path)

# ✅ Use list/dict comprehensions
squares = [x ** 2 for x in range(100)]
model_dict = {m.id: m for m in models}

# ✅ Use lru_cache para funções puras custosas
from functools import lru_cache

@lru_cache(maxsize=128)
def get_model_hash(path: Path) -> str:
    return calculate_sha256(path)

# ✅ Use __slots__ para classes com muitas instâncias
class ModelMetadata:
    __slots__ = ("id", "name", "format", "size")
    
    def __init__(self, id: str, name: str, format: str, size: int):
        self.id = id
        self.name = name
        self.format = format
        self.size = size

# ✅ Use asyncio para I/O bound
async def download_models(urls: list[str]) -> list[Path]:
    async with aiohttp.ClientSession() as session:
        tasks = [download_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)
\`\`\`

## 14.2 Profiling

\`\`\`python
# Para identificar gargalos
import cProfile
import pstats

with cProfile.Profile() as pr:
    result = expensive_function()

stats = pstats.Stats(pr)
stats.sort_stats("cumulative")
stats.print_stats(10)
\`\`\`

---

# 15. Checklist de Pull Request

Antes de submeter um PR, verifique:

## Código
- [ ] Segue o estilo PEP 8 (verificado por Black/Ruff)
- [ ] Type hints em todas as funções públicas
- [ ] Docstrings em todas as funções/classes públicas
- [ ] Sem warnings do mypy
- [ ] Sem imports não utilizados

## Testes
- [ ] Testes unitários para novas funcionalidades
- [ ] Todos os testes passando
- [ ] Cobertura de código >= 80%
- [ ] Testes de edge cases

## Documentação
- [ ] Docstrings atualizadas
- [ ] README atualizado (se necessário)
- [ ] CHANGELOG atualizado

## Git
- [ ] Commits seguem Conventional Commits
- [ ] Branch atualizada com main
- [ ] PR com descrição clara
- [ ] Labels apropriados

## Segurança
- [ ] Sem secrets hardcoded
- [ ] Inputs validados
- [ ] Sem vulnerabilidades conhecidas

---

# Referências

* [PEP 8 – Style Guide](https://peps.python.org/pep-0008/)
* [PEP 257 – Docstring Conventions](https://peps.python.org/pep-0257/)
* [Google Python Style Guide](https://google.github.io/styleguide/pyguide.html)
* [Black Code Formatter](https://black.readthedocs.io/)
* [Ruff Linter](https://docs.astral.sh/ruff/)
* [mypy Type Checker](https://mypy.readthedocs.io/)
* [pytest Documentation](https://docs.pytest.org/)
* [Conventional Commits](https://www.conventionalcommits.org/)

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

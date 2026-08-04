# OMNIA

## Documentação de Engines

**Versão:** 1.0  
**Módulo:** Engine Abstraction Layer (EAL)  
**Última atualização:** 2026  

---

# 1. Visão Geral

O OMNIA suporta múltiplas **engines de inferência** através da **Engine Abstraction Layer (EAL)**, permitindo que o mesmo modelo seja executado em diferentes backends sem alterações no código da aplicação.

## Engines Suportadas

| Engine | Status | Formatos | Plataformas |
|--------|--------|----------|-------------|
| **Ollama** | ✅ MVP | GGUF | Windows, macOS, Linux |
| **Transformers** | ✅ MVP | HuggingFace | Todas |
| **AirLLM** | ✅ MVP | HuggingFace | Todas |
| **llama.cpp** | 🔜 Planejado | GGUF | Todas |
| **vLLM** | 🔜 Planejado | HuggingFace | Linux |
| **LM Studio** | 🔜 Planejado | GGUF | Windows, macOS |
| **Text Gen WebUI** | 🔜 Planejado | Múltiplos | Todas |

## Por que múltiplas engines?

* **Flexibilidade** — Usuário escolhe a melhor engine para seu hardware
* **Compatibilidade** — Diferentes engines suportam diferentes formatos
* **Performance** — Algumas engines são otimizadas para casos específicos
* **Fallback** — Se uma engine falha, outra pode assumir

---

# 2. Arquitetura EAL

## Diagrama

\`\`\`
┌─────────────────────────────────────────────────────────────┐
│                        OMNIA Core                            │
│                    (model_manager.py)                        │
└─────────────────────────────┬───────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                      Engine Manager                          │
│                   (engine_manager.py)                        │
│  ┌─────────────────────────────────────────────────────┐    │
│  │  • discover_engines()    • get_engine(name)         │    │
│  │  • register_engine()     • select_best_engine()     │    │
│  │  • get_available()       • load_model()             │    │
│  └─────────────────────────────────────────────────────┘    │
└─────────────────────────────┬───────────────────────────────┘
                              │
          ┌───────────────────┼───────────────────┐
          │                   │                   │
          ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│  OllamaEngine   │ │TransformersEngine│ │  vLLMEngine    │
├─────────────────┤ ├─────────────────┤ ├─────────────────┤
│ • load_model()  │ │ • load_model()  │ │ • load_model()  │
│ • inference()   │ │ • inference()   │ │ • inference()   │
│ • unload()      │ │ • unload()      │ │ • unload()      │
│ • get_metrics() │ │ • get_metrics() │ │ • get_metrics() │
└────────┬────────┘ └────────┬────────┘ └────────┬────────┘
         │                   │                   │
         ▼                   ▼                   ▼
┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐
│   Ollama CLI    │ │   HuggingFace   │ │   vLLM Server   │
│   / REST API    │ │   Transformers  │ │   / Ray         │
└─────────────────┘ └─────────────────┘ └─────────────────┘
\`\`\`

## Princípios

| Princípio | Descrição |
|-----------|-----------|
| **Interface Única** | Todas as engines implementam a mesma interface |
| **Descoberta Automática** | O sistema detecta engines instaladas |
| **Seleção Inteligente** | Escolha automática da melhor engine para cada modelo |
| **Fallback Gracioso** | Se uma engine falha, tenta outra compatível |
| **Lazy Loading** | Engines são carregadas sob demanda |

---

# 3. BaseEngine

## Interface Abstrata

Todas as engines devem herdar de \`BaseEngine\` e implementar seus métodos abstratos:

\`\`\`python
# engines/base_engine.py

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Any, Iterator


class EngineStatus(Enum):
    """Status de uma engine."""
    UNKNOWN = "unknown"
    AVAILABLE = "available"
    UNAVAILABLE = "unavailable"
    LOADING = "loading"
    READY = "ready"
    ERROR = "error"


@dataclass
class EngineInfo:
    """Informações sobre uma engine."""
    id: str
    name: str
    version: str | None
    status: EngineStatus
    supported_formats: list[str]
    supported_quantizations: list[str]
    requires_gpu: bool
    max_context_length: int | None
    metadata: dict[str, Any]


@dataclass
class InferenceResult:
    """Resultado de uma inferência."""
    text: str
    tokens_generated: int
    tokens_per_second: float
    time_to_first_token_ms: float
    total_time_ms: float
    finish_reason: str  # "stop", "length", "error"


@dataclass
class ModelMetrics:
    """Métricas do modelo carregado."""
    load_time_ms: float
    ram_usage_mb: float
    vram_usage_mb: float
    context_length: int
    model_size_mb: float


class BaseEngine(ABC):
    """
    Classe base abstrata para todas as engines de inferência.
    
    Toda engine deve herdar desta classe e implementar os métodos
    abstratos para garantir compatibilidade com o Engine Manager.
    """

    def __init__(self) -> None:
        self._status = EngineStatus.UNKNOWN
        self._current_model: str | None = None
        self._model_path: Path | None = None

    # =========================================================================
    # PROPRIEDADES ABSTRATAS
    # =========================================================================

    @property
    @abstractmethod
    def id(self) -> str:
        """Identificador único da engine (ex: 'ollama', 'transformers')."""
        ...

    @property
    @abstractmethod
    def name(self) -> str:
        """Nome de exibição da engine."""
        ...

    @property
    @abstractmethod
    def version(self) -> str | None:
        """Versão da engine instalada, ou None se não detectada."""
        ...

    @property
    @abstractmethod
    def supported_formats(self) -> list[str]:
        """Lista de formatos de modelo suportados (ex: ['gguf', 'huggingface'])."""
        ...

    @property
    def supported_quantizations(self) -> list[str]:
        """Lista de quantizações suportadas."""
        return ["fp16", "fp32"]

    @property
    def requires_gpu(self) -> bool:
        """Se a engine requer GPU."""
        return False

    @property
    def max_context_length(self) -> int | None:
        """Tamanho máximo de contexto suportado, ou None se ilimitado."""
        return None

    # =========================================================================
    # MÉTODOS ABSTRATOS
    # =========================================================================

    @abstractmethod
    def is_available(self) -> bool:
        """
        Verifica se a engine está disponível no sistema.
        
        Returns:
            True se a engine está instalada e funcional.
        """
        ...

    @abstractmethod
    def load_model(
        self,
        model_path: Path,
        **kwargs: Any,
    ) -> bool:
        """
        Carrega um modelo na engine.
        
        Args:
            model_path: Caminho para o arquivo/diretório do modelo.
            **kwargs: Parâmetros específicos da engine.
        
        Returns:
            True se o modelo foi carregado com sucesso.
        
        Raises:
            ModelLoadError: Se falhar ao carregar o modelo.
        """
        ...

    @abstractmethod
    def unload_model(self) -> bool:
        """
        Descarrega o modelo atual da memória.
        
        Returns:
            True se o modelo foi descarregado com sucesso.
        """
        ...

    @abstractmethod
    def inference(
        self,
        prompt: str,
        *,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        stop: list[str] | None = None,
        **kwargs: Any,
    ) -> InferenceResult:
        """
        Executa inferência no modelo carregado.
        
        Args:
            prompt: Texto de entrada para o modelo.
            max_tokens: Número máximo de tokens a gerar.
            temperature: Temperatura de sampling (0.0-2.0).
            top_p: Nucleus sampling threshold.
            top_k: Top-k sampling.
            stop: Lista de strings que param a geração.
            **kwargs: Parâmetros específicos da engine.
        
        Returns:
            InferenceResult com o texto gerado e métricas.
        
        Raises:
            InferenceError: Se a inferência falhar.
            ModelNotLoadedError: Se nenhum modelo está carregado.
        """
        ...

    @abstractmethod
    def inference_stream(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> Iterator[str]:
        """
        Executa inferência com streaming de tokens.
        
        Args:
            prompt: Texto de entrada.
            **kwargs: Parâmetros de inferência.
        
        Yields:
            Tokens gerados um a um.
        """
        ...

    @abstractmethod
    def get_metrics(self) -> ModelMetrics | None:
        """
        Retorna métricas do modelo carregado.
        
        Returns:
            ModelMetrics ou None se nenhum modelo está carregado.
        """
        ...

    # =========================================================================
    # MÉTODOS CONCRETOS
    # =========================================================================

    @property
    def status(self) -> EngineStatus:
        """Status atual da engine."""
        return self._status

    @property
    def current_model(self) -> str | None:
        """Nome do modelo atualmente carregado."""
        return self._current_model

    @property
    def is_model_loaded(self) -> bool:
        """Se há um modelo carregado."""
        return self._current_model is not None

    def get_info(self) -> EngineInfo:
        """Retorna informações completas da engine."""
        return EngineInfo(
            id=self.id,
            name=self.name,
            version=self.version,
            status=self._status,
            supported_formats=self.supported_formats,
            supported_quantizations=self.supported_quantizations,
            requires_gpu=self.requires_gpu,
            max_context_length=self.max_context_length,
            metadata={},
        )

    def supports_format(self, format: str) -> bool:
        """Verifica se a engine suporta um formato."""
        return format.lower() in [f.lower() for f in self.supported_formats]

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(id='{self.id}', status={self.status})"
\`\`\`

---

# 4. Engine Manager

O \`EngineManager\` é o ponto central de acesso às engines, responsável por descoberta, registro e seleção.

\`\`\`python
# engines/engine_manager.py

from pathlib import Path
from typing import Type
import logging

from .base_engine import BaseEngine, EngineStatus
from .ollama_engine import OllamaEngine
from .transformers_engine import TransformersEngine
from .vllm_engine import vLLMEngine

logger = logging.getLogger(__name__)


class EngineManager:
    """
    Gerenciador central de engines de inferência.
    
    Responsável por:
    - Descobrir engines disponíveis no sistema
    - Registrar novas engines
    - Selecionar a melhor engine para cada modelo
    - Gerenciar o ciclo de vida das engines
    """

    # Engines padrão registradas
    DEFAULT_ENGINES: list[Type[BaseEngine]] = [
        OllamaEngine,
        TransformersEngine,
        vLLMEngine,
    ]

    def __init__(self) -> None:
        self._engines: dict[str, BaseEngine] = {}
        self._active_engine: BaseEngine | None = None
        self._register_default_engines()

    def _register_default_engines(self) -> None:
        """Registra as engines padrão."""
        for engine_class in self.DEFAULT_ENGINES:
            try:
                engine = engine_class()
                self.register_engine(engine)
            except Exception as e:
                logger.warning(f"Failed to register {engine_class.__name__}: {e}")

    # =========================================================================
    # REGISTRO
    # =========================================================================

    def register_engine(self, engine: BaseEngine) -> None:
        """
        Registra uma engine no manager.
        
        Args:
            engine: Instância da engine a registrar.
        """
        self._engines[engine.id] = engine
        logger.info(f"Registered engine: {engine.id}")

    def unregister_engine(self, engine_id: str) -> bool:
        """Remove uma engine do registro."""
        if engine_id in self._engines:
            del self._engines[engine_id]
            return True
        return False

    # =========================================================================
    # DESCOBERTA
    # =========================================================================

    def discover_engines(self) -> list[str]:
        """
        Verifica disponibilidade de todas as engines registradas.
        
        Returns:
            Lista de IDs das engines disponíveis.
        """
        available = []
        for engine_id, engine in self._engines.items():
            try:
                if engine.is_available():
                    engine._status = EngineStatus.AVAILABLE
                    available.append(engine_id)
                    logger.info(f"Engine available: {engine_id}")
                else:
                    engine._status = EngineStatus.UNAVAILABLE
            except Exception as e:
                engine._status = EngineStatus.ERROR
                logger.error(f"Error checking {engine_id}: {e}")
        return available

    def get_available_engines(self) -> list[BaseEngine]:
        """Retorna lista de engines disponíveis."""
        return [
            e for e in self._engines.values()
            if e.status == EngineStatus.AVAILABLE
        ]

    # =========================================================================
    # SELEÇÃO
    # =========================================================================

    def get_engine(self, engine_id: str) -> BaseEngine | None:
        """Retorna uma engine pelo ID."""
        return self._engines.get(engine_id)

    def get_engines_for_format(self, format: str) -> list[BaseEngine]:
        """Retorna engines que suportam um formato específico."""
        return [
            e for e in self.get_available_engines()
            if e.supports_format(format)
        ]

    def select_best_engine(
        self,
        model_path: Path,
        *,
        preferred_engine: str | None = None,
        require_gpu: bool = False,
    ) -> BaseEngine | None:
        """
        Seleciona a melhor engine para um modelo.
        
        Args:
            model_path: Caminho do modelo.
            preferred_engine: Engine preferida (se disponível).
            require_gpu: Se deve requerer suporte a GPU.
        
        Returns:
            Engine selecionada ou None se nenhuma compatível.
        """
        # Detectar formato do modelo
        format = self._detect_format(model_path)
        
        # Filtrar engines compatíveis
        compatible = self.get_engines_for_format(format)
        
        if require_gpu:
            compatible = [e for e in compatible if e.requires_gpu]
        
        if not compatible:
            return None
        
        # Preferência do usuário
        if preferred_engine:
            for engine in compatible:
                if engine.id == preferred_engine:
                    return engine
        
        # Retornar primeira compatível (ordem de prioridade)
        return compatible[0]

    def _detect_format(self, model_path: Path) -> str:
        """Detecta o formato do modelo pelo caminho."""
        if model_path.suffix.lower() == ".gguf":
            return "gguf"
        elif model_path.is_dir():
            # Verificar se é HuggingFace
            if (model_path / "config.json").exists():
                return "huggingface"
        elif model_path.suffix.lower() == ".onnx":
            return "onnx"
        return "unknown"

    # =========================================================================
    # OPERAÇÕES
    # =========================================================================

    def load_model(
        self,
        model_path: Path,
        *,
        engine_id: str | None = None,
        **kwargs,
    ) -> BaseEngine:
        """
        Carrega um modelo usando a engine apropriada.
        
        Args:
            model_path: Caminho do modelo.
            engine_id: ID da engine específica (opcional).
            **kwargs: Parâmetros para load_model.
        
        Returns:
            Engine com o modelo carregado.
        
        Raises:
            EngineNotFoundError: Se nenhuma engine compatível.
            ModelLoadError: Se falhar ao carregar.
        """
        # Selecionar engine
        if engine_id:
            engine = self.get_engine(engine_id)
            if not engine:
                raise EngineNotFoundError(f"Engine not found: {engine_id}")
        else:
            engine = self.select_best_engine(model_path)
            if not engine:
                raise EngineNotFoundError(
                    f"No compatible engine for: {model_path}"
                )
        
        # Descarregar modelo anterior se necessário
        if self._active_engine and self._active_engine.is_model_loaded:
            self._active_engine.unload_model()
        
        # Carregar novo modelo
        engine.load_model(model_path, **kwargs)
        self._active_engine = engine
        
        return engine

    @property
    def active_engine(self) -> BaseEngine | None:
        """Engine atualmente ativa (com modelo carregado)."""
        return self._active_engine

    def inference(self, prompt: str, **kwargs) -> str:
        """Executa inferência na engine ativa."""
        if not self._active_engine:
            raise RuntimeError("No model loaded")
        result = self._active_engine.inference(prompt, **kwargs)
        return result.text
\`\`\`

---

# 5. Ollama

## Visão Geral

| Propriedade | Valor |
|-------------|-------|
| **ID** | \`ollama\` |
| **Formatos** | GGUF |
| **GPU** | Opcional (CUDA, Metal, ROCm) |
| **Plataformas** | Windows, macOS, Linux |
| **API** | REST (localhost:11434) |

## Instalação

\`\`\`bash
# macOS / Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows
# Baixar instalador de https://ollama.ai/download

# Verificar instalação
ollama --version
\`\`\`

## Configuração

\`\`\`python
# AIModels/Engines/ollama/config.json
{
    "api_url": "http://localhost:11434",
    "timeout": 300,
    "keep_alive": "5m",
    "num_gpu": -1,
    "num_thread": 0
}
\`\`\`

## Implementação

\`\`\`python
# engines/ollama_engine.py

import httpx
from pathlib import Path
from .base_engine import BaseEngine, InferenceResult, ModelMetrics, EngineStatus


class OllamaEngine(BaseEngine):
    """Engine para Ollama."""

    def __init__(
        self,
        api_url: str = "http://localhost:11434",
        timeout: float = 300.0,
    ) -> None:
        super().__init__()
        self.api_url = api_url.rstrip("/")
        self.timeout = timeout
        self._client = httpx.Client(timeout=timeout)

    @property
    def id(self) -> str:
        return "ollama"

    @property
    def name(self) -> str:
        return "Ollama"

    @property
    def version(self) -> str | None:
        try:
            response = self._client.get(f"{self.api_url}/api/version")
            return response.json().get("version")
        except Exception:
            return None

    @property
    def supported_formats(self) -> list[str]:
        return ["gguf"]

    @property
    def supported_quantizations(self) -> list[str]:
        return ["q4_0", "q4_1", "q4_k_m", "q4_k_s", "q5_0", "q5_1", 
                "q5_k_m", "q5_k_s", "q6_k", "q8_0", "fp16"]

    def is_available(self) -> bool:
        try:
            response = self._client.get(f"{self.api_url}/api/tags")
            return response.status_code == 200
        except Exception:
            return False

    def load_model(self, model_path: Path, **kwargs) -> bool:
        model_name = model_path.stem
        
        # Criar modelo no Ollama se necessário
        response = self._client.post(
            f"{self.api_url}/api/create",
            json={
                "name": model_name,
                "modelfile": f"FROM {model_path}",
            }
        )
        
        if response.status_code == 200:
            self._current_model = model_name
            self._model_path = model_path
            self._status = EngineStatus.READY
            return True
        return False

    def unload_model(self) -> bool:
        self._current_model = None
        self._model_path = None
        self._status = EngineStatus.AVAILABLE
        return True

    def inference(
        self,
        prompt: str,
        *,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        stop: list[str] | None = None,
        **kwargs,
    ) -> InferenceResult:
        import time
        start = time.perf_counter()
        
        response = self._client.post(
            f"{self.api_url}/api/generate",
            json={
                "model": self._current_model,
                "prompt": prompt,
                "options": {
                    "num_predict": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "top_k": top_k,
                    "stop": stop or [],
                },
                "stream": False,
            }
        )
        
        data = response.json()
        elapsed = (time.perf_counter() - start) * 1000
        
        return InferenceResult(
            text=data["response"],
            tokens_generated=data.get("eval_count", 0),
            tokens_per_second=data.get("eval_count", 0) / (data.get("eval_duration", 1) / 1e9),
            time_to_first_token_ms=data.get("prompt_eval_duration", 0) / 1e6,
            total_time_ms=elapsed,
            finish_reason="stop" if data.get("done") else "length",
        )

    def inference_stream(self, prompt: str, **kwargs):
        with self._client.stream(
            "POST",
            f"{self.api_url}/api/generate",
            json={
                "model": self._current_model,
                "prompt": prompt,
                "stream": True,
            }
        ) as response:
            for line in response.iter_lines():
                if line:
                    import json
                    data = json.loads(line)
                    yield data.get("response", "")

    def get_metrics(self) -> ModelMetrics | None:
        if not self._current_model:
            return None
        
        response = self._client.post(
            f"{self.api_url}/api/show",
            json={"name": self._current_model}
        )
        data = response.json()
        
        return ModelMetrics(
            load_time_ms=0,
            ram_usage_mb=0,
            vram_usage_mb=0,
            context_length=data.get("parameters", {}).get("num_ctx", 4096),
            model_size_mb=data.get("size", 0) / 1024 / 1024,
        )
\`\`\`

## Comandos Úteis

\`\`\`bash
# Listar modelos instalados
ollama list

# Baixar modelo
ollama pull llama2

# Rodar modelo
ollama run llama2

# Criar modelo customizado
ollama create mymodel -f Modelfile

# Remover modelo
ollama rm mymodel

# Ver informações
ollama show llama2
\`\`\`

---

# 6. Transformers (HuggingFace)

## Visão Geral

| Propriedade | Valor |
|-------------|-------|
| **ID** | \`transformers\` |
| **Formatos** | HuggingFace (safetensors, bin) |
| **GPU** | Opcional (CUDA, MPS) |
| **Plataformas** | Todas |
| **Biblioteca** | transformers, torch |

## Instalação

\`\`\`bash
# CPU only
pip install transformers torch

# CUDA (Linux/Windows)
pip install transformers torch --index-url https://download.pytorch.org/whl/cu121

# Apple Silicon
pip install transformers torch
\`\`\`

## Configuração

\`\`\`python
# AIModels/Engines/transformers/config.json
{
    "device": "auto",
    "torch_dtype": "auto",
    "low_cpu_mem_usage": true,
    "trust_remote_code": false,
    "use_flash_attention": true
}
\`\`\`

## Implementação

\`\`\`python
# engines/transformers_engine.py

import torch
from pathlib import Path
from transformers import AutoModelForCausalLM, AutoTokenizer, GenerationConfig
from .base_engine import BaseEngine, InferenceResult, ModelMetrics, EngineStatus


class TransformersEngine(BaseEngine):
    """Engine para HuggingFace Transformers."""

    def __init__(
        self,
        device: str = "auto",
        torch_dtype: str = "auto",
    ) -> None:
        super().__init__()
        self.device = self._resolve_device(device)
        self.torch_dtype = self._resolve_dtype(torch_dtype)
        self._model = None
        self._tokenizer = None

    def _resolve_device(self, device: str) -> str:
        if device == "auto":
            if torch.cuda.is_available():
                return "cuda"
            elif torch.backends.mps.is_available():
                return "mps"
            return "cpu"
        return device

    def _resolve_dtype(self, dtype: str):
        if dtype == "auto":
            if torch.cuda.is_available():
                return torch.float16
            return torch.float32
        return getattr(torch, dtype)

    @property
    def id(self) -> str:
        return "transformers"

    @property
    def name(self) -> str:
        return "HuggingFace Transformers"

    @property
    def version(self) -> str | None:
        import transformers
        return transformers.__version__

    @property
    def supported_formats(self) -> list[str]:
        return ["huggingface"]

    @property
    def requires_gpu(self) -> bool:
        return False  # Opcional, mas recomendado

    def is_available(self) -> bool:
        try:
            import transformers
            import torch
            return True
        except ImportError:
            return False

    def load_model(self, model_path: Path, **kwargs) -> bool:
        try:
            self._tokenizer = AutoTokenizer.from_pretrained(
                model_path,
                trust_remote_code=kwargs.get("trust_remote_code", False),
            )
            
            self._model = AutoModelForCausalLM.from_pretrained(
                model_path,
                torch_dtype=self.torch_dtype,
                device_map=self.device if self.device != "cpu" else None,
                low_cpu_mem_usage=True,
                trust_remote_code=kwargs.get("trust_remote_code", False),
            )
            
            if self.device == "cpu":
                self._model = self._model.to("cpu")
            
            self._current_model = model_path.name
            self._model_path = model_path
            self._status = EngineStatus.READY
            return True
        except Exception as e:
            self._status = EngineStatus.ERROR
            raise

    def unload_model(self) -> bool:
        if self._model:
            del self._model
            del self._tokenizer
            torch.cuda.empty_cache() if torch.cuda.is_available() else None
        self._model = None
        self._tokenizer = None
        self._current_model = None
        self._status = EngineStatus.AVAILABLE
        return True

    def inference(
        self,
        prompt: str,
        *,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        top_k: int = 40,
        stop: list[str] | None = None,
        **kwargs,
    ) -> InferenceResult:
        import time
        start = time.perf_counter()
        
        inputs = self._tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        
        generation_config = GenerationConfig(
            max_new_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            top_k=top_k,
            do_sample=temperature > 0,
            pad_token_id=self._tokenizer.eos_token_id,
        )
        
        with torch.no_grad():
            outputs = self._model.generate(
                **inputs,
                generation_config=generation_config,
            )
        
        generated_ids = outputs[0][inputs["input_ids"].shape[1]:]
        text = self._tokenizer.decode(generated_ids, skip_special_tokens=True)
        
        elapsed = (time.perf_counter() - start) * 1000
        tokens = len(generated_ids)
        
        return InferenceResult(
            text=text,
            tokens_generated=tokens,
            tokens_per_second=tokens / (elapsed / 1000),
            time_to_first_token_ms=0,
            total_time_ms=elapsed,
            finish_reason="stop",
        )

    def inference_stream(self, prompt: str, **kwargs):
        from transformers import TextIteratorStreamer
        from threading import Thread
        
        inputs = self._tokenizer(prompt, return_tensors="pt")
        inputs = {k: v.to(self._model.device) for k, v in inputs.items()}
        
        streamer = TextIteratorStreamer(
            self._tokenizer, 
            skip_prompt=True,
            skip_special_tokens=True,
        )
        
        thread = Thread(
            target=self._model.generate,
            kwargs={**inputs, "streamer": streamer, "max_new_tokens": 512},
        )
        thread.start()
        
        for token in streamer:
            yield token

    def get_metrics(self) -> ModelMetrics | None:
        if not self._model:
            return None
        
        param_bytes = sum(p.numel() * p.element_size() for p in self._model.parameters())
        
        return ModelMetrics(
            load_time_ms=0,
            ram_usage_mb=param_bytes / 1024 / 1024 if self.device == "cpu" else 0,
            vram_usage_mb=param_bytes / 1024 / 1024 if self.device != "cpu" else 0,
            context_length=self._model.config.max_position_embeddings,
            model_size_mb=param_bytes / 1024 / 1024,
        )
\`\`\`

---

# 7. llama.cpp

## Visão Geral

| Propriedade | Valor |
|-------------|-------|
| **ID** | \`llamacpp\` |
| **Formatos** | GGUF |
| **GPU** | Opcional (CUDA, Metal, OpenCL, Vulkan) |
| **Plataformas** | Todas |
| **Biblioteca** | llama-cpp-python |

## Instalação

\`\`\`bash
# CPU only
pip install llama-cpp-python

# CUDA
CMAKE_ARGS="-DLLAMA_CUDA=on" pip install llama-cpp-python

# Metal (macOS)
CMAKE_ARGS="-DLLAMA_METAL=on" pip install llama-cpp-python

# OpenBLAS (CPU otimizado)
CMAKE_ARGS="-DLLAMA_BLAS=ON -DLLAMA_BLAS_VENDOR=OpenBLAS" pip install llama-cpp-python
\`\`\`

## Configuração

\`\`\`python
# AIModels/Engines/llamacpp/config.json
{
    "n_ctx": 4096,
    "n_batch": 512,
    "n_threads": 0,
    "n_gpu_layers": -1,
    "use_mmap": true,
    "use_mlock": false,
    "verbose": false
}
\`\`\`

---

# 8. vLLM

## Visão Geral

| Propriedade | Valor |
|-------------|-------|
| **ID** | \`vllm\` |
| **Formatos** | HuggingFace |
| **GPU** | Requerido (CUDA) |
| **Plataformas** | Linux |
| **Otimização** | PagedAttention, Continuous Batching |

## Instalação

\`\`\`bash
pip install vllm
\`\`\`

## Configuração

\`\`\`python
# AIModels/Engines/vllm/config.json
{
    "tensor_parallel_size": 1,
    "gpu_memory_utilization": 0.9,
    "max_model_len": 4096,
    "quantization": null,
    "enforce_eager": false
}
\`\`\`

---

# 9. LM Studio

## Visão Geral

| Propriedade | Valor |
|-------------|-------|
| **ID** | \`lmstudio\` |
| **Formatos** | GGUF |
| **GPU** | Opcional |
| **Plataformas** | Windows, macOS |
| **API** | REST (compatível OpenAI) |

## Configuração

\`\`\`python
# AIModels/Engines/lmstudio/config.json
{
    "api_url": "http://localhost:1234/v1",
    "timeout": 300
}
\`\`\`

---

# 10. AirLLM

## Visão Geral

| Propriedade | Valor |
|-------------|-------|
| **ID** | \`airllm\` |
| **Formatos** | HuggingFace |
| **GPU** | Baixa VRAM (4GB+) |
| **Plataformas** | Todas |
| **Técnica** | Layer-by-layer inference |

## Instalação

\`\`\`bash
pip install airllm
\`\`\`

---

# 11. Comparação

## Performance

| Engine | Tokens/s (7B) | VRAM (7B) | Startup | Streaming |
|--------|---------------|-----------|---------|-----------|
| **Ollama** | 30-50 | ~5GB | Rápido | ✅ |
| **Transformers** | 20-40 | ~14GB | Médio | ✅ |
| **llama.cpp** | 25-45 | ~5GB | Rápido | ✅ |
| **vLLM** | 50-100 | ~7GB | Lento | ✅ |
| **AirLLM** | 5-15 | ~4GB | Lento | ❌ |

## Features

| Engine | Chat | Embeddings | Vision | Function Calling |
|--------|------|------------|--------|------------------|
| **Ollama** | ✅ | ✅ | ✅ | 🔜 |
| **Transformers** | ✅ | ✅ | ✅ | ✅ |
| **llama.cpp** | ✅ | ✅ | 🔜 | ❌ |
| **vLLM** | ✅ | ✅ | ✅ | ✅ |
| **AirLLM** | ✅ | ❌ | ❌ | ❌ |

## Quando Usar

| Cenário | Engine Recomendada |
|---------|-------------------|
| Uso geral desktop | Ollama |
| Baixa VRAM (<8GB) | Ollama, llama.cpp, AirLLM |
| Alta performance | vLLM |
| Sem GPU | Transformers (CPU), llama.cpp |
| Produção/API | vLLM, Ollama |
| Experimentação | Transformers |
| Apple Silicon | Ollama, llama.cpp (Metal) |

---

# 12. Criando Nova Engine

## Passo a Passo

### 1. Criar arquivo da engine

\`\`\`python
# engines/my_engine.py

from pathlib import Path
from .base_engine import BaseEngine, InferenceResult, ModelMetrics, EngineStatus


class MyEngine(BaseEngine):
    """Minha engine customizada."""

    @property
    def id(self) -> str:
        return "myengine"

    @property
    def name(self) -> str:
        return "My Custom Engine"

    @property
    def version(self) -> str | None:
        return "1.0.0"

    @property
    def supported_formats(self) -> list[str]:
        return ["gguf", "custom"]

    def is_available(self) -> bool:
        # Verificar se dependências estão instaladas
        try:
            import my_library
            return True
        except ImportError:
            return False

    def load_model(self, model_path: Path, **kwargs) -> bool:
        # Implementar carregamento
        pass

    def unload_model(self) -> bool:
        # Implementar descarregamento
        pass

    def inference(self, prompt: str, **kwargs) -> InferenceResult:
        # Implementar inferência
        pass

    def inference_stream(self, prompt: str, **kwargs):
        # Implementar streaming
        pass

    def get_metrics(self) -> ModelMetrics | None:
        # Retornar métricas
        pass
\`\`\`

### 2. Registrar no Engine Manager

\`\`\`python
# engines/engine_manager.py

from .my_engine import MyEngine

class EngineManager:
    DEFAULT_ENGINES = [
        OllamaEngine,
        TransformersEngine,
        MyEngine,  # Adicionar aqui
    ]
\`\`\`

### 3. Criar configuração padrão

\`\`\`python
# AIModels/Engines/myengine/config.json
{
    "option1": "value1",
    "option2": 123
}
\`\`\`

### 4. Adicionar testes

\`\`\`python
# tests/unit/test_my_engine.py

import pytest
from engines.my_engine import MyEngine


class TestMyEngine:
    def test_id(self):
        engine = MyEngine()
        assert engine.id == "myengine"

    def test_supported_formats(self):
        engine = MyEngine()
        assert "gguf" in engine.supported_formats

    @pytest.mark.skipif(not MyEngine().is_available(), reason="Engine not available")
    def test_inference(self, sample_model):
        engine = MyEngine()
        engine.load_model(sample_model)
        result = engine.inference("Hello")
        assert result.text
        engine.unload_model()
\`\`\`

---

# 13. Troubleshooting

## Problemas Comuns

### Ollama não disponível

\`\`\`bash
# Verificar se está rodando
curl http://localhost:11434/api/tags

# Iniciar serviço
ollama serve

# Verificar logs
journalctl -u ollama  # Linux
# ou
tail -f ~/.ollama/logs/server.log
\`\`\`

### CUDA out of memory

\`\`\`python
# Reduzir contexto
engine.load_model(path, n_ctx=2048)

# Usar quantização menor
# Preferir q4_0 ao invés de q8_0

# Liberar memória
import torch
torch.cuda.empty_cache()
\`\`\`

### Modelo incompatível

\`\`\`python
# Verificar formato
from engines.engine_manager import EngineManager

manager = EngineManager()
format = manager._detect_format(model_path)
print(f"Formato detectado: {format}")

# Listar engines compatíveis
engines = manager.get_engines_for_format(format)
print(f"Engines compatíveis: {[e.id for e in engines]}")
\`\`\`

### Lentidão na inferência

\`\`\`python
# Verificar device
print(f"Device: {engine.device}")

# Para Transformers, verificar se está usando GPU
import torch
print(f"CUDA disponível: {torch.cuda.is_available()}")
print(f"Device do modelo: {next(model.parameters()).device}")

# Usar batching quando possível
# Usar flash attention se suportado
\`\`\`

---

# Referências

* [Ollama Documentation](https://ollama.ai/docs)
* [HuggingFace Transformers](https://huggingface.co/docs/transformers)
* [llama.cpp](https://github.com/ggerganov/llama.cpp)
* [vLLM Documentation](https://docs.vllm.ai)
* [LM Studio](https://lmstudio.ai)
* [AirLLM](https://github.com/lyogavin/Anima/tree/main/air_llm)

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

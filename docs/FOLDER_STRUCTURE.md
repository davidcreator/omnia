# OMNIA

## Estrutura de Pastas

**Versão:** 1.0  
**Última atualização:** 2026  

---

# 1. Visão Geral

O projeto OMNIA é dividido em duas partes principais:

| Componente | Descrição | Localização |
|------------|-----------|-------------|
| **AIModelHub** | Aplicação principal (código-fonte) | \`/AIModelHub/\` |
| **AIModels** | Workspace de dados (modelos, cache, logs) | Configurável pelo usuário |

Esta separação permite:

* ✅ Atualizar a aplicação sem afetar os dados
* ✅ Armazenar modelos em disco externo
* ✅ Fazer backup independente de código e dados
* ✅ Compartilhar workspace entre instalações

---

# 2. Raiz do Projeto

\`\`\`
omnia/
│
├── 📁 AIModelHub/           # Aplicação principal
├── 📁 docs/                 # Documentação do projeto
├── 📁 tests/                # Testes automatizados
├── 📁 scripts/              # Scripts utilitários
│
├── 📄 README.md             # Documentação principal
├── 📄 LICENSE               # Licença GPL-2.0
├── 📄 CHANGELOG.md          # Histórico de mudanças
├── 📄 CONTRIBUTING.md       # Guia de contribuição
├── 📄 CODE_OF_CONDUCT.md    # Código de conduta
│
├── 📄 pyproject.toml        # Configuração do projeto Python
├── 📄 requirements.txt      # Dependências (gerado)
├── 📄 requirements-dev.txt  # Dependências de desenvolvimento
│
├── 📄 .gitignore            # Arquivos ignorados pelo Git
├── 📄 .pre-commit-config.yaml # Hooks de pre-commit
├── 📄 .editorconfig         # Configuração de editores
│
└── 📁 .github/              # Configurações GitHub
    ├── 📁 workflows/        # GitHub Actions
    │   ├── ci.yml           # CI/CD pipeline
    │   ├── release.yml      # Automação de releases
    │   └── docs.yml         # Build de documentação
    ├── 📁 ISSUE_TEMPLATE/   # Templates de issues
    │   ├── bug_report.md
    │   ├── feature_request.md
    │   └── config.yml
    ├── 📄 PULL_REQUEST_TEMPLATE.md
    └── 📄 FUNDING.yml       # Configuração de sponsors
\`\`\`

---

# 3. AIModelHub — Aplicação

## 3.1 Estrutura Completa

\`\`\`
AIModelHub/
│
├── 📄 main.py                    # Ponto de entrada da aplicação
├── 📄 __init__.py                # Inicialização do pacote
│
├── 📁 app/                       # Bootstrap e lifecycle
│   ├── 📄 __init__.py
│   ├── 📄 bootstrap.py           # Sequência de inicialização
│   ├── 📄 lifecycle.py           # Eventos de startup/shutdown
│   ├── 📄 settings.py            # Classe de configurações
│   ├── 📄 constants.py           # Constantes do sistema
│   └── 📄 logger.py              # Configuração de logging
│
├── 📁 core/                      # Lógica de negócios
│   ├── 📄 __init__.py
│   ├── 📄 scanner.py             # Descoberta de modelos
│   ├── 📄 catalog.py             # Gerenciamento do catálogo
│   ├── 📄 downloader.py          # Download de modelos
│   ├── 📄 converter.py           # Conversão de formatos
│   ├── 📄 benchmark.py           # Sistema de benchmarks
│   ├── 📄 workspace.py           # Gerenciamento do workspace
│   ├── 📄 model_manager.py       # Operações com modelos
│   ├── 📄 agent_manager.py       # Gerenciamento de agentes
│   ├── 📄 rag_manager.py         # Sistema RAG
│   └── 📄 exceptions.py          # Exceções customizadas
│
├── 📁 database/                  # Persistência
│   ├── 📄 __init__.py
│   ├── 📄 connection.py          # Pool de conexões
│   ├── 📄 schema.py              # Definição das tabelas
│   ├── 📄 migrations.py          # Sistema de migrações
│   ├── 📁 migrations/            # Arquivos de migração
│   │   ├── 📄 001_initial.py
│   │   ├── 📄 002_add_agents.py
│   │   └── 📄 ...
│   ├── 📄 base_dao.py            # Classe base DAO
│   ├── 📄 dao_models.py          # DAO de modelos
│   ├── 📄 dao_engines.py         # DAO de engines
│   ├── 📄 dao_benchmarks.py      # DAO de benchmarks
│   ├── 📄 dao_downloads.py       # DAO de downloads
│   ├── 📄 dao_history.py         # DAO de histórico
│   ├── 📄 dao_settings.py        # DAO de configurações
│   └── 📄 dao_agents.py          # DAO de agentes
│
├── 📁 engines/                   # Engine Abstraction Layer
│   ├── 📄 __init__.py
│   ├── 📄 base_engine.py         # Interface abstrata
│   ├── 📄 engine_manager.py      # Gerenciador de engines
│   ├── 📄 ollama_engine.py       # Adaptador Ollama
│   ├── 📄 transformers_engine.py # Adaptador Transformers
│   ├── 📄 llamacpp_engine.py     # Adaptador llama.cpp
│   ├── 📄 vllm_engine.py         # Adaptador vLLM
│   ├── 📄 lmstudio_engine.py     # Adaptador LM Studio
│   └── 📄 airllm_engine.py       # Adaptador AirLLM
│
├── 📁 plugins/                   # Sistema de plugins
│   ├── 📄 __init__.py
│   ├── 📄 plugin_base.py         # Classe base de plugins
│   ├── 📄 plugin_manager.py      # Gerenciador de plugins
│   ├── 📄 plugin_registry.py     # Registro de plugins
│   ├── 📄 hooks.py               # Sistema de hooks
│   └── 📁 builtin/               # Plugins integrados
│       ├── 📄 __init__.py
│       └── 📄 ...
│
├── 📁 ui/                        # Interface gráfica (PySide6)
│   ├── 📄 __init__.py
│   ├── 📄 main_window.py         # Janela principal
│   ├── 📄 app.py                 # Aplicação Qt
│   ├── 📁 views/                 # Telas da aplicação
│   │   ├── 📄 __init__.py
│   │   ├── 📄 dashboard.py       # Dashboard
│   │   ├── 📄 library.py         # Biblioteca de modelos
│   │   ├── 📄 downloads.py       # Gerenciador de downloads
│   │   ├── 📄 engines_view.py    # Painel de engines
│   │   ├── 📄 benchmark_view.py  # Visualização de benchmarks
│   │   ├── 📄 agents_view.py     # Painel de agentes
│   │   ├── 📄 settings_view.py   # Configurações
│   │   └── 📄 logs_view.py       # Visualizador de logs
│   ├── 📁 components/            # Widgets reutilizáveis
│   │   ├── 📄 __init__.py
│   │   ├── 📄 sidebar.py         # Barra lateral
│   │   ├── 📄 model_card.py      # Card de modelo
│   │   ├── 📄 search_bar.py      # Barra de busca
│   │   ├── 📄 progress_bar.py    # Barra de progresso
│   │   ├── 📄 toast.py           # Notificações toast
│   │   └── 📄 ...
│   ├── 📁 dialogs/               # Diálogos modais
│   │   ├── 📄 __init__.py
│   │   ├── 📄 model_details.py   # Detalhes do modelo
│   │   ├── 📄 download_dialog.py # Diálogo de download
│   │   ├── 📄 settings_dialog.py # Diálogo de configurações
│   │   └── 📄 ...
│   └── 📁 styles/                # Estilos QSS
│       ├── 📄 dark.qss           # Tema escuro
│       ├── 📄 light.qss          # Tema claro
│       └── 📄 common.qss         # Estilos comuns
│
├── 📁 resources/                 # Assets estáticos
│   ├── 📁 icons/                 # Ícones
│   │   ├── 📁 16x16/
│   │   ├── 📁 24x24/
│   │   ├── 📁 32x32/
│   │   ├── 📁 64x64/
│   │   └── 📄 icon.svg           # Ícone vetorial
│   ├── 📁 images/                # Imagens
│   │   ├── 📄 logo.png
│   │   ├── 📄 splash.png
│   │   └── 📄 ...
│   ├── 📁 fonts/                 # Fontes
│   │   └── 📄 ...
│   └── 📄 resources.qrc          # Arquivo de recursos Qt
│
├── 📁 utils/                     # Utilitários
│   ├── 📄 __init__.py
│   ├── 📄 file_utils.py          # Operações de arquivo
│   ├── 📄 hash_utils.py          # Cálculo de hashes
│   ├── 📄 format_utils.py        # Formatação de dados
│   ├── 📄 system_info.py         # Informações do sistema
│   ├── 📄 gpu_utils.py           # Detecção de GPU
│   └── 📄 validators.py          # Validadores
│
└── 📁 config/                    # Configurações da aplicação
    ├── 📄 default.toml           # Configurações padrão
    ├── 📄 logging.toml           # Configuração de logging
    └── 📄 engines.toml           # Configurações de engines
\`\`\`

## 3.2 Descrição dos Módulos

### app/

| Arquivo | Responsabilidade |
|---------|------------------|
| \`bootstrap.py\` | Inicializa componentes na ordem correta |
| \`lifecycle.py\` | Gerencia eventos de startup, shutdown, error |
| \`settings.py\` | Carrega e persiste configurações |
| \`constants.py\` | Define constantes (caminhos, versões, defaults) |
| \`logger.py\` | Configura sistema de logging |

### core/

| Arquivo | Responsabilidade |
|---------|------------------|
| \`scanner.py\` | Varre workspace buscando modelos |
| \`catalog.py\` | CRUD de modelos (busca, filtros, tags) |
| \`downloader.py\` | Download com retry, verificação de hash |
| \`converter.py\` | Converte formatos (HF→GGUF, etc.) |
| \`benchmark.py\` | Executa e coleta métricas |
| \`workspace.py\` | Gerencia diretório AIModels |
| \`model_manager.py\` | Orquestra operações de modelos |
| \`agent_manager.py\` | Gerencia agentes de IA |
| \`rag_manager.py\` | Sistema de RAG local |
| \`exceptions.py\` | Exceções específicas do domínio |

### database/

| Arquivo | Responsabilidade |
|---------|------------------|
| \`connection.py\` | Pool de conexões SQLite |
| \`schema.py\` | Definição CREATE TABLE |
| \`migrations.py\` | Sistema de migrações |
| \`base_dao.py\` | Interface base para DAOs |
| \`dao_*.py\` | Data Access Objects específicos |

### engines/

| Arquivo | Responsabilidade |
|---------|------------------|
| \`base_engine.py\` | Interface abstrata de engines |
| \`engine_manager.py\` | Descoberta, seleção, lifecycle |
| \`*_engine.py\` | Implementações específicas |

### ui/

| Diretório | Responsabilidade |
|-----------|------------------|
| \`views/\` | Telas completas da aplicação |
| \`components/\` | Widgets reutilizáveis |
| \`dialogs/\` | Janelas modais |
| \`styles/\` | Arquivos QSS para temas |

---

# 4. AIModels — Workspace

## 4.1 Estrutura Completa

\`\`\`
AIModels/                         # Raiz configurável pelo usuário
│
├── 📁 Models/                    # Modelos de IA
│   ├── 📁 HuggingFace/           # Formato HuggingFace
│   │   └── 📁 <org>/
│   │       └── 📁 <model>/
│   │           ├── 📄 config.json
│   │           ├── 📄 tokenizer.json
│   │           ├── 📄 model.safetensors
│   │           └── 📄 ...
│   ├── 📁 GGUF/                  # Formato GGUF
│   │   └── 📄 <model>.gguf
│   ├── 📁 ONNX/                  # Formato ONNX
│   │   └── 📄 <model>.onnx
│   ├── 📁 TensorRT/              # Formato TensorRT
│   │   └── 📄 <model>.plan
│   ├── 📁 MLX/                   # Formato Apple MLX
│   │   └── 📁 <model>/
│   └── 📁 Custom/                # Modelos personalizados
│
├── 📁 Catalog/                   # Metadados do catálogo
│   ├── 📄 index.json             # Índice centralizado
│   └── 📁 metadata/              # Metadados por modelo
│       └── 📄 <model_id>.json
│
├── 📁 Engines/                   # Configurações por engine
│   ├── 📁 ollama/
│   │   └── 📄 config.json
│   ├── 📁 transformers/
│   │   └── 📄 config.json
│   ├── 📁 llamacpp/
│   │   └── 📄 config.json
│   └── 📁 vllm/
│       └── 📄 config.json
│
├── 📁 Downloads/                 # Gerenciamento de downloads
│   ├── 📁 active/                # Downloads em andamento
│   │   └── 📄 <file>.part
│   ├── 📁 completed/             # Downloads concluídos (pré-organização)
│   │   └── 📄 <file>
│   └── 📁 failed/                # Downloads com falha
│       └── 📄 <file>.failed
│
├── 📁 Cache/                     # Cache do sistema
│   ├── 📁 inference/             # Cache de inferência
│   ├── 📁 embeddings/            # Cache de embeddings (RAG)
│   ├── 📁 thumbnails/            # Thumbnails de modelos
│   └── 📁 huggingface/           # Cache do HuggingFace Hub
│
├── 📁 Logs/                      # Logs do sistema
│   ├── 📄 app.log                # Log da aplicação
│   ├── 📄 engine.log             # Log das engines
│   ├── 📄 download.log           # Log de downloads
│   ├── 📄 error.log              # Apenas erros
│   └── 📁 archive/               # Logs arquivados
│       └── 📄 app_2026-01-15.log.gz
│
├── 📁 Benchmarks/                # Resultados de benchmarks
│   └── 📁 <model_id>/
│       └── 📄 <timestamp>.json
│
├── 📁 Agents/                    # Agentes personalizados
│   └── 📁 <agent_id>/
│       ├── 📄 config.json        # Configuração do agente
│       ├── 📄 system_prompt.md   # Prompt de sistema
│       └── 📁 knowledge/         # Base de conhecimento
│
├── 📁 RAG/                       # Sistema RAG
│   ├── 📁 documents/             # Documentos fonte
│   ├── 📁 vectors/               # Vetores de embedding
│   │   └── 📁 <collection>/
│   │       └── 📄 index.faiss
│   └── 📄 config.json            # Configuração RAG
│
├── 📁 Scripts/                   # Scripts do usuário
│   ├── 📁 automation/            # Scripts de automação
│   ├── 📁 conversion/            # Scripts de conversão
│   └── 📄 README.md              # Documentação
│
├── 📁 Temp/                      # Arquivos temporários
│   └── 📄 ...                    # Limpo automaticamente
│
├── 📁 Exports/                   # Exportações
│   └── 📁 <export_name>/
│       ├── 📄 manifest.json
│       └── 📄 ...
│
├── 📁 Backups/                   # Backups
│   ├── 📁 db/                    # Backups do banco
│   │   └── 📄 omnia_<timestamp>.db
│   └── 📁 config/                # Backups de configuração
│       └── 📄 settings_<timestamp>.json
│
└── 📁 database/                  # Banco de dados
    ├── 📄 omnia.db               # SQLite principal
    ├── 📄 omnia.db-wal           # Write-Ahead Log
    └── 📄 omnia.db-shm           # Shared Memory
\`\`\`

## 4.2 Descrição dos Diretórios

### Models/

Armazena os arquivos de modelo organizados por formato:

| Diretório | Formato | Extensão | Engines |
|-----------|---------|----------|---------|
| \`HuggingFace/\` | Transformers | .safetensors, .bin | Transformers, vLLM |
| \`GGUF/\` | GGUF | .gguf | Ollama, llama.cpp |
| \`ONNX/\` | ONNX | .onnx | ONNX Runtime |
| \`TensorRT/\` | TensorRT | .plan, .engine | TensorRT |
| \`MLX/\` | Apple MLX | diretório | MLX |
| \`Custom/\` | Outros | variado | Depende |

### Cache/

| Diretório | Conteúdo | TTL |
|-----------|----------|-----|
| \`inference/\` | Respostas cacheadas | 7 dias |
| \`embeddings/\` | Vetores calculados | 30 dias |
| \`thumbnails/\` | Imagens de preview | Permanente |
| \`huggingface/\` | Cache do HF Hub | Configurável |

### Logs/

| Arquivo | Conteúdo | Rotação |
|---------|----------|---------|
| \`app.log\` | Log geral da aplicação | Diário |
| \`engine.log\` | Operações de engines | Diário |
| \`download.log\` | Downloads e verificações | Diário |
| \`error.log\` | Apenas erros/exceções | Semanal |

---

# 5. Documentação

\`\`\`
docs/
│
├── 📄 ROADMAP.md               # Plano de desenvolvimento
├── 📄 ARCHITECTURE.md          # Arquitetura do sistema
├── 📄 DATABASE.md              # Documentação do banco
├── 📄 ENGINES.md               # Documentação de engines
├── 📄 CODING_STANDARD.md       # Padrões de código
├── 📄 FOLDER_STRUCTURE.md      # Este documento
├── 📄 API.md                   # Documentação da API
├── 📄 PLUGINS.md               # Sistema de plugins
│
├── 📁 guides/                  # Guias práticos
│   ├── 📄 getting-started.md   # Início rápido
│   ├── 📄 installation.md      # Instalação detalhada
│   ├── 📄 configuration.md     # Configuração
│   ├── 📄 first-model.md       # Primeiro modelo
│   └── 📄 troubleshooting.md   # Resolução de problemas
│
├── 📁 api/                     # Referência da API
│   ├── 📄 core.md              # API do core
│   ├── 📄 engines.md           # API de engines
│   ├── 📄 database.md          # API do banco
│   └── 📄 plugins.md           # API de plugins
│
├── 📁 tutorials/               # Tutoriais
│   ├── 📄 custom-engine.md     # Criar engine custom
│   ├── 📄 plugin-development.md # Desenvolver plugin
│   └── 📄 rag-setup.md         # Configurar RAG
│
└── 📁 images/                  # Imagens da documentação
    ├── 📄 architecture.png
    ├── 📄 screenshot-*.png
    └── 📄 ...
\`\`\`

---

# 6. Testes

\`\`\`
tests/
│
├── 📄 __init__.py
├── 📄 conftest.py              # Fixtures globais
├── 📄 pytest.ini               # Configuração pytest
│
├── 📁 unit/                    # Testes unitários
│   ├── 📄 __init__.py
│   ├── 📄 test_scanner.py
│   ├── 📄 test_catalog.py
│   ├── 📄 test_downloader.py
│   ├── 📄 test_benchmark.py
│   ├── 📁 database/
│   │   ├── 📄 test_connection.py
│   │   ├── 📄 test_dao_models.py
│   │   └── 📄 ...
│   ├── 📁 engines/
│   │   ├── 📄 test_base_engine.py
│   │   ├── 📄 test_engine_manager.py
│   │   ├── 📄 test_ollama.py
│   │   └── 📄 ...
│   └── 📁 utils/
│       ├── 📄 test_file_utils.py
│       └── 📄 ...
│
├── 📁 integration/             # Testes de integração
│   ├── 📄 __init__.py
│   ├── 📄 test_model_workflow.py
│   ├── 📄 test_download_workflow.py
│   └── 📄 test_engine_workflow.py
│
├── 📁 e2e/                     # Testes end-to-end
│   ├── 📄 __init__.py
│   └── 📄 test_full_workflow.py
│
└── 📁 fixtures/                # Dados de teste
    ├── 📁 models/              # Modelos mock
    │   └── 📄 tiny_model.gguf
    ├── 📁 configs/             # Configurações de teste
    │   └── 📄 test_config.toml
    └── 📁 data/                # Dados de teste
        └── 📄 sample_prompts.json
\`\`\`

---

# 7. Configuração

## 7.1 Arquivos de Configuração

\`\`\`
config/
├── 📄 default.toml             # Configurações padrão
├── 📄 logging.toml             # Configuração de logging
└── 📄 engines.toml             # Configurações de engines
\`\`\`

## 7.2 Arquivos na Raiz

| Arquivo | Propósito |
|---------|-----------|
| \`pyproject.toml\` | Configuração do projeto Python, dependências, ferramentas |
| \`.pre-commit-config.yaml\` | Hooks de pre-commit (black, ruff, mypy) |
| \`.editorconfig\` | Configurações de editores (indent, charset) |
| \`.gitignore\` | Arquivos ignorados pelo Git |
| \`.python-version\` | Versão do Python (pyenv) |
| \`ruff.toml\` | Configuração do linter Ruff |
| \`mypy.ini\` | Configuração do type checker |

## 7.3 pyproject.toml

\`\`\`toml
[project]
name = "omnia"
version = "1.0.0"
description = "One Platform. Every AI."
authors = [{name = "David L. Almeida", email = "contato@davidcreator.com"}]
license = {text = "GPL-2.0-or-later"}
readme = "README.md"
requires-python = ">=3.13"
keywords = ["ai", "llm", "model-management", "local-ai"]
classifiers = [
    "Development Status :: 3 - Alpha",
    "Intended Audience :: Developers",
    "License :: OSI Approved :: GNU General Public License v2 or later (GPLv2+)",
    "Programming Language :: Python :: 3.13",
]

dependencies = [
    "pyside6>=6.6.0",
    "sqlalchemy>=2.0",
    "httpx>=0.25",
    "pydantic>=2.5",
    "toml>=0.10",
]

[project.optional-dependencies]
dev = [
    "pytest>=7.4",
    "pytest-cov>=4.1",
    "black>=24.1",
    "ruff>=0.1",
    "mypy>=1.8",
    "pre-commit>=3.6",
]

[project.scripts]
omnia = "AIModelHub.main:main"

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.black]
line-length = 88
target-version = ["py313"]

[tool.ruff]
line-length = 88
target-version = "py313"
select = ["E", "W", "F", "I", "B", "C4", "UP", "SIM"]

[tool.mypy]
python_version = "3.13"
strict = true
\`\`\`

---

# 8. Convenções

## 8.1 Nomenclatura de Arquivos

| Tipo | Convenção | Exemplo |
|------|-----------|---------|
| Módulos Python | snake_case | \`model_manager.py\` |
| Classes | PascalCase | \`class ModelManager\` |
| Testes | test_<modulo>.py | \`test_scanner.py\` |
| Migrations | NNN_descricao.py | \`001_initial.py\` |
| Configs | snake_case | \`default.toml\` |
| QSS | snake_case | \`dark.qss\` |
| Docs | UPPER_CASE.md | \`ARCHITECTURE.md\` |
| Guides | kebab-case.md | \`getting-started.md\` |

## 8.2 Estrutura de Módulo

Todo módulo Python deve ter:

\`\`\`python
# module_name.py

"""
Descrição breve do módulo.

Descrição mais detalhada sobre o propósito e uso.
"""

# Imports
from __future__ import annotations

import standard_library
from typing import TYPE_CHECKING

import third_party

from local import module

if TYPE_CHECKING:
    from typing_only import imports

# Constantes
MODULE_CONSTANT = "value"

# Logger
logger = logging.getLogger(__name__)

# Classes
class MainClass:
    ...

# Funções
def helper_function():
    ...

# Main (se aplicável)
if __name__ == "__main__":
    main()
\`\`\`

## 8.3 Estrutura de Pacote

Todo pacote deve ter um \`__init__.py\`:

\`\`\`python
# __init__.py

"""
Descrição do pacote.
"""

from .main_class import MainClass
from .helper import helper_function

__all__ = ["MainClass", "helper_function"]
\`\`\`

---

# 9. Onde Colocar Novos Arquivos

## Guia Rápido

| Você quer... | Coloque em... |
|--------------|---------------|
| Nova funcionalidade de negócio | \`core/\` |
| Nova engine de IA | \`engines/\` |
| Novo DAO | \`database/\` |
| Nova tela | \`ui/views/\` |
| Novo widget | \`ui/components/\` |
| Novo diálogo | \`ui/dialogs/\` |
| Nova migração | \`database/migrations/\` |
| Novo utilitário | \`utils/\` |
| Novo plugin | \`plugins/builtin/\` ou externo |
| Ícones/imagens | \`resources/icons/\` ou \`resources/images/\` |
| Documentação | \`docs/\` |
| Teste unitário | \`tests/unit/\` |
| Teste de integração | \`tests/integration/\` |
| Fixture de teste | \`tests/fixtures/\` |
| Script utilitário | \`scripts/\` |
| Configuração padrão | \`config/\` |

## Checklist para Novo Arquivo

- [ ] Está no diretório correto?
- [ ] Segue a convenção de nomenclatura?
- [ ] Tem docstring de módulo?
- [ ] Está importado no \`__init__.py\`?
- [ ] Tem testes correspondentes?
- [ ] Está documentado (se público)?

---

# Referências

* [ARCHITECTURE.md](ARCHITECTURE.md) — Arquitetura do sistema
* [CODING_STANDARD.md](CODING_STANDARD.md) — Padrões de código
* [DATABASE.md](DATABASE.md) — Estrutura do banco

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

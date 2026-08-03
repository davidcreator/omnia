# OMNIA

## Documento de Arquitetura

**Versão:** 1.0  
**Status:** Em definição  
**Última atualização:** 2026  
**Autor:** David L. Almeida — David Creator  

---

# 1. Visão Geral

OMNIA é uma plataforma desktop modular, desenvolvida em **Python 3.13+**, para gerenciamento, organização e execução de modelos de Inteligência Artificial locais.

O sistema é composto por dois grandes blocos:

| Bloco | Papel |
|---|---|
| **AIModelHub** | Aplicação principal — interface gráfica, lógica de negócios, banco de dados, engines e plugins. |
| **AIModels** | Workspace de dados — diretório estruturado que armazena modelos, downloads, cache, logs, benchmarks e backups. |

A separação entre **aplicação** e **dados** é intencional: permite reinstalar, atualizar ou versionar a aplicação sem afetar os modelos e configurações do usuário.

---

# 2. Princípios Arquiteturais

O OMNIA adota cinco princípios fundamentais que orientam todas as decisões técnicas:

| # | Princípio | Descrição |
|---|---|---|
| 1 | **Organização antes da complexidade** | A estrutura do projeto deve ser compreensível antes de ser sofisticada. |
| 2 | **Workspace único** | Todos os modelos ficam centralizados em um único diretório estruturado, eliminando duplicações entre engines. |
| 3 | **Baixo acoplamento** | Cada módulo deve poder ser substituído, atualizado ou removido sem causar efeitos colaterais nos demais. |
| 4 | **Arquitetura modular e extensível** | Novas funcionalidades entram como plugins ou módulos independentes, sem alterar o núcleo. |
| 5 | **Evolução contínua baseada em documentação** | Toda mudança é documentada antes (ou junto com) a implementação. |

Além destes, o projeto segue:

- **Código desacoplado** — separação clara entre UI, lógica e dados.
- **Configuração centralizada** — um único ponto de configuração por ambiente.
- **Alta reutilização** — componentes internos são projetados para reuso.
- **Independência entre engines** — nenhuma engine é tratada como obrigatória.

---

# 3. Estrutura Macro

```
OMNIA/
│
├── AIModelHub/                 # Aplicação
│   ├── main.py                 # Ponto de entrada
│   ├── app/                    # Bootstrap, inicialização, lifecycle
│   ├── core/                   # Lógica de negócios central
│   ├── database/               # SQLite — schemas, migrações, DAOs
│   ├── engines/                # Engine Abstraction Layer
│   ├── plugins/                # Sistema de plugins
│   ├── ui/                     # Interface gráfica (PySide6)
│   ├── resources/              # Assets estáticos (ícones, temas)
│   ├── config/                 # Arquivos de configuração
│   ├── tests/                  # Testes unitários e de integração
│   └── docs/                   # Documentação interna do hub
│
└── AIModels/                   # Workspace de Dados
    ├── Models/                 # Modelos de IA organizados
    ├── Catalog/                # Metadados do catálogo
    ├── Engines/                # Configurações específicas por engine
    ├── Downloads/              # Downloads em andamento / concluídos
    ├── Cache/                  # Cache de inferência e dados temporários
    ├── Logs/                   # Logs de execução, erros e auditoria
    ├── Benchmarks/             # Resultados de benchmarks
    ├── Scripts/                # Scripts utilitários do usuário
    ├── Temp/                   # Arquivos temporários (limpos automaticamente)
    ├── Exports/                # Modelos e dados exportados
    └── Backups/                # Backups do workspace e banco de dados
```

---

# 4. AIModelHub — Aplicação

## 4.1 Ponto de Entrada

```
AIModelHub/
└── main.py
```

Responsável por:

- Inicializar o sistema de configuração.
- Verificar/criar o workspace `AIModels`.
- Inicializar o banco de dados SQLite.
- Registrar engines disponíveis.
- Carregar plugins habilitados.
- Iniciar a interface gráfica (PySide6).

## 4.2 Módulo `app/`

Controla o **lifecycle** da aplicação:

| Arquivo | Responsabilidade |
|---|---|
| `bootstrap.py` | Sequência de inicialização |
| `lifecycle.py` | Eventos de startup, shutdown, error |
| `settings.py` | Classe de configurações globais |
| `constants.py` | Constantes do sistema (paths, versões, defaults) |
| `logger.py` | Configuração do sistema de log |

## 4.3 Módulo `core/`

Contém a **lógica de negócios** central, desacoplada da interface:

| Arquivo | Responsabilidade |
|---|---|
| `scanner.py` | Descoberta automática de modelos no workspace |
| `catalog.py` | CRUD do catálogo (busca, filtros, tags, favoritos) |
| `downloader.py` | Download de modelos (HuggingFace, GGUF, custom) |
| `converter.py` | Conversão entre formatos (HF→GGUF, GGUF→Ollama) |
| `benchmark.py` | Execução e coleta de métricas de benchmark |
| `workspace.py` | Gerenciamento do diretório AIModels |
| `model_manager.py` | Operações de alto nível sobre modelos |
| `agent_manager.py` | Gerenciamento de agentes especializados |
| `rag_manager.py` | Indexação, embeddings e busca semântica |

## 4.4 Módulo `database/`

Banco de dados relacional local usando **SQLite**:

| Arquivo | Responsabilidade |
|---|---|
| `connection.py` | Pool de conexão e inicialização |
| `migrations.py` | Sistema de migrações versionadas |
| `schema.py` | Definição das tabelas |
| `dao_models.py` | Data Access Object — modelos |
| `dao_catalog.py` | Data Access Object — catálogo |
| `dao_benchmarks.py` | Data Access Object — benchmarks |
| `dao_history.py` | Data Access Object — histórico |
| `dao_settings.py` | Data Access Object — configurações |

## 4.5 Módulo `engines/`

Implementa a **Engine Abstraction Layer (EAL)**:

| Arquivo | Responsabilidade |
|---|---|
| `base_engine.py` | Classe abstrata que define a interface de toda engine |
| `engine_manager.py` | Registro, descoberta e seleção de engines |
| `ollama_engine.py` | Adaptador para Ollama |
| `airllm_engine.py` | Adaptador para AirLLM |
| `transformers_engine.py` | Adaptador para Transformers (HuggingFace) |
| `vllm_engine.py` | Adaptador para vLLM |
| `llamacpp_engine.py` | Adaptador para llama.cpp |
| `lmstudio_engine.py` | Adaptador para LM Studio |
| `tgwui_engine.py` | Adaptador para Text Generation WebUI |

## 4.6 Módulo `plugins/`

Sistema extensível de plugins:

| Arquivo | Responsabilidade |
|---|---|
| `plugin_base.py` | Classe base para criação de plugins |
| `plugin_manager.py` | Descoberta, carregamento e lifecycle dos plugins |
| `plugin_registry.py` | Registro centralizado dos plugins instalados |
| `hooks.py` | Sistema de hooks para extensão de funcionalidades |

## 4.7 Módulo `ui/`

Interface gráfica construída com **PySide6 (Qt for Python)**:

| Arquivo | Responsabilidade |
|---|---|
| `main_window.py` | Janela principal e navegação |
| `dashboard.py` | Tela inicial com resumo do sistema |
| `library.py` | Biblioteca de modelos (catálogo visual) |
| `downloads.py` | Gerenciador de downloads |
| `engines_view.py` | Painel de engines instaladas |
| `benchmark_view.py` | Visualização de benchmarks |
| `settings_view.py` | Tela de configurações |
| `logs_view.py` | Visualizador de logs |
| `agents_view.py` | Painel de agentes |
| `styles/` | Diretório com QSS (Qt Style Sheets) |
| `components/` | Widgets reutilizáveis |

---

# 5. AIModels — Workspace

O workspace é o **diretório de dados** do OMNIA, independente da aplicação.

## 5.1 Estrutura Detalhada

```
AIModels/
│
├── Models/
│   ├── HuggingFace/            # Modelos no formato HuggingFace
│   │   └── <org>/<model>/
│   ├── GGUF/                   # Modelos quantizados GGUF
│   │   └── <model>.gguf
│   ├── ONNX/                   # Modelos ONNX
│   ├── TensorRT/               # Modelos TensorRT
│   ├── MLX/                    # Modelos Apple MLX
│   └── Custom/                 # Modelos personalizados
│
├── Catalog/
│   ├── index.json              # Índice centralizado dos modelos
│   └── metadata/               # Metadados individuais por modelo
│       └── <model_id>.json
│
├── Engines/
│   ├── ollama/                 # Configurações para Ollama
│   ├── transformers/           # Configurações para Transformers
│   └── ...
│
├── Downloads/
│   ├── active/                 # Downloads em andamento
│   ├── completed/              # Downloads concluídos (pré-organização)
│   └── failed/                 # Downloads com falha (para retry)
│
├── Cache/
│   ├── inference/              # Cache de inferência
│   ├── embeddings/             # Cache de embeddings (RAG)
│   └── thumbnails/             # Thumbnails gerados
│
├── Logs/
│   ├── app.log                 # Log da aplicação
│   ├── engine.log              # Log das engines
│   ├── download.log            # Log de downloads
│   └── error.log               # Log de erros
│
├── Benchmarks/
│   └── <model_id>/
│       └── <timestamp>.json    # Resultado do benchmark
│
├── Scripts/
│   └── user_scripts/           # Scripts do usuário
│
├── Temp/                       # Limpo automaticamente
│
├── Exports/
│   └── <export_name>/          # Pacotes exportados
│
└── Backups/
    ├── db/                     # Backups do banco SQLite
    └── config/                 # Backups de configuração
```

## 5.2 Regras do Workspace

| Regra | Descrição |
|---|---|
| **Imutabilidade do caminho** | O caminho raiz do workspace é definido uma vez e armazenado nas configurações. |
| **Auto-criação** | Subdiretórios são criados automaticamente na inicialização se não existirem. |
| **Isolamento de engines** | Cada engine pode ter configurações específicas dentro de `Engines/`. |
| **Limpeza automática** | `Temp/` é limpo na inicialização. `Cache/` pode ter TTL configurável. |
| **Portabilidade** | O workspace pode ser movido para outro disco/máquina com ajuste de um único path. |

---

# 6. Camadas da Aplicação

A arquitetura do AIModelHub segue o padrão de **camadas desacopladas**:

```
┌─────────────────────────────────────────────┐
│                  UI Layer                    │
│            (PySide6 / Qt Widgets)            │
├─────────────────────────────────────────────┤
│               Service Layer                  │
│        (core/ — lógica de negócios)          │
├─────────────────────────────────────────────┤
│            Abstraction Layer                 │
│     (Engine Abstraction Layer — EAL)         │
├─────────────────────────────────────────────┤
│              Data Layer                      │
│       (database/ — SQLite + DAOs)            │
├─────────────────────────────────────────────┤
│            Storage Layer                     │
│        (AIModels/ — filesystem)              │
└─────────────────────────────────────────────┘
```

### Regras de dependência:

1. **UI → Service**: A interface chama apenas métodos do `core/`.
2. **Service → Abstraction + Data**: O core acessa engines via EAL e dados via DAOs.
3. **Abstraction → External**: Engines se comunicam com backends externos (Ollama, llama.cpp, etc.).
4. **Data → Storage**: DAOs leem/gravam no SQLite; o workspace gerencia o filesystem.
5. **Nenhuma camada pula outra**: UI nunca acessa o banco diretamente. Engines nunca manipulam a UI.

---

# 7. Engine Abstraction Layer (EAL)

A EAL é o componente central que permite ao OMNIA trabalhar com **múltiplas engines de inferência** sem acoplamento direto.

## 7.1 Diagrama

```
                    ┌─────────────────┐
                    │  Engine Manager  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              │              │              │
       ┌──────┴──────┐ ┌────┴────┐ ┌───────┴───────┐
       │   Ollama    │ │ AirLLM  │ │ Transformers  │ ...
       │   Engine    │ │ Engine  │ │    Engine      │
       └──────┬──────┘ └────┬────┘ └───────┬───────┘
              │              │              │
       ┌──────┴──────┐ ┌────┴────┐ ┌───────┴───────┐
       │  Ollama CLI │ │ AirLLM  │ │  HuggingFace  │
       │  / API      │ │ Python  │ │   Library      │
       └─────────────┘ └─────────┘ └───────────────┘
```

## 7.2 Interface Base

```python
class BaseEngine(ABC):
    """Classe abstrata para todas as engines."""
    
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def is_available(self) -> bool: ...
    
    @abstractmethod
    def supported_formats(self) -> list[str]: ...
    
    @abstractmethod
    def load_model(self, model_path: str, **kwargs) -> Any: ...
    
    @abstractmethod
    def unload_model(self) -> None: ...
    
    @abstractmethod
    def inference(self, prompt: str, **kwargs) -> str: ...
    
    @abstractmethod
    def get_metrics(self) -> dict: ...
```

## 7.3 Engine Manager

O `EngineManager` é responsável por:

- **Descoberta**: Detectar quais engines estão instaladas no sistema.
- **Registro**: Manter um registro de engines disponíveis.
- **Seleção**: Escolher a engine adequada para um determinado modelo.
- **Lifecycle**: Gerenciar load/unload das engines.
- **Fallback**: Se uma engine falha, tentar outra compatível.

---

# 8. Banco de Dados

## 8.1 Tecnologia

**SQLite** — banco relacional embutido, sem necessidade de servidor.

## 8.2 Schema Principal

```sql
-- Tabela de Modelos
CREATE TABLE models (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    format          TEXT NOT NULL,       -- huggingface, gguf, onnx, tensorrt, mlx
    architecture    TEXT,                -- llama, mistral, phi, gemma...
    quantization    TEXT,                -- q4_0, q5_k_m, q8_0, fp16...
    size_bytes      INTEGER,
    path            TEXT NOT NULL,
    manufacturer    TEXT,
    description     TEXT,
    is_favorite     BOOLEAN DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used_at    DATETIME,
    metadata        TEXT                 -- JSON com dados extras
);

-- Tabela de Tags
CREATE TABLE tags (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT UNIQUE NOT NULL
);

-- Relação N:N Modelos ↔ Tags
CREATE TABLE model_tags (
    model_id    TEXT REFERENCES models(id),
    tag_id      INTEGER REFERENCES tags(id),
    PRIMARY KEY (model_id, tag_id)
);

-- Tabela de Engines
CREATE TABLE engines (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    version     TEXT,
    path        TEXT,
    is_active   BOOLEAN DEFAULT 1,
    config      TEXT                    -- JSON de configuração
);

-- Tabela de Benchmarks
CREATE TABLE benchmarks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id        TEXT REFERENCES models(id),
    engine_id       TEXT REFERENCES engines(id),
    load_time_ms    REAL,
    tokens_per_sec  REAL,
    ram_usage_mb    REAL,
    vram_usage_mb   REAL,
    cpu_percent     REAL,
    gpu_percent     REAL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata        TEXT
);

-- Tabela de Downloads
CREATE TABLE downloads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    url             TEXT NOT NULL,
    model_name      TEXT,
    status          TEXT DEFAULT 'pending',  -- pending, active, completed, failed
    progress        REAL DEFAULT 0,
    size_bytes      INTEGER,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at    DATETIME
);

-- Tabela de Histórico
CREATE TABLE history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id    TEXT REFERENCES models(id),
    engine_id   TEXT REFERENCES engines(id),
    action      TEXT NOT NULL,            -- load, inference, benchmark, export...
    details     TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Configurações
CREATE TABLE settings (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    category    TEXT DEFAULT 'general',
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

## 8.3 Estratégia de Migrações

- Cada migração é numerada sequencialmente: `001_initial.sql`, `002_add_agents.sql`, etc.
- A tabela `_migrations` registra quais migrações já foram aplicadas.
- Na inicialização, o sistema aplica automaticamente migrações pendentes.

---

# 9. Sistema de Plugins

## 9.1 Arquitetura

```
┌────────────────────────────────────┐
│          Plugin Manager            │
│  (descoberta, loading, lifecycle)  │
├────────────────────────────────────┤
│         Plugin Registry            │
│   (registro central dos plugins)   │
├────────────────────────────────────┤
│           Hook System              │
│  (pontos de extensão do sistema)   │
├────────────────────────────────────┤
│         Plugin Base                │
│   (classe abstrata para plugins)   │
└────────────────────────────────────┘
```

## 9.2 Interface Base de Plugin

```python
class PluginBase(ABC):
    """Classe base para todos os plugins OMNIA."""
    
    @abstractmethod
    def name(self) -> str: ...
    
    @abstractmethod
    def version(self) -> str: ...
    
    @abstractmethod
    def description(self) -> str: ...
    
    @abstractmethod
    def on_activate(self) -> None: ...
    
    @abstractmethod
    def on_deactivate(self) -> None: ...
    
    def on_model_loaded(self, model) -> None: ...
    def on_model_unloaded(self, model) -> None: ...
    def on_inference_complete(self, result) -> None: ...
    def on_benchmark_complete(self, result) -> None: ...
    def register_ui_components(self) -> list: ...
```

## 9.3 Hooks Disponíveis

| Hook | Quando dispara |
|---|---|
| `on_startup` | Aplicação inicializada |
| `on_shutdown` | Aplicação encerrando |
| `on_model_loaded` | Modelo carregado em uma engine |
| `on_model_unloaded` | Modelo descarregado |
| `on_inference_start` | Início de inferência |
| `on_inference_complete` | Fim de inferência |
| `on_download_start` | Início de download |
| `on_download_complete` | Download finalizado |
| `on_benchmark_complete` | Benchmark finalizado |
| `on_scan_complete` | Scanner finalizou varredura |

## 9.4 Plugins Planejados

| Plugin | Função |
|---|---|
| **VS Code** | Integrar modelos do OMNIA diretamente no editor. |
| **Docker** | Empacotar modelos em containers. |
| **GitHub** | Sincronizar catálogo e configurações. |
| **WordPress** | Geração de conteúdo via IA. |
| **n8n** | Automações com modelos locais. |
| **Obsidian** | RAG com base de conhecimento Obsidian. |

---

# 10. Fluxo de Dados

## 10.1 Fluxo: Descoberta de Modelos (Scanner)

```
Inicialização
      │
      ▼
Scanner varre AIModels/Models/
      │
      ▼
Identifica formatos (GGUF, HF, ONNX...)
      │
      ▼
Lê metadados de cada modelo
      │
      ▼
Atualiza banco SQLite (tabela models)
      │
      ▼
Atualiza Catalog/index.json
      │
      ▼
Emite hook on_scan_complete
      │
      ▼
UI atualiza a biblioteca
```

## 10.2 Fluxo: Inferência

```
Usuário seleciona modelo + engine
      │
      ▼
core/model_manager verifica compatibilidade
      │
      ▼
EngineManager.load_model()
      │
      ▼
Usuário envia prompt
      │
      ▼
EngineManager.inference()
      │
      ▼
Engine processa via backend
      │
      ▼
Resultado retorna para UI
      │
      ▼
Histórico registrado no banco
      │
      ▼
Hook on_inference_complete
```

## 10.3 Fluxo: Download de Modelo

```
Usuário solicita download
      │
      ▼
core/downloader valida URL/fonte
      │
      ▼
Inicia download em AIModels/Downloads/active/
      │
      ▼
Progress reportado para UI
      │
      ▼
Verificação de integridade (hash)
      │
      ▼
Move para AIModels/Models/<format>/
      │
      ▼
Scanner re-indexa o modelo
      │
      ▼
Registro no banco + notificação
```

---

# 11. Interface Gráfica

## 11.1 Tecnologia

**PySide6** (Qt 6 para Python) — framework multiplataforma para interfaces nativas.

## 11.2 Telas Planejadas

| Tela | Descrição |
|---|---|
| **Dashboard** | Visão geral: total de modelos, engines ativas, status do sistema. |
| **Biblioteca** | Catálogo visual com busca, filtros, tags e favoritos. |
| **Downloads** | Fila de downloads com progresso e status. |
| **Engines** | Painel de engines instaladas, status e configurações. |
| **Benchmark** | Execução e visualização de benchmarks com gráficos. |
| **Agentes** | Gerenciamento de agentes especializados. |
| **Configurações** | Preferências do sistema, caminhos, temas. |
| **Logs** | Visualizador de logs em tempo real com filtros. |

## 11.3 Padrões de UI

- **Navegação lateral**: Sidebar fixa com ícones e labels.
- **Tema escuro/claro**: Suporte via QSS (Qt Style Sheets).
- **Componentes reutilizáveis**: Widgets em `ui/components/`.
- **Responsividade**: Layout adaptável ao tamanho da janela.
- **Feedback visual**: Indicadores de progresso, loading states, toasts.

---

# 12. Segurança & Integridade

## 12.1 Integridade de Modelos

| Mecanismo | Descrição |
|---|---|
| **Hash SHA-256** | Todo modelo baixado tem seu hash verificado contra o esperado. |
| **Verificação de formato** | Antes de registrar, o scanner valida se o arquivo é um modelo válido. |
| **Quarentena** | Modelos com hash inválido vão para `Downloads/failed/`. |

## 12.2 Segurança do Banco

| Mecanismo | Descrição |
|---|---|
| **Backups automáticos** | Banco é copiado periodicamente para `Backups/db/`. |
| **WAL mode** | SQLite usa Write-Ahead Logging para resiliência. |
| **Migrações versionadas** | Toda alteração de schema é controlada. |

## 12.3 Segurança de Plugins

| Mecanismo | Descrição |
|---|---|
| **Sandbox básico** | Plugins não têm acesso direto ao banco; usam APIs fornecidas. |
| **Manifest obrigatório** | Todo plugin deve declarar suas permissões. |
| **Ativação manual** | Plugins são instalados desativados; o usuário ativa explicitamente. |

---

# 13. Extensibilidade

O OMNIA foi projetado para crescer em três eixos:

## 13.1 Novas Engines

Para adicionar uma nova engine:

1. Criar classe que herda de `BaseEngine`.
2. Implementar os métodos obrigatórios.
3. Registrar no `EngineManager`.
4. (Opcional) Adicionar configurações em `AIModels/Engines/<nome>/`.

## 13.2 Novos Plugins

Para criar um plugin:

1. Criar classe que herda de `PluginBase`.
2. Implementar `name()`, `version()`, `on_activate()`, `on_deactivate()`.
3. (Opcional) Registrar hooks e componentes UI.
4. Colocar na pasta `plugins/`.

## 13.3 Novos Formatos de Modelo

Para suportar um novo formato:

1. Adicionar detector no `scanner.py`.
2. Criar subpasta em `AIModels/Models/<formato>/`.
3. Atualizar schema do banco se necessário.
4. Verificar compatibilidade com engines existentes.

---

# 14. Decisões Técnicas (ADRs)

## ADR-001: Python como linguagem principal

**Contexto:** O ecossistema de IA é predominantemente Python.  
**Decisão:** Python 3.13+ para máxima compatibilidade com bibliotecas de ML/AI.  
**Consequência:** Acesso nativo a Transformers, PyTorch, ONNX Runtime, etc.

## ADR-002: PySide6 para interface

**Contexto:** Necessidade de interface nativa, performática e multiplataforma.  
**Decisão:** PySide6 (Qt 6) ao invés de Electron, Tkinter ou web.  
**Consequência:** UI nativa com boa performance. Curva de aprendizado moderada.

## ADR-003: SQLite como banco de dados

**Contexto:** Aplicação local, single-user, sem necessidade de servidor.  
**Decisão:** SQLite com WAL mode para persistência local.  
**Consequência:** Zero configuração. Backup simples (copiar arquivo). Limitado a single-writer.

## ADR-004: Workspace separado da aplicação

**Contexto:** Modelos podem ocupar dezenas/centenas de GB.  
**Decisão:** Separar AIModelHub (app) de AIModels (dados) fisicamente.  
**Consequência:** Flexibilidade de armazenamento. Pode apontar para disco externo. Update da app não afeta dados.

## ADR-005: Engine Abstraction Layer

**Contexto:** Múltiplas engines com APIs diferentes.  
**Decisão:** Criar camada de abstração com interface unificada.  
**Consequência:** Novas engines são adicionadas sem alterar o core. Usuário troca de engine sem fricção.

## ADR-006: Sistema de plugins

**Contexto:** Impossível prever todas as integrações que os usuários vão querer.  
**Decisão:** Arquitetura de plugins com hooks e registry.  
**Consequência:** Comunidade pode estender o OMNIA. Core permanece enxuto.

---

# 15. Glossário

| Termo | Definição |
|---|---|
| **AIModelHub** | Aplicação principal do OMNIA — contém toda a lógica, interface e gerenciamento. |
| **AIModels** | Diretório de dados (workspace) onde modelos, cache, logs e backups ficam armazenados. |
| **Engine** | Backend de inferência que executa modelos (ex: Ollama, llama.cpp, Transformers). |
| **EAL** | Engine Abstraction Layer — camada que unifica a interface de diferentes engines. |
| **Scanner** | Módulo que varre o workspace automaticamente para descobrir modelos instalados. |
| **Catálogo** | Biblioteca indexada de todos os modelos com busca, tags e favoritos. |
| **GGUF** | Formato de modelo quantizado usado por llama.cpp e derivados. |
| **Quantização** | Processo de reduzir a precisão dos pesos para diminuir o tamanho do modelo. |
| **Plugin** | Módulo externo que estende as funcionalidades do OMNIA via hooks. |
| **Hook** | Ponto de extensão onde plugins podem registrar callbacks. |
| **DAO** | Data Access Object — classe que encapsula o acesso ao banco de dados. |
| **RAG** | Retrieval-Augmented Generation — técnica que combina busca semântica com geração de texto. |
| **Workspace** | Diretório raiz do AIModels, contendo toda a estrutura de dados do OMNIA. |
| **Benchmark** | Teste de desempenho que mede métricas como tokens/s, RAM, VRAM, etc. |
| **Manifest** | Arquivo declarativo de um plugin, listando suas permissões e dependências. |

---

# Referências

- [README.md](../README.md) — Visão geral do projeto
- [ROADMAP.md](ROADMAP.md) — Fases de desenvolvimento
- [Python 3.13](https://docs.python.org/3.13/)
- [PySide6](https://doc.qt.io/qtforpython-6/)
- [SQLite](https://www.sqlite.org/docs.html)
- [Ollama](https://ollama.ai)
- [Hugging Face](https://huggingface.co)
- [llama.cpp](https://github.com/ggerganov/llama.cpp)

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*

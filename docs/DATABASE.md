# OMNIA

## Documentação do Banco de Dados

**Versão:** 1.0  
**Tecnologia:** SQLite 3  
**Modo:** WAL (Write-Ahead Logging)  
**Última atualização:** 2026  

---

# 1. Visão Geral

O OMNIA utiliza **SQLite** como banco de dados principal, armazenando todas as informações sobre modelos, engines, benchmarks, downloads, configurações e histórico de operações.

## Características

| Característica | Valor |
|----------------|-------|
| **Banco** | SQLite 3 |
| **Modo** | WAL (Write-Ahead Logging) |
| **Encoding** | UTF-8 |
| **Localização** | \`AIModels/database/omnia.db\` |
| **Backup** | \`AIModels/Backups/db/\` |

## Vantagens do SQLite

* ✅ **Zero configuração** — Não requer servidor
* ✅ **Portabilidade** — Banco é um único arquivo
* ✅ **Performance** — Excelente para aplicações locais
* ✅ **Confiabilidade** — ACID compliant
* ✅ **Backup simples** — Copiar o arquivo
* ✅ **Integração Python** — Biblioteca padrão

## Arquivos do Banco

\`\`\`
AIModels/
├── database/
│   ├── omnia.db           # Banco principal
│   ├── omnia.db-wal       # Write-Ahead Log
│   └── omnia.db-shm       # Shared Memory
└── Backups/
    └── db/
        ├── omnia_2026-01-15_120000.db
        └── omnia_2026-01-14_120000.db
\`\`\`

---

# 2. Tecnologia

## Configuração de Conexão

\`\`\`python
import sqlite3
from pathlib import Path

def get_connection(db_path: Path) -> sqlite3.Connection:
    """Cria conexão otimizada com o banco."""
    conn = sqlite3.connect(
        db_path,
        check_same_thread=False,
        timeout=30.0,
    )
    
    # Configurações de performance
    conn.execute("PRAGMA journal_mode=WAL")
    conn.execute("PRAGMA synchronous=NORMAL")
    conn.execute("PRAGMA cache_size=-64000")  # 64MB cache
    conn.execute("PRAGMA temp_store=MEMORY")
    conn.execute("PRAGMA mmap_size=268435456")  # 256MB mmap
    
    # Foreign keys
    conn.execute("PRAGMA foreign_keys=ON")
    
    # Row factory para dicts
    conn.row_factory = sqlite3.Row
    
    return conn
\`\`\`

## PRAGMAs Utilizados

| PRAGMA | Valor | Descrição |
|--------|-------|-----------|
| \`journal_mode\` | WAL | Write-Ahead Logging para melhor concorrência |
| \`synchronous\` | NORMAL | Balanço entre segurança e performance |
| \`cache_size\` | -64000 | 64MB de cache em memória |
| \`temp_store\` | MEMORY | Tabelas temporárias em memória |
| \`mmap_size\` | 256MB | Memory-mapped I/O |
| \`foreign_keys\` | ON | Habilita verificação de chaves estrangeiras |

---

# 3. Schema Completo

## Diagrama ER

\`\`\`
┌─────────────────┐       ┌─────────────────┐
│     models      │       │      tags       │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ name            │       │ name            │
│ format          │       └────────┬────────┘
│ architecture    │                │
│ quantization    │       ┌────────┴────────┐
│ size_bytes      │       │   model_tags    │
│ path            │       ├─────────────────┤
│ manufacturer    │◄──────│ model_id (FK)   │
│ description     │       │ tag_id (FK)     │
│ is_favorite     │       └─────────────────┘
│ metadata        │
└────────┬────────┘
         │
         │        ┌─────────────────┐
         │        │     engines     │
         │        ├─────────────────┤
         │        │ id (PK)         │
         │        │ name            │
         │        │ version         │
         │        │ path            │
         │        │ is_active       │
         │        │ config          │
         │        └────────┬────────┘
         │                 │
         ▼                 ▼
┌─────────────────────────────────────┐
│            benchmarks               │
├─────────────────────────────────────┤
│ id (PK)                             │
│ model_id (FK) ──────────────────────┤
│ engine_id (FK) ─────────────────────┤
│ load_time_ms                        │
│ tokens_per_sec                      │
│ ram_usage_mb                        │
│ vram_usage_mb                       │
│ cpu_percent                         │
│ gpu_percent                         │
│ created_at                          │
└─────────────────────────────────────┘

┌─────────────────┐       ┌─────────────────┐
│    downloads    │       │     history     │
├─────────────────┤       ├─────────────────┤
│ id (PK)         │       │ id (PK)         │
│ url             │       │ model_id (FK)   │
│ model_name      │       │ engine_id (FK)  │
│ status          │       │ action          │
│ progress        │       │ details         │
│ size_bytes      │       │ created_at      │
│ created_at      │       └─────────────────┘
│ completed_at    │
└─────────────────┘       ┌─────────────────┐
                          │    settings     │
┌─────────────────┐       ├─────────────────┤
│     agents      │       │ key (PK)        │
├─────────────────┤       │ value           │
│ id (PK)         │       │ category        │
│ name            │       │ updated_at      │
│ type            │       └─────────────────┘
│ system_prompt   │
│ model_id (FK)   │
│ config          │
│ is_active       │
└─────────────────┘
\`\`\`

---

# 4. Tabelas Detalhadas

## 4.1 models

Armazena informações sobre todos os modelos de IA registrados.

\`\`\`sql
CREATE TABLE models (
    -- Identificação
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    
    -- Especificações técnicas
    format          TEXT NOT NULL,           -- huggingface, gguf, onnx, tensorrt, mlx
    architecture    TEXT,                    -- llama, mistral, phi, gemma, qwen...
    quantization    TEXT,                    -- q4_0, q4_k_m, q5_k_m, q8_0, fp16, fp32
    size_bytes      INTEGER,                 -- Tamanho em bytes
    context_length  INTEGER DEFAULT 4096,    -- Tamanho máximo de contexto
    
    -- Localização
    path            TEXT NOT NULL UNIQUE,    -- Caminho absoluto do arquivo
    
    -- Metadados
    manufacturer    TEXT,                    -- Meta, Mistral AI, Google, etc.
    description     TEXT,                    -- Descrição do modelo
    license         TEXT,                    -- Licença (MIT, Apache, etc.)
    
    -- Organização
    is_favorite     BOOLEAN DEFAULT 0,
    is_hidden       BOOLEAN DEFAULT 0,
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used_at    DATETIME,
    
    -- Dados extras (JSON)
    metadata        TEXT,                    -- {"parameters": "7B", "family": "llama"}
    
    -- Constraints
    CHECK (format IN ('huggingface', 'gguf', 'onnx', 'tensorrt', 'mlx', 'custom'))
);

-- Índices
CREATE INDEX idx_models_format ON models(format);
CREATE INDEX idx_models_architecture ON models(architecture);
CREATE INDEX idx_models_manufacturer ON models(manufacturer);
CREATE INDEX idx_models_favorite ON models(is_favorite) WHERE is_favorite = 1;
CREATE INDEX idx_models_last_used ON models(last_used_at DESC);
\`\`\`

### Campos

| Campo | Tipo | Descrição |
|-------|------|-----------|
| \`id\` | TEXT | UUID único do modelo |
| \`name\` | TEXT | Nome de exibição |
| \`format\` | TEXT | Formato do arquivo (gguf, huggingface, etc.) |
| \`architecture\` | TEXT | Arquitetura base (llama, mistral, etc.) |
| \`quantization\` | TEXT | Tipo de quantização |
| \`size_bytes\` | INTEGER | Tamanho do arquivo em bytes |
| \`context_length\` | INTEGER | Tamanho máximo de contexto |
| \`path\` | TEXT | Caminho absoluto no filesystem |
| \`manufacturer\` | TEXT | Empresa/organização criadora |
| \`description\` | TEXT | Descrição textual |
| \`license\` | TEXT | Licença de uso |
| \`is_favorite\` | BOOLEAN | Marcado como favorito |
| \`is_hidden\` | BOOLEAN | Oculto da listagem |
| \`metadata\` | TEXT | JSON com dados extras |

---

## 4.2 tags

Sistema de etiquetas para organização dos modelos.

\`\`\`sql
CREATE TABLE tags (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    name        TEXT UNIQUE NOT NULL,
    color       TEXT DEFAULT '#6366f1',      -- Cor hex para UI
    icon        TEXT,                        -- Emoji ou ícone
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índice
CREATE INDEX idx_tags_name ON tags(name);
\`\`\`

---

## 4.3 model_tags

Relação muitos-para-muitos entre modelos e tags.

\`\`\`sql
CREATE TABLE model_tags (
    model_id    TEXT NOT NULL,
    tag_id      INTEGER NOT NULL,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    PRIMARY KEY (model_id, tag_id),
    FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE,
    FOREIGN KEY (tag_id) REFERENCES tags(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_model_tags_model ON model_tags(model_id);
CREATE INDEX idx_model_tags_tag ON model_tags(tag_id);
\`\`\`

---

## 4.4 engines

Engines de inferência registradas no sistema.

\`\`\`sql
CREATE TABLE engines (
    id              TEXT PRIMARY KEY,        -- ollama, transformers, vllm...
    name            TEXT NOT NULL,           -- Nome de exibição
    version         TEXT,                    -- Versão detectada
    path            TEXT,                    -- Caminho do executável
    
    -- Status
    is_active       BOOLEAN DEFAULT 1,       -- Habilitada para uso
    is_available    BOOLEAN DEFAULT 0,       -- Detectada no sistema
    
    -- Formatos suportados
    supported_formats TEXT,                  -- JSON array: ["gguf", "huggingface"]
    
    -- Configuração (JSON)
    config          TEXT,                    -- {"api_url": "http://localhost:11434"}
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_check_at   DATETIME                 -- Última verificação de disponibilidade
);
\`\`\`

### Engines Padrão

| ID | Nome | Formatos |
|----|------|----------|
| \`ollama\` | Ollama | gguf |
| \`transformers\` | Transformers | huggingface |
| \`vllm\` | vLLM | huggingface |
| \`llamacpp\` | llama.cpp | gguf |
| \`lmstudio\` | LM Studio | gguf |
| \`airllm\` | AirLLM | huggingface |

---

## 4.5 benchmarks

Resultados de benchmarks de performance.

\`\`\`sql
CREATE TABLE benchmarks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Referências
    model_id        TEXT NOT NULL,
    engine_id       TEXT NOT NULL,
    
    -- Métricas de tempo
    load_time_ms    REAL,                    -- Tempo de carregamento
    first_token_ms  REAL,                    -- Tempo até primeiro token
    
    -- Métricas de throughput
    tokens_per_sec  REAL,                    -- Tokens por segundo
    prompt_tokens   INTEGER,                 -- Tokens do prompt
    completion_tokens INTEGER,               -- Tokens gerados
    
    -- Métricas de recurso
    ram_usage_mb    REAL,                    -- Uso de RAM
    vram_usage_mb   REAL,                    -- Uso de VRAM
    cpu_percent     REAL,                    -- % CPU utilizado
    gpu_percent     REAL,                    -- % GPU utilizado
    gpu_temp_c      REAL,                    -- Temperatura da GPU
    
    -- Configuração do teste
    batch_size      INTEGER DEFAULT 1,
    context_length  INTEGER,
    temperature     REAL DEFAULT 0.7,
    
    -- Ambiente
    gpu_name        TEXT,                    -- Nome da GPU
    gpu_memory_mb   INTEGER,                 -- Memória total da GPU
    cpu_name        TEXT,                    -- Nome do CPU
    ram_total_mb    INTEGER,                 -- RAM total
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    -- Dados extras
    metadata        TEXT,                    -- JSON com detalhes adicionais
    
    FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE CASCADE,
    FOREIGN KEY (engine_id) REFERENCES engines(id) ON DELETE SET NULL
);

-- Índices
CREATE INDEX idx_benchmarks_model ON benchmarks(model_id);
CREATE INDEX idx_benchmarks_engine ON benchmarks(engine_id);
CREATE INDEX idx_benchmarks_date ON benchmarks(created_at DESC);
CREATE INDEX idx_benchmarks_tps ON benchmarks(tokens_per_sec DESC);
\`\`\`

---

## 4.6 downloads

Fila e histórico de downloads de modelos.

\`\`\`sql
CREATE TABLE downloads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Origem
    url             TEXT NOT NULL,
    source          TEXT DEFAULT 'huggingface',  -- huggingface, direct, custom
    
    -- Identificação
    model_name      TEXT,
    file_name       TEXT,
    
    -- Status
    status          TEXT DEFAULT 'pending',  -- pending, downloading, paused, completed, failed
    progress        REAL DEFAULT 0,          -- 0.0 a 1.0
    
    -- Tamanho
    size_bytes      INTEGER,                 -- Tamanho total
    downloaded_bytes INTEGER DEFAULT 0,      -- Bytes baixados
    
    -- Velocidade
    speed_bps       INTEGER,                 -- Bytes por segundo atual
    eta_seconds     INTEGER,                 -- Tempo estimado restante
    
    -- Verificação
    expected_hash   TEXT,                    -- SHA256 esperado
    actual_hash     TEXT,                    -- SHA256 calculado
    
    -- Caminhos
    temp_path       TEXT,                    -- Caminho temporário
    final_path      TEXT,                    -- Destino final
    
    -- Retry
    retry_count     INTEGER DEFAULT 0,
    max_retries     INTEGER DEFAULT 3,
    error_message   TEXT,
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    started_at      DATETIME,
    completed_at    DATETIME,
    
    CHECK (status IN ('pending', 'downloading', 'paused', 'completed', 'failed', 'cancelled'))
);

-- Índices
CREATE INDEX idx_downloads_status ON downloads(status);
CREATE INDEX idx_downloads_date ON downloads(created_at DESC);
\`\`\`

---

## 4.7 history

Histórico de ações do sistema para auditoria.

\`\`\`sql
CREATE TABLE history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    
    -- Contexto
    model_id    TEXT,
    engine_id   TEXT,
    
    -- Ação
    action      TEXT NOT NULL,               -- load, unload, inference, benchmark, download, delete...
    category    TEXT DEFAULT 'general',      -- model, engine, system, download, benchmark
    
    -- Detalhes
    details     TEXT,                        -- JSON com detalhes da ação
    duration_ms INTEGER,                     -- Duração da ação em ms
    
    -- Resultado
    success     BOOLEAN DEFAULT 1,
    error       TEXT,
    
    -- Timestamp
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE SET NULL,
    FOREIGN KEY (engine_id) REFERENCES engines(id) ON DELETE SET NULL
);

-- Índices
CREATE INDEX idx_history_action ON history(action);
CREATE INDEX idx_history_model ON history(model_id);
CREATE INDEX idx_history_date ON history(created_at DESC);
CREATE INDEX idx_history_category ON history(category);
\`\`\`

### Ações Registradas

| Categoria | Ações |
|-----------|-------|
| \`model\` | load, unload, scan, favorite, hide, delete |
| \`engine\` | register, activate, deactivate, check |
| \`download\` | start, pause, resume, complete, fail, cancel |
| \`benchmark\` | start, complete, fail |
| \`system\` | startup, shutdown, backup, restore, migrate |

---

## 4.8 settings

Configurações do sistema em formato chave-valor.

\`\`\`sql
CREATE TABLE settings (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    type        TEXT DEFAULT 'string',       -- string, integer, float, boolean, json
    category    TEXT DEFAULT 'general',      -- general, ui, engine, download, benchmark
    description TEXT,
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Índice
CREATE INDEX idx_settings_category ON settings(category);
\`\`\`

### Configurações Padrão

| Chave | Valor | Categoria |
|-------|-------|-----------|
| \`workspace_path\` | \`~/AIModels\` | general |
| \`default_engine\` | \`ollama\` | engine |
| \`theme\` | \`system\` | ui |
| \`language\` | \`pt-BR\` | ui |
| \`auto_scan\` | \`true\` | general |
| \`scan_interval_hours\` | \`24\` | general |
| \`max_parallel_downloads\` | \`2\` | download |
| \`auto_backup\` | \`true\` | general |
| \`backup_interval_hours\` | \`24\` | general |
| \`keep_backups\` | \`7\` | general |

---

## 4.9 agents

Agentes de IA especializados.

\`\`\`sql
CREATE TABLE agents (
    id              TEXT PRIMARY KEY,
    
    -- Identificação
    name            TEXT NOT NULL,
    type            TEXT NOT NULL,           -- programmer, writer, translator, assistant...
    description     TEXT,
    icon            TEXT,                    -- Emoji ou ícone
    
    -- Configuração
    system_prompt   TEXT NOT NULL,           -- Prompt de sistema
    model_id        TEXT,                    -- Modelo preferido
    
    -- Parâmetros
    temperature     REAL DEFAULT 0.7,
    max_tokens      INTEGER DEFAULT 2048,
    top_p           REAL DEFAULT 0.9,
    
    -- Status
    is_active       BOOLEAN DEFAULT 1,
    is_builtin      BOOLEAN DEFAULT 0,       -- Agente padrão do sistema
    
    -- Uso
    use_count       INTEGER DEFAULT 0,
    last_used_at    DATETIME,
    
    -- Config extra (JSON)
    config          TEXT,
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE SET NULL
);

-- Índices
CREATE INDEX idx_agents_type ON agents(type);
CREATE INDEX idx_agents_active ON agents(is_active) WHERE is_active = 1;
\`\`\`

---

## 4.10 conversations

Histórico de conversas com agentes (futuro).

\`\`\`sql
CREATE TABLE conversations (
    id              TEXT PRIMARY KEY,
    agent_id        TEXT,
    model_id        TEXT,
    title           TEXT,
    
    -- Contadores
    message_count   INTEGER DEFAULT 0,
    token_count     INTEGER DEFAULT 0,
    
    -- Status
    is_archived     BOOLEAN DEFAULT 0,
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (agent_id) REFERENCES agents(id) ON DELETE SET NULL,
    FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE SET NULL
);

CREATE TABLE messages (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    conversation_id TEXT NOT NULL,
    
    -- Conteúdo
    role            TEXT NOT NULL,           -- user, assistant, system
    content         TEXT NOT NULL,
    
    -- Métricas
    token_count     INTEGER,
    generation_time_ms INTEGER,
    
    -- Timestamps
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (conversation_id) REFERENCES conversations(id) ON DELETE CASCADE
);

-- Índices
CREATE INDEX idx_conversations_agent ON conversations(agent_id);
CREATE INDEX idx_conversations_date ON conversations(updated_at DESC);
CREATE INDEX idx_messages_conversation ON messages(conversation_id);
\`\`\`

---

# 5. Relacionamentos

## Diagrama de Relacionamentos

\`\`\`
models ─────────────┬─────────────────────┐
   │                │                     │
   │ 1:N            │ N:M                 │ 1:N
   │                │                     │
   ▼                ▼                     ▼
benchmarks      model_tags              agents
   │                │
   │ N:1            │ N:1
   │                │
   ▼                ▼
engines           tags


downloads (standalone)
history (referencia models, engines)
settings (standalone)
conversations ──► messages (1:N)
\`\`\`

## Foreign Keys

| Tabela | Campo | Referencia | On Delete |
|--------|-------|------------|-----------|
| \`model_tags\` | \`model_id\` | \`models.id\` | CASCADE |
| \`model_tags\` | \`tag_id\` | \`tags.id\` | CASCADE |
| \`benchmarks\` | \`model_id\` | \`models.id\` | CASCADE |
| \`benchmarks\` | \`engine_id\` | \`engines.id\` | SET NULL |
| \`history\` | \`model_id\` | \`models.id\` | SET NULL |
| \`history\` | \`engine_id\` | \`engines.id\` | SET NULL |
| \`agents\` | \`model_id\` | \`models.id\` | SET NULL |
| \`messages\` | \`conversation_id\` | \`conversations.id\` | CASCADE |

---

# 6. Índices

## Índices por Tabela

### models
\`\`\`sql
CREATE INDEX idx_models_format ON models(format);
CREATE INDEX idx_models_architecture ON models(architecture);
CREATE INDEX idx_models_manufacturer ON models(manufacturer);
CREATE INDEX idx_models_favorite ON models(is_favorite) WHERE is_favorite = 1;
CREATE INDEX idx_models_last_used ON models(last_used_at DESC);
CREATE INDEX idx_models_size ON models(size_bytes);
\`\`\`

### benchmarks
\`\`\`sql
CREATE INDEX idx_benchmarks_model ON benchmarks(model_id);
CREATE INDEX idx_benchmarks_engine ON benchmarks(engine_id);
CREATE INDEX idx_benchmarks_date ON benchmarks(created_at DESC);
CREATE INDEX idx_benchmarks_tps ON benchmarks(tokens_per_sec DESC);
\`\`\`

### downloads
\`\`\`sql
CREATE INDEX idx_downloads_status ON downloads(status);
CREATE INDEX idx_downloads_date ON downloads(created_at DESC);
\`\`\`

### history
\`\`\`sql
CREATE INDEX idx_history_action ON history(action);
CREATE INDEX idx_history_model ON history(model_id);
CREATE INDEX idx_history_date ON history(created_at DESC);
CREATE INDEX idx_history_category ON history(category);
\`\`\`

## Índices Parciais

\`\`\`sql
-- Apenas modelos favoritos
CREATE INDEX idx_models_favorite ON models(is_favorite) WHERE is_favorite = 1;

-- Apenas engines ativas
CREATE INDEX idx_engines_active ON engines(is_active) WHERE is_active = 1;

-- Downloads pendentes/ativos
CREATE INDEX idx_downloads_pending ON downloads(status) 
    WHERE status IN ('pending', 'downloading');
\`\`\`

---

# 7. Migrações

## Sistema de Migrações

\`\`\`python
# database/migrations.py

class MigrationManager:
    """Gerencia migrações do banco de dados."""
    
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
        self._ensure_migrations_table()
    
    def _ensure_migrations_table(self) -> None:
        """Cria tabela de controle de migrações."""
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS _migrations (
                id          INTEGER PRIMARY KEY,
                name        TEXT UNIQUE NOT NULL,
                applied_at  DATETIME DEFAULT CURRENT_TIMESTAMP
            )
        """)
    
    def get_pending(self) -> list[Migration]:
        """Retorna migrações pendentes."""
        applied = self._get_applied()
        return [m for m in ALL_MIGRATIONS if m.name not in applied]
    
    def apply_all(self) -> int:
        """Aplica todas as migrações pendentes."""
        count = 0
        for migration in self.get_pending():
            self._apply(migration)
            count += 1
        return count
\`\`\`

## Estrutura de Arquivos

\`\`\`
database/
├── migrations/
│   ├── __init__.py
│   ├── 001_initial_schema.py
│   ├── 002_add_agents.py
│   ├── 003_add_conversations.py
│   ├── 004_add_benchmarks_gpu.py
│   └── ...
└── migrations.py
\`\`\`

## Exemplo de Migração

\`\`\`python
# migrations/002_add_agents.py

from database.migrations import Migration

migration = Migration(
    name="002_add_agents",
    description="Adiciona tabela de agentes",
    
    up="""
        CREATE TABLE agents (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            type TEXT NOT NULL,
            system_prompt TEXT NOT NULL,
            model_id TEXT,
            is_active BOOLEAN DEFAULT 1,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (model_id) REFERENCES models(id) ON DELETE SET NULL
        );
        
        CREATE INDEX idx_agents_type ON agents(type);
    """,
    
    down="""
        DROP INDEX IF EXISTS idx_agents_type;
        DROP TABLE IF EXISTS agents;
    """
)
\`\`\`

---

# 8. Data Access Objects (DAOs)

## Estrutura

\`\`\`
database/
├── connection.py      # Gerenciamento de conexão
├── base_dao.py        # Classe base para DAOs
├── dao_models.py      # DAO de modelos
├── dao_engines.py     # DAO de engines
├── dao_benchmarks.py  # DAO de benchmarks
├── dao_downloads.py   # DAO de downloads
├── dao_history.py     # DAO de histórico
├── dao_settings.py    # DAO de configurações
└── dao_agents.py      # DAO de agentes
\`\`\`

## Base DAO

\`\`\`python
# database/base_dao.py

from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from dataclasses import dataclass

T = TypeVar("T")

class BaseDAO(ABC, Generic[T]):
    """Classe base para todos os DAOs."""
    
    def __init__(self, conn: sqlite3.Connection):
        self.conn = conn
    
    @abstractmethod
    def get_by_id(self, id: str) -> T | None:
        """Busca registro por ID."""
        pass
    
    @abstractmethod
    def get_all(self) -> list[T]:
        """Retorna todos os registros."""
        pass
    
    @abstractmethod
    def create(self, entity: T) -> T:
        """Cria novo registro."""
        pass
    
    @abstractmethod
    def update(self, entity: T) -> T:
        """Atualiza registro existente."""
        pass
    
    @abstractmethod
    def delete(self, id: str) -> bool:
        """Remove registro por ID."""
        pass
\`\`\`

## Exemplo: ModelDAO

\`\`\`python
# database/dao_models.py

@dataclass
class Model:
    id: str
    name: str
    format: str
    architecture: str | None
    quantization: str | None
    size_bytes: int | None
    path: str
    manufacturer: str | None
    description: str | None
    is_favorite: bool
    created_at: datetime
    updated_at: datetime
    last_used_at: datetime | None
    metadata: dict | None


class ModelDAO(BaseDAO[Model]):
    """DAO para operações com modelos."""
    
    def get_by_id(self, id: str) -> Model | None:
        cursor = self.conn.execute(
            "SELECT * FROM models WHERE id = ?", (id,)
        )
        row = cursor.fetchone()
        return self._row_to_model(row) if row else None
    
    def get_all(
        self,
        *,
        format: str | None = None,
        architecture: str | None = None,
        favorites_only: bool = False,
        order_by: str = "name",
        limit: int | None = None,
    ) -> list[Model]:
        query = "SELECT * FROM models WHERE 1=1"
        params = []
        
        if format:
            query += " AND format = ?"
            params.append(format)
        
        if architecture:
            query += " AND architecture = ?"
            params.append(architecture)
        
        if favorites_only:
            query += " AND is_favorite = 1"
        
        query += f" ORDER BY {order_by}"
        
        if limit:
            query += " LIMIT ?"
            params.append(limit)
        
        cursor = self.conn.execute(query, params)
        return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def search(self, query: str) -> list[Model]:
        """Busca modelos por nome ou descrição."""
        cursor = self.conn.execute(
            """
            SELECT * FROM models 
            WHERE name LIKE ? OR description LIKE ?
            ORDER BY name
            """,
            (f"%{query}%", f"%{query}%")
        )
        return [self._row_to_model(row) for row in cursor.fetchall()]
    
    def get_by_format(self, format: str) -> list[Model]:
        return self.get_all(format=format)
    
    def get_favorites(self) -> list[Model]:
        return self.get_all(favorites_only=True)
    
    def get_recent(self, limit: int = 10) -> list[Model]:
        return self.get_all(order_by="last_used_at DESC", limit=limit)
    
    def toggle_favorite(self, id: str) -> bool:
        self.conn.execute(
            "UPDATE models SET is_favorite = NOT is_favorite WHERE id = ?",
            (id,)
        )
        self.conn.commit()
        return True
    
    def update_last_used(self, id: str) -> None:
        self.conn.execute(
            "UPDATE models SET last_used_at = CURRENT_TIMESTAMP WHERE id = ?",
            (id,)
        )
        self.conn.commit()
\`\`\`

---

# 9. Queries Comuns

## Modelos

\`\`\`sql
-- Buscar modelos por formato
SELECT * FROM models WHERE format = 'gguf' ORDER BY name;

-- Modelos favoritos
SELECT * FROM models WHERE is_favorite = 1 ORDER BY name;

-- Modelos recentes
SELECT * FROM models 
WHERE last_used_at IS NOT NULL 
ORDER BY last_used_at DESC LIMIT 10;

-- Busca por texto
SELECT * FROM models 
WHERE name LIKE '%llama%' OR description LIKE '%llama%';

-- Modelos com tags específicas
SELECT DISTINCT m.* FROM models m
JOIN model_tags mt ON m.id = mt.model_id
JOIN tags t ON mt.tag_id = t.id
WHERE t.name IN ('coding', 'fast');

-- Estatísticas por formato
SELECT format, COUNT(*) as count, SUM(size_bytes) as total_size
FROM models GROUP BY format;
\`\`\`

## Benchmarks

\`\`\`sql
-- Melhor benchmark por modelo
SELECT m.name, b.tokens_per_sec, e.name as engine
FROM benchmarks b
JOIN models m ON b.model_id = m.id
JOIN engines e ON b.engine_id = e.id
WHERE b.id IN (
    SELECT id FROM benchmarks b2 
    WHERE b2.model_id = b.model_id 
    ORDER BY tokens_per_sec DESC LIMIT 1
);

-- Média de performance por engine
SELECT e.name, AVG(b.tokens_per_sec) as avg_tps
FROM benchmarks b
JOIN engines e ON b.engine_id = e.id
GROUP BY e.id;

-- Histórico de benchmarks de um modelo
SELECT * FROM benchmarks 
WHERE model_id = ? 
ORDER BY created_at DESC;
\`\`\`

## Downloads

\`\`\`sql
-- Downloads ativos
SELECT * FROM downloads 
WHERE status IN ('pending', 'downloading')
ORDER BY created_at;

-- Downloads falhados para retry
SELECT * FROM downloads 
WHERE status = 'failed' AND retry_count < max_retries;

-- Estatísticas de download
SELECT 
    status, 
    COUNT(*) as count,
    SUM(size_bytes) as total_bytes
FROM downloads 
GROUP BY status;
\`\`\`

---

# 10. Backup & Recuperação

## Backup Automático

\`\`\`python
# core/backup.py

import shutil
from datetime import datetime
from pathlib import Path

class BackupManager:
    """Gerencia backups do banco de dados."""
    
    def __init__(self, db_path: Path, backup_dir: Path):
        self.db_path = db_path
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)
    
    def create_backup(self) -> Path:
        """Cria um backup do banco."""
        timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
        backup_path = self.backup_dir / f"omnia_{timestamp}.db"
        
        # Checkpoint WAL antes do backup
        conn = sqlite3.connect(self.db_path)
        conn.execute("PRAGMA wal_checkpoint(TRUNCATE)")
        conn.close()
        
        # Copiar arquivo
        shutil.copy2(self.db_path, backup_path)
        
        # Limpar backups antigos
        self._cleanup_old_backups()
        
        return backup_path
    
    def restore_backup(self, backup_path: Path) -> bool:
        """Restaura um backup."""
        if not backup_path.exists():
            raise FileNotFoundError(f"Backup not found: {backup_path}")
        
        # Fazer backup do atual primeiro
        self.create_backup()
        
        # Restaurar
        shutil.copy2(backup_path, self.db_path)
        return True
    
    def _cleanup_old_backups(self, keep: int = 7) -> None:
        """Remove backups antigos, mantendo os N mais recentes."""
        backups = sorted(
            self.backup_dir.glob("omnia_*.db"),
            key=lambda p: p.stat().st_mtime,
            reverse=True
        )
        
        for backup in backups[keep:]:
            backup.unlink()
\`\`\`

## Backup Manual via SQL

\`\`\`sql
-- Criar backup via SQL
VACUUM INTO '/path/to/backup.db';
\`\`\`

---

# 11. Performance

## Otimizações Implementadas

| Técnica | Descrição |
|---------|-----------|
| **WAL Mode** | Permite leituras concorrentes durante escritas |
| **Cache 64MB** | Reduz I/O de disco |
| **Memory-mapped I/O** | Acesso mais rápido a dados frequentes |
| **Índices parciais** | Índices menores e mais eficientes |
| **Prepared statements** | Reutilização de queries compiladas |

## Análise de Queries

\`\`\`sql
-- Habilitar análise
PRAGMA query_only = ON;

-- Analisar query
EXPLAIN QUERY PLAN
SELECT * FROM models WHERE format = 'gguf';

-- Estatísticas de índices
SELECT * FROM sqlite_stat1;
\`\`\`

## Manutenção Periódica

\`\`\`sql
-- Reconstruir índices
REINDEX;

-- Analisar estatísticas
ANALYZE;

-- Compactar banco
VACUUM;
\`\`\`

---

# 12. Manutenção

## Tarefas Automáticas

| Tarefa | Frequência | Descrição |
|--------|------------|-----------|
| Backup | Diário | Cópia do banco para Backups/db/ |
| Cleanup history | Semanal | Remove histórico > 30 dias |
| Cleanup downloads | Diário | Remove downloads cancelled/failed antigos |
| ANALYZE | Semanal | Atualiza estatísticas de índices |
| Integrity check | Mensal | Verifica integridade do banco |

## Scripts de Manutenção

\`\`\`python
# Limpeza de histórico antigo
def cleanup_old_history(conn: sqlite3.Connection, days: int = 30) -> int:
    cursor = conn.execute(
        """
        DELETE FROM history 
        WHERE created_at < datetime('now', ?)
        """,
        (f"-{days} days",)
    )
    conn.commit()
    return cursor.rowcount

# Verificação de integridade
def check_integrity(conn: sqlite3.Connection) -> bool:
    result = conn.execute("PRAGMA integrity_check").fetchone()
    return result[0] == "ok"

# Otimização
def optimize(conn: sqlite3.Connection) -> None:
    conn.execute("ANALYZE")
    conn.execute("PRAGMA optimize")
\`\`\`

## Monitoramento

\`\`\`sql
-- Tamanho do banco
SELECT page_count * page_size as size_bytes 
FROM pragma_page_count(), pragma_page_size();

-- Número de registros por tabela
SELECT 'models' as table_name, COUNT(*) as count FROM models
UNION ALL
SELECT 'benchmarks', COUNT(*) FROM benchmarks
UNION ALL
SELECT 'downloads', COUNT(*) FROM downloads
UNION ALL
SELECT 'history', COUNT(*) FROM history;

-- Espaço livre
SELECT freelist_count * page_size as free_bytes 
FROM pragma_freelist_count(), pragma_page_size();
\`\`\`

---

# Referências

* [SQLite Documentation](https://www.sqlite.org/docs.html)
* [SQLite WAL Mode](https://www.sqlite.org/wal.html)
* [Python sqlite3](https://docs.python.org/3/library/sqlite3.html)
* [ARCHITECTURE.md](ARCHITECTURE.md)

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

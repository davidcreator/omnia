"""
Schema do banco de dados SQLite do AIModelHub.
Define todas as tabelas e índices do sistema.
"""

# SQL completo de criação do schema inicial
SCHEMA_SQL = """

-- ─────────────────────────────────────────
-- Tabela de controle de migrações
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS _migrations (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    version     INTEGER NOT NULL UNIQUE,
    name        TEXT NOT NULL,
    applied_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- Modelos
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS models (
    id              TEXT PRIMARY KEY,
    name            TEXT NOT NULL,
    format          TEXT NOT NULL,
    architecture    TEXT,
    quantization    TEXT,
    size_bytes      INTEGER,
    path            TEXT NOT NULL,
    manufacturer    TEXT,
    description     TEXT,
    is_favorite     BOOLEAN DEFAULT 0,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_used_at    DATETIME,
    metadata        TEXT
);

-- ─────────────────────────────────────────
-- Tags
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS tags (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    name    TEXT UNIQUE NOT NULL
);

-- Relação N:N Modelos ↔ Tags
CREATE TABLE IF NOT EXISTS model_tags (
    model_id    TEXT REFERENCES models(id) ON DELETE CASCADE,
    tag_id      INTEGER REFERENCES tags(id) ON DELETE CASCADE,
    PRIMARY KEY (model_id, tag_id)
);

-- ─────────────────────────────────────────
-- Engines
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS engines (
    id          TEXT PRIMARY KEY,
    name        TEXT NOT NULL,
    version     TEXT,
    path        TEXT,
    is_active   BOOLEAN DEFAULT 1,
    config      TEXT
);

-- ─────────────────────────────────────────
-- Benchmarks
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS benchmarks (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id        TEXT REFERENCES models(id) ON DELETE CASCADE,
    engine_id       TEXT REFERENCES engines(id) ON DELETE SET NULL,
    load_time_ms    REAL,
    tokens_per_sec  REAL,
    ram_usage_mb    REAL,
    vram_usage_mb   REAL,
    cpu_percent     REAL,
    gpu_percent     REAL,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    metadata        TEXT
);

-- ─────────────────────────────────────────
-- Downloads
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS downloads (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    url             TEXT NOT NULL,
    model_name      TEXT,
    status          TEXT DEFAULT 'pending',
    progress        REAL DEFAULT 0,
    size_bytes      INTEGER,
    created_at      DATETIME DEFAULT CURRENT_TIMESTAMP,
    completed_at    DATETIME
);

-- ─────────────────────────────────────────
-- Histórico
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS history (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    model_id    TEXT REFERENCES models(id) ON DELETE SET NULL,
    engine_id   TEXT REFERENCES engines(id) ON DELETE SET NULL,
    action      TEXT NOT NULL,
    details     TEXT,
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- Configurações
-- ─────────────────────────────────────────
CREATE TABLE IF NOT EXISTS settings (
    key         TEXT PRIMARY KEY,
    value       TEXT NOT NULL,
    category    TEXT DEFAULT 'general',
    updated_at  DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- ─────────────────────────────────────────
-- Índices
-- ─────────────────────────────────────────
CREATE INDEX IF NOT EXISTS idx_models_format
    ON models(format);

CREATE INDEX IF NOT EXISTS idx_models_favorite
    ON models(is_favorite);

CREATE INDEX IF NOT EXISTS idx_models_last_used
    ON models(last_used_at);

CREATE INDEX IF NOT EXISTS idx_benchmarks_model
    ON benchmarks(model_id);

CREATE INDEX IF NOT EXISTS idx_history_model
    ON history(model_id);

CREATE INDEX IF NOT EXISTS idx_history_created
    ON history(created_at);

CREATE INDEX IF NOT EXISTS idx_downloads_status
    ON downloads(status);

CREATE INDEX IF NOT EXISTS idx_settings_category
    ON settings(category);
"""
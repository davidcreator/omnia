# 📄 Relatório da Fase 1 — Fundação

**Projeto:** OMNIA — AIModelHub  
**Fase:** 1 — Fundação  
**Status:** ✅ Concluída  
**Data:** 2026-08-08  
**Autor:** David L. Almeida — David Creator  

---

## 1. Objetivo da Fase
Construir a base sólida do AIModelHub garantindo que todos os
módulos subsequentes tenham infraestrutura confiável para:

- Logging estruturado e rotativo
- Configurações centralizadas e hierárquicas
- Banco de dados SQLite com migrações versionadas
- Workspace AIModels verificado e estruturado
- Interface gráfica base inicializada
- Ciclo de vida da aplicação controlado

---

## 2. Decisões Técnicas Tomadas
### ADR-007: Criação da camada `shared/`

**Contexto:**  
Durante a implementação da Fase 1, identificou-se que arquivos
como `constants.py`, `logger.py` e `settings.py` precisavam ser
consumidos por **todos os módulos** do sistema (`app/`, `core/`,
`database/`, `engines/`, `ui/`, `plugins/`).

Mantê-los em `app/` criaria uma dependência circular onde `core/`
precisaria importar de `app/`, violando as regras de dependência
entre camadas.

**Decisão:**  
Criar a camada `shared/` como infraestrutura transversal,
separada de `app/` e sem dependência de nenhum outro módulo
interno.

**Consequências:**
- ✅ Elimina dependências circulares entre módulos
- ✅ Qualquer módulo pode importar de `shared/` sem restrições
- ✅ `app/` fica com responsabilidade única: lifecycle
- ✅ `core/` fica com responsabilidade única: negócios
- ⚠️ Diverge levemente da estrutura original do ARCHITECTURE.md
  (documentado e justificado)

**Regra de dependência do `shared/`:**
- ✅ Pode ser importado por qualquer módulo
- ❌ Não importa nada de `app/`, `core/`, `ui/`,
     `engines/` ou `plugins/`
- ❌ Não contém lógica de negócios

---

## 3. Estrutura Implementada
    AIModelHub/
    │
    ├── main.py # Ponto de entrada da aplicação
    ├── requirements.txt # Dependências do projeto
    │
    ├── shared/ # Infraestrutura compartilhada
    │ ├── init.py
    │ ├── constants.py # Paths, versões e defaults globais
    │ ├── logger.py # Sistema de log (loguru)
    │ └── settings.py # Singleton de configurações
    │
    ├── app/ # Lifecycle da aplicação
    │ ├── init.py
    │ ├── bootstrap.py # Sequência de inicialização (7 etapas)
    │ └── lifecycle.py # Startup, shutdown e erro crítico
    │
    ├── config/
    │ └── default.json # Configurações padrão do sistema
    │
    ├── database/ # Persistência local
    │ ├── init.py
    │ ├── connection.py # Conexão SQLite singleton + WAL
    │ ├── schema.py # Definição de tabelas e índices
    │ ├── migrations.py # Sistema de migrações versionadas
    │ └── migrations/
    │ └── 001_initial.sql # Migração inicial (registro histórico)
    │
    └── ui/ # Interface gráfica
    ├── init.py
    └── main_window.py # Janela principal (provisória)

---

## 4. Descrição dos Módulos

### 4.1 `main.py` — Ponto de Entrada

Responsabilidades:
- Instanciar `Bootstrap` e `Lifecycle`
- Chamar `bootstrap.initialize()` para executar o startup
- Conectar o sinal `aboutToQuit` do Qt ao `lifecycle.on_shutdown()`
- Retornar o código de saída via `sys.exit(app.exec())`
- Capturar erros críticos e delegar ao `lifecycle.on_error()`

---

### 4.2 `shared/constants.py` — Constantes Globais

Centraliza todos os valores fixos do sistema organizados
em grupos:

| Grupo | Constantes |
|---|---|
| Aplicação | `APP_NAME`, `APP_VERSION`, `APP_AUTHOR` |
| Paths internos | `APP_ROOT`, `CONFIG_DIR`, `MIGRATIONS_DIR` |
| Paths do SO | `USER_DATA_DIR`, `DATABASE_FILE`, `LOG_FILE` |
| Workspace | `DEFAULT_WORKSPACE`, `WORKSPACE_SUBDIRS` |
| Formatos | `SUPPORTED_FORMATS`, `FORMAT_EXTENSIONS` |
| Interface | `WINDOW_MIN_*`, `WINDOW_DEFAULT_*` |
| Logs | `LOG_LEVEL`, `LOG_MAX_SIZE`, `LOG_RETENTION` |

**Nota sobre `USER_DATA_DIR`:**  
Utiliza `platformdirs` para respeitar as convenções de cada SO:

| SO | Caminho |
|---|---|
| Windows | `C:\Users\<user>\AppData\Local\AIModelHub` |
| macOS | `~/Library/Application Support/AIModelHub` |
| Linux | `~/.local/share/AIModelHub` |

---

### 4.3 `shared/logger.py` — Sistema de Log
Tecnologia: **loguru**
Dois handlers configurados:

| Handler | Destino | Nível | Formato |
|---|---|---|---|
| Console | `stdout` | DEBUG | Colorido com timestamp |
| Arquivo | `logs/app.log` | DEBUG | Texto estruturado |

Configurações do handler de arquivo:

| Configuração | Valor |
|---|---|
| Rotação | 10 MB |
| Retenção | 30 dias |
| Encoding | UTF-8 |
| Thread-safe | ✅ (`enqueue=True`) |
| Stack trace | ✅ (`backtrace=True`) |
| Diagnóstico | ✅ (`diagnose=True`) |

---

### 4.4 `shared/settings.py` — Configurações

Implementa o padrão **Singleton** com hierarquia de três níveis:
    Prioridade 1 — Runtime (banco de dados)
    ↓ fallback
    Prioridade 2 — Defaults (default.json)
    ↓ fallback
    Prioridade 3 — Hardcoded (código)

Funcionalidades:
- Acesso por **notação de ponto**: `settings.get("workspace.path")`
- Definição em runtime: `settings.set("general.theme", "light")`
- Atalhos tipados: `settings.workspace_path`, `settings.theme`
- Expansão automática de `~` em paths

---

### 4.5 `app/bootstrap.py` — Inicialização

Executa **7 etapas sequenciais** de inicialização:

| Etapa | Método | Responsabilidade |
|---|---|---|
| 1 | `_step_logger()` | Configura o sistema de log |
| 2 | `_step_system_dirs()` | Cria diretórios internos do sistema |
| 3 | `_step_database()` | Inicializa SQLite e aplica migrações |
| 4 | `_step_settings()` | Carrega configurações padrão |
| 5 | `_step_workspace()` | Verifica/cria workspace AIModels |
| 6 | `_step_qt()` | Cria a instância do QApplication |
| 7 | `_step_ui()` | Inicializa e exibe a janela principal |

**Comportamento do workspace na inicialização:**
- Cria todos os 20 subdiretórios se não existirem
- Limpa o diretório `Temp/` automaticamente

---

### 4.6 `app/lifecycle.py` — Ciclo de Vida

| Evento | Método | Ação |
|---|---|---|
| Startup OK | `on_startup()` | Loga sucesso |
| Shutdown | `on_shutdown()` | Fecha banco + limpeza |
| Erro crítico | `on_error()` | Loga + encerra com código 1 |

---

### 4.7 `database/connection.py` — Conexão SQLite

Padrão **Singleton** com configurações otimizadas:

| PRAGMA | Valor | Motivo |
|---|---|---|
| `journal_mode` | WAL | Performance + resiliência |
| `busy_timeout` | 5000ms | Evita erros em operações longas |
| `foreign_keys` | ON | Integridade referencial |
| `cache_size` | -65536 (64MB) | Performance de leitura |

---

### 4.8 `database/schema.py` — Schema

Tabelas criadas:

| Tabela | Descrição |
|---|---|
| `_migrations` | Controle de migrações aplicadas |
| `models` | Modelos de IA registrados |
| `tags` | Tags para categorização |
| `model_tags` | Relação N:N modelos ↔ tags |
| `engines` | Engines registradas |
| `benchmarks` | Resultados de benchmark |
| `downloads` | Fila e histórico de downloads |
| `history` | Histórico de ações |
| `settings` | Configurações persistidas |

Índices criados:

| Índice | Tabela | Campo |
|---|---|---|
| `idx_models_format` | models | format |
| `idx_models_favorite` | models | is_favorite |
| `idx_models_last_used` | models | last_used_at |
| `idx_benchmarks_model` | benchmarks | model_id |
| `idx_history_model` | history | model_id |
| `idx_history_created` | history | created_at |
| `idx_downloads_status` | downloads | status |
| `idx_settings_category` | settings | category |

---

### 4.9 `database/migrations.py` — Migrações

Estratégia de migrações versionadas:

- Arquivos `.sql` nomeados como `001_nome.sql`
- Tabela `_migrations` registra versões aplicadas
- Idempotente: nunca aplica a mesma migração duas vezes
- Executa automaticamente no startup

---

### 4.10 `config/default.json` — Configurações Padrão

Grupos de configuração:

| Grupo | Configurações |
|---|---|
| `general` | theme, language, check_updates |
| `workspace` | path, auto_scan, clean_temp |
| `database` | backup, interval, wal_mode |
| `ui` | sidebar, window size, remember size |
| `engines` | auto_detect, fallback |
| `downloads` | max_concurrent, verify_hash |
| `logs` | level, max_size, retention |

---

## 5. Dependências
### requirements.txt
```python
PySide6>=6.7.0 # Interface gráfica
python-dotenv>=1.0.0 # Variáveis de ambiente (uso futuro)
platformdirs>=4.2.0 # Paths padrão por SO
loguru>=0.7.2 # Sistema de log

pytest>=8.2.0 # Testes
pytest-qt>=4.4.0 # Testes de UI Qt
```
---

## 6. Regra de Imports — Padrão do Projeto

Todo arquivo do AIModelHub deve seguir esta regra:

```python
# ✅ Correto
from shared.constants import DATABASE_FILE
from shared.logger import logger
from shared.settings import Settings

# ❌ Errado — não existe mais
from app.constants import DATABASE_FILE
```

7. Sequência de Inicialização Verificada
Log de execução bem-sucedida em ambiente Windows:

✅ Sistema de log iniciado
✅ Iniciando OMNIA AIModelHub v0.1.0
✅ Diretórios do sistema verificados
✅ Banco de dados conectado (WAL mode)
✅ Schema base aplicado
✅ Nenhuma migração pendente
✅ Configurações carregadas
✅ Workspace AIModels verificado
✅ Pasta Temp limpa
✅ Qt Application criada
✅ Interface gráfica iniciada
Ambiente de teste:

Item	Valor
SO	Windows 11
Python	3.13
PySide6	6.7+
Banco	AppData\Local\AIModelHub\omnia.db
Workspace	C:\Users\David\AIModels
8. Pontos Pendentes para Fases Futuras
Pendência	Fase	Descrição
DAOs	Fase 2	Implementar acesso ao banco via DAOs
Settings do banco	Fase 2	load_from_db() ainda não é chamado
Scanner	Fase 2	Descoberta automática de modelos
Engines	Fase 2	EAL + primeiro adaptador (Ollama)
UI completa	Fase 3	Substituir janela provisória
Testes	Fase 4	Cobertura unitária e de integração
9. Atualização do ARCHITECTURE.md
A criação da camada shared/ foi documentada no
ARCHITECTURE.md com as seguintes alterações:

Seção 3 — Estrutura Macro: adicionada pasta shared/
Seção 4.2 — app/: removidos constants, logger, settings
Nova Seção 4.X — shared/: documentada com regras de uso
Seção 6 — Camadas: adicionada Shared Layer no diagrama
Seção 6 — Regras: adicionada regra número 5 para shared/
Relatório gerado por David L. Almeida — David Creator
OMNIA AIModelHub — Fase 1 concluída em 2026-08-08
Licença: GPL-2.0-or-later
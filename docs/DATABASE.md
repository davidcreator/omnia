# Banco de dados

## Visão geral

O AIModelHub utiliza SQLite, sem servidor externo. A conexão é criada sob demanda em `shared.constants.DATABASE_FILE` e configurada para uso local concorrente:

- `journal_mode=WAL`;
- `busy_timeout=5000` ms;
- `foreign_keys=ON`;
- `cache_size=-65536` (64 MiB);
- `check_same_thread=False`.

No Windows, o arquivo padrão é `%LOCALAPPDATA%\AIModelHub\omnia.db`. O caminho pode ser substituído em testes por patch de `database.connection.DATABASE_FILE`.

## Schema atual

O schema base em `database/schema.py` cria as tabelas:

| Tabela | Finalidade |
|---|---|
| `_migrations` | Controle das migrações aplicadas. |
| `models` | Modelos registrados e seus metadados. |
| `tags` | Tags de organização. |
| `model_tags` | Relação entre modelos e tags. |
| `engines` | Engines cadastradas. |
| `benchmarks` | Resultados de desempenho. |
| `downloads` | Fila e estado de downloads. |
| `history` | Histórico de ações. |
| `settings` | Configurações persistidas. |

Os índices principais cobrem formato, favoritos e último uso de modelos, modelo em benchmarks e histórico, status de downloads e categoria de configurações.

## Migrações

Migrações são arquivos SQL em `AIModelHub/database/migrations/` no formato `NNN_nome.sql`, por exemplo `001_initial.sql`. O `MigrationManager`:

1. garante o schema base;
2. lê as versões registradas em `_migrations`;
3. descobre arquivos pendentes em ordem numérica;
4. executa cada arquivo e registra sua versão;
5. faz rollback em caso de erro SQLite.

O processo é idempotente: uma migração já registrada não é executada novamente.

## Uso básico

```python
from database.connection import DatabaseConnection

db = DatabaseConnection()
db.initialize()
connection = db.get()

# Ao encerrar a aplicação:
DatabaseConnection.close()
```

## Testes

As fixtures em `AIModelHub/tests/conftest.py` usam SQLite em memória para manter isolamento entre testes. O teste de WAL usa um arquivo temporário, porque o modo WAL não é aplicável da mesma forma a uma conexão em memória:

```powershell
cd AIModelHub
pytest tests/unit/database/test_connection.py -q --no-cov
```

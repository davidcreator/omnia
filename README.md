# OMNIA AIModelHub

OMNIA é uma plataforma modular para organizar e executar modelos de IA localmente. O repositório contém a aplicação `AIModelHub`, responsável pelo ciclo de vida, configurações, persistência, interface e futuras integrações com engines.

## Estado atual

A fundação da aplicação está implementada:

- bootstrap e lifecycle da aplicação Qt;
- infraestrutura compartilhada em `AIModelHub/shared/`;
- workspace `AIModels` com diretórios padronizados;
- SQLite com schema inicial e migrações versionadas;
- conexão SQLite com WAL, foreign keys, timeout de escrita e cache;
- DAOs para modelos, catálogo, downloads, histórico, benchmarks e configurações;
- testes unitários, de integração e de performance.

O projeto está em desenvolvimento. Engines, catálogo visual completo e fluxos avançados de download ainda estão em evolução.

## Requisitos

- Python 3.13 ou superior;
- PySide6;
- dependências listadas em `AIModelHub/requirements.txt`.

## Instalação

```powershell
cd AIModelHub
python -m pip install -r requirements.txt
```

## Execução

```powershell
cd AIModelHub
python main.py
```

O banco SQLite é criado em um diretório de dados específico do sistema operacional. No Windows, o padrão é `%LOCALAPPDATA%\AIModelHub\omnia.db`; os logs ficam em `logs/app.log` dentro do mesmo diretório.

## Testes

Execute a suíte a partir de `AIModelHub`:

```powershell
pytest
```

Para validar apenas a conexão do banco sem aplicar o limite global de cobertura:

```powershell
pytest tests/unit/database/test_connection.py -q --no-cov
```

Os testes de conexão cobrem inicialização, acesso singleton, erro antes da inicialização, WAL em banco de arquivo, foreign keys e encerramento da conexão.

## Estrutura

```text
AIModelHub/
├── app/          # bootstrap, startup, shutdown e lifecycle
├── config/       # configuração padrão
├── core/         # regras de negócio em evolução
├── database/     # conexão, schema, migrações e DAOs
├── plugins/      # extensões
├── resources/    # recursos da aplicação
├── shared/       # constantes, logging e configurações compartilhadas
├── tests/        # testes unitários, integração e performance
├── ui/           # interface PySide6
└── main.py       # ponto de entrada
```

## Documentação

- [Arquitetura](docs/ARCHITECTURE.md)
- [Banco de dados](docs/DATABASE.md)
- [Estrutura de pastas](docs/FOLDER_STRUCTURE.md)
- [Workspace](docs/WORKSPACE.md)
- [Roadmap](docs/ROADMAP.md)
- [Changelog](docs/CHANGELOG.md)

## Licença

GPL-2.0-or-later. Consulte [LICENSE](AIModelHub/LICENSE).

# Arquitetura do OMNIA AIModelHub

## Visão geral

O projeto separa o código da aplicação do workspace de dados do usuário. A aplicação fica em `AIModelHub/`; o workspace padrão é `AIModels/` no diretório do usuário.

```text
main.py
  └── app.Bootstrap
        ├── shared       # constantes, logs e configurações
        ├── database     # SQLite, schema, migrações e DAOs
        ├── core         # regras de negócio
        └── ui           # interface PySide6
```

## Camadas

| Camada | Responsabilidade |
|---|---|
| `shared/` | Infraestrutura transversal sem regras de negócio. |
| `app/` | Inicialização, lifecycle, startup e shutdown. |
| `core/` | Serviços e regras de negócio do domínio. |
| `database/` | Persistência SQLite e objetos de acesso a dados. |
| `ui/` | Janela e componentes da interface PySide6. |
| `plugins/` | Extensões desacopladas da aplicação principal. |

`shared/` pode ser importado pelas outras camadas, mas não deve depender de `app/`, `core/`, `ui/`, `plugins/` ou de uma camada de infraestrutura específica.

## Inicialização

`app/bootstrap.py` coordena a inicialização do logger, diretórios do sistema, banco, configurações, workspace, Qt e interface. `app/lifecycle.py` concentra as ações de startup, shutdown e tratamento de erro crítico.

## Persistência

`database/connection.py` gerencia a conexão SQLite e configura WAL, `busy_timeout`, foreign keys e cache. `database/migrations.py` aplica o schema base e migrações SQL pendentes em ordem numérica. Os DAOs encapsulam as operações das entidades e usam a conexão centralizada.

## Regras de dependência

- a UI não deve conter regras de persistência;
- DAOs não devem conhecer widgets;
- novas alterações de schema devem ser acompanhadas por migração em `database/migrations/`;
- testes de banco devem usar fixtures isoladas e não o banco de produção;
- caminhos e valores globais devem ser obtidos de `shared/constants.py`.

# Estrutura de pastas

## Repositório

```text
omnia/
├── AIModelHub/
│   ├── app/
│   ├── config/
│   ├── core/
│   ├── database/
│   ├── EngineManager/
│   ├── plugins/
│   ├── resources/
│   ├── shared/
│   ├── tests/
│   ├── ui/
│   ├── main.py
│   ├── requirements.txt
│   └── pytest.ini
├── docs/
└── README.md
```

## Pacote da aplicação

| Diretório | Conteúdo atual |
|---|---|
| `app/` | Bootstrap, startup, shutdown, lifecycle e workspace. |
| `config/` | `default.json`. |
| `core/` | Scanner, catálogo, downloader, manager e benchmark. |
| `database/` | Conexão, schema, migrações, modelos, repositório e DAOs. |
| `shared/` | Constantes, logger e settings compartilhados. |
| `ui/` | Janela principal PySide6. |
| `plugins/` | Estrutura para extensões. |
| `tests/` | Fixtures, testes unitários, integração e performance. |

## Testes

```text
AIModelHub/tests/
├── conftest.py
├── unit/
│   ├── database/
│   └── shared/
├── integration/
└── performance/
```

As fixtures de banco criam conexões SQLite isoladas em memória. Testes que dependem de persistência real devem usar `tmp_path`.

## Workspace AIModels

O workspace padrão é definido por `shared/constants.py` e contém:

```text
AIModels/
├── Models/{HuggingFace,GGUF,ONNX,TensorRT,MLX,Custom}/
├── Catalog/metadata/
├── Engines/
├── Downloads/{active,completed,failed}/
├── Cache/{inference,embeddings,thumbnails}/
├── Logs/
├── Benchmarks/
├── Scripts/user_scripts/
├── Temp/
├── Exports/
└── Backups/{db,config}/
```

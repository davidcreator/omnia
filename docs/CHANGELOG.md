# Changelog

## 2026-08-08 — Fundação e persistência

- consolidada a camada `shared/` para constantes, logging e configurações;
- implementado bootstrap e lifecycle da aplicação PySide6;
- implementado workspace padrão com subdiretórios de modelos, downloads, cache, logs e backups;
- implementado SQLite com schema inicial, migrações versionadas e DAOs;
- configurada conexão com WAL, foreign keys, timeout e cache;
- adicionados testes unitários de conexão, migrações, DAOs e componentes compartilhados;
- corrigido o teste de conexão para validar WAL em banco de arquivo temporário e restaurar o estado entre testes;
- documentada a estrutura real do projeto e o fluxo de execução dos testes.

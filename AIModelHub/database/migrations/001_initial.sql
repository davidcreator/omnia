-- Migração 001 — Schema inicial
-- Criado automaticamente pelo schema.py na inicialização
-- Este arquivo serve como registro histórico da versão 1

-- Nenhuma alteração adicional nesta migração.
-- O schema base é aplicado diretamente pelo MigrationManager.

INSERT OR IGNORE INTO _migrations (version, name)
VALUES (1, '001_initial');
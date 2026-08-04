# OMNIA

## Guia de Contribuição

**Versão:** 1.0  
**Última atualização:** 2026  

---

# 👋 Bem-vindo

Obrigado pelo seu interesse em contribuir com o **OMNIA**! 

Este documento fornece diretrizes e instruções para contribuir com o projeto. Seja você um desenvolvedor experiente ou alguém fazendo sua primeira contribuição open source, sua ajuda é muito bem-vinda.

## Por que Contribuir?

* 🌟 Fazer parte de uma plataforma inovadora de IA local
* 📚 Aprender sobre arquitetura de software, IA e Python moderno
* 🤝 Conectar-se com uma comunidade de desenvolvedores
* 🏆 Ter seu trabalho reconhecido publicamente
* 💼 Adicionar experiência relevante ao seu portfólio

## Tipos de Contribuição

| Tipo | Descrição |
|------|-----------|
| 🐛 **Bug Reports** | Reportar problemas encontrados |
| ✨ **Features** | Propor ou implementar novas funcionalidades |
| 📖 **Documentação** | Melhorar docs, README, exemplos |
| 🧪 **Testes** | Adicionar ou melhorar testes |
| 🌐 **Traduções** | Traduzir documentação ou interface |
| 💡 **Ideias** | Sugerir melhorias via Discussions |
| 👀 **Code Review** | Revisar PRs de outros contribuidores |

---

# 📜 Código de Conduta

Antes de contribuir, por favor leia nosso [Código de Conduta](CODE_OF_CONDUCT.md).

Resumo dos pontos principais:

* ✅ Seja respeitoso e inclusivo
* ✅ Aceite feedback construtivo
* ✅ Foque no que é melhor para a comunidade
* ❌ Não toleramos assédio ou discriminação
* ❌ Não toleramos comportamento tóxico

**Violações podem resultar em banimento do projeto.**

---

# 🚀 Como Começar

## Primeira Contribuição?

Se é sua primeira vez contribuindo com open source, recomendamos:

1. **Leia a documentação** — README, ARCHITECTURE, ROADMAP
2. **Explore as issues** — Procure por labels \`good first issue\` ou \`help wanted\`
3. **Comece pequeno** — Correções de typos, documentação, testes simples
4. **Pergunte** — Use Discussions para tirar dúvidas

## Issues para Iniciantes

Procure por estas labels:

| Label | Descrição |
|-------|-----------|
| \`good first issue\` | Ideal para primeira contribuição |
| \`help wanted\` | Precisamos de ajuda |
| \`documentation\` | Melhorias em documentação |
| \`beginner friendly\` | Não requer conhecimento profundo |

---

# 💻 Ambiente de Desenvolvimento

## Pré-requisitos

* **Python** 3.13 ou superior
* **Git** 2.x ou superior
* **pip** ou **uv** (recomendado)
* **Editor** com suporte a Python (VS Code, PyCharm)

### Verificar Versões

\`\`\`bash
python --version    # Python 3.13.x
git --version       # git version 2.x.x
pip --version       # pip 24.x
\`\`\`

## Setup do Projeto

### 1. Fork e Clone

\`\`\`bash
# Fork o repositório no GitHub, depois:
git clone https://github.com/SEU_USERNAME/omnia.git
cd omnia

# Adicione o upstream
git remote add upstream https://github.com/davidcreator/omnia.git
\`\`\`

### 2. Criar Ambiente Virtual

\`\`\`bash
# Com venv (padrão)
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
.venv\\Scripts\\activate     # Windows

# Ou com uv (mais rápido)
uv venv
source .venv/bin/activate
\`\`\`

### 3. Instalar Dependências

\`\`\`bash
# Dependências de desenvolvimento
pip install -e ".[dev]"

# Ou com uv
uv pip install -e ".[dev]"
\`\`\`

### 4. Configurar Pre-commit

\`\`\`bash
# Instalar hooks
pre-commit install

# Testar hooks
pre-commit run --all-files
\`\`\`

### 5. Verificar Instalação

\`\`\`bash
# Rodar testes
pytest

# Verificar tipos
mypy omnia/

# Verificar estilo
ruff check .
black --check .
\`\`\`

## Estrutura de Pastas

\`\`\`
omnia/
├── .venv/              # Ambiente virtual (não commitado)
├── AIModelHub/         # Aplicação principal
│   ├── app/            # Bootstrap e lifecycle
│   ├── core/           # Lógica de negócios
│   ├── database/       # SQLite e DAOs
│   ├── engines/        # Adaptadores de engines
│   ├── plugins/        # Sistema de plugins
│   ├── ui/             # Interface PySide6
│   └── main.py         # Ponto de entrada
├── docs/               # Documentação
├── tests/              # Testes
├── pyproject.toml      # Configuração do projeto
└── README.md
\`\`\`

---

# 📁 Estrutura do Projeto

## Módulos Principais

| Módulo | Responsabilidade | Contato |
|--------|------------------|---------|
| \`core/\` | Lógica de negócios | @maintainer |
| \`engines/\` | Adaptadores de IA | @maintainer |
| \`database/\` | Persistência SQLite | @maintainer |
| \`ui/\` | Interface gráfica | @maintainer |
| \`plugins/\` | Sistema de extensões | @maintainer |

## Arquivos Importantes

| Arquivo | Descrição |
|---------|-----------|
| \`pyproject.toml\` | Configuração do projeto e dependências |
| \`.pre-commit-config.yaml\` | Hooks de pre-commit |
| \`pytest.ini\` | Configuração de testes |
| \`docs/ARCHITECTURE.md\` | Arquitetura do sistema |
| \`docs/ROADMAP.md\` | Plano de desenvolvimento |

---

# 🔄 Fluxo de Contribuição

## Visão Geral

\`\`\`
1. Issue       →  Discutir a mudança
2. Fork        →  Criar sua cópia
3. Branch      →  Criar branch de trabalho
4. Develop     →  Implementar mudanças
5. Test        →  Garantir qualidade
6. Commit      →  Commits semânticos
7. Push        →  Enviar para seu fork
8. PR          →  Abrir Pull Request
9. Review      →  Responder feedback
10. Merge      →  Celebrar! 🎉
\`\`\`

## Passo a Passo Detalhado

### 1. Sincronize seu Fork

\`\`\`bash
# Buscar atualizações do upstream
git fetch upstream

# Atualizar sua main
git checkout main
git merge upstream/main

# Enviar para seu fork
git push origin main
\`\`\`

### 2. Crie uma Branch

\`\`\`bash
# Nomenclatura: tipo/descricao-curta
git checkout -b feature/add-vllm-engine
git checkout -b fix/scanner-symlink-handling
git checkout -b docs/improve-installation-guide
\`\`\`

### 3. Faça suas Mudanças

* Escreva código seguindo o [CODING_STANDARD.md](CODING_STANDARD.md)
* Adicione testes para novas funcionalidades
* Atualize documentação se necessário

### 4. Teste Localmente

\`\`\`bash
# Rodar todos os testes
pytest

# Rodar testes específicos
pytest tests/unit/test_engines.py -v

# Verificar cobertura
pytest --cov=omnia --cov-report=html

# Verificar tipos e estilo
mypy omnia/
ruff check .
black --check .
\`\`\`

### 5. Commit suas Mudanças

\`\`\`bash
# Commits pequenos e focados
git add .
git commit -m "feat(engines): add vLLM engine adapter"
\`\`\`

### 6. Push e PR

\`\`\`bash
# Enviar para seu fork
git push origin feature/add-vllm-engine

# Abrir PR no GitHub
# Use o template fornecido
\`\`\`

---

# 🎫 Issues

## Antes de Abrir uma Issue

1. **Pesquise** — Verifique se já existe uma issue similar
2. **Verifique a versão** — Teste com a versão mais recente
3. **Reproduza** — Confirme que consegue reproduzir o problema

## Tipos de Issues

### 🐛 Bug Report

Use o template e inclua:

\`\`\`markdown
## Descrição
Descrição clara e concisa do bug.

## Passos para Reproduzir
1. Vá para '...'
2. Clique em '...'
3. Role até '...'
4. Veja o erro

## Comportamento Esperado
O que deveria acontecer.

## Comportamento Atual
O que está acontecendo.

## Screenshots
Se aplicável.

## Ambiente
- OS: [ex: Windows 11, Ubuntu 24.04]
- Python: [ex: 3.13.1]
- OMNIA: [ex: 1.0.0]
- Engine: [ex: Ollama 0.1.x]

## Logs
\\\`\\\`\\\`
Cole logs relevantes aqui
\\\`\\\`\\\`

## Contexto Adicional
Qualquer outra informação relevante.
\`\`\`

### ✨ Feature Request

\`\`\`markdown
## Problema
Descrição do problema que esta feature resolve.

## Solução Proposta
Descrição clara da solução desejada.

## Alternativas Consideradas
Outras soluções que você considerou.

## Contexto Adicional
Mockups, exemplos, referências.
\`\`\`

### 📖 Documentação

\`\`\`markdown
## Página/Seção
Qual documentação precisa de melhoria.

## Problema
O que está faltando ou incorreto.

## Sugestão
Como poderia ser melhorado.
\`\`\`

## Labels

| Label | Cor | Descrição |
|-------|-----|-----------|
| \`bug\` | 🔴 | Algo não funciona |
| \`feature\` | 🟢 | Nova funcionalidade |
| \`documentation\` | 🔵 | Melhorias em docs |
| \`good first issue\` | 🟡 | Boa para iniciantes |
| \`help wanted\` | 🟣 | Precisamos de ajuda |
| \`wontfix\` | ⚪ | Não será resolvido |
| \`duplicate\` | ⚪ | Issue duplicada |
| \`invalid\` | ⚪ | Issue inválida |

---

# 🔀 Pull Requests

## Antes de Abrir um PR

- [ ] Código segue o [CODING_STANDARD.md](CODING_STANDARD.md)
- [ ] Testes adicionados/atualizados
- [ ] Documentação atualizada
- [ ] Commits seguem Conventional Commits
- [ ] Branch atualizada com main
- [ ] CI passando localmente

## Template de PR

\`\`\`markdown
## Descrição
Descrição clara das mudanças.

## Tipo de Mudança
- [ ] 🐛 Bug fix (mudança que corrige um problema)
- [ ] ✨ Nova feature (mudança que adiciona funcionalidade)
- [ ] 💥 Breaking change (mudança que quebra compatibilidade)
- [ ] 📖 Documentação (mudança em documentação apenas)
- [ ] 🔧 Refatoração (mudança que não corrige bug nem adiciona feature)

## Issue Relacionada
Fixes #(número da issue)

## Como Testar
1. Passo 1
2. Passo 2
3. Passo 3

## Screenshots
Se aplicável.

## Checklist
- [ ] Meu código segue o estilo do projeto
- [ ] Revisei meu próprio código
- [ ] Comentei código complexo
- [ ] Atualizei a documentação
- [ ] Minhas mudanças não geram warnings
- [ ] Adicionei testes
- [ ] Testes novos e existentes passam
\`\`\`

## Tamanho do PR

| Tamanho | Linhas | Recomendação |
|---------|--------|--------------|
| 🟢 Pequeno | < 100 | Ideal |
| 🟡 Médio | 100-400 | Aceitável |
| 🔴 Grande | > 400 | Divida em PRs menores |

## Processo de Review

1. **Automated checks** — CI roda automaticamente
2. **Maintainer review** — Pelo menos 1 aprovação necessária
3. **Feedback** — Responda comentários educadamente
4. **Aprovação** — Quando aprovado, será mergeado
5. **Merge** — Maintainer faz o merge

---

# 📝 Commits

## Conventional Commits

\`\`\`
<tipo>(<escopo>): <descrição>

[corpo opcional]

[rodapé opcional]
\`\`\`

## Tipos

| Tipo | Emoji | Descrição |
|------|-------|-----------|
| \`feat\` | ✨ | Nova funcionalidade |
| \`fix\` | 🐛 | Correção de bug |
| \`docs\` | 📖 | Documentação |
| \`style\` | 🎨 | Formatação (sem mudança de código) |
| \`refactor\` | ♻️ | Refatoração |
| \`perf\` | ⚡ | Performance |
| \`test\` | 🧪 | Testes |
| \`build\` | 📦 | Build/dependências |
| \`ci\` | 🔧 | CI/CD |
| \`chore\` | 🔨 | Outras tarefas |

## Exemplos

\`\`\`bash
# Feature
feat(engines): add support for vLLM backend

# Bug fix
fix(scanner): handle symlinks in model directory

Fixes #123

# Breaking change
feat(api)!: redesign model loading interface

BREAKING CHANGE: load_model() now requires keyword arguments.
Migration guide: see docs/migration-1.0.md

# Multiple scopes
feat(core,engines): implement model hot-reload
\`\`\`

## Boas Práticas

* ✅ Use imperativo: "add feature" não "added feature"
* ✅ Primeira letra minúscula
* ✅ Sem ponto final
* ✅ Máximo 72 caracteres na primeira linha
* ✅ Corpo do commit explica o "porquê"

---

# 🧪 Testes

## Estrutura

\`\`\`
tests/
├── conftest.py           # Fixtures globais
├── unit/                 # Testes unitários
│   ├── test_models.py
│   ├── test_engines.py
│   └── test_database.py
├── integration/          # Testes de integração
│   └── test_workflows.py
└── fixtures/             # Dados de teste
    └── models/
\`\`\`

## Nomenclatura

\`\`\`python
# Arquivo: test_<módulo>.py
# Classe: Test<Classe>
# Método: test_<método>_<cenário>_<resultado>

class TestModelManager:
    def test_load_model_valid_path_returns_model(self):
        pass
    
    def test_load_model_invalid_path_raises_error(self):
        pass
\`\`\`

## Comandos

\`\`\`bash
# Rodar todos os testes
pytest

# Com verbose
pytest -v

# Arquivo específico
pytest tests/unit/test_engines.py

# Teste específico
pytest -k "test_load_model"

# Com cobertura
pytest --cov=omnia --cov-report=html

# Parar no primeiro erro
pytest -x

# Modo debug
pytest --pdb
\`\`\`

## Requisitos

* **Cobertura mínima:** 80%
* **Testes obrigatórios para:**
  * Novas funcionalidades
  * Bug fixes (teste que reproduz o bug)
  * Refatorações (manter testes existentes passando)

---

# 📖 Documentação

## O que Documentar

| Tipo | Onde | Quando |
|------|------|--------|
| API pública | Docstrings | Sempre |
| Arquitetura | ARCHITECTURE.md | Mudanças estruturais |
| Instalação | README.md | Novos requisitos |
| Changelog | CHANGELOG.md | Todo PR |
| Exemplos | docs/examples/ | Features novas |

## Docstrings (Google Style)

\`\`\`python
def load_model(path: Path, *, validate: bool = True) -> Model:
    """Carrega um modelo do disco.

    Args:
        path: Caminho para o arquivo do modelo.
        validate: Se True, valida o modelo antes de carregar.

    Returns:
        Modelo carregado e pronto para uso.

    Raises:
        FileNotFoundError: Se o arquivo não existe.
        InvalidModelError: Se o modelo é inválido.

    Example:
        >>> model = load_model(Path("model.gguf"))
        >>> model.inference("Hello!")
    """
\`\`\`

## CHANGELOG

Seguimos [Keep a Changelog](https://keepachangelog.com/):

\`\`\`markdown
## [Unreleased]

### Added
- Nova engine vLLM (#123)

### Changed
- Melhorada performance do scanner (#124)

### Fixed
- Corrigido bug em symlinks (#125)

### Removed
- Removido suporte a Python 3.12
\`\`\`

---

# 👀 Revisão de Código

## Para Autores

* Responda todos os comentários
* Seja receptivo a feedback
* Explique suas decisões
* Atualize o PR conforme solicitado
* Marque conversas como resolvidas

## Para Revisores

* Seja respeitoso e construtivo
* Explique o "porquê" das sugestões
* Diferencie "obrigatório" de "sugestão"
* Aprove quando estiver satisfeito
* Responda em tempo hábil

## Checklist de Review

- [ ] Código segue os padrões do projeto
- [ ] Lógica está correta
- [ ] Testes são adequados
- [ ] Performance é aceitável
- [ ] Segurança foi considerada
- [ ] Documentação está atualizada
- [ ] Não há código comentado
- [ ] Não há TODOs esquecidos

## Convenções de Comentário

\`\`\`
# Obrigatório - deve ser corrigido
🔴 Isso vai causar um bug em produção...

# Sugestão - pode melhorar
🟡 Considere usar X ao invés de Y...

# Nitpick - opcional
🟢 Nit: poderia renomear para...

# Pergunta
❓ Por que escolheu essa abordagem?

# Elogio
🎉 Ótima solução!
\`\`\`

---

# 💬 Comunidade

## Canais de Comunicação

| Canal | Uso |
|-------|-----|
| **GitHub Issues** | Bugs e feature requests |
| **GitHub Discussions** | Perguntas, ideias, ajuda |
| **Pull Requests** | Revisão de código |

## Etiqueta

* 🔍 Pesquise antes de perguntar
* 📝 Seja claro e específico
* 🙏 Seja paciente
* ❤️ Agradeça quem ajuda
* 🌐 Use inglês ou português

## Obtendo Ajuda

1. **Documentação** — Leia README, ARCHITECTURE, etc.
2. **Pesquisa** — Issues existentes, Discussions
3. **Pergunte** — Abra uma Discussion com tag \`question\`

---

# 🏆 Reconhecimento

## Contributors

Todos os contribuidores são listados em:

* README.md (seção Contributors)
* GitHub Contributors page
* Release notes

## Níveis de Contribuição

| Nível | Requisitos | Benefícios |
|-------|------------|------------|
| 🌱 **Contributor** | 1+ PR mergeado | Listado em Contributors |
| 🌿 **Regular** | 5+ PRs | Badge especial |
| 🌳 **Core** | Contribuições significativas | Acesso ao time |
| 👑 **Maintainer** | Convite | Merge access |

## Como ser Reconhecido

* PRs mergeados
* Issues resolvidas
* Ajuda em Discussions
* Code reviews
* Documentação
* Traduções

---

# Checklist Final

Antes de contribuir, verifique:

- [ ] Li o README.md
- [ ] Li o CODE_OF_CONDUCT.md
- [ ] Li este CONTRIBUTING.md
- [ ] Li o CODING_STANDARD.md
- [ ] Configurei o ambiente de desenvolvimento
- [ ] Entendi o fluxo de contribuição
- [ ] Sei como pedir ajuda

---

# Obrigado! 🙏

Agradecemos seu interesse em contribuir com o OMNIA!

Cada contribuição, por menor que seja, ajuda a construir uma plataforma melhor para toda a comunidade de IA local.

**Vamos construir juntos!**

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

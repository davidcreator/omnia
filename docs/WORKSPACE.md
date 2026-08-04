# OMNIA

## Workspace AIModels

**Versão:** 1.0  
**Diretório:** \`AIModels/\` (configurável)  
**Última atualização:** 2026  

---

# 1. Visão Geral

O **AIModels** é o workspace centralizado do OMNIA — o diretório onde todos os dados do ecossistema de IA são armazenados de forma organizada. A separação entre aplicação (AIModelHub) e dados (AIModels) é um dos princípios fundamentais do projeto.

## Por que um Workspace Centralizado?

| Problema sem Workspace | Solução com AIModels |
|----------------------|----------------------|
| Modelos duplicados entre apps | Todos os apps compartilham o mesmo arquivo |
| Configurações fragmentadas | Configuração centralizada por workspace |
| Downloads repetidos | Cache compartilhado |
| Backups complexos | Backup simples de um único diretório |
| Dificuldade de migração | Mover um diretório = migrar tudo |

---

# 2. Estrutura Completa

## 2.1 Árvore de Diretórios

\`\`\`
AIModels/                          # Workspace raiz (configurável)
│
├── 📁 Models/                     # Modelos de IA organizados
│   ├── 📁 HuggingFace/            # Formato HuggingFace (transformers)
│   │   └── 📁 <org>/
│   │       └── 📁 <model>/
│   │           ├── 📄 config.json
│   │           ├── 📄 tokenizer.json
│   │           ├── 📄 model.safetensors
│   │           └── 📄 tokenizer_config.json
│   ├── 📁 GGUF/                   # Formato quantizado GGUF
│   │   └── 📄 <model>.gguf
│   ├── 📁 ONNX/                   # Formato ONNX
│   │   └── 📄 <model>.onnx
│   ├── 📁 TensorRT/               # Formato TensorRT
│   │   └── 📄 <model>.plan
│   ├── 📁 MLX/                    # Apple MLX
│   │   └── 📁 <model>/
│   └── 📁 Custom/                 # Modelos personalizados
│
├── 📁 Catalog/                    # Metadados e índices
│   ├── 📄 index.json              # Índice central de todos os modelos
│   ├── 📄 catalog.db              # Banco do catálogo (opcional)
│   └── 📁 metadata/               # Metadados individuais (JSON)
│       └── 📄 <model_id>.json
│
├── 📁 Engines/                    # Configurações por engine
│   ├── 📁 ollama/
│   │   ├── 📄 config.json         # Configuração específica
│   │   └── 📁 logs/
│   ├── 📁 transformers/
│   │   └── 📄 config.json
│   ├── 📁 llamacpp/
│   │   └── 📄 config.json
│   ├── 📁 vllm/
│   │   └── 📄 config.json
│   └── 📁 lmstudio/
│       └── 📄 config.json
│
├── 📁 Downloads/                  # Gerenciamento de downloads
│   ├── 📁 active/                 # Downloads em progresso
│   │   └── 📄 <file>.part         # Arquivo parcial
│   ├── 📁 completed/              # Concluídos (pré-organização)
│   │   └── 📄 <file>
│   └── 📁 failed/                 # Falhados (para retry)
│       └── 📄 <file>.failed
│
├── 📁 Cache/                      # Cache do sistema
│   ├── 📁 inference/              # Cache de resultados de inferência
│   │   └── 📄 <hash>.json
│   ├── 📁 embeddings/             # Cache de embeddings (RAG)
│   │   └── 📁 <collection>/
│   │       └── 📄 index.faiss
│   ├── 📁 thumbnails/             # Thumbnails de modelos
│   │   └── 📄 <model_id>.png
│   └── 📁 huggingface/            # Cache do HF Hub
│       └── 📁 <org>/
│
├── 📁 Logs/                       # Logs operacionais
│   ├── 📄 app.log                 # Log geral da aplicação
│   ├── 📄 engine.log              # Operações de engines
│   ├── 📄 download.log            # Progresso de downloads
│   ├── 📄 error.log               # Apenas erros
│   ├── 📁 archive/                # Logs arquivados (rotacionados)
│   │   └── 📄 app_2026-01-15.log.gz
│   └── 📁 benchmark/              # Logs de benchmarks
│
├── 📁 Benchmarks/                 # Resultados de benchmarks
│   └── 📁 <model_id>/
│       ├── 📄 <timestamp>_ollama.json
│       ├── 📄 <timestamp>_transformers.json
│       └── 📄 summary.json
│
├── 📁 Agents/                     # Agentes de IA
│   ├── 📁 programmer/
│   │   ├── 📄 config.json         # Config do agente
│   │   └── 📄 system_prompt.md    # Prompt base
│   ├── 📁 writer/
│   ├── 📁 translator/
│   └── 📁 custom/
│
├── 📁 RAG/                        # Sistema RAG (Retrieval Augmented Generation)
│   ├── 📁 documents/              # Documentos fonte
│   │   └── 📄 documento_01.md
│   ├── 📁 vectors/                # Índices vetoriais
│   │   └── 📁 knowledge_base/
│   │       ├── 📄 index.faiss
│   │       └── 📄 chunks.json
│   ├── 📄 config.json             # Config RAG
│   └── 📄 embeddings_cache.json
│
├── 📁 Scripts/                    # Scripts do usuário
│   ├── 📁 automation/             # Automação (n8n, scripts)
│   │   └── 📄 workflow.json
│   ├── 📁 conversion/             # Conversão personalizada
│   │   └── 📄 hf_to_gguf.py
│   └── 📄 README.md               # Documentação
│
├── 📁 Temp/                       # Arquivos temporários
│   └── 📄 ...                     # Limpo automaticamente na inicialização
│
├── 📁 Exports/                    # Pacotes exportados
│   └── 📁 <export_name>/
│       ├── 📄 manifest.json       # Manifesto do export
│       ├── 📄 README.md
│       └── 📁 models/
│
├── 📁 Backups/                    # Backups automáticos
│   ├── 📁 db/                     # Backups do banco SQLite
│   │   ├── 📄 omnia_2026-01-15_120000.db
│   │   └── 📄 omnia_2026-01-14_120000.db
│   └── 📁 config/                 # Backups de configurações
│       └── 📄 settings_2026-01-15.json
│
└── 📁 database/                   # Banco SQLite
    ├── 📄 omnia.db                # Arquivo principal
    ├── 📄 omnia.db-wal            # Write-Ahead Log
    └── 📄 omnia.db-shm            # Shared Memory
\`\`\`

---

# 3. Modelos

## 3.1 Formato HuggingFace

\`\`\`
AIModels/Models/HuggingFace/
└── meta-llama/
    └── Llama-2-7b-hf/
        ├── config.json         # Configuração (arch, params)
        ├── tokenizer_config.json
        ├── tokenizer.json     # Vocabulário
        ├── model.safetensors  # Pesos (formato seguro)
        ├── generation_config.json
        ├── special_tokens_map.json
        └── pytorch_model.bin  # Alternativa (.bin legado)
\`\`\`

## 3.2 Formato GGUF

\`\`\`
AIModels/Models/GGUF/
├── llama-2-7b.Q4_0.gguf
├── llama-2-7b.Q4_K_M.gguf
├── mistral-7b.Q5_K_M.gguf
└── phi-2.Q8_0.gguf
\`\`\`

## 3.3 Catalogo

O arquivo \`AIModels/Catalog/index.json\` armazena:

\`\`\`json
{
    "version": "1.0",
    "updated_at": "2026-01-15T12:00:00Z",
    "models": [
        {
            "id": "llama-2-7b-gguf",
            "name": "Llama 2 7B (GGUF Q4_K_M)",
            "format": "gguf",
            "path": "/home/user/AIModels/Models/GGUF/llama-2-7b.Q4_K_M.gguf",
            "architecture": "llama",
            "quantization": "q4_k_m",
            "size_bytes": 3677884928,
            "manufacturer": "Meta",
            "tags": ["llm", "chat", "english"],
            "favorite": true
        }
    ],
    "tags": [
        {"id": 1, "name": "llm", "color": "#6366f1"},
        {"id": 2, "name": "chat", "color": "#10b981"}
    ]
}
\`\`\`

---

# 4. Downloads

## 4.1 Estados

| Estado | Descrição | Ação Automática |
|--------|-----------|----------------|
| \`pending\` | Aguardando início | Inicia após fila |
| \`downloading\` | Em progresso | Continua automaticamente |
| \`paused\` | Pausado pelo usuário | Nada |
| \`completed\` | Concluído com sucesso | Move para Models/ |
| \`failed\` | Falhou (hash inválido) | Tenta novamente (max 3x) |
| \`cancelled\` | Cancelado pelo usuário | Remove arquivo parcial |

## 4.2 Arquivos

\`\`\`
Downloads/
├── active/
│   └── model_abc123.part      # Arquivo em progresso (.part)
├── completed/
│   └── model_abc123.gguf      # Arquivo completo
└── failed/
    └── model_abc123.failed     # Registro de falha
\`\`\`

---

# 5. Cache

## 5.1 Tipos de Cache

| Diretório | Conteúdo | TTL | Tamanho Típico |
|-----------|----------|-----|---------------|
| \`inference/\` | Respostas de inferência | 7 dias | Pequeno |
| \`embeddings/\` | Vetores para RAG | 30 dias | Médio |
| \`thumbnails/\` | Pré-visualizações | Permanente | Pequeno |
| \`huggingface/\` | Cache do HF Hub | Configurável | Grande |

---

# 6. Logs

## 6.1 Arquivos

| Arquivo | Nível | Rotação | Compressão |
|---------|-------|---------|------------|
| \`app.log\` | INFO+ | Diária | Sim (gzip) |
| \`engine.log\` | INFO+ | Diária | Sim |
| \`download.log\` | INFO+ | Diária | Não |
| \`error.log\` | ERROR+ | Semanal | Sim |

---

# 7. Backups

## 7.1 Estrutura

\`\`\`
Backups/
├── db/
│   └── omnia_2026-01-15_120000.db    # Backup SQLite
└── config/
    └── settings_2026-01-15.json        # Configurações
\`\`\`

## 7.2 Política

* **Frequência:** Diária (configurável)
* **Retenção:** Últimos 7 backups (default)
* **Verificação:** Checksum após backup
* **Restaurar:** Cópia para \`database/omnia.db\`

---

# 8. Regras do Workspace

## 8.1 Regras Fundamentais

| Regra | Descrição |
|-------|-----------|
| **Caminho Fixo** | Definido uma vez, armazenado em settings |
| **Auto-Criação** | Subdiretórios criados na inicialização se faltarem |
| **Isolamento de Engines** | Cada engine tem config própria |
| **Limpeza Automática** | \`Temp/\` limpo a cada inicialização |
| **Cache com TTL** | \`Cache/\` pode ser limpo automaticamente |
| **Portabilidade** | Workspace pode ser movido com ajuste de um path |

---

# 9. Portabilidade

## 9.1 Mover Workspace

1. **Parar aplicação** (se rodando)
2. **Copiar/mover** \`AIModels/\` para novo local
3. **Atualizar** configuração \`workspace_path\`
4. **Reiniciar** aplicação

\`\`\`python
# Atualizar workspace
settings = load_settings()
settings["workspace_path"] = "/new/path/to/AIModels"
save_settings(settings)
\`\`\`

---

# 10. Manutenção

## 10.1 Tarefas Automáticas

| Tarefa | Frequência | Descrição |
|--------|------------|-----------|
| **Backup do DB** | Diária | Copia \`database/omnia.db\` |
| **Limpeza de cache** | Semanal | Remove arquivos antigos |
| **Limpeza de logs** | Mensal | Arquiva/comprime |
| **Verificação de hash** | Por download | Valida integridade |

---

# Referências

* [ARCHITECTURE.md](ARCHITECTURE.md) — Arquitetura
* [README.md](../README.md) — Visão geral
* [DATABASE.md](DATABASE.md) — Estrutura do banco

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

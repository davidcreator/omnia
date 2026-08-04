# OMNIA

## Sistema de Plugins

**Versão:** 1.0  
**Status:** Em desenvolvimento  
**Última atualização:** 2026  

---

# 1. Visão Geral

O sistema de plugins do OMNIA permite estender a plataforma com novas funcionalidades sem modificar o código principal. Cada plugin é um módulo independente que se integra via **hooks** e **registry**.

## Por que Plugins?

* ✅ **Extensibilidade** — Adicione recursos sem alterar o core
* ✅ **Modularidade** — Funcionalidades opcionais
* ✅ **Isolamento** — Plugins não afetam uns aos outros
* ✅ **Comunidade** — Qualquer pessoa pode criar plugins
* ✅ **Segurança** — Sandboxing básico e permissões declaradas

## Plugins Planejados

| Plugin | Ícone | Função |
|--------|-------|--------|
| **VS Code** | 💻 | Integrar modelos diretamente no editor |
| **Docker** | 🐳 | Empacotar modelos em containers |
| **GitHub** | 🐙 | Sincronizar catálogo e configurações |
| **WordPress** | 📝 | Geração de conteúdo via IA |
| **n8n** | 🔗 | Automação de fluxos com modelos locais |
| **Obsidian** | 💎 | RAG com base de conhecimento |

---

# 2. Arquitetura

## Diagrama

\`\`\`
┌──────────────────────────────────────────────┐
│                 OMNIA Core                    │
│              (core/, ui/, ...)                 │
└─────────────────────┬────────────────────────┘
                      │
                      ▼
        ┌─────────────────────────────┐
        │       Plugin Manager        │
        │  • discover()              │
        │  • load()                  │
        │  • activate()/deactivate() │
        │  • get_registry()          │
        └─────────────┬───────────────┘
                      │
        ┌─────────────┼───────────────┐
        │             │               │
        ▼             ▼               ▼
┌───────────┐ ┌───────────┐ ┌───────────────┐
│  Plugin   │ │  Plugin   │ │    Plugin     │
│  Registry │ │  Hooks    │ │     Base      │
└───────────┘ └───────────┘ └───────────────┘
        │             │               │
        ▼             ▼               ▼
┌──────────────────────────────────────────────┐
│              Plugin Instances                 │
│  • VSCodePlugin  • DockerPlugin             │
│  • GitHubPlugin  • WordPressPlugin          │
│  • n8nPlugin     • ObsidianPlugin           │
└──────────────────────────────────────────────┘
\`\`\`

## Componentes

| Componente | Arquivo | Responsabilidade |
|-----------|---------|------------------|
| **PluginBase** | \`plugins/plugin_base.py\` | Classe abstrata |
| **PluginManager** | \`plugins/plugin_manager.py\` | Lifecycle e registro |
| **PluginRegistry** | \`plugins/plugin_registry.py\` | Registro central |
| **Hook System** | \`plugins/hooks.py\` | Eventos de extensão |
| **Plugins Integrados** | \`plugins/builtin/\` | Plugins padrão |

---

# 3. PluginBase

## Interface Abstrata

\`\`\`python
# plugins/plugin_base.py

from abc import ABC, abstractmethod
from typing import Any, Optional, List, Dict


class PluginBase(ABC):
    """
    Classe base para todos os plugins do OMNIA.
    
    Todos os plugins devem herdar desta classe e implementar
    pelo menos os métodos abstratos.
    """
    
    # ==========================================================================
    # PROPRIEDADES ABSTRATAS (obrigatórias)
    # ==========================================================================
    
    @property
    @abstractmethod
    def name(self) -> str:
        """Nome único do plugin (ex: 'vscode')."""
        ...
    
    @property
    @abstractmethod
    def version(self) -> str:
        """Versão semântica (ex: '1.0.0')."""
        ...
    
    @property
    @abstractmethod
    def description(self) -> str:
        """Descrição breve para UI."""
        ...
    
    @property
    @abstractmethod
    def author(self) -> str:
        """Autor ou organização."""
        ...
    
    @property
    @abstractmethod
    def requires(self) -> List[str]:
        """
        Lista de dependências (plugins ou versões).
        Exemplo: ['omni-core>=1.0', 'plugin-utils>=0.5']
        """
        ...
    
    @property
    def permissions(self) -> List[str]:
        """
        Permissões solicitadas pelo plugin.
        Padrão: permissões mínimas.
        
        Opções:
        - 'database:read'  # Ler banco
        - 'database:write' # Escrever banco
        - 'models:read'    # Ler modelos
        - 'models:write'   # Modificar modelos
        - 'ui:inject'      # Injetar componentes na UI
        - 'api:rest'       # Acessar API REST
        - 'system:exec'    # Executar comandos do sistema
        """
        return ["database:read", "models:read"]
    
    # ==========================================================================
    # MÉTODOS ABSTRATOS (obrigatórios)
    # ==========================================================================
    
    @abstractmethod
    def on_activate(self) -> None:
        """
        Chamado quando o plugin é ativado pelo usuário.
        
        Use para:
        - Inicializar recursos
        - Registrar hooks
        - Criar conexões
        """
        ...
    
    @abstractmethod
    def on_deactivate(self) -> None:
        """
        Chamado quando o plugin é desativado.
        
        Use para:
        - Limpar recursos
        - Remover hooks
        - Fechar conexões
        """
        ...
    
    # ==========================================================================
    # MÉTODOS OPCIONAIS (hooks)
    # ==========================================================================
    
    def on_startup(self) -> None:
        """Chamado quando o OMNIA inicia."""
        pass
    
    def on_shutdown(self) -> None:
        """Chamado quando o OMNIA encerra."""
        pass
    
    def on_model_loaded(self, model: Any) -> None:
        """Chamado quando um modelo é carregado."""
        pass
    
    def on_model_unloaded(self, model: Any) -> None:
        """Chamado quando um modelo é descarregado."""
        pass
    
    def on_inference_start(self, prompt: str, **kwargs) -> None:
        """Chamado antes de iniciar inferência."""
        pass
    
    def on_inference_complete(
        self, 
        prompt: str, 
        result: Any, 
        **kwargs
    ) -> None:
        """Chamado após completar inferência."""
        pass
    
    def on_download_start(self, url: str, **kwargs) -> None:
        """Chamado quando um download inicia."""
        pass
    
    def on_download_complete(
        self, 
        url: str, 
        path: str, 
        **kwargs
    ) -> None:
        """Chamado quando um download completa."""
        pass
    
    def on_download_failed(
        self, 
        url: str, 
        error: Exception, 
        **kwargs
    ) -> None:
        """Chamado quando um download falha."""
        pass
    
    def on_benchmark_start(
        self, 
        model: Any, 
        engine: Any, 
        **kwargs
    ) -> None:
        """Chamado antes de iniciar benchmark."""
        pass
    
    def on_benchmark_complete(
        self, 
        model: Any, 
        engine: Any, 
        results: Dict, 
        **kwargs
    ) -> None:
        """Chamado após completar benchmark."""
        pass
    
    def on_scan_complete(self, models: List[Any], **kwargs) -> None:
        """Chamado após scanner finalizar."""
        pass
    
    def register_ui_components(self) -> List[Any]:
        """
        Registra componentes de UI para injeção.
        
        Returns:
            Lista de componentes (widgets, menus, etc.).
        """
        return []
    
    def register_menu_items(self) -> List[Dict]:
        """
        Registra itens de menu.
        
        Returns:
            Lista de dicionários com: {'label': str, 'action': callable}
        """
        return []
    
    # ==========================================================================
    # MÉTODOS AUXILIARES (opcionais)
    # ==========================================================================
    
    def get_settings(self) -> Dict[str, Any]:
        """
        Retorna configurações padrão do plugin.
        
        Returns:
            Dicionário de configurações.
        """
        return {}
    
    def save_settings(self, settings: Dict[str, Any]) -> bool:
        """
        Salva configurações do plugin.
        
        Args:
            settings: Configurações a salvar.
        
        Returns:
            True se salvo com sucesso.
        """
        return True
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Retorna metadados adicionais do plugin.
        
        Returns:
            Dicionário de metadados.
        """
        return {
            "category": "utility",
            "tags": ["ai", "extension"],
            "platform": "all",
        }
\`\`\`

---

# 4. Plugin Manager

## Descoberta e Carregamento

\`\`\`python
# plugins/plugin_manager.py

import importlib
import inspect
import pkgutil
from pathlib import Path
from typing import Type, Dict, List, Optional

from .plugin_base import PluginBase, PluginInfo
from .plugin_registry import PluginRegistry


class PluginManager:
    """
    Gerenciador central dos plugins.
    
    Responsabilidades:
    - Descobrir plugins no sistema
    - Carregar e ativar plugins
    - Gerenciar lifecycle (activate/deactivate)
    - Fornecer acesso ao registry
    """
    
    def __init__(self, plugins_dir: Optional[Path] = None):
        self.plugins_dir = plugins_dir or Path(__file__).parent / "builtin"
        self.registry = PluginRegistry()
        self._loaded: Dict[str, PluginBase] = {}
        self._active: List[str] = []
        
    def discover(self) -> List[str]:
        """
        Descobre plugins disponíveis.
        
        Escaneia:
        1. Plugins integrados (builtin/)
        2. Plugins externos (plugins_dir/)
        3. Plugins do sistema (site-packages)
        
        Returns:
            Lista de IDs de plugins descobertos.
        """
        discovered: List[str] = []
        
        # Descobrir plugins integrados
        for module_name in self._discover_builtin():
            discovered.append(module_name)
        
        # Descobrir plugins externos
        if self.plugins_dir.exists():
            for entry in self.plugins_dir.iterdir():
                if entry.is_dir() and (entry / "plugin.py").exists():
                    plugin_id = entry.name
                    discovered.append(plugin_id)
        
        # Atualizar registry
        for plugin_id in discovered:
            self.registry.register_available(plugin_id)
        
        return discovered
    
    def load_plugin(self, plugin_id: str) -> Optional[PluginBase]:
        """
        Carrega um plugin pelo ID.
        
        Args:
            plugin_id: Identificador do plugin.
        
        Returns:
            Instância do plugin ou None se não encontrado.
        
        Raises:
            PluginNotFoundError: Se o plugin não existe.
            PluginLoadError: Se falhar ao carregar.
        """
        if plugin_id in self._loaded:
            return self._loaded[plugin_id]
        
        # Tentar carregar plugin integrado
        try:
            plugin = self._load_builtin(plugin_id)
            if plugin:
                self._loaded[plugin_id] = plugin
                return plugin
        except Exception as e:
            pass
        
        # Tentar carregar plugin externo
        plugin_path = self.plugins_dir / plugin_id
        if plugin_path.exists():
            try:
                plugin = self._load_external(plugin_path)
                if plugin:
                    self._loaded[plugin_id] = plugin
                    return plugin
            except Exception as e:
                raise PluginLoadError(f"Failed to load plugin {plugin_id}: {e}")
        
        raise PluginNotFoundError(f"Plugin not found: {plugin_id}")
    
    def activate_plugin(self, plugin_id: str, settings: Optional[Dict] = None) -> bool:
        """
        Ativa um plugin.
        
        Args:
            plugin_id: ID do plugin a ativar.
            settings: Configurações opcionais.
        
        Returns:
            True se ativado com sucesso.
        """
        plugin = self.load_plugin(plugin_id)
        
        # Carregar configurações
        if settings:
            plugin.save_settings(settings)
        else:
            settings = plugin.get_settings()
        
        # Ativar
        try:
            plugin.on_activate()
            self._active.append(plugin_id)
            self.registry.activate(plugin_id)
            return True
        except Exception as e:
            raise PluginActivationError(f"Failed to activate {plugin_id}: {e}")
    
    def deactivate_plugin(self, plugin_id: str) -> bool:
        """
        Desativa um plugin.
        
        Args:
            plugin_id: ID do plugin a desativar.
        
        Returns:
            True se desativado com sucesso.
        """
        if plugin_id not in self._loaded:
            return False
        
        plugin = self._loaded[plugin_id]
        
        try:
            plugin.on_deactivate()
            self._active.remove(plugin_id)
            self.registry.deactivate(plugin_id)
            return True
        except Exception as e:
            raise PluginDeactivationError(f"Failed to deactivate {plugin_id}: {e}")
    
    def get_active_plugins(self) -> List[PluginBase]:
        """Retorna plugins ativos."""
        return [self._loaded[pid] for pid in self._active if pid in self._loaded]
    
    def get_hook_subscribers(self, hook_name: str) -> List[PluginBase]:
        """
        Retorna plugins que se inscreveram em um hook.
        
        Args:
            hook_name: Nome do hook (ex: 'on_model_loaded').
        
        Returns:
            Lista de plugins inscritos.
        """
        subscribers: List[PluginBase] = []
        
        for plugin in self.get_active_plugins():
            # Verificar se o plugin implementa o hook
            hook_method = getattr(plugin, hook_name, None)
            if hook_method and callable(hook_method):
                subscribers.append(plugin)
        
        return subscribers
    
    def call_hook(self, hook_name: str, *args, **kwargs) -> List[Any]:
        """
        Chama um hook em todos os plugins inscritos.
        
        Args:
            hook_name: Nome do hook.
            *args: Argumentos posicionais.
            **kwargs: Argumentos nomeados.
        
        Returns:
            Lista de resultados.
        """
        results = []
        subscribers = self.get_hook_subscribers(hook_name)
        
        for plugin in subscribers:
            try:
                method = getattr(plugin, hook_name)
                result = method(*args, **kwargs)
                if result is not None:
                    results.append(result)
            except Exception as e:
                # Logar erro mas não interromper outros plugins
                pass
        
        return results
    
    # Métodos internos
    def _discover_builtin(self) -> List[str]:
        from . import builtin
        plugins = []
        
        # Descobrir módulos no pacote builtin
        for name in dir(builtin):
            obj = getattr(builtin, name)
            if isinstance(obj, type) and issubclass(obj, PluginBase) and obj is not PluginBase:
                plugins.append(obj().name)
        
        return plugins
    
    def _load_builtin(self, plugin_id: str) -> Optional[PluginBase]:
        from . import builtin
        
        for name in dir(builtin):
            obj = getattr(builtin, name)
            if isinstance(obj, type) and issubclass(obj, PluginBase):
                instance = obj()
                if instance.name == plugin_id:
                    return instance
        return None
    
    def _load_external(self, plugin_path: Path) -> Optional[PluginBase]:
        import importlib.util
        
        spec = importlib.util.spec_from_file_location(
            "plugin_module", plugin_path / "plugin.py"
        )
        if not spec or not spec.loader:
            return None
        
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        
        # Encontrar classe Plugin
        for name in dir(module):
            obj = getattr(module, name)
            if isinstance(obj, type) and issubclass(obj, PluginBase) and obj is not PluginBase:
                return obj()
        
        return None
\`\`\`

---

# 5. Hooks

## Lista Completa

| Hook | Quando | Argumentos |
|------|--------|------------|
| \`on_startup\` | Aplicação inicia | - |
| \`on_shutdown\` | Aplicação encerra | - |
| \`on_model_loaded\` | Modelo carregado | \`model: Any\` |
| \`on_model_unloaded\` | Modelo descarregado | \`model: Any\` |
| \`on_inference_start\` | Antes de inferência | \`prompt: str, **kwargs\` |
| \`on_inference_complete\` | Após inferência | \`prompt: str, result: Any, **kwargs\` |
| \`on_download_start\` | Download inicia | \`url: str, **kwargs\` |
| \`on_download_complete\` | Download completa | \`url: str, path: str, **kwargs\` |
| \`on_download_failed\` | Download falha | \`url: str, error: Exception, **kwargs\` |
| \`on_benchmark_start\` | Benchmark inicia | \`model: Any, engine: Any, **kwargs\` |
| \`on_benchmark_complete\` | Benchmark completa | \`model: Any, engine: Any, results: Dict, **kwargs\` |
| \`on_benchmark_failed\` | Benchmark falha | \`model: Any, engine: Any, error: Exception, **kwargs\` |
| \`on_scan_complete\` | Scanner finaliza | \`models: List[Any], **kwargs\` |

## Exemplo de Uso em Plugin

\`\`\`python
class LoggingPlugin(PluginBase):
    """Plugin que registra inferências em log."""
    
    @property
    def name(self) -> str:
        return "logging"
    
    @property
    def version(self) -> str:
        return "1.0.0"
    
    @property
    def description(self) -> str:
        return "Log de inferências para auditoria"
    
    @property
    def author(self) -> str:
        return "OMNIA Team"
    
    def on_activate(self) -> None:
        # Inicializar arquivo de log
        pass
    
    def on_inference_complete(
        self, 
        prompt: str, 
        result: Any, 
        **kwargs
    ) -> None:
        # Registrar inferência
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "prompt": prompt[:100],  # Truncar
            "result_length": len(str(result)),
            "token_count": result.tokens_generated,
        }
        # Salvar em arquivo
    
    def on_deactivate(self) -> None:
        # Limpar recursos
        pass
\`\`\`

---

# 6. Plugins Previstos

## VS Code

| Propriedade | Valor |
|-------------|-------|
| **Nome** | VS Code Integration |
| **Descrição** | Integrar modelos diretamente no VS Code |
| **Hooks** | \`register_ui_components\`, \`on_model_loaded\` |
| **Permissões** | \`ui:inject\`, \`models:read\` |

**Funcionalidades:**

* Painel lateral com catálogo de modelos
* Comando para inferência rápida (Ctrl+Shift+I)
* Destaque de código gerado por IA
* Integração com workspace do usuário

---

## Docker

| Propriedade | Valor |
|-------------|-------|
| **Nome** | Docker Integration |
| **Descrição** | Empacotar modelos em containers |
| **Hooks** | \`on_model_loaded\`, \`register_menu_items\` |
| **Permissões** | \`system:exec\` |

**Funcionalidades:**

* Exportar modelos como imagens Docker
* Criar containers otimizados para inferência
* Configurar volumes de dados
* Gerenciar redes e portas

---

## GitHub

| Propriedade | Valor |
|-------------|-------|
| **Nome** | GitHub Sync |
| **Descrição** | Sincronizar catálogo e configurações |
| **Hooks** | \`on_startup\`, \`on_shutdown\` |
| **Permissões** | \`database:read\`, \`database:write\` |

**Funcionalidades:**

* Sincronizar catálogo de modelos com repositório
* Fazer backup automático para GitHub
* Restaurar configurações de outro workspace
* Compartilhar benchmarks com a comunidade

---

## WordPress

| Propriedade | Valor |
|-------------|-------|
| **Nome** | WordPress Integration |
| **Descrição** | Geração de conteúdo via IA |
| **Hooks** | \`on_inference_complete\`, \`register_ui_components\` |
| **Permissões** | \`api:rest\`, \`models:read\` |

**Funcionalidades:**

* Gerar posts automaticamente
* Criar descrições de produtos
* Traduzir conteúdo
* Gerar meta-descrições SEO

---

## n8n

| Propriedade | Valor |
|-------------|-------|
| **Nome** | n8n Automation |
| **Descrição** | Automação de fluxos com modelos locais |
| **Hooks** | \`register_menu_items\`, \`on_model_loaded\` |
| **Permissões** | \`api:rest\`, \`database:read\` |

**Funcionalidades:**

* Criar nodes customizados para n8n
* Executar inferência em workflows
* Processar dados com IA
* Integrar com APIs externas

---

## Obsidian

| Propriedade | Valor |
|-------------|-------|
| **Nome** | Obsidian RAG |
| **Descrição** | RAG com base de conhecimento Obsidian |
| **Hooks** | \`register_ui_components\`, \`on_scan_complete\` |
| **Permissões** | \`database:read\`, \`database:write\` |

**Funcionalidades:**

* Indexar notas do Obsidian
* Buscar semanticamente em vaults
* Gerar respostas baseadas em notas
* Criar links automáticos entre conceitos

---

# 7. Criando Plugin

## Passo 1: Criar Estrutura

\`\`\`bash
mkdir -p plugins/myplugin
```

```
plugins/myplugin/
├── 📄 plugin.py          # Implementação
├── 📄 manifest.json       # Manifesto do plugin
├── 📄 README.md           # Documentação
└── 📁 assets/             # Recursos (opcional)
\`\`\`

## Passo 2: Implementar Plugin

Veja exemplo em \`plugin_base.py\` acima.

## Passo 3: Criar Manifesto

\`\`\`json
{
    "name": "myplugin",
    "version": "1.0.0",
    "author": "Seu Nome",
    "description": "Descrição breve do plugin",
    "requires": ["omni-core>=1.0"],
    "permissions": ["database:read"],
    "category": "utility",
    "tags": ["custom", "example"],
    "platform": "all"
}
\`\`\`

## Passo 4: Ativar Plugin

\`\`\`python
from omnia.plugins.plugin_manager import PluginManager

manager = PluginManager()
manager.load_plugin("myplugin")
manager.activate_plugin("myplugin")
\`\`\`

---

# 8. Manifesto

## Schema Completo

\`\`\`json
{
    "name": "string",              // Obrigatório - ID único
    "version": "string",           // Obrigatório - SemVer
    "author": "string",            // Obrigatório
    "description": "string",       // Obrigatório
    "license": "string",           // Padrão: GPL-2.0-or-later
    "requires": ["string"],        // Dependências
    "permissions": ["string"],     // Permissões
    "category": "string",          // utility, ui, automation, integration
    "tags": ["string"],            // Tags de busca
    "platform": "string",          // all, windows, linux, macos
    "min_omni_version": "string",  // Versão mínima do OMNIA
    "max_omni_version": "string",  // Versão máxima compatível
    "homepage": "string",          // URL do projeto
    "repository": "string",        // URL do repositório
    "issues": "string",            // URL para reportar bugs
    "icon": "string",              // Caminho para ícone
    "dependencies": {
        "python": ["string"],       // Pacotes Python
        "system": ["string"]       // Dependências do sistema
    }
}
\`\`\`

## Exemplo Completo

\`\`\`json
{
    "name": "vscode",
    "version": "1.2.0",
    "author": "David Creator",
    "description": "Integrar modelos do OMNIA no VS Code",
    "license": "GPL-2.0-or-later",
    "requires": ["omni-core>=1.0", "omni-plugin-utils>=0.1"],
    "permissions": ["ui:inject", "database:read", "models:read"],
    "category": "integration",
    "tags": ["editor", "vscode", "development"],
    "platform": "all",
    "min_omni_version": "1.0.0",
    "homepage": "https://github.com/davidcreator/omnia-plugins/vscode",
    "repository": "https://github.com/davidcreator/omnia-plugins",
    "issues": "https://github.com/davidcreator/omnia-plugins/issues",
    "icon": "assets/icon.svg",
    "dependencies": {
        "python": ["vscode-python>=1.0"],
        "system": ["vscode>=1.70"]
    }
}
\`\`\`

---

# 9. Segurança

## Modelo de Permissões

| Permissão | Escopo | Risco |
|-----------|--------|-------|
| \`database:read\` | Ler tabelas | Baixo |
| \`database:write\` | Modificar dados | Médio |
| \`models:read\` | Ler informações de modelos | Baixo |
| \`models:write\` | Modificar/remover modelos | Alto |
| \`ui:inject\` | Injetar componentes na UI | Baixo |
| \`api:rest\` | Acessar endpoints REST | Médio |
| \`system:exec\` | Executar comandos | Alto |

## Sandboxing

Plugins operam com permissões declaradas:

* **Verificação no load** — Permissões são validadas
* **Isolamento de processo** — Plugins rodam no mesmo processo mas com restrições
* **Validação de entrada** — Todos os dados de plugins são validados
* **Limite de execução** — Hooks têm timeout

## Boas Práticas

\`\`\`python
# Sempre declare permissões mínimas
@property
def permissions(self) -> List[str]:
    return ["database:read"]  # Apenas o necessário

# Nunca solicite permissões desnecessárias
# NUNCA solicite 'system:exec' sem necessidade real

# Sempre valide dados
@classmethod
def validate_settings(cls, settings: Dict) -> bool:
    # Validar todas as entradas
    pass
\`\`\`

---

# 10. Marketplace

## Estrutura Futuro

\`\`\`
marketplace/
├── 📁 plugins/                # Plugins aprovados
│   ├── 📁 vscode/
│   ├── 📁 docker/
│   ├── 📁 github/
│   └── 📁 ...
├── 📄 index.json              # Índice do marketplace
├── 📄 approved.json           # Lista de plugins aprovados
└── 📄 guidelines.md           # Diretrizes para publicação
\`\`\`

## Processo de Publicação

1. **Desenvolver** — Criar plugin seguindo este guia
2. **Testar** — Verificar em ambiente local
3. **Documentar** — Criar README.md completo
4. **Enviar** — Abrir PR no repositório de plugins
5. **Revisar** — Manterer revisa código e permissões
6. **Aprovar** — Plugin é adicionado ao marketplace
7. **Publicar** — Disponível para instalação via UI

---

# Referências

* [Plugin Development Guide](docs/plugins.md)
* [API Reference](docs/api.md)
* [ARCHITECTURE.md](ARCHITECTURE.md)
* [Plugin Registry](plugins/plugin_registry.py)
* [Plugin Base](plugins/plugin_base.py)

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

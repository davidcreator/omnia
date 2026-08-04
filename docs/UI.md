# OMNIA

## Documentação da Interface Gráfica

**Versão:** 1.0  
**Framework:** PySide6 (Qt 6 for Python)  
**Status:** Em desenvolvimento  
**Última atualização:** 2026  

---

# 1. Visão Geral

A interface gráfica do OMNIA é construída com **PySide6**, o binding oficial do Qt 6 para Python. Foi escolhida por ser:

* ✅ **Nativa** — Performance e aparência nativa em todas as plataformas
* ✅ **Multiplataforma** — Windows, macOS, Linux
* ✅ **Moderna** — Qt 6 com suporte a High DPI e animações
* ✅ **Pythonic** — Integração perfeita com o ecossistema Python

## Características

| Característica | Descrição |
|----------------|-----------|
| **Tema** | Escuro/claro automático (system follow) |
| **Layout** | Sidebar + Main Content |
| **Navegação** | Sidebar fixa com ícones |
| **Responsivo** | Adaptável ao tamanho da janela |
| **Componentes** | Widgets reutilizáveis |
| **Estilos** | QSS (Qt Style Sheets) |

---

# 2. Tecnologia

## PySide6

| Componente | Versão | Descrição |
|-----------|--------|-----------|
| PySide6 | 6.6.0+ | Binding Qt 6 para Python |
| Qt | 6.5+ | Framework de interface |
| Python | 3.13+ | Linguagem |

## Dependências

\`\`\`toml
# pyproject.toml
[project.dependencies]
"pyside6>=6.6.0"
```

## Vantagens sobre Alternativas

| Alternativa | Vantagem do PySide6 |
|-------------|---------------------|
| **Electron** | Menor consumo de RAM, performance nativa |
| **Tkinter** | Design moderno, widgets avançados |
| **Web (Flask/Django)** | Não precisa de servidor, arquivo único |
| **Kivy** | Melhor suporte a desktop, estilos profissionais |

---

# 3. Estrutura

## 3.1 Organização de Arquivos

\`\`\`
ui/
│
├── 📄 main_window.py         # Janela principal
├── 📄 app.py                 # Aplicação Qt
├── 📄 __init__.py
│
├── 📁 views/                  # Telas completas
│   ├── 📄 dashboard.py        # Dashboard inicial
│   ├── 📄 library.py          # Biblioteca de modelos
│   ├── 📄 downloads.py        # Gerenciador de downloads
│   ├── 📄 engines_view.py     # Painel de engines
│   ├── 📄 benchmark_view.py   # Visualização de benchmarks
│   ├── 📄 agents_view.py      # Painel de agentes
│   ├── 📄 settings_view.py    # Configurações
│   └── 📄 logs_view.py        # Visualizador de logs
│
├── 📁 components/             # Widgets reutilizáveis
│   ├── 📄 sidebar.py          # Barra lateral de navegação
│   ├── 📄 model_card.py       # Card de modelo
│   ├── 📄 search_bar.py       # Barra de busca
│   ├── 📄 progress_bar.py     # Barra de progresso
│   ├── 📄 toast.py            # Notificações toast
│   └── 📄 ...
│
├── 📁 dialogs/                # Janelas modais
│   ├── 📄 model_details.py    # Detalhes do modelo
│   ├── 📄 download_dialog.py  # Diálogo de download
│   └── 📄 settings_dialog.py  # Configurações
│
└── 📁 styles/                 # Arquivos QSS
    ├── 📄 dark.qss             # Tema escuro
    ├── 📄 light.qss            # Tema claro
    └── 📄 common.qss           # Estilos compartilhados
\`\`\`

## 3.2 Hierarquia de Componentes

\`\`\`
QApplication
└── QMainWindow (MainWindow)
    ├── Sidebar (Navigation)
    │   ├── Logo / Brand
    │   ├── Nav Items (Dashboard, Library, Downloads...)
    │   └── User / Settings
    └── Main Content (StackedWidget / Area)
        ├── Dashboard View
        │   ├── Stats Cards
        │   ├── Recent Activity
        │   └── Quick Actions
        ├── Library View
        │   ├── Search Bar
        │   ├── Filter Tags
        │   ├── Model Grid (Cards)
        │   └── Pagination
        ├── Downloads View
        │   ├── Progress Bars
        │   ├── Download List
        │   └── Actions
        └── ... (outras views)
\`\`\`

---

# 4. Main Window

## Implementação

\`\`\`python
# ui/main_window.py

from PySide6.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QStackedWidget, QSplitter
)
from PySide6.QtCore import Qt, QSize
from PySide6.QtGui import QIcon

from ui.components.sidebar import Sidebar
from ui.views.dashboard import DashboardView
from ui.views.library import LibraryView


class MainWindow(QMainWindow):
    """
    Janela principal do OMNIA.
    
    Layout:
    - Sidebar (esquerda, fixo)
    - Main Content (direita, dinâmico)
    """
    
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        
        self.setWindowTitle("OMNIA — One Platform. Every AI.")
        self.setMinimumSize(1024, 768)
        self.resize(1280, 900)
        
        # Configurar janela
        self.setWindowIcon(QIcon("resources/icons/omnia.svg"))
        
        # Layout central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        main_layout = QHBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Sidebar
        self.sidebar = Sidebar()
        self.sidebar.navigation_changed.connect(self.on_navigation_changed)
        main_layout.addWidget(self.sidebar)
        
        # Main content (StackedWidget para troca de telas)
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack)
        
        # Adicionar views
        self.dashboard_view = DashboardView(self)
        self.content_stack.addWidget(self.dashboard_view)
        
        self.library_view = LibraryView(self)
        self.content_stack.addWidget(self.library_view)
        
        # Definir tela inicial
        self.content_stack.setCurrentWidget(self.dashboard_view)
        
        # Aplicar estilo
        self.load_styles()
    
    def load_styles(self) -> None:
        """Carrega arquivo QSS de estilos."""
        with open("ui/styles/dark.qss", "r") as f:
            self.setStyleSheet(f.read())
    
    def on_navigation_changed(self, view_name: str) -> None:
        """Troca de tela baseada no sidebar."""
        view_mapping = {
            "dashboard": self.dashboard_view,
            "library": self.library_view,
            # ... outras views
        }
        view = view_mapping.get(view_name)
        if view:
            self.content_stack.setCurrentWidget(view)
    
    def closeEvent(self, event) -> None:
        """Evento de fechamento da janela."""
        # Salvar configurações
        # Limpar recursos
        event.accept()
\`\`\`

---

# 5. Telas

## 5.1 Dashboard

Tela inicial com resumo do sistema.

\`\`\`python
# ui/views/dashboard.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QGridLayout, QLabel, QPushButton
from PySide6.QtCore import Qt


class StatsCard(QWidget):
    """Card de estatística."""
    
    def __init__(self, title: str, value: str, subtitle: str, icon: str, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Título
        title_label = QLabel(title)
        title_label.setObjectName("stats-title")
        
        # Valor
        value_label = QLabel(value)
        value_label.setObjectName("stats-value")
        
        # Subtítulo
        subtitle_label = QLabel(subtitle)
        subtitle_label.setObjectName("stats-subtitle")
        
        layout.addWidget(title_label)
        layout.addWidget(value_label)
        layout.addWidget(subtitle_label)


class DashboardView(QWidget):
    """Tela de dashboard."""
    
    def __init__(self, parent: QWidget | None = None):
        super().__init__(parent)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(20)
        
        # Header
        header = QLabel("Dashboard")
        header.setObjectName("view-header")
        layout.addWidget(header)
        
        # Grid de cards de estatísticas
        stats_grid = QGridLayout()
        
        stats = [
            {"title": "Modelos", "value": "42", "subtitle": "8 favoritos", "icon": "🧠"},
            {"title": "Engines", "value": "3", "subtitle": "2 disponíveis", "icon": "⚙️"},
            {"title": "Downloads", "value": "5", "subtitle": "2 ativos", "icon": "📥"},
            {"title": "Benchmarks", "value": "128", "subtitle": "Esta semana", "icon": "📊"},
        ]
        
        for i, stat in enumerate(stats):
            card = StatsCard(**stat)
            stats_grid.addWidget(card, 0, i)
        
        layout.addLayout(stats_grid)
        
        # Seção de ações rápidas
        quick_actions = QWidget()
        quick_layout = QHBoxLayout(quick_actions)
        
        actions = [
            ("Novo Modelo", "📥", lambda: print("Download")),
            ("Benchmark", "📊", lambda: print("Benchmark")),
            ("Inferência", "💬", lambda: print("Inference")),
            ("Configurações", "⚙️", lambda: print("Settings")),
        ]
        
        for text, icon, callback in actions:
            btn = QPushButton(f"{icon} {text}")
            btn.clicked.connect(callback)
            quick_layout.addWidget(btn)
        
        layout.addWidget(quick_actions)
        
        # Atividade recente
        recent = QLabel("Atividade Recente")
        recent.setObjectName("section-header")
        layout.addWidget(recent)
        
        # Lista de atividade (exemplo)
        activity_list = QWidget()
        # ... implementação
        layout.addWidget(activity_list)
\`\`\`

## 5.2 Library (Biblioteca)

Tela de catálogo de modelos com busca e filtros.

\`\`\`python
# Componentes principais:
# • Search Bar (com autocomplete)
# • Filter Tags (tags selecionáveis)
# • Model Grid (cards de modelos)
# • Pagination (se muitos modelos)
# • Sidebar Filters (formato, arquitetura, favoritos)
\`\`\`

## 5.3 Downloads

Gerenciador de downloads com progresso visual.

\`\`\`python
# Componentes:
# • Download List (nome, progresso, status)
# • Progress Bars (com porcentagem e tempo estimado)
# • Action Buttons (pausar, retomar, cancelar)
# • Retry Button (para downloads falhados)
\`\`\`

## 5.4 Engines View

Painel mostrando engines disponíveis e status.

## 5.5 Benchmark View

Visualização gráfica de benchmarks com:
* Tabelas de resultados
* Gráficos comparativos
* Exportação de dados

## 5.6 Agents View

Gerenciamento de agentes com:
* Lista de agentes
* Configuração por agente
* Histórico de conversas

---

# 6. Componentes

## 6.1 Sidebar

\`\`\`python
# ui/components/sidebar.py

class Sidebar(QWidget):
    """Barra lateral de navegação."""
    
    navigation_changed = Signal(str)  # Emite nome da view
    
    def __init__(self, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Logo
        logo = QLabel("OMNIA")
        logo.setObjectName("logo")
        layout.addWidget(logo)
        
        # Itens de navegação
        nav_items = [
            ("Dashboard", "📊", "dashboard"),
            ("Biblioteca", "📚", "library"),
            ("Downloads", "📥", "downloads"),
            ("Engines", "⚙️", "engines_view"),
            ("Benchmarks", "📈", "benchmark_view"),
            ("Agentes", "🤖", "agents_view"),
            ("Configurações", "⚙️", "settings_view"),
        ]
        
        for label, icon, name in nav_items:
            btn = QPushButton(f"{icon} {label}")
            btn.setProperty("view_name", name)
            btn.clicked.connect(lambda checked, n=name: self.navigation_changed.emit(n))
            layout.addWidget(btn)
    
    def set_active(self, view_name: str) -> None:
        """Destaca o item ativo."""
        for btn in self.findChildren(QPushButton):
            if btn.property("view_name") == view_name:
                btn.setProperty("active", True)
            else:
                btn.setProperty("active", False)
            btn.style().unpolish(btn)
            btn.style().polish(btn)
\`\`\`

## 6.2 Model Card

\`\`\`python
# ui/components/model_card.py

class ModelCard(QWidget):
    """Card de exibição de modelo."""
    
    clicked = Signal(str)  # Emite model_id
    
    def __init__(self, model_data: Dict, parent=None):
        super().__init__(parent)
        layout = QVBoxLayout(self)
        
        # Nome do modelo
        name = QLabel(model_data["name"])
        name.setObjectName("model-name")
        
        # Tags
        tags = QLabel(" | ".join(model_data.get("tags", [])))
        tags.setObjectName("model-tags")
        
        # Informações
        info = QLabel(f"{model_data['format']} • {model_data.get('size', 'N/A')}")
        info.setObjectName("model-info")
        
        # Ações
        actions = QHBoxLayout()
        load_btn = QPushButton("Carregar")
        load_btn.clicked.connect(lambda: self.clicked.emit(model_data["id"]))
        actions.addWidget(load_btn)
        
        layout.addWidget(name)
        layout.addWidget(tags)
        layout.addWidget(info)
        layout.addLayout(actions)
\`\`\`

---

# 7. Estilos QSS

## 7.1 Estrutura

\`\`\`css
/* ui/styles/common.qss */

/* Variáveis */
* {
    color: #e0e0e0;
    font-family: "Inter", sans-serif;
}

/* Aplicação */
QMainWindow {
    background-color: #1a1a2e;
}

/* Sidebar */
QWidget#sidebar {
    background-color: #16213e;
    border-right: 1px solid #0f3460;
}

/* Cards */
QFrame#card {
    background-color: #0f3460;
    border-radius: 12px;
    border: 1px solid #1a4a7a;
}
\`\`\`

## 7.2 Tema Escuro

\`\`\`css
/* ui/styles/dark.qss */

QMainWindow {
    background-color: #0f0f23;
}

/* Sidebar */
#sidebar {
    background-color: #1a1a2e;
    border-right: 1px solid #2a2a40;
}

/* Botões */
QPushButton {
    background-color: #3f3f5f;
    border: none;
    border-radius: 6px;
    padding: 8px 16px;
    color: #e0e0f0;
}

QPushButton:hover {
    background-color: #4f4f7f;
}

QPushButton:pressed {
    background-color: #2f2f4f;
}

/* Cards */
#model-card {
    background-color: #1a1a2e;
    border: 1px solid #2a2a40;
    border-radius: 12px;
    padding: 16px;
}
\`\`\`

## 7.3 Tema Claro

\`\`\`css
/* ui/styles/light.qss */

QMainWindow {
    background-color: #f5f5f7;
}

#sidebar {
    background-color: #ffffff;
    border-right: 1px solid #e5e5e5;
}

QPushButton {
    background-color: #0a84ff;
    color: white;
}
\`\`\`

---

# 8. Navegação

## 8.1 Fluxo de Navegação

\`\`\`
┌──────────────────────────────────────────────┐
│              Sidebar (Fixo)                   │
│  • Logo                                      │
│  • Dashboard  📊                             │
│  • Biblioteca 📚                             │
│  • Downloads  📥                             │
│  • Engines     ⚙️                             │
│  • Benchmarks 📈                             │
│  • Agentes     🤖                             │
│  • Configs     ⚙️                             │
└──────────────────────────────────────────────┘
                     │
                     ▼ (clicar)
        ┌──────────────────────────┐
        │     Main Content         │
        │  (Troca via QStacked)    │
        │                          │
        │  • Dashboard View        │
        │  • Library View          │
        │  • Downloads View        │
        │  • ...                   │
        └──────────────────────────┘
\`\`\`

## 8.2 Eventos de Navegação

\`\`\`python
# ui/components/sidebar.py

class Sidebar(QWidget):
    navigation_changed = Signal(str)  # Emite: "dashboard", "library", etc.
    
    def __init__(self):
        ...
        # Quando clicado:
        btn.clicked.connect(lambda: self.navigation_changed.emit("library"))
    
    # No MainWindow:
    self.sidebar.navigation_changed.connect(self.on_navigation_changed)
    def on_navigation_changed(self, view_name: str):
        self.content_stack.setCurrentWidget(self.view_mapping[view_name])
\`\`\`

---

# 9. Tema Escuro/Claro

## 9.1 Detecção Automática

\`\`\`python
# ui/app.py

from PySide6.QtGui import QPalette
from PySide6.QtWidgets import QApplication

class UIApp(QApplication):
    """Aplicação com suporte a temas."""
    
    def __init__(self, argv):
        super().__init__(argv)
        self.theme = self.detect_system_theme()
        self.apply_theme(self.theme)
    
    def detect_system_theme(self) -> str:
        """Detecta tema do sistema operacional."""
        # No macOS/Linux: consultar configuração
        # No Windows: consultar registro
        # Padrão: escuro
        return "dark"
    
    def apply_theme(self, theme: str) -> None:
        """Aplica tema via QSS."""
        with open(f"ui/styles/{theme}.qss") as f:
            self.setStyleSheet(f.read())
    
    def toggle_theme(self) -> None:
        """Alterna entre escuro e claro."""
        self.theme = "light" if self.theme == "dark" else "dark"
        self.apply_theme(self.theme)
\`\`\`

---

# 10. Responsividade

## 10.1 Princípios

* **Layout flexível** — Usar QHBoxLayout/QVBoxLayout
* **Stretch factors** — Distribuir espaço proporcionalmente
* **Scroll areas** — Para conteúdo grande
* **Wrap** — Componentes se reorganizam em janelas pequenas

## 10.2 Exemplo

\`\`\`python
# Layout responsivo
layout = QHBoxLayout()

# Sidebar com largura fixa mínima
sidebar = Sidebar()
sidebar.setFixedWidth(240)
sidbar.setMinimumWidth(200)
layout.addWidget(sidebar)

# Main content que se expande
main_area = QWidget()
main_layout = QVBoxLayout(main_area)
main_layout.setContentsMargins(20, 20, 20, 20)
layout.addWidget(main_area)

# Se janela pequena, sidebar pode ser ocultada
if self.width() < 1000:
    sidebar.hide()
    # Mostrar botão de menu
\`\`\`

---

# 11. Ícones

## 11.1 Sistema de Ícones

\`\`\`
resources/icons/
├── 📁 16x16/          # Ícones pequenos
├── 📁 24x24/          # Padrão
├── 📁 32x32/          # Grande
├── 📁 64x64/          # Extra grande
└── 📄 icon.svg        # Vetor principal
\`\`\`

## 11.2 Uso

\`\`\`python
# Carregar ícone
from PySide6.QtGui import QIcon

icon = QIcon("resources/icons/32x32/model_icon.png")
btn.setIcon(icon)
btn.setIconSize(QSize(24, 24))
\`\`\`

---

# 12. Internacionalização (i18n)

## 12.1 Estrutura

\`\`\`
ui/
├── 📁 i18n/                  # Traduções
│   ├── 📄 pt_BR.ts            # Português (Brasil)
│   ├── 📄 en_US.ts            # Inglês (EUA)
│   ├── 📄 es_ES.ts            # Espanhol
│   └── 📁 ...
└── 📁 locales/               # Arquivos .qm (compilados)
    └── 📄 pt_BR.qm
\`\`\`

## 12.2 Uso

\`\`\`python
from PySide6.QtCore import QTranslator, QLocale

# Configurar tradutor
translator = QTranslator()
translator.load(QLocale(), "omnia", "_", "ui/i18n/")
app.installTranslator(translator)

# Em código
label.setText(tr("Dashboard"))
label.setText(tr("Library"))
label.setText(tr("Model loaded: %1").arg(model_name))
\`\`\`

---

# Referências

* [PySide6 Documentation](https://doc.qt.io/qtforpython-6/)
* [Qt Style Sheets (QSS)](https://doc.qt.io/qt-6/stylesheet-reference.html)
* [Qt Designer Manual](https://doc.qt.io/qt-6/qtdesigner-manual.html)
* [ARCHITECTURE.md](ARCHITECTURE.md)

---

*Documento mantido por David L. Almeida — David Creator*  
*Licença: GPL-2.0-or-later*
`;

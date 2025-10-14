import streamlit as st

# Configurações do app
st.set_page_config(
    page_title="Dashboard Empresarial - Vendas & Leads",
    layout="wide",
    page_icon="📊",
    initial_sidebar_state="expanded"
)

# Carregar CSS
def load_css():
    try:
        # Tentar com UTF-8 primeiro
        with open("styles/app.css", "r", encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except UnicodeDecodeError:
        # Se UTF-8 falhar, tentar latin-1
        with open("styles/app.css", "r", encoding="latin-1") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Aplicar estilos CSS
load_css()

# Header principal
st.markdown("""
<div class="dashboard-header">
    <h1>🚀 DASHBOARD EMPRESARIAL</h1>
    <p>Análise Completa de Vendas & Performance de Leads</p>
    <div>
        <span>📊 Visualizar Dados</span>
        <span>📈 Gráficos Vendas</span>
        <span>📈👥 Gráficos Leads</span>
        <span>⚙️ Configurações</span>
        <span>👥 Leads do painel</span>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar com navegação
st.sidebar.markdown("""
<div>
    <h2>🧭 NAVEGAÇÃO</h2>
</div>
""", unsafe_allow_html=True)

st.sidebar.markdown("""
### 📊 DASHBOARDS

**🎯 Vendas**  
Análise de performance comercial  
*Métricas, gráficos e tendências*

**👥 Leads**  
Gestão de leads e conversões  
*Perfil, comportamento e analytics*

**📈 Analytics**  
Visualização de dados completa  
*Gráficos interativos e relatórios*

### 🔧 UTILIDADES

**📋 Visualizar Dados**  
Editar dados como Excel  
*Tabelas editáveis em tempo real*

**⚙️ Configurações**  
Importar/exportar dados  
*Gerenciamento do sistema*
""")

# Footer na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("""
<div>
    <strong>Dashboard Empresarial v2.0</strong><br>
    Desenvolvido com Streamlit
</div>
""", unsafe_allow_html=True)

# Conteúdo principal
st.markdown("""
<div class="main-content">
    <h3>Selecione uma página na sidebar para começar</h3>
    <p>Use o menu de navegação à esquerda para acessar as diferentes funcionalidades do dashboard.</p>
</div>
""", unsafe_allow_html=True)
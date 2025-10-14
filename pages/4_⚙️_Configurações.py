import streamlit as st
from utils.core.session_manager import SessionManager  # ✅ CORRETO

# Inicializar aplicação
SessionManager.initialize_app()

st.set_page_config(page_title="Configurações", page_icon="⚙️", layout="wide")
st.title("⚙️ Configurações")

# Menu de navegação entre subpáginas
st.sidebar.title("🔧 Configurações")
page = st.sidebar.radio(
    "Navegar para:",
    ["📤 Exportar Dados", "📥 Importar Dados", "➕ Gerenciar Colunas", "🔄 Manutenção"]
)

# Navegação entre páginas
if page == "📤 Exportar Dados":
    from utils.config.export_manager import ExportManager
    ExportManager.render()
    
elif page == "📥 Importar Dados":
    from utils.config.import_manager import ImportManager
    ImportManager.render()
    
elif page == "➕ Gerenciar Colunas":
    from utils.config.columns_manager import ColumnsManager
    ColumnsManager.render()
    
elif page == "🔄 Manutenção":
    from utils.config.management_manager import ManagementManager
    ManagementManager.render()
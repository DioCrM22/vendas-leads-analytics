import streamlit as st
from utils.core.session_manager import SessionManager  # ✅ CORRETO
from utils.components import UIComponents  # ✅ CORRETO

class ManagementManager:
    """Gerencia operações de manutenção do sistema"""
    
    @staticmethod
    def render():
        st.subheader("🔄 Manutenção do Sistema")
        
        # UIComponents.stats_overview() - REMOVIDO (método não existe)
        st.info("Gerencie a manutenção dos dados do sistema")
        
        st.markdown("### 🛠️ Ações de Manutenção")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### 💰 Dados de Vendas")
            if st.button("🔄 Restaurar Vendas", use_container_width=True):
                SessionManager.restore_category('vendas')
                st.success("✅ Vendas restauradas!")
                st.rerun()
            
            if st.button("🗑️ Limpar Vendas", use_container_width=True):
                SessionManager.clear_category('vendas')
                st.success("✅ Vendas limpas!")
                st.rerun()
        
        with col2:
            st.markdown("#### 👥 Dados de Leads")
            if st.button("🔄 Restaurar Leads", use_container_width=True):
                SessionManager.restore_category('leads')
                st.success("✅ Leads restaurados!")
                st.rerun()
            
            if st.button("🗑️ Limpar Leads", use_container_width=True):
                SessionManager.clear_category('leads')
                st.success("✅ Leads limpos!")
                st.rerun()
        
        st.markdown("---")
        if st.button("🔄 RESTAURAR TODOS OS DADOS", type="primary", use_container_width=True):
            SessionManager.restore_category('vendas')
            SessionManager.restore_category('leads')
            st.success("✅ Todos os dados restaurados!")
            st.rerun()
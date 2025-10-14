import streamlit as st
from utils.core.session_manager import SessionManager  # ✅ CORRETO
from utils.import_helpers import get_session_df  # ✅ CORRETO

class ExportManager:
    """Gerencia exportação de dados"""
    
    @staticmethod
    def render():
        st.subheader("📤 Exportar Dados")
        
        tab_vendas, tab_leads = st.tabs(["💰 Vendas", "👥 Leads"])
        
        with tab_vendas:
            ExportManager._render_category('vendas')
        
        with tab_leads:
            ExportManager._render_category('leads')
    
    @staticmethod
    def _render_category(category: str):
        configs = SessionManager.get_table_configs()[category]
        st.markdown(f"### 📊 {category.title()}")
        
        cols = st.columns(2)
        for idx, config in enumerate(configs):
            with cols[idx % 2]:
                df = get_session_df(config["data_key"])
                
                # Botão de download simplificado (substituindo download_csv_button)
                if not df.empty:
                    csv_data = df.to_csv(index=False)
                    st.download_button(
                        label=f"📥 {config['title']}",
                        data=csv_data,
                        file_name=f"{config['data_key']}.csv",
                        mime="text/csv",
                        key=f"export_{config['key']}",
                        use_container_width=True
                    )
                else:
                    st.button(
                        f"📥 {config['title']}",
                        disabled=True,
                        use_container_width=True,
                        help="Nenhum dado disponível para exportar"
                    )
import pandas as pd
import streamlit as st
from utils.core.session_manager import SessionManager  # ✅ CORRETO
from utils.import_helpers import get_session_df, save_to_session  # ✅ CORRETO
from utils.core.validation import DataValidator  # ✅ CORRETO
from utils.components import UIComponents  # ✅ CORRETO

class ImportManager:
    """Gerencia importação de dados"""
    
    @staticmethod
    def render():
        st.subheader("📥 Importar Dados")
        
        tab_vendas, tab_leads = st.tabs(["💰 Vendas", "👥 Leads"])
        
        with tab_vendas:
            ImportManager._render_category('vendas')
        
        with tab_leads:
            ImportManager._render_category('leads')
    
    @staticmethod
    def _render_category(category: str):
        configs = SessionManager.get_table_configs()[category]
        
        selected_config = st.selectbox(
            "Selecione a tabela:",
            options=configs,
            format_func=lambda x: x["title"],
            key=f"select_{category}"
        )
        
        ImportManager._render_import_interface(selected_config)
    
    @staticmethod
    def _render_import_interface(config: dict):
        data_key = config["data_key"]
        
        import_option = st.radio(
            "Tipo de importação:",
            ["Substituir Tabela Completa", "Adicionar Linhas"],
            horizontal=True,
            key=f"option_{data_key}"
        )
        
        # Preview dos dados atuais
        st.markdown("### 📋 Dados Atuais")
        current_df = get_session_df(data_key)
        if not current_df.empty:
            st.dataframe(current_df, use_container_width=True)
            st.write(f"**Total de registros:** {len(current_df)}")
        else:
            st.info("Nenhum dado disponível atualmente")
        
        uploaded_file = st.file_uploader(
            f"📤 Escolher arquivo CSV para {config['title']}",
            type=['csv'],
            key=f"file_{data_key}"
        )
        
        if uploaded_file:
            ImportManager._process_upload(uploaded_file, data_key, config['title'], import_option)
    
    @staticmethod
    def _process_upload(uploaded_file, data_key: str, display_name: str, import_option: str):
        try:
            df_raw = pd.read_csv(uploaded_file)
            current_df = get_session_df(data_key)
            
            # Validar estrutura dos dados
            is_valid, message, df_sanitized = DataValidator.validate_dataframe_structure(df_raw, data_key)
            
            if not is_valid:
                st.error(f"❌ {message}")
                return
            
            # Mostrar avisos ou sucesso
            if "avisos" in message.lower():
                st.warning(message)
            else:
                st.success(message)
            
            # Preview dos novos dados
            st.markdown("### 📊 Novos Dados")
            st.dataframe(df_sanitized, use_container_width=True)
            st.write(f"**Registros a importar:** {len(df_sanitized)}")
            
            ImportManager._render_confirmation(data_key, display_name, import_option, current_df, df_sanitized)
            
        except Exception as e:
            st.error(f"❌ Erro ao processar arquivo: {str(e)}")
    
    @staticmethod
    def _render_confirmation(data_key: str, display_name: str, import_option: str, current_df: pd.DataFrame, new_df: pd.DataFrame):
        st.markdown("---")
        st.markdown("### ✅ Confirmação de Importação")
        
        # Simulação (simplificada)
        if st.button("🎯 Simular Importação", key=f"sim_{data_key}"):
            if import_option == "Substituir Tabela Completa":
                st.info(f"**Simulação:** Substituirá {len(current_df)} registros por {len(new_df)} novos registros")
            else:
                st.info(f"**Simulação:** Adicionará {len(new_df)} registros aos {len(current_df)} existentes")
        
        if import_option == "Substituir Tabela Completa":
            st.warning("⚠️ Substituirá todos os dados atuais!")
            if st.button("🔄 Confirmar Substituição", type="primary", key=f"confirm_{data_key}"):
                save_to_session(data_key, new_df)
                st.success(f"✅ {display_name} substituída com sucesso!")
                st.rerun()
        
        elif import_option == "Adicionar Linhas":
            st.info(f"➕ Adicionará {len(new_df)} novas linhas")
            if st.button("➕ Adicionar Linhas", type="secondary", key=f"add_{data_key}"):
                combined_df = pd.concat([current_df, new_df], ignore_index=True)
                save_to_session(data_key, combined_df)
                st.success(f"✅ {len(new_df)} linhas adicionadas!")
                st.rerun()
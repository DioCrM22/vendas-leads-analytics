import streamlit as st
from utils.core.session_manager import SessionManager
from utils.import_helpers import get_session_df 
from utils.core.validation import DataValidator 
from utils.components import UIComponents 

class ColumnsManager:
    """Gerencia adição de novas colunas"""
    
    @staticmethod
    def render():
        st.subheader("➕ Gerenciar Colunas")
        st.info("Adicione novas colunas às tabelas existentes do sistema.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            categoria = st.selectbox("Categoria:", ["vendas", "leads"], key="add_col_categoria")
        
        with col2:
            configs = SessionManager.get_table_configs()[categoria]
            tabela_selecionada = st.selectbox(
                "Selecione a Tabela:",
                options=configs,
                format_func=lambda x: x["title"],
                key="add_col_tabela"
            )
        
        ColumnsManager._render_column_form(tabela_selecionada)
    
    @staticmethod
    def _render_column_form(config: dict):
        data_key = config["data_key"]
        df_atual = get_session_df(data_key)
        
        st.markdown("### 📋 Estrutura Atual")
        if not df_atual.empty:
            st.write(f"**Tabela:** {config['title']}")
            st.write(f"**Colunas:** {', '.join(df_atual.columns.tolist())}")
            st.write(f"**Registros:** {len(df_atual)}")
        
        st.markdown("### 🆕 Nova Coluna")
        nome_coluna = st.text_input("Nome da Coluna*", placeholder="custo, roi, observacoes")
        tipo_coluna = st.selectbox("Tipo de Dado*", ["Texto", "Número", "Data", "Booleano"])
        
        # Validação
        if nome_coluna:
            is_valid, message = DataValidator.validate_column_addition(data_key, nome_coluna, tipo_coluna)
            if not is_valid:
                st.error(f"❌ {message}")
        
        if st.button("✅ Adicionar Coluna", type="primary") and nome_coluna:
            ColumnsManager._add_column(data_key, nome_coluna, tipo_coluna)
    
    @staticmethod
    def _add_column(data_key: str, nome_coluna: str, tipo_coluna: str):
        try:
            if data_key not in st.session_state:
                st.error(f"❌ Tabela não encontrada")
                return
            
            # Valor padrão baseado no tipo
            valor_padrao = ""
            if tipo_coluna == "Número":
                valor_padrao = 0
            elif tipo_coluna == "Booleano":
                valor_padrao = False
            
            # Adicionar coluna
            novos_dados = [dict(registro, **{nome_coluna: valor_padrao}) for registro in st.session_state[data_key]]
            st.session_state[data_key] = novos_dados
            
            st.success(f"✅ Coluna '{nome_coluna}' adicionada com sucesso!")
            st.rerun()
            
        except Exception as e:
            st.error(f"❌ Erro ao adicionar coluna: {str(e)}")
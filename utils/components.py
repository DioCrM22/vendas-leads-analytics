"""
Componentes de UI reutilizáveis para o dashboard
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List, Callable
from .import_helpers import get_session_df, save_to_session

class UIComponents:
    """Componentes de interface do usuário reutilizáveis"""
    
    @staticmethod
    def metric_card(value: str, label: str, color: str = "#3498db", help_text: str = None) -> None:
        """
        Componente de cartão de métrica estilizado
        """
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, {color}20, {color}40);
            border: 1px solid {color}30;
            border-radius: 10px;
            padding: 1.5rem;
            text-align: center;
            margin: 0.5rem 0;
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        ">
            <div style="font-size: 2rem; font-weight: bold; color: {color};">
                {value}
            </div>
            <div style="font-size: 0.9rem; color: #666; margin-top: 0.5rem;">
                {label}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        if help_text:
            st.caption(f"💡 {help_text}")
    
    @staticmethod
    def data_table_with_controls(
        data_key: str, 
        title: str, 
        default_columns: List[str] = None,
        editable: bool = True
    ) -> None:
        """
        Tabela de dados com controles de edição
        """
        st.subheader(title)
        
        # Obter dados da sessão
        df = get_session_df(data_key, default_columns)
        
        # Controles superiores
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            if editable and st.button("➕ Adicionar Linha", key=f"add_{data_key}"):
                new_row = {col: "" for col in df.columns} if not df.empty else {}
                df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                save_to_session(data_key, df)
                st.rerun()
        
        with col2:
            if editable and st.button("🗑️ Limpar Tabela", key=f"clear_{data_key}"):
                df = pd.DataFrame(columns=default_columns or [])
                save_to_session(data_key, df)
                st.rerun()
        
        with col3:
            if not df.empty:
                st.download_button(
                    "📥 Exportar CSV",
                    df.to_csv(index=False),
                    f"{data_key}.csv",
                    "text/csv"
                )
        
        # Exibir tabela
        if not df.empty:
            if editable:
                edited_df = st.data_editor(
                    df,
                    use_container_width=True,
                    num_rows="dynamic",
                    key=f"editor_{data_key}"
                )
                # Salvar alterações
                if not edited_df.equals(df):
                    save_to_session(data_key, edited_df)
                    st.success("✅ Alterações salvas!")
            else:
                st.dataframe(df, use_container_width=True)
        else:
            st.info("📝 Nenhum dado disponível. Adicione dados para começar.")
    
    @staticmethod
    def filter_sidebar(filters_config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Sidebar de filtros dinâmica
        """
        filters = {}
        
        st.sidebar.markdown("### 🔍 Filtros")
        
        for filter_name, config in filters_config.items():
            filter_type = config.get('type', 'select')
            
            if filter_type == 'select':
                options = config.get('options', [])
                default = config.get('default', [])
                filters[filter_name] = st.sidebar.multiselect(
                    config.get('label', filter_name),
                    options,
                    default=default
                )
            elif filter_type == 'slider':
                min_val = config.get('min', 0)
                max_val = config.get('max', 100)
                default_val = config.get('default', (min_val, max_val))
                filters[filter_name] = st.sidebar.slider(
                    config.get('label', filter_name),
                    min_val,
                    max_val,
                    default_val
                )
        
        # Botão para limpar filtros
        if st.sidebar.button("🧹 Limpar Filtros"):
            filters = {}
            st.rerun()
        
        return filters
    
    @staticmethod
    def success_message(message: str) -> None:
        """Exibe mensagem de sucesso estilizada"""
        st.markdown(f"""
        <div style="
            background-color: #d4edda;
            border: 1px solid #c3e6cb;
            border-radius: 5px;
            padding: 12px;
            color: #155724;
            margin: 10px 0;
        ">
            ✅ {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def error_message(message: str) -> None:
        """Exibe mensagem de erro estilizada"""
        st.markdown(f"""
        <div style="
            background-color: #f8d7da;
            border: 1px solid #f5c6cb;
            border-radius: 5px;
            padding: 12px;
            color: #721c24;
            margin: 10px 0;
        ">
            ❌ {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def warning_message(message: str) -> None:
        """Exibe mensagem de aviso estilizada"""
        st.markdown(f"""
        <div style="
            background-color: #fff3cd;
            border: 1px solid #ffeaa7;
            border-radius: 5px;
            padding: 12px;
            color: #856404;
            margin: 10px 0;
        ">
            ⚠️ {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def info_message(message: str) -> None:
        """Exibe mensagem informativa estilizada"""
        st.markdown(f"""
        <div style="
            background-color: #d1ecf1;
            border: 1px solid #bee5eb;
            border-radius: 5px;
            padding: 12px;
            color: #0c5460;
            margin: 10px 0;
        ">
            ℹ️ {message}
        </div>
        """, unsafe_allow_html=True)
    
    @staticmethod
    def loading_spinner(text: str = "Carregando..."):
        """
        Decorator para exibir spinner durante execução
        """
        def decorator(func):
            def wrapper(*args, **kwargs):
                with st.spinner(text):
                    return func(*args, **kwargs)
            return wrapper
        return decorator
    
    @staticmethod
    def chart_container(func: Callable) -> None:
        """
        Container estilizado para gráficos
        """
        st.markdown('<div class="chart-container">', unsafe_allow_html=True)
        func()
        st.markdown('</div>', unsafe_allow_html=True)
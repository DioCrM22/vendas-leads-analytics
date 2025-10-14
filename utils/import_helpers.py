"""
Helpers para importação e manipulação de dados da sessão
"""

import streamlit as st
import pandas as pd
from typing import Optional, Dict, Any, List

def get_session_df(data_key: str, default_columns: List[str] = None) -> pd.DataFrame:
    """
    Obtém DataFrame do session_state ou cria um vazio
    """
    try:
        if data_key in st.session_state and st.session_state[data_key]:
            data = st.session_state[data_key]
            if isinstance(data, list):
                return pd.DataFrame(data)
            elif isinstance(data, pd.DataFrame):
                return data.copy()
            else:
                return pd.DataFrame()
        else:
            if default_columns:
                return pd.DataFrame(columns=default_columns)
            return pd.DataFrame()
    except Exception as e:
        st.error(f"Erro ao carregar dados de {data_key}: {str(e)}")
        return pd.DataFrame(columns=default_columns or [])

def save_to_session(data_key: str, data: Any) -> None:
    """
    Salva dados no session_state
    """
    try:
        if isinstance(data, pd.DataFrame):
            st.session_state[data_key] = data.to_dict('records')
        else:
            st.session_state[data_key] = data
    except Exception as e:
        st.error(f"Erro ao salvar dados em {data_key}: {str(e)}")

def clear_session_data(data_key: str) -> None:
    """
    Limpa dados específicos do session_state
    """
    if data_key in st.session_state:
        del st.session_state[data_key]

def get_session_value(key: str, default: Any = None) -> Any:
    """
    Obtém valor do session_state com fallback
    """
    return st.session_state.get(key, default)

def set_session_value(key: str, value: Any) -> None:
    """
    Define valor no session_state
    """
    st.session_state[key] = value

def initialize_session_defaults(defaults: Dict[str, Any]) -> None:
    """
    Inicializa valores padrão no session_state
    """
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value
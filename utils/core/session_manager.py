import streamlit as st
# CORREÇÃO: Importar dos caminhos absolutos corretos
from utils.vendas.data_manager import initialize_session_data
from utils.leads.leads_manager import initialize_leads_data

class SessionManager:
    """Gerencia o estado da sessão e inicialização de dados"""
    
    @staticmethod
    def initialize_app():
        """Inicializa todos os dados da aplicação"""
        if 'app_initialized' not in st.session_state:
            initialize_session_data()  # ✅ Agora do caminho correto
            initialize_leads_data()    # ✅ Agora do caminho correto
            st.session_state.app_initialized = True
    
    @staticmethod
    def get_table_configs():
        """Retorna configurações das tabelas"""
        return {
            'vendas': [
                {"key": "mensal", "title": "📅 Mensal", "data_key": "dados_mensais"},
                {"key": "estados", "title": "🗺️ Estados", "data_key": "dados_estados"},
                {"key": "marcas", "title": "🚗 Marcas", "data_key": "dados_marcas"},
                {"key": "lojas", "title": "🏪 Lojas", "data_key": "dados_lojas"},
                {"key": "visitas", "title": "📱 Visitas", "data_key": "dados_visitas"}
            ],
            'leads': [
                {"key": "genero", "title": "👥 Gênero", "data_key": "dados_genero"},
                {"key": "status_prof", "title": "💼 Status Profissional", "data_key": "dados_status_profissional"},
                {"key": "faixa_etaria", "title": "🎂 Faixa Etária", "data_key": "dados_faixa_etaria"},
                {"key": "faixa_salarial", "title": "💰 Faixa Salarial", "data_key": "dados_faixa_salarial"},
                {"key": "classificacao", "title": "🚗 Classificação Veículos", "data_key": "dados_classificacao_veiculo"},
                {"key": "idade_veiculo", "title": "📅 Idade Veículos", "data_key": "dados_idade_veiculo"},
                {"key": "veiculos", "title": "🏆 Veículos Visitados", "data_key": "dados_veiculos_visitados"}
            ]
        }
    
    @staticmethod
    def clear_category(category: str):
        """Limpa dados de uma categoria"""
        configs = SessionManager.get_table_configs()[category]
        for config in configs:
            st.session_state[config["data_key"]] = []
    
    @staticmethod
    def restore_category(category: str):
        """Restaura dados de uma categoria"""
        configs = SessionManager.get_table_configs()[category]
        for config in configs:
            if config["data_key"] in st.session_state:
                del st.session_state[config["data_key"]]
        
        if category == 'vendas':
            initialize_session_data()
        else:
            initialize_leads_data()
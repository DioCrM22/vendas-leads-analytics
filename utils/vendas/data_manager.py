import pandas as pd
import streamlit as st
from typing import Dict, List, Any

class VendasDataManager:
    """Gerenciador específico para dados de vendas"""
    
    # Dados padrão de vendas
    DEFAULT_MENSAL_DATA = [
        {'mes': 'set-20', 'leads': 26, 'vendas': 5, 'receita': 259, 'conversao': 0.19, 'ticket_medio': 51.9},
        {'mes': 'out-20', 'leads': 931, 'vendas': 35, 'receita': 1676, 'conversao': 0.04, 'ticket_medio': 47.9},
        {'mes': 'nov-20', 'leads': 1207, 'vendas': 44, 'receita': 2279, 'conversao': 0.04, 'ticket_medio': 51.8},
        {'mes': 'dez-20', 'leads': 1008, 'vendas': 33, 'receita': 2603, 'conversao': 0.03, 'ticket_medio': 78.9},
        {'mes': 'jan-21', 'leads': 1058, 'vendas': 32, 'receita': 2297, 'conversao': 0.03, 'ticket_medio': 71.8},
        {'mes': 'fev-21', 'leads': 1300, 'vendas': 68, 'receita': 3631, 'conversao': 0.05, 'ticket_medio': 53.4},
        {'mes': 'mar-21', 'leads': 1932, 'vendas': 119, 'receita': 7911, 'conversao': 0.06, 'ticket_medio': 66.5},
        {'mes': 'abr-21', 'leads': 2376, 'vendas': 142, 'receita': 7478, 'conversao': 0.06, 'ticket_medio': 52.7},
        {'mes': 'mai-21', 'leads': 3819, 'vendas': 394, 'receita': 21508, 'conversao': 0.10, 'ticket_medio': 54.6},
        {'mes': 'jun-21', 'leads': 4440, 'vendas': 589, 'receita': 33179, 'conversao': 0.13, 'ticket_medio': 56.3},
        {'mes': 'jul-21', 'leads': 6130, 'vendas': 1073, 'receita': 58988, 'conversao': 0.18, 'ticket_medio': 55.0},
        {'mes': 'ago-21', 'leads': 6353, 'vendas': 1254, 'receita': 68274, 'conversao': 0.20, 'ticket_medio': 54.4}
    ]

    DEFAULT_ESTADOS_DATA = [
        {'estado': 'São Paulo', 'uf': 'SP', 'vendas': 734, 'lat': -23.5505, 'lon': -46.6333, 'regiao': 'Sudeste'},
        {'estado': 'Minas Gerais', 'uf': 'MG', 'vendas': 142, 'lat': -19.9167, 'lon': -43.9345, 'regiao': 'Sudeste'},
        {'estado': 'Santa Catarina', 'uf': 'SC', 'vendas': 110, 'lat': -27.5954, 'lon': -48.5480, 'regiao': 'Sul'},
        {'estado': 'Rio Grande do Sul', 'uf': 'RS', 'vendas': 98, 'lat': -30.0346, 'lon': -51.2177, 'regiao': 'Sul'},
        {'estado': 'Rio de Janeiro', 'uf': 'RJ', 'vendas': 66, 'lat': -22.9068, 'lon': -43.1729, 'regiao': 'Sudeste'}
    ]

    DEFAULT_MARCAS_DATA = [
        {'marca': 'FIAT', 'vendas': 248, 'categoria': 'Popular'},
        {'marca': 'CHEVROLET', 'vendas': 237, 'categoria': 'Popular'},
        {'marca': 'VOLKSWAGEN', 'vendas': 193, 'categoria': 'Popular'},
        {'marca': 'FORD', 'vendas': 136, 'categoria': 'SUV'},
        {'marca': 'RENAULT', 'vendas': 108, 'categoria': 'Popular'}
    ]

    DEFAULT_LOJAS_DATA = [
        {'loja': 'KIYOKO CILEIDI JERY LTDA', 'vendas': 18, 'cidade': 'São Paulo', 'estado': 'SP'},
        {'loja': 'CLAUDINEO JOZENAIDE LUYANE LTDA', 'vendas': 15, 'cidade': 'Belo Horizonte', 'estado': 'MG'},
        {'loja': 'ADO JUBERTH VALTUIDES LTDA', 'vendas': 10, 'cidade': 'Florianópolis', 'estado': 'SC'},
        {'loja': 'GERRIVALDO ROSIELEN VALTEIDE LTDA', 'vendas': 10, 'cidade': 'Porto Alegre', 'estado': 'RS'},
        {'loja': 'NILFA CID SILVANDRO LTDA', 'vendas': 10, 'cidade': 'Rio de Janeiro', 'estado': 'RJ'}
    ]

    DEFAULT_VISITAS_DATA = [
        {'dia_semana': 'domingo', 'visitas': 67, 'ordem': 0},
        {'dia_semana': 'segunda', 'visitas': 1301, 'ordem': 1},
        {'dia_semana': 'terça', 'visitas': 1238, 'ordem': 2},
        {'dia_semana': 'quarta', 'visitas': 1038, 'ordem': 3},
        {'dia_semana': 'quinta', 'visitas': 1076, 'ordem': 4},
        {'dia_semana': 'sexta', 'visitas': 956, 'ordem': 5},
        {'dia_semana': 'sábado', 'visitas': 677, 'ordem': 6}
    ]

    DATA_MAPPINGS = {
        'dados_mensais': DEFAULT_MENSAL_DATA,
        'dados_estados': DEFAULT_ESTADOS_DATA,
        'dados_marcas': DEFAULT_MARCAS_DATA,
        'dados_lojas': DEFAULT_LOJAS_DATA,
        'dados_visitas': DEFAULT_VISITAS_DATA
    }

    @staticmethod
    def initialize_session_data():
        """Inicializa dados de vendas na session_state"""
        for data_key, default_data in VendasDataManager.DATA_MAPPINGS.items():
            if data_key not in st.session_state:
                st.session_state[data_key] = default_data

    @staticmethod
    def get_dataframes() -> Dict[str, pd.DataFrame]:
        """Retorna todos os dados de vendas como DataFrames"""
        return {
            'mensal': pd.DataFrame(st.session_state.dados_mensais),
            'estados': pd.DataFrame(st.session_state.dados_estados),
            'marcas': pd.DataFrame(st.session_state.dados_marcas),
            'lojas': pd.DataFrame(st.session_state.dados_lojas),
            'visitas': pd.DataFrame(st.session_state.dados_visitas)
        }

    @staticmethod
    def calculate_kpis() -> Dict[str, float]:
        """Calcula KPIs específicos de vendas"""
        if 'dados_mensais' not in st.session_state:
            return {
                'total_receita': 0,
                'total_vendas': 0,
                'total_leads': 0,
                'conversao_media': 0
            }
            
        total_receita = sum(item['receita'] for item in st.session_state.dados_mensais)
        total_vendas = sum(item['vendas'] for item in st.session_state.dados_mensais)
        total_leads = sum(item['leads'] for item in st.session_state.dados_mensais)
        conversao_media = (total_vendas / total_leads) * 100 if total_leads > 0 else 0
        
        return {
            'total_receita': total_receita,
            'total_vendas': total_vendas,
            'total_leads': total_leads,
            'conversao_media': conversao_media
        }

    @staticmethod
    def get_monthly_summary() -> Dict[str, Any]:
        """Retorna resumo mensal para análises"""
        df_mensal = pd.DataFrame(st.session_state.dados_mensais)
        
        if df_mensal.empty:
            return {}
            
        ultimo_mes = df_mensal.iloc[-1]
        penultimo_mes = df_mensal.iloc[-2] if len(df_mensal) > 1 else ultimo_mes
        
        crescimento_receita = ((ultimo_mes['receita'] - penultimo_mes['receita']) / penultimo_mes['receita']) * 100
        crescimento_vendas = ((ultimo_mes['vendas'] - penultimo_mes['vendas']) / penultimo_mes['vendas']) * 100
        
        return {
            'ultimo_mes': ultimo_mes['mes'],
            'receita_ultimo_mes': ultimo_mes['receita'],
            'vendas_ultimo_mes': ultimo_mes['vendas'],
            'crescimento_receita': crescimento_receita,
            'crescimento_vendas': crescimento_vendas,
            'ticket_medio_ultimo_mes': ultimo_mes['ticket_medio']
        }

    @staticmethod
    def get_top_performers() -> Dict[str, List]:
        """Retorna os melhores desempenhos"""
        dfs = VendasDataManager.get_dataframes()
        
        top_estados = dfs['estados'].nlargest(3, 'vendas')[['estado', 'vendas']].to_dict('records')
        top_marcas = dfs['marcas'].nlargest(3, 'vendas')[['marca', 'vendas']].to_dict('records')
        top_lojas = dfs['lojas'].nlargest(3, 'vendas')[['loja', 'vendas']].to_dict('records')
        
        return {
            'top_estados': top_estados,
            'top_marcas': top_marcas,
            'top_lojas': top_lojas
        }

# Aliases para compatibilidade
initialize_session_data = VendasDataManager.initialize_session_data
get_dataframes = VendasDataManager.get_dataframes
calculate_kpis = VendasDataManager.calculate_kpis
import pandas as pd
import streamlit as st
from typing import Dict, List, Any

class LeadsDataManager:
    """Gerenciador específico para dados de leads"""
    
    # Dados padrão de leads
    DEFAULT_GENERO_DATA = [
        {'genero': 'mulheres', 'leads': 15106},
        {'genero': 'homens', 'leads': 10003}
    ]

    DEFAULT_STATUS_PROFISSIONAL_DATA = [
        {'status': 'estudante', 'leads_percent': 0},
        {'status': 'funcionário(a) público(a)', 'leads_percent': 2},
        {'status': 'aposentado(a)', 'leads_percent': 4},
        {'status': 'freelancer', 'leads_percent': 5},
        {'status': 'autônomo(a)', 'leads_percent': 7},
        {'status': 'empresário(a)', 'leads_percent': 8},
        {'status': 'outro', 'leads_percent': 9},
        {'status': 'clt', 'leads_percent': 65}
    ]

    DEFAULT_FAIXA_ETARIA_DATA = [
        {'faixa': '80+', 'leads_percent': 0},
        {'faixa': '60-80', 'leads_percent': 19},
        {'faixa': '40-60', 'leads_percent': 30},
        {'faixa': '20-40', 'leads_percent': 49},
        {'faixa': '0-20', 'leads_percent': 2}
    ]

    DEFAULT_FAIXA_SALARIAL_DATA = [
        {'faixa': '20000+', 'leads_percent': 2, 'ordem': 5},
        {'faixa': '15000-20000', 'leads_percent': 2, 'ordem': 4},
        {'faixa': '10000-15000', 'leads_percent': 10, 'ordem': 3},
        {'faixa': '5000-10000', 'leads_percent': 71, 'ordem': 2},
        {'faixa': '0-5000', 'leads_percent': 16, 'ordem': 1}
    ]

    DEFAULT_CLASSIFICACAO_VEICULO_DATA = [
        {'classificacao': 'novo', 'visitas': 1162},
        {'classificacao': 'seminovo', 'visitas': 29418}
    ]

    DEFAULT_IDADE_VEICULO_DATA = [
        {'idade': 'até 2 anos', 'visitas_percent': 4, 'ordem': 1},
        {'idade': 'de 2 à 4 anos', 'visitas_percent': 11, 'ordem': 2},
        {'idade': 'de 4 à 6 anos', 'visitas_percent': 18, 'ordem': 3},
        {'idade': 'de 6 à 8 anos', 'visitas_percent': 20, 'ordem': 4},
        {'idade': 'de 8 à 10 anos', 'visitas_percent': 25, 'ordem': 5},
        {'idade': 'acima de 10 anos', 'visitas_percent': 23, 'ordem': 6}
    ]

    DEFAULT_VEICULOS_VISITADOS_DATA = [
        {'marca': 'AUDI', 'modelo': 'A1', 'visitas': 18},
        {'marca': 'AUDI', 'modelo': 'A3', 'visitas': 32},
        {'marca': 'AUDI', 'modelo': 'A4', 'visitas': 19},
        {'marca': 'AUDI', 'modelo': 'A5', 'visitas': 7},
        {'marca': 'AUDI', 'modelo': 'A6', 'visitas': 1},
        {'marca': 'AUDI', 'modelo': 'A7', 'visitas': 1},
        {'marca': 'AUDI', 'modelo': 'Q3', 'visitas': 30},
        {'marca': 'AUDI', 'modelo': 'Q5', 'visitas': 6},
        {'marca': 'AUDI', 'modelo': 'Q7', 'visitas': 4},
        {'marca': 'AUDI', 'modelo': 'R8', 'visitas': 1},
        {'marca': 'AUDI', 'modelo': 'RS4', 'visitas': 1},
        {'marca': 'AUDI', 'modelo': 'TT', 'visitas': 4},
        {'marca': 'AUDI', 'modelo': 'TTS', 'visitas': 1},
        {'marca': 'BMW', 'modelo': 'Série 1', 'visitas': 65},
        {'marca': 'BMW', 'modelo': 'X1', 'visitas': 57},
        {'marca': 'CHEVROLET', 'modelo': 'ONIX', 'visitas': 1012},
        {'marca': 'CHEVROLET', 'modelo': 'CELTA', 'visitas': 1028},
        {'marca': 'CHEVROLET', 'modelo': 'PRISMA', 'visitas': 680},
        {'marca': 'FIAT', 'modelo': 'PALIO', 'visitas': 1699},
        {'marca': 'FIAT', 'modelo': 'UNO', 'visitas': 1385},
        {'marca': 'FORD', 'modelo': 'FIESTA', 'visitas': 1221},
        {'marca': 'FORD', 'modelo': 'KA', 'visitas': 968},
        {'marca': 'HYUNDAI', 'modelo': 'HB20', 'visitas': 768},
        {'marca': 'RENAULT', 'modelo': 'SANDERO', 'visitas': 1039},
        {'marca': 'VOLKSWAGEN', 'modelo': 'GOL', 'visitas': 1547},
        {'marca': 'VOLKSWAGEN', 'modelo': 'FOX', 'visitas': 983}
    ]

    DATA_MAPPINGS = {
        'dados_genero': DEFAULT_GENERO_DATA,
        'dados_status_profissional': DEFAULT_STATUS_PROFISSIONAL_DATA,
        'dados_faixa_etaria': DEFAULT_FAIXA_ETARIA_DATA,
        'dados_faixa_salarial': DEFAULT_FAIXA_SALARIAL_DATA,
        'dados_classificacao_veiculo': DEFAULT_CLASSIFICACAO_VEICULO_DATA,
        'dados_idade_veiculo': DEFAULT_IDADE_VEICULO_DATA,
        'dados_veiculos_visitados': DEFAULT_VEICULOS_VISITADOS_DATA
    }

    @staticmethod
    def initialize_leads_data():
        """Inicializa dados de leads na session_state"""
        for data_key, default_data in LeadsDataManager.DATA_MAPPINGS.items():
            if data_key not in st.session_state:
                st.session_state[data_key] = default_data

    @staticmethod
    def get_leads_dataframes() -> Dict[str, pd.DataFrame]:
        """Retorna todos os dados de leads como DataFrames"""
        return {
            'genero': pd.DataFrame(st.session_state.dados_genero),
            'status_profissional': pd.DataFrame(st.session_state.dados_status_profissional),
            'faixa_etaria': pd.DataFrame(st.session_state.dados_faixa_etaria),
            'faixa_salarial': pd.DataFrame(st.session_state.dados_faixa_salarial),
            'classificacao_veiculo': pd.DataFrame(st.session_state.dados_classificacao_veiculo),
            'idade_veiculo': pd.DataFrame(st.session_state.dados_idade_veiculo),
            'veiculos_visitados': pd.DataFrame(st.session_state.dados_veiculos_visitados)
        }

    @staticmethod
    def calculate_leads_kpis() -> Dict[str, Any]:
        """Calcula KPIs específicos de leads"""
        if 'dados_genero' not in st.session_state or 'dados_classificacao_veiculo' not in st.session_state:
            return {
                'total_leads': 0,
                'total_visitas': 0,
                'mulheres': 0,
                'homens': 0,
                'percent_mulheres': 0,
                'percent_homens': 0,
                'veiculo_mais_visitado': 'N/A',
                'visitas_veiculo_top': 0
            }
            
        total_leads = sum(item['leads'] for item in st.session_state.dados_genero)
        total_visitas = sum(item['visitas'] for item in st.session_state.dados_classificacao_veiculo)
        
        # Encontrar veículo mais visitado
        veiculo_mais_visitado = max(st.session_state.dados_veiculos_visitados, key=lambda x: x['visitas'])
        
        # Calcular distribuição por gênero
        mulheres = next(item for item in st.session_state.dados_genero if item['genero'] == 'mulheres')['leads']
        homens = next(item for item in st.session_state.dados_genero if item['genero'] == 'homens')['leads']
        percent_mulheres = (mulheres / total_leads * 100) if total_leads > 0 else 0
        percent_homens = (homens / total_leads * 100) if total_leads > 0 else 0
        
        return {
            'total_leads': total_leads,
            'total_visitas': total_visitas,
            'mulheres': mulheres,
            'homens': homens,
            'percent_mulheres': percent_mulheres,
            'percent_homens': percent_homens,
            'veiculo_mais_visitado': f"{veiculo_mais_visitado['marca']} {veiculo_mais_visitado['modelo']}",
            'visitas_veiculo_top': veiculo_mais_visitado['visitas']
        }

    @staticmethod
    def get_demographic_summary() -> Dict[str, Any]:
        """Retorna resumo demográfico dos leads"""
        dfs = LeadsDataManager.get_leads_dataframes()
        
        if dfs['genero'].empty or dfs['faixa_etaria'].empty or dfs['faixa_salarial'].empty:
            return {}
            
        # Perfil demográfico predominante
        faixa_etaria_predominante = dfs['faixa_etaria'].loc[dfs['faixa_etaria']['leads_percent'].idxmax()]
        faixa_salarial_predominante = dfs['faixa_salarial'].loc[dfs['faixa_salarial']['leads_percent'].idxmax()]
        status_predominante = dfs['status_profissional'].loc[dfs['status_profissional']['leads_percent'].idxmax()]
        
        return {
            'perfil_predominante': {
                'genero': 'mulheres' if dfs['genero'].iloc[0]['leads'] > dfs['genero'].iloc[1]['leads'] else 'homens',
                'faixa_etaria': faixa_etaria_predominante['faixa'],
                'faixa_salarial': faixa_salarial_predominante['faixa'],
                'status_profissional': status_predominante['status']
            },
            'diversidade_etaria': len(dfs['faixa_etaria']),
            'diversidade_salarial': len(dfs['faixa_salarial']),
            'diversidade_profissional': len(dfs['status_profissional'])
        }

    @staticmethod
    def get_vehicle_preferences() -> Dict[str, Any]:
        """Retorna preferências de veículos dos leads"""
        dfs = LeadsDataManager.get_leads_dataframes()
        
        if dfs['veiculos_visitados'].empty:
            return {}
            
        # Top marcas
        top_marcas = dfs['veiculos_visitados'].groupby('marca')['visitas'].sum().nlargest(5)
        
        # Preferência por tipo (novo vs seminovo)
        preferencia_tipo = dfs['classificacao_veiculo'].set_index('classificacao')['visitas'].to_dict()
        
        # Preferência por idade
        preferencia_idade = dfs['idade_veiculo'].set_index('idade')['visitas_percent'].to_dict()
        
        return {
            'top_marcas': top_marcas.to_dict(),
            'preferencia_tipo': preferencia_tipo,
            'preferencia_idade': preferencia_idade,
            'total_modelos_visitados': len(dfs['veiculos_visitados']),
            'marcas_unicas': dfs['veiculos_visitados']['marca'].nunique()
        }

# Aliases para compatibilidade
initialize_leads_data = LeadsDataManager.initialize_leads_data
get_leads_dataframes = LeadsDataManager.get_leads_dataframes
calculate_leads_kpis = LeadsDataManager.calculate_leads_kpis
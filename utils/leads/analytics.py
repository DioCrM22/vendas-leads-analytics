import pandas as pd
import numpy as np
from typing import Dict, List, Any, Tuple

class LeadsAnalytics:
    """Análises avançadas para dados de leads"""
    
    @staticmethod
    def analyze_demographic_profile(dfs: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analisa o perfil demográfico completo dos leads"""
        if any(df.empty for df in dfs.values()):
            return {}
            
        # Perfil principal
        perfil_principal = {
            'genero_principal': 'mulheres' if dfs['genero'].iloc[0]['leads'] > dfs['genero'].iloc[1]['leads'] else 'homens',
            'faixa_etaria_principal': dfs['faixa_etaria'].loc[dfs['faixa_etaria']['leads_percent'].idxmax()]['faixa'],
            'faixa_salarial_principal': dfs['faixa_salarial'].loc[dfs['faixa_salarial']['leads_percent'].idxmax()]['faixa'],
            'status_principal': dfs['status_profissional'].loc[dfs['status_profissional']['leads_percent'].idxmax()]['status']
        }
        
        # Diversidade demográfica
        diversidade = {
            'concentracao_etaria': LeadsAnalytics._calculate_concentration_index(dfs['faixa_etaria']['leads_percent']),
            'concentracao_salarial': LeadsAnalytics._calculate_concentration_index(dfs['faixa_salarial']['leads_percent']),
            'concentracao_profissional': LeadsAnalytics._calculate_concentration_index(dfs['status_profissional']['leads_percent'])
        }
        
        # Segmentos de alto valor
        segmentos_alto_valor = LeadsAnalytics._identify_high_value_segments(dfs)
        
        return {
            'perfil_principal': perfil_principal,
            'diversidade': diversidade,
            'segmentos_alto_valor': segmentos_alto_valor,
            'insights_demograficos': LeadsAnalytics._generate_demographic_insights(dfs)
        }
    
    @staticmethod
    def _calculate_concentration_index(percentages: pd.Series) -> float:
        """Calcula índice de concentração (0-1), onde 1 é máxima concentração"""
        return (percentages ** 2).sum() / 10000
    
    @staticmethod
    def _identify_high_value_segments(dfs: Dict[str, pd.DataFrame]) -> List[Dict[str, Any]]:
        """Identifica segmentos de leads de alto valor"""
        segmentos = []
        
        # Segmento: Profissionais CLT com boa renda
        if dfs['status_profissional']['leads_percent'].max() > 50:  # CLT predominante
            segmentos.append({
                'nome': 'Profissionais CLT Estáveis',
                'descricao': 'Leads com emprego formal e renda consistente',
                'potencial': 'Alto',
                'caracteristicas': ['Estabilidade financeira', 'Capacidade de financiamento']
            })
        
        # Segmento: Faixa etária 20-40 anos
        if dfs['faixa_etaria']['leads_percent'].max() > 40:
            faixa_principal = dfs['faixa_etaria'].loc[dfs['faixa_etaria']['leads_percent'].idxmax()]['faixa']
            segmentos.append({
                'nome': f'Adultos Jovens ({faixa_principal})',
                'descricao': 'Leads em fase de consolidação profissional e familiar',
                'potencial': 'Médio-Alto',
                'caracteristicas': ['Mobilidade ascendente', 'Necessidade de veículo familiar']
            })
        
        # Segmento: Renda acima de R$ 10.000
        renda_alta = dfs['faixa_salarial'][dfs['faixa_salarial']['faixa'].str.contains(r'10000|15000|20000', regex=True)]
        if not renda_alta.empty and renda_alta['leads_percent'].sum() > 10:
            segmentos.append({
                'nome': 'Alta Renda',
                'descricao': 'Leads com poder aquisitivo elevado',
                'potencial': 'Muito Alto',
                'caracteristicas': ['Capacidade de compra à vista', 'Interesse em veículos premium']
            })
        
        return segmentos
    
    @staticmethod
    def _generate_demographic_insights(dfs: Dict[str, pd.DataFrame]) -> List[str]:
        """Gera insights baseados na análise demográfica"""
        insights = []
        
        # Insight de gênero
        diff_genero = abs(dfs['genero'].iloc[0]['leads'] - dfs['genero'].iloc[1]['leads'])
        total_genero = dfs['genero']['leads'].sum()
        if diff_genero / total_genero > 0.2:
            genero_maioria = 'mulheres' if dfs['genero'].iloc[0]['leads'] > dfs['genero'].iloc[1]['leads'] else 'homens'
            insights.append(f"Predominância significativa de {genero_maioria} ({diff_genero/total_genero*100:.1f}% de diferença)")
        
        # Insight de faixa etária
        if dfs['faixa_etaria']['leads_percent'].max() > 45:
            faixa_principal = dfs['faixa_etaria'].loc[dfs['faixa_etaria']['leads_percent'].idxmax()]['faixa']
            insights.append(f"Concentração marcante na faixa etária {faixa_principal}")
        
        # Insight de renda
        if dfs['faixa_salarial']['leads_percent'].max() > 60:
            faixa_principal = dfs['faixa_salarial'].loc[dfs['faixa_salarial']['leads_percent'].idxmax()]['faixa']
            insights.append(f"Perfil de renda muito definido: {faixa_principal} representa a maioria")
        
        return insights
    
    @staticmethod
    def analyze_vehicle_preferences(dfs: Dict[str, pd.DataFrame]) -> Dict[str, Any]:
        """Analisa preferências de veículos dos leads"""
        if any(df.empty for df in [dfs.get('classificacao_veiculo'), dfs.get('idade_veiculo'), dfs.get('veiculos_visitados')]):
            return {}
            
        # Preferência por tipo de veículo
        preferencia_tipo = {
            'novo_vs_seminovo': dfs['classificacao_veiculo'].set_index('classificacao')['visitas'].to_dict(),
            'preferencia_novo': dfs['classificacao_veiculo'].iloc[0]['visitas'] / dfs['classificacao_veiculo']['visitas'].sum() * 100
        }
        
        # Preferência por idade do veículo
        preferencia_idade = dfs['idade_veiculo'].set_index('idade')['visitas_percent'].to_dict()
        idade_preferida = dfs['idade_veiculo'].loc[dfs['idade_veiculo']['visitas_percent'].idxmax()]['idade']
        
        # Análise de marcas e modelos
        analise_marcas = LeadsAnalytics._analyze_brands_performance(dfs['veiculos_visitados'])
        tendencias_modelos = LeadsAnalytics._identify_vehicle_trends(dfs['veiculos_visitados'])
        
        return {
            'preferencia_tipo': preferencia_tipo,
            'preferencia_idade': preferencia_idade,
            'idade_preferida': idade_preferida,
            'analise_marcas': analise_marcas,
            'tendencias_modelos': tendencias_modelos,
            'recomendacoes_estoque': LeadsAnalytics._generate_inventory_recommendations(dfs)
        }
    
    @staticmethod
    def _analyze_brands_performance(df_veiculos: pd.DataFrame) -> Dict[str, Any]:
        """Analisa performance das marcas"""
        vendas_por_marca = df_veiculos.groupby('marca')['visitas'].agg(['sum', 'count', 'mean']).reset_index()
        vendas_por_marca = vendas_por_marca.sort_values('sum', ascending=False)
        
        # Concentração de mercado
        market_share_top3 = vendas_por_marca.head(3)['sum'].sum() / vendas_por_marca['sum'].sum() * 100
        market_share_top5 = vendas_por_marca.head(5)['sum'].sum() / vendas_por_marca['sum'].sum() * 100
        
        return {
            'top_marcas': vendas_por_marca.head(5).to_dict('records'),
            'concentracao_mercado': {
                'top3_share': market_share_top3,
                'top5_share': market_share_top5,
                'marcas_ativas': len(vendas_por_marca)
            },
            'diversidade_modelos': vendas_por_marca['count'].mean()
        }
    
    @staticmethod
    def _identify_vehicle_trends(df_veiculos: pd.DataFrame) -> List[Dict[str, Any]]:
        """Identifica tendências nos modelos de veículos"""
        tendencias = []
        
        # Análise por categoria de modelo (compacto, sedan, SUV, etc.)
        categorias = {
            'compacto': ['ONIX', 'CELTA', 'HB20', 'KA', 'FIESTA', 'GOL', 'FOX', 'SANDERO', 'PALIO', 'UNO', 'PRISMA'],
            'sedan': ['A3', 'A4', 'A5', 'A6', 'A7'],
            'suv': ['X1', 'Q3', 'Q5', 'Q7'],
            'esportivo': ['R8', 'RS4', 'TT', 'TTS']
        }
        
        for categoria, modelos in categorias.items():
            visitas_categoria = df_veiculos[df_veiculos['modelo'].isin(modelos)]['visitas'].sum()
            if visitas_categoria > 0:
                tendencias.append({
                    'categoria': categoria,
                    'visitas': visitas_categoria,
                    'modelos_populares': df_veiculos[df_veiculos['modelo'].isin(modelos)].nlargest(3, 'visitas')[['modelo', 'visitas']].to_dict('records')
                })
        
        return tendencias
    
    @staticmethod
    def _generate_inventory_recommendations(dfs: Dict[str, pd.DataFrame]) -> List[str]:
        """Gera recomendações para estoque baseadas nas preferências"""
        recomendacoes = []
        
        # Recomendação baseada em tipo de veículo
        pref_novo = dfs['classificacao_veiculo'].iloc[0]['visitas'] / dfs['classificacao_veiculo']['visitas'].sum()
        if pref_novo > 0.7:
            recomendacoes.append("Focar em veículos novos no estoque")
        elif pref_novo < 0.3:
            recomendacoes.append("Ampliar oferta de veículos seminovos")
        else:
            recomendacoes.append("Manter mix balanceado entre novos e seminovos")
        
        # Recomendação baseada em idade preferida
        idade_preferida = dfs['idade_veiculo'].loc[dfs['idade_veiculo']['visitas_percent'].idxmax()]['idade']
        recomendacoes.append(f"Priorizar veículos na faixa de {idade_preferida} no estoque")
        
        # Recomendação baseada em marcas populares
        top_marcas = dfs['veiculos_visitados'].groupby('marca')['visitas'].sum().nlargest(3)
        if len(top_marcas) >= 2:
            recomendacoes.append(f"Manter estoque forte nas marcas: {', '.join(top_marcas.index.tolist())}")
        
        return recomendacoes
    
    @staticmethod
    def calculate_conversion_potential(dfs: Dict[str, pd.DataFrame]) -> Dict[str, float]:
        """Calcula potencial de conversão por segmento"""
        if any(df.empty for df in dfs.values()):
            return {}
            
        # Fatores de conversão (baseados em benchmarks do setor)
        fatores_conversao = {
            'genero': {'mulheres': 1.1, 'homens': 1.0},  # Mulheres convertem 10% melhor
            'faixa_etaria': {'20-40': 1.2, '40-60': 1.0, '60-80': 0.8, '0-20': 0.6, '80+': 0.4},
            'faixa_salarial': {'5000-10000': 1.1, '10000-15000': 1.3, '15000-20000': 1.5, '20000+': 1.7, '0-5000': 0.7},
            'status_profissional': {'clt': 1.2, 'empresário(a)': 1.4, 'autônomo(a)': 1.1, 'funcionário(a) público(a)': 1.3, 'freelancer': 1.0, 'aposentado(a)': 0.9, 'estudante': 0.6, 'outro': 0.8}
        }
        
        # Calcular score médio de conversão
        scores = []
        
        # Score por gênero
        for _, row in dfs['genero'].iterrows():
            score = row['leads'] * fatores_conversao['genero'].get(row['genero'], 1.0)
            scores.append(score)
        
        # Score por faixa etária
        for _, row in dfs['faixa_etaria'].iterrows():
            score = row['leads_percent'] * fatores_conversao['faixa_etaria'].get(row['faixa'], 1.0)
            scores.append(score)
        
        # Score por faixa salarial
        for _, row in dfs['faixa_salarial'].iterrows():
            score = row['leads_percent'] * fatores_conversao['faixa_salarial'].get(row['faixa'], 1.0)
            scores.append(score)
        
        # Score por status profissional
        for _, row in dfs['status_profissional'].iterrows():
            score = row['leads_percent'] * fatores_conversao['status_profissional'].get(row['status'], 1.0)
            scores.append(score)
        
        potencial_medio = np.mean(scores) if scores else 0
        potencial_maximo = max(scores) if scores else 0
        
        return {
            'potencial_conversao_medio': potencial_medio,
            'potencial_conversao_maximo': potencial_maximo,
            'segmento_alto_potencial': 'Identificar baseado na análise',
            'recomendacao_priorizacao': 'Focar em segmentos com score acima da média'
        }
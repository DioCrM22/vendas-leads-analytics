import pandas as pd
from typing import Dict, List, Tuple, Any
import numpy as np

class VendasAnalytics:
    """Análises avançadas para dados de vendas"""
    
    @staticmethod
    def analyze_monthly_trends(df_mensal: pd.DataFrame) -> Dict[str, Any]:
        """Analisa tendências mensais"""
        if df_mensal.empty:
            return {}
            
        df = df_mensal.copy()
        df['mes_num'] = range(len(df))
        
        # Calcular tendências
        tendencia_receita = np.polyfit(df['mes_num'], df['receita'], 1)[0]
        tendencia_vendas = np.polyfit(df['mes_num'], df['vendas'], 1)[0]
        tendencia_conversao = np.polyfit(df['mes_num'], df['conversao'], 1)[0]
        
        # Calcular médias móveis
        df['receita_mm'] = df['receita'].rolling(window=3, min_periods=1).mean()
        df['vendas_mm'] = df['vendas'].rolling(window=3, min_periods=1).mean()
        
        # Identificar melhores e piores meses
        melhor_mes_receita = df.loc[df['receita'].idxmax()]
        pior_mes_receita = df.loc[df['receita'].idxmin()]
        melhor_mes_vendas = df.loc[df['vendas'].idxmax()]
        pior_mes_vendas = df.loc[df['vendas'].idxmin()]
        
        return {
            'tendencia_receita': tendencia_receita,
            'tendencia_vendas': tendencia_vendas,
            'tendencia_conversao': tendencia_conversao,
            'melhor_mes_receita': {
                'mes': melhor_mes_receita['mes'],
                'receita': melhor_mes_receita['receita']
            },
            'pior_mes_receita': {
                'mes': pior_mes_receita['mes'],
                'receita': pior_mes_receita['receita']
            },
            'melhor_mes_vendas': {
                'mes': melhor_mes_vendas['mes'],
                'vendas': melhor_mes_vendas['vendas']
            },
            'pior_mes_vendas': {
                'mes': pior_mes_vendas['mes'],
                'vendas': pior_mes_vendas['vendas']
            },
            'dados_tendencias': df[['mes', 'receita_mm', 'vendas_mm']].to_dict('records')
        }
    
    @staticmethod
    def analyze_geographic_performance(df_estados: pd.DataFrame) -> Dict[str, Any]:
        """Analisa performance geográfica"""
        if df_estados.empty:
            return {}
            
        total_vendas = df_estados['vendas'].sum()
        df_estados['participacao'] = (df_estados['vendas'] / total_vendas) * 100
        
        # Análise por região
        vendas_por_regiao = df_estados.groupby('regiao')['vendas'].agg(['sum', 'count']).reset_index()
        vendas_por_regiao['participacao'] = (vendas_por_regiao['sum'] / total_vendas) * 100
        
        # Estados com maior potencial (baixa participação mas alta performance relativa)
        media_vendas_por_estado = df_estados['vendas'].mean()
        df_estados['performance_relativa'] = df_estados['vendas'] / media_vendas_por_estado
        
        return {
            'total_estados': len(df_estados),
            'vendas_por_regiao': vendas_por_regiao.to_dict('records'),
            'estados_destaque': df_estados.nlargest(3, 'vendas')[['estado', 'vendas', 'participacao']].to_dict('records'),
            'estados_potencial': df_estados[df_estados['performance_relativa'] > 1.5][['estado', 'vendas', 'performance_relativa']].to_dict('records'),
            'distribuicao_regioes': vendas_por_regiao[['regiao', 'participacao']].to_dict('records')
        }
    
    @staticmethod
    def analyze_brand_performance(df_marcas: pd.DataFrame) -> Dict[str, Any]:
        """Analisa performance das marcas"""
        if df_marcas.empty:
            return {}
            
        total_vendas = df_marcas['vendas'].sum()
        df_marcas['market_share'] = (df_marcas['vendas'] / total_vendas) * 100
        
        # Análise por categoria
        vendas_por_categoria = df_marcas.groupby('categoria')['vendas'].agg(['sum', 'count', 'mean']).reset_index()
        vendas_por_categoria['participacao'] = (vendas_por_categoria['sum'] / total_vendas) * 100
        
        # Concentração de mercado
        df_marcas = df_marcas.sort_values('market_share', ascending=False)
        df_marcas['market_share_acumulado'] = df_marcas['market_share'].cumsum()
        
        return {
            'total_marcas': len(df_marcas),
            'market_share_top3': df_marcas.head(3)[['marca', 'market_share']].to_dict('records'),
            'vendas_por_categoria': vendas_por_categoria.to_dict('records'),
            'concentracao_mercado': {
                'top3_share': df_marcas.head(3)['market_share'].sum(),
                'top5_share': df_marcas.head(5)['market_share'].sum(),
                'indice_herfindahl': (df_marcas['market_share'] ** 2).sum() / 10000  # Normalizado
            },
            'marcas_crescimento_potencial': df_marcas[df_marcas['market_share'] < 10][['marca', 'market_share']].to_dict('records')
        }
    
    @staticmethod
    def analyze_store_performance(df_lojas: pd.DataFrame) -> Dict[str, Any]:
        """Analisa performance das lojas"""
        if df_lojas.empty:
            return {}
            
        # Análise por localização
        vendas_por_estado = df_lojas.groupby('estado')['vendas'].agg(['sum', 'count', 'mean']).reset_index()
        vendas_por_cidade = df_lojas.groupby('cidade')['vendas'].agg(['sum', 'count', 'mean']).reset_index()
        
        # Identificar lojas de alto e baixo desempenho
        media_vendas = df_lojas['vendas'].mean()
        std_vendas = df_lojas['vendas'].std()
        
        lojas_alto_desempenho = df_lojas[df_lojas['vendas'] > media_vendas + std_vendas]
        lojas_baixo_desempenho = df_lojas[df_lojas['vendas'] < media_vendas - std_vendas]
        
        return {
            'total_lojas': len(df_lojas),
            'vendas_por_estado': vendas_por_estado.to_dict('records'),
            'vendas_por_cidade': vendas_por_cidade.to_dict('records'),
            'metricas_desempenho': {
                'media_vendas': media_vendas,
                'desvio_padrao': std_vendas,
                'coeficiente_variacao': (std_vendas / media_vendas) * 100 if media_vendas > 0 else 0
            },
            'lojas_alto_desempenho': lojas_alto_desempenho[['loja', 'vendas', 'cidade']].to_dict('records'),
            'lojas_baixo_desempenho': lojas_baixo_desempenho[['loja', 'vendas', 'cidade']].to_dict('records')
        }
    
    @staticmethod
    def analyze_visits_patterns(df_visitas: pd.DataFrame) -> Dict[str, Any]:
        """Analisa padrões de visitas"""
        if df_visitas.empty:
            return {}
            
        df = df_visitas.sort_values('ordem')
        total_visitas = df['visitas'].sum()
        df['participacao_dia'] = (df['visitas'] / total_visitas) * 100
        
        # Identificar padrões semanais
        dias_util = ['segunda', 'terça', 'quarta', 'quinta', 'sexta']
        dias_fim_semana = ['sábado', 'domingo']
        
        visitas_util = df[df['dia_semana'].isin(dias_util)]['visitas'].sum()
        visitas_fim_semana = df[df['dia_semana'].isin(dias_fim_semana)]['visitas'].sum()
        
        # Calcular eficiência (visitas por dia útil vs fim de semana)
        eficiencia_util = visitas_util / len(dias_util) if len(dias_util) > 0 else 0
        eficiencia_fim_semana = visitas_fim_semana / len(dias_fim_semana) if len(dias_fim_semana) > 0 else 0
        
        return {
            'total_visitas': total_visitas,
            'distribuicao_diaria': df[['dia_semana', 'visitas', 'participacao_dia']].to_dict('records'),
            'analise_semanal': {
                'visitas_dias_uteis': visitas_util,
                'visitas_fim_semana': visitas_fim_semana,
                'participacao_uteis': (visitas_util / total_visitas) * 100,
                'participacao_fim_semana': (visitas_fim_semana / total_visitas) * 100,
                'eficiencia_uteis': eficiencia_util,
                'eficiencia_fim_semana': eficiencia_fim_semana
            },
            'recomendacoes': VendasAnalytics._generate_visits_recommendations(df)
        }
    
    @staticmethod
    def _generate_visits_recommendations(df_visitas: pd.DataFrame) -> List[str]:
        """Gera recomendações baseadas nos padrões de visita"""
        recomendacoes = []
        
        dia_max = df_visitas.loc[df_visitas['visitas'].idxmax()]
        dia_min = df_visitas.loc[df_visitas['visitas'].idxmin()]
        
        if dia_max['visitas'] / dia_min['visitas'] > 3:
            recomendacoes.append(f"Considerar redistribuir recursos do {dia_max['dia_semana']} para o {dia_min['dia_semana']}")
        
        if df_visitas[df_visitas['dia_semana'].isin(['sábado', 'domingo'])]['visitas'].sum() < df_visitas['visitas'].sum() * 0.2:
            recomendacoes.append("Implementar campanhas específicas para fins de semana")
        
        media_visitas = df_visitas['visitas'].mean()
        dias_abaixo_media = df_visitas[df_visitas['visitas'] < media_visitas * 0.7]
        if len(dias_abaixo_media) > 0:
            dias = ", ".join(dias_abaixo_media['dia_semana'].tolist())
            recomendacoes.append(f"Otimizar operações nos dias de menor movimento: {dias}")
        
        return recomendacoes
    
    @staticmethod
    def calculate_roi_metrics(df_mensal: pd.DataFrame, investimento_marketing: float = None) -> Dict[str, float]:
        """Calcula métricas de ROI"""
        if df_mensal.empty:
            return {}
            
        total_receita = df_mensal['receita'].sum()
        total_vendas = df_mensal['vendas'].sum()
        
        # Se não for fornecido investimento, estimar baseado na receita
        if investimento_marketing is None:
            investimento_marketing = total_receita * 0.15  # 15% da receita como estimativa
        
        roi = ((total_receita - investimento_marketing) / investimento_marketing) * 100 if investimento_marketing > 0 else 0
        cac = investimento_marketing / total_vendas if total_vendas > 0 else 0  # Custo de Aquisição por Cliente
        ltv = total_receita / total_vendas if total_vendas > 0 else 0  # Lifetime Value
        
        return {
            'roi': roi,
            'cac': cac,
            'ltv': ltv,
            'ltv_cac_ratio': ltv / cac if cac > 0 else 0,
            'investimento_marketing': investimento_marketing,
            'receita_total': total_receita
        }
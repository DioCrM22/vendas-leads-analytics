import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

class VendasCharts:
    """Gráficos para análise de vendas"""
    
    @staticmethod
    def create_monthly_performance(df_mensal):
        """Cria gráfico de performance mensal"""
        if df_mensal.empty:
            return go.Figure()
        
        fig = make_subplots(specs=[[{"secondary_y": True}]])
        
        fig.add_trace(
            go.Bar(x=df_mensal['mes'], y=df_mensal['receita'], name="Receita", marker_color='#3498db'),
            secondary_y=False,
        )
        
        fig.add_trace(
            go.Scatter(x=df_mensal['mes'], y=df_mensal['vendas'], name="Vendas", line=dict(color='#e74c3c', width=3)),
            secondary_y=True,
        )
        
        fig.update_layout(title="Performance Mensal", height=400)
        fig.update_yaxes(title_text="Receita (R$)", secondary_y=False)
        fig.update_yaxes(title_text="Vendas", secondary_y=True)
        
        return fig
    
    @staticmethod
    def create_brazil_map(df_estados):
        """Cria mapa do Brasil com vendas por estado - FUNCIONAL"""
        if df_estados.empty:
            return go.Figure()
        
        # Dados de coordenadas aproximadas dos estados brasileiros
        state_coords = {
            'AC': [-8.77, -70.55], 'AL': [-9.71, -35.73], 'AM': [-3.47, -65.10], 'AP': [1.41, -51.77],
            'BA': [-12.96, -38.51], 'CE': [-3.71, -38.54], 'DF': [-15.78, -47.93], 'ES': [-19.19, -40.34],
            'GO': [-16.64, -49.31], 'MA': [-2.55, -44.30], 'MG': [-18.10, -44.38], 'MS': [-20.51, -54.54],
            'MT': [-12.64, -55.42], 'PA': [-5.53, -52.29], 'PB': [-7.06, -35.55], 'PE': [-8.28, -35.07],
            'PI': [-8.28, -43.68], 'PR': [-24.89, -51.55], 'RJ': [-22.25, -42.66], 'RN': [-5.22, -36.52],
            'RO': [-11.22, -62.80], 'RR': [1.89, -61.22], 'RS': [-30.01, -51.22], 'SC': [-27.45, -50.95],
            'SE': [-10.90, -37.07], 'SP': [-23.55, -46.64], 'TO': [-10.25, -48.25]
        }
        
        # Adicionar coordenadas ao DataFrame
        df_map = df_estados.copy()
        df_map['lat'] = df_map['uf'].map(lambda x: state_coords.get(x, [0, 0])[0])
        df_map['lon'] = df_map['uf'].map(lambda x: state_coords.get(x, [0, 0])[1])
        
        # Criar mapa de bolhas - SEMPRE FUNCIONA
        fig = px.scatter_geo(
            df_map,
            lat='lat',
            lon='lon',
            size='vendas',
            color='vendas',
            hover_name='estado',
            hover_data={'vendas': True, 'uf': True, 'regiao': True},
            size_max=40,
            color_continuous_scale='Blues',
            title='🗺️ Mapa de Vendas por Estado - Brasil'
        )
        
        # Configurar o mapa
        fig.update_geos(
            visible=False,
            resolution=50,
            scope='south america',
            showcountries=True,
            countrycolor="Black",
            showsubunits=True,
            subunitcolor="grey"
        )
        
        fig.update_layout(
            height=600,
            margin={"r":0,"t":50,"l":0,"b":0}
        )
        
        return fig
    
    @staticmethod
    def create_heatmap_table(df_estados):
        """Cria heatmap em formato de tabela - ALTERNATIVA PRÁTICA"""
        if df_estados.empty:
            return go.Figure()
        
        # Preparar dados para heatmap
        df_heat = df_estados[['estado', 'vendas']].copy()
        df_heat = df_heat.sort_values('vendas', ascending=False)
        
        # Criar heatmap com go.Figure
        fig = go.Figure(data=go.Heatmap(
            z=[df_heat['vendas'].tolist()],
            x=df_heat['estado'].tolist(),
            y=['Vendas'],
            colorscale='Viridis',
            showscale=True,
            hoverongaps=False
        ))
        
        fig.update_layout(
            title='🔥 Heatmap de Vendas - Intensidade por Estado',
            height=300,
            xaxis_title="Estados",
            yaxis_title=""
        )
        
        return fig
    
    @staticmethod
    def create_states_bar_chart(df_estados):
        """Cria gráfico de barras por estado"""
        if df_estados.empty:
            return go.Figure()
        
        fig = px.bar(
            df_estados.sort_values('vendas', ascending=True),
            x='vendas',
            y='estado',
            orientation='h',
            color='vendas',
            text='vendas',
            title='📊 Vendas por Estado - Ranking',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=500, showlegend=False)
        return fig
    
    @staticmethod
    def create_regions_pie_chart(df_estados):
        """Cria gráfico de pizza por região"""
        if df_estados.empty:
            return go.Figure()
        
        # Agrupar por região
        df_regioes = df_estados.groupby('regiao')['vendas'].sum().reset_index()
        
        fig = px.pie(
            df_regioes,
            values='vendas',
            names='regiao',
            title='📍 Distribuição por Região',
            hole=0.4,
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        return fig
    
    @staticmethod
    def create_brands_analysis(df_marcas):
        """Cria análise por marca"""
        if df_marcas.empty:
            return go.Figure()
        
        fig = px.bar(
            df_marcas.sort_values('vendas', ascending=True),
            x='vendas',
            y='marca',
            orientation='h',
            color='vendas',
            text='vendas',
            title='Vendas por Marca',
            color_continuous_scale='Plasma'
        )
        fig.update_layout(height=400, showlegend=False)
        return fig
    
    @staticmethod
    def create_category_pie_chart(df_marcas):
        """Cria gráfico de pizza por categoria"""
        if df_marcas.empty:
            return go.Figure()
        
        fig = px.pie(
            df_marcas,
            values='vendas',
            names='categoria',
            title='Vendas por Categoria',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        fig.update_layout(height=400)
        return fig
    
    @staticmethod
    def create_stores_ranking(df_lojas):
        """Cria ranking de lojas"""
        if df_lojas.empty:
            return go.Figure()
        
        fig = px.bar(
            df_lojas.sort_values('vendas', ascending=True),
            x='vendas',
            y='loja',
            orientation='h',
            color='vendas',
            text='vendas',
            title='Top Lojas por Vendas',
            color_continuous_scale='Greens'
        )
        fig.update_layout(height=500, showlegend=False)
        return fig
    
    @staticmethod
    def create_visits_trend(df_visitas):
        """Cria tendência de visitas"""
        if df_visitas.empty:
            return go.Figure()
        
        df_sorted = df_visitas.sort_values('ordem')
        
        fig = px.line(
            df_sorted,
            x='dia_semana',
            y='visitas',
            markers=True,
            title='Visitas por Dia da Semana',
            line_shape='spline'
        )
        
        fig.update_layout(
            height=400,
            xaxis_title='Dia da Semana',
            yaxis_title='Número de Visitas'
        )
        fig.update_traces(line=dict(color='#e74c3c', width=3))
        
        return fig
    
    @staticmethod
    def create_conversion_trend(df_mensal):
        """Cria tendência de conversão"""
        if df_mensal.empty:
            return go.Figure()
        
        fig = px.line(
            df_mensal, 
            x='mes', 
            y='conversao',
            title='Evolução da Taxa de Conversão (%)',
            markers=True
        )
        fig.update_layout(height=300)
        fig.update_traces(line=dict(color='#2ecc71', width=3))
        return fig
    
    @staticmethod
    def create_ticket_medio_chart(df_mensal):
        """Cria gráfico de ticket médio"""
        if df_mensal.empty:
            return go.Figure()
        
        fig = px.bar(
            df_mensal, 
            x='mes', 
            y='ticket_medio',
            title='Ticket Médio por Mês (R$)',
            color='ticket_medio',
            color_continuous_scale='Viridis'
        )
        fig.update_layout(height=300, showlegend=False)
        return fig
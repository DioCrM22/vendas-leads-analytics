import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from typing import Dict, List, Optional, Any

class LeadsCharts:
    """Gráficos profissionais e intuitivos para análise de LEADS"""
    
    # Paleta de cores profissional
    COLOR_PALETTE = {
        'primary': '#2E86AB',    # Azul profissional
        'secondary': '#A23B72',  # Rosa/Magenta
        'success': '#18A999',    # Verde/Teal
        'warning': '#F18F01',    # Laranja
        'danger': '#C73E1D',     # Vermelho
        'dark': '#2B2D42',       # Cinza escuro
        'light': '#8D99AE',      # Cinza claro
        'accent1': '#6A4C93',    # Roxo
        'accent2': '#F7B801',    # Amarelo
        'accent3': '#118AB2'     # Azul claro
    }
    
    # Cores específicas por categoria
    GENDER_COLORS = ['#A23B72', '#2E86AB']  # Rosa para mulheres, Azul para homens
    AGE_COLORS = ['#F18F01', '#F7B801', '#18A999', '#2E86AB', '#6A4C93']
    SALARY_COLORS = ['#8D99AE', '#118AB2', '#18A999', '#F7B801', '#F18F01']
    VEHICLE_COLORS = ['#2E86AB', '#A23B72']  # Novo vs Seminovo
    
    @staticmethod
    def create_gender_distribution(df_genero: pd.DataFrame):
        """Cria gráfico de distribuição por gênero - MELHORADO"""
        if df_genero.empty:
            return go.Figure()
        
        # Ordenar para consistência visual
        df_sorted = df_genero.sort_values('leads', ascending=False)
        
        fig = px.pie(
            df_sorted,
            values='leads',
            names='genero',
            title='👥 Distribuição por Gênero',
            color='genero',
            color_discrete_sequence=LeadsCharts.GENDER_COLORS,
            hole=0.4
        )
        
        fig.update_layout(
            height=450,
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=-0.2,
                xanchor="center",
                x=0.5
            ),
            font=dict(size=12)
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            hovertemplate='<b>%{label}</b><br>Leads: %{value:,}<br>Percentual: %{percent}',
            marker=dict(line=dict(color='white', width=2))
        )
        
        return fig
    
    @staticmethod
    def create_professional_status(df_status: pd.DataFrame):
        """Cria gráfico de status profissional - MELHORADO"""
        if df_status.empty:
            return go.Figure()
        
        df_sorted = df_status.sort_values('leads_percent', ascending=True)
        
        fig = px.bar(
            df_sorted,
            x='leads_percent',
            y='status',
            orientation='h',
            color='leads_percent',
            text=df_sorted['leads_percent'].apply(lambda x: f'{x}%'),
            title='💼 Distribuição por Status Profissional',
            color_continuous_scale='Teal',
            color_continuous_midpoint=df_sorted['leads_percent'].median()
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            xaxis_title="Percentual de Leads (%)",
            yaxis_title="",
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='outside',
            marker=dict(line=dict(color='white', width=1))
        )
        
        return fig
    
    @staticmethod
    def create_age_distribution(df_faixa_etaria: pd.DataFrame):
        """Cria gráfico de distribuição por faixa etária - MELHORADO"""
        if df_faixa_etaria.empty:
            return go.Figure()
        
        df_sorted = df_faixa_etaria.sort_values('leads_percent', ascending=False)
        
        fig = px.bar(
            df_sorted,
            x='faixa',
            y='leads_percent',
            color='leads_percent',
            text=df_sorted['leads_percent'].apply(lambda x: f'{x}%'),
            title='🎂 Distribuição por Faixa Etária',
            color_continuous_scale='Viridis',
            labels={'leads_percent': 'Percentual (%)', 'faixa': 'Faixa Etária'}
        )
        
        fig.update_layout(
            height=450,
            showlegend=False,
            xaxis_title="Faixa Etária",
            yaxis_title="Percentual de Leads (%)",
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='outside',
            marker=dict(
                line=dict(color='white', width=1),
                opacity=0.8
            )
        )
        
        return fig
    
    @staticmethod
    def create_salary_distribution(df_faixa_salarial: pd.DataFrame):
        """Cria gráfico de distribuição por faixa salarial - MELHORADO"""
        if df_faixa_salarial.empty:
            return go.Figure()
        
        df_sorted = df_faixa_salarial.sort_values('ordem')
        
        fig = px.bar(
            df_sorted,
            x='faixa',
            y='leads_percent',
            color='leads_percent',
            text=df_sorted['leads_percent'].apply(lambda x: f'{x}%'),
            title='💰 Distribuição por Faixa Salarial (R$)',
            color_continuous_scale='Blues',
            labels={'leads_percent': 'Percentual (%)', 'faixa': 'Faixa Salarial'}
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            xaxis_title="Faixa Salarial (R$)",
            yaxis_title="Percentual de Leads (%)",
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='outside',
            marker=dict(
                line=dict(color='white', width=1),
                opacity=0.8
            )
        )
        
        return fig
    
    @staticmethod
    def create_vehicle_classification(df_classificacao: pd.DataFrame):
        """Cria gráfico de classificação de veículos - MELHORADO"""
        if df_classificacao.empty:
            return go.Figure()
        
        fig = make_subplots(
            rows=1, cols=2,
            specs=[[{"type": "bar"}, {"type": "pie"}]],
            subplot_titles=['Visitas por Classificação', 'Distribuição Percentual']
        )
        
        # Gráfico de barras
        fig.add_trace(
            go.Bar(
                x=df_classificacao['classificacao'],
                y=df_classificacao['visitas'],
                marker_color=LeadsCharts.VEHICLE_COLORS,
                text=df_classificacao['visitas'],
                textposition='auto',
                name='Visitas'
            ),
            row=1, col=1
        )
        
        # Gráfico de pizza
        fig.add_trace(
            go.Pie(
                labels=df_classificacao['classificacao'],
                values=df_classificacao['visitas'],
                marker_colors=LeadsCharts.VEHICLE_COLORS,
                hole=0.5,
                name='Distribuição'
            ),
            row=1, col=2
        )
        
        fig.update_layout(
            height=400,
            title_text='🚗 Preferência por Tipo de Veículo',
            showlegend=False,
            font=dict(size=12)
        )
        
        fig.update_traces(
            texttemplate='%{text:,}',
            selector=dict(type='bar')
        )
        
        fig.update_traces(
            textposition='inside',
            textinfo='percent+label',
            selector=dict(type='pie')
        )
        
        return fig
    
    @staticmethod
    def create_vehicle_age_distribution(df_idade_veiculo: pd.DataFrame):
        """Cria gráfico de distribuição por idade do veículo - MELHORADO"""
        if df_idade_veiculo.empty:
            return go.Figure()
        
        df_sorted = df_idade_veiculo.sort_values('ordem')
        
        fig = px.bar(
            df_sorted,
            x='idade',
            y='visitas_percent',
            color='visitas_percent',
            text=df_sorted['visitas_percent'].apply(lambda x: f'{x}%'),
            title='📅 Preferência por Idade do Veículo',
            color_continuous_scale='Purples',
            labels={'visitas_percent': 'Percentual de Visitas (%)', 'idade': 'Idade do Veículo'}
        )
        
        fig.update_layout(
            height=500,
            showlegend=False,
            xaxis_title="Idade do Veículo",
            yaxis_title="Percentual de Visitas (%)",
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='outside',
            marker=dict(
                line=dict(color='white', width=1),
                opacity=0.8
            )
        )
        
        return fig
    
    @staticmethod
    def create_top_vehicles(df_veiculos: pd.DataFrame):
        """Cria gráfico dos veículos mais visitados - MELHORADO"""
        if df_veiculos.empty:
            return go.Figure()
        
        # Top 15 veículos
        df_top = df_veiculos.nlargest(15, 'visitas')
        df_sorted = df_top.sort_values('visitas', ascending=True)
        
        fig = px.bar(
            df_sorted,
            x='visitas',
            y='modelo',
            orientation='h',
            color='visitas',
            text=df_sorted['visitas'],
            title='🏆 Top 15 Veículos Mais Visitados',
            color_continuous_scale='Rainbow',
            labels={'visitas': 'Número de Visitas', 'modelo': 'Modelo do Veículo'}
        )
        
        fig.update_layout(
            height=600,
            showlegend=False,
            xaxis_title="Número de Visitas",
            yaxis_title="",
            font=dict(size=12),
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        fig.update_traces(
            textposition='outside',
            marker=dict(line=dict(color='white', width=1))
        )
        
        return fig
    
    @staticmethod
    def create_demographic_dashboard(dfs: Dict[str, pd.DataFrame]):
        """Cria dashboard demográfico completo - NOVO"""
        if any(df.empty for df in dfs.values()):
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                '👥 Distribuição por Gênero',
                '🎂 Faixa Etária',
                '💰 Faixa Salarial', 
                '💼 Status Profissional'
            ],
            specs=[
                [{"type": "pie"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "bar"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        # Gênero (Pizza)
        fig.add_trace(
            go.Pie(
                labels=dfs['genero']['genero'],
                values=dfs['genero']['leads'],
                marker_colors=LeadsCharts.GENDER_COLORS,
                hole=0.4,
                showlegend=False,
                textinfo='percent+label'
            ),
            row=1, col=1
        )
        
        # Faixa Etária (Barras)
        df_idade_sorted = dfs['faixa_etaria'].sort_values('leads_percent', ascending=True)
        fig.add_trace(
            go.Bar(
                x=df_idade_sorted['leads_percent'],
                y=df_idade_sorted['faixa'],
                orientation='h',
                marker_color=LeadsCharts.COLOR_PALETTE['primary'],
                text=df_idade_sorted['leads_percent'].apply(lambda x: f'{x}%'),
                textposition='auto',
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Faixa Salarial (Barras)
        df_salario_sorted = dfs['faixa_salarial'].sort_values('ordem')
        fig.add_trace(
            go.Bar(
                x=df_salario_sorted['faixa'],
                y=df_salario_sorted['leads_percent'],
                marker_color=LeadsCharts.COLOR_PALETTE['success'],
                text=df_salario_sorted['leads_percent'].apply(lambda x: f'{x}%'),
                textposition='outside',
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Status Profissional (Barras)
        df_status_sorted = dfs['status_profissional'].sort_values('leads_percent', ascending=True)
        fig.add_trace(
            go.Bar(
                x=df_status_sorted['leads_percent'],
                y=df_status_sorted['status'],
                orientation='h',
                marker_color=LeadsCharts.COLOR_PALETTE['secondary'],
                text=df_status_sorted['leads_percent'].apply(lambda x: f'{x}%'),
                textposition='auto',
                showlegend=False
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=700,
            title_text="📊 Dashboard Demográfico - Perfil dos Leads",
            title_x=0.5,
            showlegend=False,
            font=dict(size=11),
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        # Atualizar eixos
        fig.update_xaxes(title_text="Percentual (%)", row=1, col=2)
        fig.update_yaxes(title_text="Faixa Etária", row=1, col=2)
        fig.update_xaxes(title_text="Faixa Salarial", row=2, col=1)
        fig.update_yaxes(title_text="Percentual (%)", row=2, col=1)
        fig.update_xaxes(title_text="Percentual (%)", row=2, col=2)
        fig.update_yaxes(title_text="Status Profissional", row=2, col=2)
        
        return fig
    
    @staticmethod
    def create_demographic_dashboard(dfs: Dict[str, pd.DataFrame]):
        """Cria dashboard demográfico simplificado"""
        # Verificar dados necessários
        required = ['genero', 'faixa_etaria', 'faixa_salarial', 'status_profissional']
        if any(key not in dfs or dfs[key].empty for key in required):
            return go.Figure()
        
        # Dashboard simples com 4 gráficos
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['👥 Gênero', '🎂 Faixa Etária', '💰 Faixa Salarial', '💼 Status Profissional'],
            specs=[[{"type": "pie"}, {"type": "bar"}], [{"type": "bar"}, {"type": "bar"}]]
        )
        
        # Gênero
        fig.add_trace(
            go.Pie(
                labels=dfs['genero']['genero'],
                values=dfs['genero']['leads'],
                textinfo='label+percent',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Faixa Etária
        fig.add_trace(
            go.Bar(
                x=dfs['faixa_etaria']['faixa'],
                y=dfs['faixa_etaria']['leads_percent'],
                text=dfs['faixa_etaria']['leads_percent'].apply(lambda x: f'{x}%'),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Faixa Salarial
        fig.add_trace(
            go.Bar(
                x=dfs['faixa_salarial']['faixa'],
                y=dfs['faixa_salarial']['leads_percent'],
                text=dfs['faixa_salarial']['leads_percent'].apply(lambda x: f'{x}%'),
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Status Profissional
        fig.add_trace(
            go.Bar(
                x=dfs['status_profissional']['leads_percent'],
                y=dfs['status_profissional']['status'],
                orientation='h',
                text=dfs['status_profissional']['leads_percent'].apply(lambda x: f'{x}%'),
                showlegend=False
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=600, title_text="Dashboard Demográfico")
        return fig

    @staticmethod
    def create_vehicle_preference_dashboard(dfs: Dict[str, pd.DataFrame]):
        """Cria dashboard de veículos simplificado"""
        # Verificar dados necessários
        required = ['classificacao_veiculo', 'idade_veiculo', 'veiculos_visitados']
        if any(key not in dfs or dfs[key].empty for key in required):
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=['🚗 Tipo Veículo', '📅 Idade Veículo', '🏆 Top Marcas', '📊 Distribuição'],
            specs=[[{"type": "pie"}, {"type": "bar"}], [{"type": "bar"}, {"type": "pie"}]]
        )
        
        # Tipo de Veículo
        fig.add_trace(
            go.Pie(
                labels=dfs['classificacao_veiculo']['classificacao'],
                values=dfs['classificacao_veiculo']['visitas'],
                textinfo='percent+label',
                showlegend=False
            ),
            row=1, col=1
        )
        
        # Idade do Veículo
        fig.add_trace(
            go.Bar(
                x=dfs['idade_veiculo']['idade'],
                y=dfs['idade_veiculo']['visitas_percent'],
                text=dfs['idade_veiculo']['visitas_percent'].apply(lambda x: f'{x}%'),
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Top Marcas
        top_marcas = dfs['veiculos_visitados'].groupby('marca')['visitas'].sum().nlargest(5)
        fig.add_trace(
            go.Bar(
                x=top_marcas.values,
                y=top_marcas.index,
                orientation='h',
                text=top_marcas.values,
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Distribuição de Visitas (exemplo)
        fig.add_trace(
            go.Pie(
                labels=top_marcas.index,
                values=top_marcas.values,
                textinfo='percent+label',
                showlegend=False
            ),
            row=2, col=2
        )
        
        fig.update_layout(height=600, title_text="Dashboard de Veículos")
        return fig

    @staticmethod
    def create_vehicle_preference_dashboard(dfs: Dict[str, pd.DataFrame]):
        """Cria dashboard de preferências de veículos - NOVO"""
        if any(df.empty for df in [dfs.get('classificacao_veiculo'), dfs.get('idade_veiculo'), dfs.get('veiculos_visitados')]):
            return go.Figure()
        
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=[
                '🚗 Tipo de Veículo Preferido',
                '📅 Idade do Veículo Preferida',
                '🏆 Top 8 Marcas por Visitas',
                '📊 Distribuição de Visitas'
            ],
            specs=[
                [{"type": "pie"}, {"type": "bar"}],
                [{"type": "bar"}, {"type": "funnel"}]
            ],
            vertical_spacing=0.12,
            horizontal_spacing=0.08
        )
        
        # Tipo de Veículo (Pizza)
        fig.add_trace(
            go.Pie(
                labels=dfs['classificacao_veiculo']['classificacao'],
                values=dfs['classificacao_veiculo']['visitas'],
                marker_colors=LeadsCharts.VEHICLE_COLORS,
                hole=0.5,
                showlegend=False,
                textinfo='percent+label'
            ),
            row=1, col=1
        )
        
        # Idade do Veículo (Barras)
        df_idade_sorted = dfs['idade_veiculo'].sort_values('ordem')
        fig.add_trace(
            go.Bar(
                x=df_idade_sorted['idade'],
                y=df_idade_sorted['visitas_percent'],
                marker_color=LeadsCharts.COLOR_PALETTE['accent1'],
                text=df_idade_sorted['visitas_percent'].apply(lambda x: f'{x}%'),
                textposition='outside',
                showlegend=False
            ),
            row=1, col=2
        )
        
        # Top Marcas (Barras)
        top_marcas = dfs['veiculos_visitados'].groupby('marca')['visitas'].sum().nlargest(8)
        fig.add_trace(
            go.Bar(
                x=top_marcas.values,
                y=top_marcas.index,
                orientation='h',
                marker_color=LeadsCharts.COLOR_PALETTE['warning'],
                text=top_marcas.values,
                textposition='auto',
                showlegend=False
            ),
            row=2, col=1
        )
        
        # Funil de Engajamento (exemplo)
        engagement_data = {
            'stage': ['Leads Totais', 'Visitaram Veículos', 'Veículos Favoritos', 'Contataram Vendedor'],
            'value': [25109, 30580, 15000, 5000]  # Valores exemplos
        }
        
        fig.add_trace(
            go.Funnel(
                y=engagement_data['stage'],
                x=engagement_data['value'],
                textinfo="value+percent initial",
                marker_color=LeadsCharts.COLOR_PALETTE['danger'],
                showlegend=False
            ),
            row=2, col=2
        )
        
        fig.update_layout(
            height=700,
            title_text="🚗 Dashboard de Preferências - Comportamento dos Leads",
            title_x=0.5,
            showlegend=False,
            font=dict(size=11),
            margin=dict(t=100, b=50, l=50, r=50)
        )
        
        # Atualizar eixos
        fig.update_xaxes(title_text="Idade do Veículo", row=1, col=2)
        fig.update_yaxes(title_text="Percentual (%)", row=1, col=2)
        fig.update_xaxes(title_text="Visitas", row=2, col=1)
        fig.update_yaxes(title_text="Marca", row=2, col=1)
        fig.update_xaxes(title_text="Quantidade", row=2, col=2)
        
        return fig
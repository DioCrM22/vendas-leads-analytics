import streamlit as st
import pandas as pd
import plotly.express as px
from utils.vendas.data_manager import initialize_session_data, get_dataframes

# Inicializar dados
initialize_session_data()

st.title("👥 Dashboard de Leads")

st.markdown("""
<div class="dashboard-header">
    <h2 style="margin:0; font-size: 2rem;">📊 Análise de Performance de Leads</h2>
    <p style="margin:0; font-size: 1rem; opacity: 0.9;">Acompanhamento completo da jornada do lead</p>
</div>
""", unsafe_allow_html=True)

# Obter dados
dfs = get_dataframes()
df_mensal = dfs['mensal']

# KPIs de Leads
total_leads = df_mensal['leads'].sum()
total_vendas = df_mensal['vendas'].sum()
taxa_conversao_geral = (total_vendas / total_leads * 100) if total_leads > 0 else 0
melhor_mes_leads = df_mensal.loc[df_mensal['leads'].idxmax()]
pior_mes_leads = df_mensal.loc[df_mensal['leads'].idxmin()]

# Métricas
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">👥 Total de Leads</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #9b59b6;">{total_leads:,}</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">📈 Taxa de Conversão</div>
        <div style="font-size: 1.8rem; font-weight: bold; color: #2ecc71;">{taxa_conversao_geral:.1f}%</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">🏆 Melhor Mês</div>
        <div style="font-size: 1.2rem; font-weight: bold; color: #3498db;">{melhor_mes_leads['mes']}</div>
        <div style="font-size: 0.9rem;">{melhor_mes_leads['leads']:,} leads</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div style="font-size: 0.9rem; color: #666; margin-bottom: 0.5rem;">📉 Pior Mês</div>
        <div style="font-size: 1.2rem; font-weight: bold; color: #e74c3c;">{pior_mes_leads['mes']}</div>
        <div style="font-size: 0.9rem;">{pior_mes_leads['leads']:,} leads</div>
    </div>
    """, unsafe_allow_html=True)

# Gráficos
col_grafico1, col_grafico2 = st.columns(2)

with col_grafico1:
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.subheader("📈 Evolução de Leads vs Vendas")
    
    fig = px.line(df_mensal, x='mes', y=['leads', 'vendas'],
                  title='Leads e Vendas ao Longo do Tempo',
                  markers=True)
    fig.update_layout(
        height=400,
        xaxis_title='Mês',
        yaxis_title='Quantidade',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col_grafico2:
    st.markdown('<div class="graph-container">', unsafe_allow_html=True)
    st.subheader("🎯 Taxa de Conversão Mensal")
    
    df_mensal['conversao_percent'] = df_mensal['conversao'] * 100
    fig = px.bar(df_mensal, x='mes', y='conversao_percent',
                 title='Taxa de Conversão por Mês (%)',
                 color='conversao_percent',
                 color_continuous_scale='Viridis')
    fig.update_layout(
        height=400,
        xaxis_title='Mês',
        yaxis_title='Taxa de Conversão (%)',
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
    )
    st.plotly_chart(fig, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Tabela detalhada
st.markdown('<div class="graph-container">', unsafe_allow_html=True)
st.subheader("📋 Detalhamento Mensal de Performance")

# Calcular métricas adicionais
df_detalhado = df_mensal.copy()
df_detalhado['conversao_%'] = (df_detalhado['conversao'] * 100).round(1)
df_detalhado = df_detalhado[['mes', 'leads', 'vendas', 'conversao_%', 'receita', 'ticket_medio']]

st.dataframe(df_detalhado, use_container_width=True)
st.markdown('</div>', unsafe_allow_html=True)
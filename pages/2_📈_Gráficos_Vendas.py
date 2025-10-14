import streamlit as st
from utils.core.session_manager import SessionManager
from utils.vendas.data_manager import get_dataframes, calculate_kpis
from utils.vendas.charts import VendasCharts
from utils.components import UIComponents

class VendasDashboard:
    """Dashboard profissional para análise de vendas"""
    
    def __init__(self):
        SessionManager.initialize_app()
        self._load_css()
        self.dfs = get_dataframes()
        self.kpis = calculate_kpis()
    
    def _load_css(self) -> None:
        """Carrega estilos CSS"""
        try:
            with open('styles/vendas.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("Arquivo CSS não encontrado. Usando estilos padrão.")
    
    def render_header(self) -> None:
        """Renderiza cabeçalho do dashboard"""
        st.markdown("""
        <div class="dashboard-header-vendas">
            <h1 style="margin:0; font-size: 2.5rem;">💰 DASHBOARD DE VENDAS</h1>
            <p style="margin:0; font-size: 1.2rem; opacity: 0.9;">Análise de Performance e Performance Comercial</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_kpi_metrics(self) -> None:
        """Renderiza métricas principais de KPI"""
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_config = [
            {
                "value": f"R$ {self.kpis.get('total_receita', 0):,.0f}", 
                "label": "💰 Receita Total", 
                "color": "#e74c3c"
            },
            {
                "value": f"{self.kpis.get('total_vendas', 0):,}", 
                "label": "🚗 Vendas Totais", 
                "color": "#3498db"
            },
            {
                "value": f"{self.kpis.get('total_leads', 0):,}", 
                "label": "👥 Total de Leads", 
                "color": "#2ecc71"
            },
            {
                "value": f"{self.kpis.get('conversao_media', 0):.2f}%", 
                "label": "📊 Taxa de Conversão", 
                "color": "#9b59b6"
            }
        ]
        
        for col, metric in zip([col1, col2, col3, col4], metrics_config):
            with col:
                UIComponents.metric_card(
                    value=metric["value"],
                    label=metric["label"],
                    color=metric["color"]
                )
    
    def render_monthly_performance(self) -> None:
        """Renderiza análise de performance mensal"""
        st.subheader("📈 Performance Mensal")
        
        if 'mensal' not in self.dfs or self.dfs['mensal'].empty:
            st.info("📝 Nenhum dado mensal disponível")
            return
            
        # Gráfico principal
        fig = VendasCharts.create_monthly_performance(self.dfs['mensal'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Gráficos secundários
        col1, col2 = st.columns(2)
        
        with col1:
            fig = VendasCharts.create_conversion_trend(self.dfs['mensal'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            fig = VendasCharts.create_ticket_medio_chart(self.dfs['mensal'])
            st.plotly_chart(fig, use_container_width=True)
    
    def render_geographic_analysis(self) -> None:
        """Renderiza análise geográfica"""
        st.subheader("🗺️ Análise Geográfica por Estado")
        
        if 'estados' not in self.dfs or self.dfs['estados'].empty:
            st.info("📝 Nenhum dado geográfico disponível")
            return
            
        # Abas para diferentes visualizações de mapa
        tab1, tab2, tab3 = st.tabs([
            "🗺️ Mapa do Brasil", "📊 Ranking", "📍 Regiões"
        ])
        
        with tab1:
            # ✅ MÉTODO CORRETO: create_brazil_map
            fig = VendasCharts.create_brazil_map(self.dfs['estados'])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab2:
            # ✅ MÉTODO CORRETO: create_states_bar_chart
            fig = VendasCharts.create_states_bar_chart(self.dfs['estados'])
            st.plotly_chart(fig, use_container_width=True)
        
        with tab3:
            # ✅ MÉTODO CORRETO: create_regions_pie_chart
            fig = VendasCharts.create_regions_pie_chart(self.dfs['estados'])
            st.plotly_chart(fig, use_container_width=True)

    def render_brand_analysis(self) -> None:
        """Renderiza análise por marca"""
        st.subheader("🚗 Performance por Marca")
        
        if 'marcas' not in self.dfs or self.dfs['marcas'].empty:
            st.info("📝 Nenhum dado de marcas disponível")
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            # ✅ MÉTODO CORRETO: create_brands_analysis
            fig = VendasCharts.create_brands_analysis(self.dfs['marcas'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # ✅ MÉTODO CORRETO: create_category_pie_chart
            fig = VendasCharts.create_category_pie_chart(self.dfs['marcas'])
            st.plotly_chart(fig, use_container_width=True)
    
    def render_store_analysis(self) -> None:
        """Renderiza análise por loja"""
        st.subheader("🏪 Performance por Loja")
        
        if 'lojas' not in self.dfs or self.dfs['lojas'].empty:
            st.info("📝 Nenhum dado de lojas disponível")
            return
            
        # ✅ MÉTODO CORRETO: create_stores_ranking
        fig = VendasCharts.create_stores_ranking(self.dfs['lojas'])
        st.plotly_chart(fig, use_container_width=True)
    
    def render_visits_analysis(self) -> None:
        """Renderiza análise de visitas"""
        st.subheader("📱 Padrão de Visitas por Dia da Semana")
        
        if 'visitas' not in self.dfs or self.dfs['visitas'].empty:
            st.info("📝 Nenhum dado de visitas disponível")
            return
            
        # ✅ MÉTODO CORRETO: create_visits_trend
        fig = VendasCharts.create_visits_trend(self.dfs['visitas'])
        st.plotly_chart(fig, use_container_width=True)
        
        # Insights
        with st.expander("💡 Insights sobre Padrão de Visitas"):
            df_visitas = self.dfs['visitas'].sort_values('ordem')
            if not df_visitas.empty:
                dia_max = df_visitas.loc[df_visitas['visitas'].idxmax()]
                dia_min = df_visitas.loc[df_visitas['visitas'].idxmin()]
                
                st.markdown(f"""
                **Padrões Identificados:**
                - **Pico de visitas:** {dia_max['dia_semana'].title()} ({dia_max['visitas']} visitas)
                - **Menor movimento:** {dia_min['dia_semana'].title()} ({dia_min['visitas']} visitas)
                - **Variação:** {(dia_max['visitas']/dia_min['visitas'] - 1)*100:.1f}% entre melhor e pior dia
                - **Recomendação:** Intensificar campanhas nos dias de menor movimento
                """)
            else:
                st.info("Dados insuficientes para análise de insights")
    
    def render_dashboard(self) -> None:
        """Renderiza o dashboard completo"""
        self.render_header()
        self.render_kpi_metrics()
        
        # Verificar se há dados
        if not self.dfs or all(df.empty for df in self.dfs.values()):
            st.warning("⚠️ Nenhum dado disponível. Por favor, carregue os dados na página 'Dados'.")
            return
        
        # Abas organizadas
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "📈 Mensal", "🗺️ Estados", "🚗 Marcas", "🏪 Lojas", "📱 Visitas"
        ])
        
        with tab1:
            self.render_monthly_performance()
        
        with tab2:
            self.render_geographic_analysis()
        
        with tab3:
            self.render_brand_analysis()
        
        with tab4:
            self.render_store_analysis()
        
        with tab5:
            self.render_visits_analysis()

def main():
    """Função principal do dashboard de vendas"""
    st.set_page_config(
        page_title="Dashboard de Vendas", 
        page_icon="💰", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        dashboard = VendasDashboard()
        dashboard.render_dashboard()
    except Exception as e:
        st.error(f"Erro ao carregar dashboard de vendas: {str(e)}")
        st.info("Verifique se os dados foram inicializados corretamente.")

if __name__ == "__main__":
    main()
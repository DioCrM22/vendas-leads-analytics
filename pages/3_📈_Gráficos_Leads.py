import streamlit as st
import plotly.express as px  # ✅ ADICIONAR ESTE IMPORT
from utils.core.session_manager import SessionManager
from utils.leads.leads_manager import initialize_leads_data, get_leads_dataframes, calculate_leads_kpis
from utils.leads.charts import LeadsCharts
from utils.components import UIComponents

class LeadsDashboard:
    """Dashboard profissional para análise de leads"""
    
    def __init__(self):
        SessionManager.initialize_app()
        self._load_css()
        self.dfs = get_leads_dataframes()
        self.kpis = calculate_leads_kpis()
    
    def _load_css(self) -> None:
        """Carrega estilos CSS"""
        try:
            with open('styles/leads.css') as f:
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
        except FileNotFoundError:
            st.warning("Arquivo CSS não encontrado. Usando estilos padrão.")
    
    def render_header(self) -> None:
        """Renderiza cabeçalho do dashboard"""
        st.markdown("""
        <div class="dashboard-header">
            <h1 style="margin:0; font-size: 2.5rem;">👥 DASHBOARD DE LEADS</h1>
            <p style="margin:0; font-size: 1.2rem; opacity: 0.9;">Análise Detalhada do Perfil e Comportamento</p>
        </div>
        """, unsafe_allow_html=True)
    
    def render_kpi_metrics(self) -> None:
        """Renderiza métricas principais de KPI"""
        col1, col2, col3, col4 = st.columns(4)
        
        metrics_config = [
            {
                "value": f"{self.kpis.get('total_leads', 0):,}", 
                "label": "👥 Total de Leads", 
                "color": "#3498db"
            },
            {
                "value": f"{self.kpis.get('total_visitas', 0):,}", 
                "label": "📊 Visitas a Veículos", 
                "color": "#2ecc71"
            },
            {
                "value": f"{self.kpis.get('percent_mulheres', 0):.1f}%", 
                "label": "👩 Porcentagem Mulheres", 
                "color": "#9b59b6"
            },
            {
                "value": self.kpis.get('veiculo_mais_visitado', 'N/A'), 
                "label": "🚗 Veículo Top", 
                "color": "#e74c3c"
            }
        ]
        
        for col, metric in zip([col1, col2, col3, col4], metrics_config):
            with col:
                UIComponents.metric_card(
                    value=metric["value"],
                    label=metric["label"],
                    color=metric["color"]
                )
    
    def render_gender_analysis(self) -> None:
        """Renderiza análise de gênero"""
        st.subheader("👥 Distribuição por Gênero")
        
        if 'genero' not in self.dfs or self.dfs['genero'].empty:
            st.info("📝 Nenhum dado de gênero disponível")
            return
            
        col1, col2 = st.columns([2, 1])
        
        with col1:
            fig = LeadsCharts.create_gender_distribution(self.dfs['genero'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico adicional de pizza
            fig = px.pie(
                self.dfs['genero'],
                values='leads',
                names='genero',
                title='Distribuição Percentual',
                color_discrete_sequence=['#FF69B4', '#4169E1'],
                hole=0.4
            )
            fig.update_layout(height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    def render_professional_status(self) -> None:
        """Renderiza análise de status profissional"""
        st.subheader("💼 Status Profissional dos Leads")
        
        if 'status_profissional' not in self.dfs or self.dfs['status_profissional'].empty:
            st.info("📝 Nenhum dado de status profissional disponível")
            return
            
        fig = LeadsCharts.create_professional_status(self.dfs['status_profissional'])
        st.plotly_chart(fig, use_container_width=True)
    
    def render_age_distribution(self) -> None:
        """Renderiza análise de faixa etária"""
        st.subheader("🎂 Distribuição por Faixa Etária")
        
        if 'faixa_etaria' not in self.dfs or self.dfs['faixa_etaria'].empty:
            st.info("📝 Nenhum dado de faixa etária disponível")
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            fig = LeadsCharts.create_age_distribution(self.dfs['faixa_etaria'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico adicional de pizza
            fig = px.pie(
                self.dfs['faixa_etaria'],
                values='leads_percent',
                names='faixa',
                title='Distribuição por Idade',
                hole=0.3,
                color_discrete_sequence=px.colors.sequential.RdBu
            )
            fig.update_layout(height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    def render_salary_distribution(self) -> None:
        """Renderiza análise de faixa salarial"""
        st.subheader("💰 Distribuição por Faixa Salarial")
        
        if 'faixa_salarial' not in self.dfs or self.dfs['faixa_salarial'].empty:
            st.info("📝 Nenhum dado de faixa salarial disponível")
            return
            
        fig = LeadsCharts.create_salary_distribution(self.dfs['faixa_salarial'])
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("💡 Análise da Distribuição Salarial"):
            st.markdown("""
            **Insights:**
            - Maior concentração na faixa de R$ 5.000-10.000 (71%)
            - Apenas 4% dos leads têm renda acima de R$ 15.000
            - Distribuição típica de classe média
            """)
    
    def render_vehicle_classification(self) -> None:
        """Renderiza análise de classificação de veículos"""
        st.subheader("🚗 Preferência por Tipo de Veículo")
        
        if 'classificacao_veiculo' not in self.dfs or self.dfs['classificacao_veiculo'].empty:
            st.info("📝 Nenhum dado de classificação de veículos disponível")
            return
            
        col1, col2 = st.columns(2)
        
        with col1:
            fig = LeadsCharts.create_vehicle_classification(self.dfs['classificacao_veiculo'])
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Gráfico adicional de pizza
            fig = px.pie(
                self.dfs['classificacao_veiculo'],
                values='visitas',
                names='classificacao',
                title='Distribuição: Novo vs Seminovo',
                hole=0.4,
                color_discrete_sequence=['#1f77b4', '#aec7e8']
            )
            fig.update_layout(height=400)
            fig.update_traces(textposition='inside', textinfo='percent+label')
            st.plotly_chart(fig, use_container_width=True)
    
    def render_vehicle_age_preference(self) -> None:
        """Renderiza análise de preferência por idade do veículo"""
        st.subheader("📅 Preferência por Idade do Veículo")
        
        if 'idade_veiculo' not in self.dfs or self.dfs['idade_veiculo'].empty:
            st.info("📝 Nenhum dado de idade de veículo disponível")
            return
            
        fig = LeadsCharts.create_vehicle_age_distribution(self.dfs['idade_veiculo'])
        st.plotly_chart(fig, use_container_width=True)
        
        with st.expander("💡 Análise de Preferência por Idade"):
            st.markdown("""
            **Padrões Identificados:**
            - Maior interesse em veículos de 8-10 anos (25%)
            - Menor interesse em veículos muito novos (até 2 anos - 4%)
            - Preferência por veículos com 6-10 anos (45% combinado)
            """)
    
    def render_top_vehicles(self) -> None:
        """Renderiza análise dos veículos mais visitados"""
        st.subheader("🏆 Veículos Mais Visitados")
        
        if 'veiculos_visitados' not in self.dfs or self.dfs['veiculos_visitados'].empty:
            st.info("📝 Nenhum dado de veículos visitados disponível")
            return
            
        fig = LeadsCharts.create_top_vehicles(self.dfs['veiculos_visitados'])
        st.plotly_chart(fig, use_container_width=True)
    
    def render_demographic_dashboard(self) -> None:
        """Renderiza dashboard demográfico completo"""
        st.subheader("📊 Dashboard Demográfico Completo")
        
        # Verificar se todos os dados necessários estão disponíveis
        required_keys = ['genero', 'faixa_etaria', 'faixa_salarial', 'status_profissional']
        missing_keys = [key for key in required_keys if key not in self.dfs or self.dfs[key].empty]
        
        if missing_keys:
            st.info(f"📝 Dados incompletos para o dashboard. Faltando: {', '.join(missing_keys)}")
            return
            
        fig = LeadsCharts.create_demographic_dashboard(self.dfs)
        st.plotly_chart(fig, use_container_width=True)

    def render_vehicle_preference_dashboard(self) -> None:
        """Renderiza dashboard de preferências de veículos"""
        st.subheader("🚗 Dashboard de Preferências de Veículos")
        
        # Verificar se todos os dados necessários estão disponíveis
        required_keys = ['classificacao_veiculo', 'idade_veiculo', 'veiculos_visitados']
        missing_keys = [key for key in required_keys if key not in self.dfs or self.dfs[key].empty]
        
        if missing_keys:
            st.info(f"📝 Dados incompletos para o dashboard. Faltando: {', '.join(missing_keys)}")
            return
            
        fig = LeadsCharts.create_vehicle_preference_dashboard(self.dfs)
        st.plotly_chart(fig, use_container_width=True)

    def render_dashboard(self) -> None:
        """Renderiza o dashboard completo"""
        self.render_header()
        self.render_kpi_metrics()
        
        # Verificar se há dados
        if not self.dfs or all(df.empty for df in self.dfs.values()):
            st.warning("⚠️ Nenhum dado disponível. Por favor, carregue os dados na página 'Dados'.")
            return
        
        # Abas organizadas - AGORA COM DASHBOARDS
        tab1, tab2, tab3, tab4, tab5, tab6, tab7, tab8, tab9 = st.tabs([
            "📊 Demográfico", "🚗 Veículos", "👥 Gênero", "💼 Status", "🎂 Idade", 
            "💰 Salário", "🚗 Tipo Veículo", "📅 Idade Veículo", "🏆 Top Veículos"
        ])
        
        with tab1:
            self.render_demographic_dashboard()
        
        with tab2:
            self.render_vehicle_preference_dashboard()
        
        with tab3:
            self.render_gender_analysis()
        
        with tab4:
            self.render_professional_status()
        
        with tab5:
            self.render_age_distribution()
        
        with tab6:
            self.render_salary_distribution()
        
        with tab7:
            self.render_vehicle_classification()
        
        with tab8:
            self.render_vehicle_age_preference()
        
        with tab9:
            self.render_top_vehicles()

def main():
    """Função principal do dashboard"""
    st.set_page_config(
        page_title="Dashboard de Leads", 
        page_icon="👥", 
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    try:
        dashboard = LeadsDashboard()
        dashboard.render_dashboard()
    except Exception as e:
        st.error(f"Erro ao carregar dashboard: {str(e)}")
        st.info("Verifique se os dados foram inicializados corretamente.")

if __name__ == "__main__":
    main()
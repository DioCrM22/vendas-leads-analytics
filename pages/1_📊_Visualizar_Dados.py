import streamlit as st
from utils.vendas.data_manager import initialize_session_data
from utils.leads.leads_manager import initialize_leads_data

# Inicializar dados
initialize_session_data()
initialize_leads_data()

st.title("📊 Dados - Aba 'Resultados'")
st.markdown("Aqui você pode visualizar e editar os dados como no Excel")

# Configuração das abas
TAB_CONFIGS = [
    {"key": "mensal", "title": "📅 Mensal", "data_key": "dados_mensais", "subheader": "Dados Mensais"},
    {"key": "estados", "title": "🗺️ Estados", "data_key": "dados_estados", "subheader": "Dados por Estado"},
    {"key": "marcas", "title": "🚗 Marcas", "data_key": "dados_marcas", "subheader": "Dados por Marca"},
    {"key": "lojas", "title": "🏪 Lojas", "data_key": "dados_lojas", "subheader": "Dados por Loja"},
    {"key": "visitas", "title": "📱 Visitas", "data_key": "dados_visitas", "subheader": "Dados de Visitas"},
    {"key": "genero", "title": "👥 Gênero", "data_key": "dados_genero", "subheader": "Dados de Gênero"},
    {"key": "status_prof", "title": "💼 Status Profissional", "data_key": "dados_status_profissional", "subheader": "Dados de Status Profissional"},
    {"key": "faixa_etaria", "title": "🎂 Faixa Etária", "data_key": "dados_faixa_etaria", "subheader": "Dados de Faixa Etária"},
    {"key": "faixa_salarial", "title": "💰 Faixa Salarial", "data_key": "dados_faixa_salarial", "subheader": "Dados de Faixa Salarial"},
    {"key": "classificacao", "title": "🚗 Classificação Veículos", "data_key": "dados_classificacao_veiculo", "subheader": "Dados de Classificação do Veículo"},
    {"key": "idade_veiculo", "title": "📅 Idade Veículos", "data_key": "dados_idade_veiculo", "subheader": "Dados de Idade do Veículo"},
    {"key": "veiculos", "title": "🏆 Veículos Visitados", "data_key": "dados_veiculos_visitados", "subheader": "Dados de Veículos Visitados"}
]

# Criar abas dinamicamente
tab_titles = [config["title"] for config in TAB_CONFIGS]
tabs = st.tabs(tab_titles)

# Renderizar conteúdo de cada aba
for tab, config in zip(tabs, TAB_CONFIGS):
    with tab:
        st.subheader(config["subheader"])
        edited_data = st.data_editor(
            st.session_state[config["data_key"]],
            use_container_width=True,
            num_rows="dynamic",
            key=f"editor_{config['key']}"
        )
        if edited_data is not None:
            st.session_state[config["data_key"]] = edited_data
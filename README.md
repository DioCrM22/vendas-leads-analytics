# 📊 Dashboard de Análise de Vendas & Leads

<div align="center">

![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)
![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-316192?style=for-the-badge&logo=postgresql&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-2C2D72?style=for-the-badge&logo=pandas&logoColor=white)

**Dashboard interativo desenvolvido como projeto final do curso de PostgreSQL**

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://seusuario-streamlit-app.streamlit.app/)
[![GitHub](https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white)](https://github.com/seuusuario/dashboard-vendas-leads)

</div>

## 🎯 Sobre o Projeto

Como parte da conclusão do meu curso de **PostgreSQL**, desenvolvi este dashboard completo para demonstrar minhas habilidades em **análise de dados** e **visualização**. A aplicação consolida conceitos avançados de SQL com Python para criar uma ferramenta empresarial prática e profissional.

> 💡 **Destaque Técnico:** Todo o modelo de dados foi estruturado seguindo as melhores práticas de normalização SQL que aprendi no curso.

![Dashboard Preview](https://via.placeholder.com/800x400/2E86AB/FFFFFF?text=Dashboard+Vendas+%26+Leads+Preview)
**(Adicione screenshots reais do seu dashboard aqui)*

## 🚀 Funcionalidades

### 💰 **Dashboard de Vendas**
- 📈 **Performance Mensal**: Tendências de receita e vendas
- 🗺️ **Análise Geográfica**: Mapa de vendas por estado
- 🚗 **Performance por Marca**: Market share e categorias
- 🏪 **Ranking de Lojas**: Performance por unidade
- 📊 **KPIs em Tempo Real**: Métricas essenciais de negócio

### 👥 **Dashboard de Leads**
- 👤 **Segmentação Demográfica**: Idade, gênero, localização
- 💼 **Perfil Profissional**: Status profissional e faixa salarial
- 🚗 **Preferências**: Tipo de veículo e idade preferida
- 🏆 **Veículos Mais Visitados**: Top modelos e marcas
- 📈 **Funil de Conversão**: Journey completo do lead

### ⚙️ **Recursos Técnicos**
- 📤 **Exportação de Dados**: CSV e relatórios personalizados
- 📥 **Importação Flexível**: Múltiplos formatos de arquivo
- 🔧 **Gerenciamento de Colunas**: Estrutura dinâmica de dados
- 🎨 **Interface Responsiva**: Design moderno e intuitivo

## 🛠️ Tecnologias & Habilidades

### **Backend & Análise**
``python
# Habilidades demonstradas no projeto
- Python 3.11+
- Pandas (Manipulação avançada de dados)
- PostgreSQL (Modelagem e consultas complexas)
- NumPy (Cálculos numéricos)
Frontend & Visualização
python
- Streamlit (Framework web)
- Plotly (Gráficos interativos)
- CSS Personalizado (Design profissional)
- Visualização Geográfica (Mapas e heatmaps)
DevOps & Deploy
python
- Git & GitHub (Controle de versão)
- Streamlit Cloud (Deploy automatizado)
- Gestão de Dependências
- CI/CD Básico
📊 Estrutura do Projeto
text
dashboard-vendas-leads/
├── 📁 pages/                 # Módulos da aplicação
│   ├── 1_📊_Dados.py        # Gerenciamento de dados
│   ├── 2_💰_Dashboard_Vendas.py
│   ├── 3_👥_Dashboard_Leads.py
│   └── 4_⚙️_Configurações.py
├── 📁 utils/                 # Lógica de negócio
│   ├── 📁 core/             # Funcionalidades centrais
│   ├── 📁 vendas/           # Específico para vendas
│   ├── 📁 leads/            # Específico para leads
│   └── 📁 config/           # Configurações do sistema
├── 📁 styles/               # Estilos CSS
├── 📄 requirements.txt      # Dependências
└── 📄 README.md            # Documentação
🎓 Minha Jornada com SQL
Conhecimentos Adquiridos no Curso:
sql
-- ✅ Consultas Complexas
SELECT 
    EXTRACT(MONTH FROM data_venda) as mes,
    SUM(receita) as total_receita,
    AVG(ticket_medio) as ticket_medio
FROM vendas 
GROUP BY mes 
ORDER BY mes;

-- ✅ Junções e Subconsultas
SELECT 
    c.nome,
    COUNT(v.id) as total_compras,
    RANK() OVER (ORDER BY COUNT(v.id) DESC) as ranking
FROM clientes c
LEFT JOIN vendas v ON c.id = v.cliente_id
GROUP BY c.id, c.nome;

-- ✅ Otimização e Performance
CREATE INDEX idx_vendas_data ON vendas(data_venda);
CREATE INDEX idx_leads_regiao ON leads(regiao);
Aplicação Prática no Dashboard:
Modelagem Relacional: Estrutura de dados normalizada

Consultas Otimizadas: Agregações e análises complexas

Funções de Janela: Cálculos de ranking e tendências

Índices Estratégicos: Performance em grandes volumes

🚀 Como Executar
Pré-requisitos
bash
Python 3.8+
Git
Instalação e Execução
bash
# 1. Clone o repositório
git clone https://github.com/seuusuario/dashboard-vendas-leads.git

# 2. Acesse o diretório
cd dashboard-vendas-leads

# 3. Instale as dependências
pip install -r requirements.txt

# 4. Execute a aplicação
streamlit run app.py

# 5. Acesse no navegador
# http://localhost:8501
Deploy Automático
O projeto está configurado para deploy automático no Streamlit Cloud. Qualquer push para a branch main atualiza automaticamente a aplicação.

📈 Próximos Passos
Integração com banco de dados PostgreSQL em tempo real

Autenticação de usuários

Relatórios automatizados por email

Análises preditivas com machine learning

Dashboard mobile responsivo

👨‍💻 Sobre o Desenvolvedor
Seu Nome - Analista de Dados & Desenvolvedor Python

🎓 Formação: Curso de PostgreSQL - [Nome da Instituição]
💼 Experiência: Desenvolvimento de dashboards e análise de dados
🚀 Foco: Python, SQL, Análise de Dados, Visualização

Conecte-se Comigo:
https://img.shields.io/badge/LinkedIn-0077B5?style=for-the-badge&logo=linkedin&logoColor=white
https://img.shields.io/badge/GitHub-100000?style=for-the-badge&logo=github&logoColor=white
https://img.shields.io/badge/Portfolio-FF7139?style=for-the-badge&logo=Firefox-Browser&logoColor=white

📄 Licença
Este projeto está sob a licença MIT. Veja o arquivo LICENSE para detalhes.

<div align="center">
⭐ Se este projeto te ajudou, deixe uma estrela no repositório!

Desenvolvido com 💙 e ☕ durante o curso de PostgreSQL

</div> ``
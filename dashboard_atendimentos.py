import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Configuração inicial
st.set_page_config(page_title='Dashboard UPA 24H', layout='wide')
st.image('TESTEIRA PAINEL UPA1.png', width=500)
st.title('Análises de Atendimentos - UPA 24H Dona Zulmira Soares')

# Sidebar com imagem e filtros
st.sidebar.image('TESTEIRA PAINEL UPA1.png', width=350)
st.sidebar.header('Filtros')
uploaded_file = st.sidebar.file_uploader("Envie a planilha de atendimentos", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    df_clean = df.dropna(how="all").reset_index(drop=True)
    df_clean.columns = df_clean.iloc[0]
    df_clean = df_clean[1:].reset_index(drop=True)

    # Aplicação de filtros
    filtros = {
        'Especialidade': st.sidebar.multiselect('Filtrar por Especialidade', df_clean['Especialidade'].unique()),
        'Profissional': st.sidebar.multiselect('Filtrar por Profissional', df_clean['Profissional'].unique()),
        'Cid10': st.sidebar.multiselect('Filtrar por CID-10', df_clean['Cid10'].unique()),
        'Prioridade': st.sidebar.multiselect('Filtrar por Prioridade', df_clean['Prioridade'].unique())
    }

    for coluna, filtro in filtros.items():
        if filtro:
            df_clean = df_clean[df_clean[coluna].isin(filtro)]

    # Funções para criar gráficos
    def criar_grafico_pizza(df, coluna, titulo):
        contagem = df[coluna].value_counts().reset_index()
        contagem.columns = [coluna, 'Quantidade']
        return px.pie(contagem, names=coluna, values='Quantidade', title=titulo)

    def criar_grafico_barra(df, coluna, titulo, top_n=10):
        contagem = df[coluna].value_counts().reset_index()
        contagem.columns = [coluna, 'Quantidade']
        return px.bar(contagem.head(top_n), x=coluna, y='Quantidade', title=titulo, color='Quantidade', color_continuous_scale='Reds')

    def criar_grafico_linha(df, coluna, titulo, top_n=10):
        contagem = df[coluna].value_counts().reset_index()
        contagem.columns = [coluna, 'Quantidade']
        return px.line(contagem.head(top_n), x=coluna, y='Quantidade', title=titulo)

    def criar_grafico_dispersao(df, x_col, y_col, titulo):
        return px.scatter(df, x=x_col, y=y_col, title=titulo, color=y_col, size=y_col)

    # Exibição dos gráficos
    st.plotly_chart(criar_grafico_pizza(df_clean, 'Especialidade', '% de Atendimentos por Categoria'))
    st.plotly_chart(criar_grafico_pizza(df_clean, 'Motivo Alta', 'Motivos de Alta'))
    st.plotly_chart(criar_grafico_barra(df_clean, 'Cid10', 'Top 10 CID-10 Mais Frequentes'))
    st.plotly_chart(criar_grafico_linha(df_clean, 'Usuário', 'Top 10 Usuários com Mais Atendimentos'))
    st.plotly_chart(criar_grafico_barra(df_clean, 'Profissional', 'Top 10 Profissionais com Mais Atendimentos'))
    st.plotly_chart(criar_grafico_barra(df_clean, 'Prioridade', 'Distribuição de Atendimentos por Prioridade'))

    # Análise combinada de Profissional e Especialidade
    if 'Profissional' in df_clean.columns and 'Especialidade' in df_clean.columns:
        prof_esp_counts = df_clean.groupby(['Profissional', 'Especialidade']).size().reset_index(name='Quantidade')
        for especialidade in prof_esp_counts['Especialidade'].unique():
            esp_data = prof_esp_counts[prof_esp_counts['Especialidade'] == especialidade]
            st.plotly_chart(px.bar(esp_data, x='Profissional', y='Quantidade', title=f'Atendimentos por Profissional - {especialidade}', color='Quantidade', color_continuous_scale='Reds'))

    # Gráfico de dispersão entre especialidade e quantidade de atendimentos
    if 'Especialidade' in df_clean.columns and 'Quantidade' in prof_esp_counts.columns:
        st.plotly_chart(criar_grafico_dispersao(prof_esp_counts, 'Especialidade', 'Quantidade', 'Distribuição de Atendimentos por Especialidade'))

    # Visualização final dos dados
    st.write("Visualização dos dados:", df_clean)
    st.success("Análise concluída com sucesso!")

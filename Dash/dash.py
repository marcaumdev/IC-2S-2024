import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from query import conexao

# Configuração da página
st.set_page_config(
    page_title="Morte emissão por países",
    page_icon="📊",
    layout="wide"
)

# Consultas ao banco
pais_query = "SELECT * FROM pais"
mortes_query = "SELECT * FROM mortes"
emissao_query = "SELECT * FROM emissao"
temperatura_query = "SELECT * FROM temperatura"

# Carregar os dados do banco e arquivos locais
pais = conexao(pais_query)
mortes = conexao(mortes_query)
emissoes = conexao(emissao_query)
temperatura = conexao(temperatura_query)

st.sidebar.title("Filtros")
pais_selecionado = st.sidebar.selectbox("Selecione o País", pais['nome'].unique())
# Slider para intervalo de anos
ano_inicio, ano_fim = st.sidebar.slider(
    "Selecione o Intervalo de Anos",
    int(temperatura['ano'].min()),
    int(temperatura['ano'].max()),
    value=(int(temperatura['ano'].min()), int(temperatura['ano'].max())),
    step=1
)

# Filtrar dados com base no país selecionado e no intervalo de anos
dados_filtrados = temperatura.merge(pais, left_on='id_pais', right_on='id')
dados_filtrados = dados_filtrados[
    (dados_filtrados['nome'] == pais_selecionado) &
    (dados_filtrados['ano'] >= ano_inicio) &
    (dados_filtrados['ano'] <= ano_fim)
]

# Função de visualização principal
def Home():
    st.title("Dashboard")

# Função de gráficos
def graficos():
    st.header("Gráficos Interativos")
    aba1, aba2, aba3, aba4, aba5, aba6 = st.tabs(["Temperatura Média por País", "Mortes por País e Ano", "Emissões Totais por Tipo de Fonte", "Temperatura por pais", f"Mortes por temperatura no {pais_selecionado}", f"mortes por emissao no {pais_selecionado}"])

    with aba1:
        # Juntar dados
        dados_temp = temperatura.merge(pais, left_on='id_pais', right_on='id')

        # Calcular a média
        media_temp = dados_temp.groupby('nome')['indice'].mean().reset_index()

        # Criar gráfico com tons de vermelho
        fig_temp = px.bar(media_temp.sort_values(by='indice', ascending=False), x='nome', y='indice', title='Temperatura Média por País')
        st.plotly_chart(fig_temp)

    with aba2:
        # Juntar dados
        dados_mortes = mortes.merge(pais, left_on='id_pais', right_on='id')

        # Criar gráfico
        fig_mortes = px.line(dados_mortes, x='ano', y='quantidade', color='nome', title='Mortes por País ao Longo dos Anos')
        fig_mortes.update_layout(
            legend=dict(
                yanchor="top",
                y=1,
                xanchor="left",
                x=1.05,  # Move a legenda para fora do gráfico
                orientation="h",  # Orientação vertical
                itemwidth=30,
                traceorder='normal',
                itemsizing='constant'
            ),
            legend_title="Países",
            showlegend=True
        )
        # Alterar as bolinhas de legenda
        fig_mortes.update_traces(marker=dict(symbol='circle'))
        st.plotly_chart(fig_mortes)

    with aba3:
        # Somar emissões
        emissoes_totais = emissoes[['carvao', 'petroleo', 'gas', 'cimento', 'queima', 'outros']].sum()

        # Criar gráfico
        fig_emissoes = px.pie(values=emissoes_totais, names=emissoes_totais.index, title='Distribuição de Emissões por Fonte')
        st.plotly_chart(fig_emissoes)

    with aba4:
        # Exibir gráfico com tons de vermelho
        fig_filtro = px.bar(dados_filtrados, x='ano', y='indice', title=f'Temperatura em {pais_selecionado} de {ano_inicio} a {ano_fim}', color='ano', color_continuous_scale='reds')
        st.plotly_chart(fig_filtro)

    with aba5:
        # Junção de dados de temperatura com mortes
        dados_mortes_temperatura = mortes.merge(pais, left_on='id_pais', right_on='id')
        dados_mortes_temperatura = dados_mortes_temperatura[
            (dados_mortes_temperatura['nome'] == pais_selecionado) & 
            (dados_mortes_temperatura['ano'] >= ano_inicio) & 
            (dados_mortes_temperatura['ano'] <= ano_fim)
        ]
        dados_mortes_temperatura = dados_mortes_temperatura.merge(temperatura, left_on=['id_pais', 'ano'], right_on=['id_pais', 'ano'], suffixes=('_mortes', '_temperatura'))
        fig_temperatura = px.scatter(dados_mortes_temperatura, x='indice', y='quantidade', color='ano',
                                     title=f'Mortes por Temperatura no {pais_selecionado} de {ano_inicio} a {ano_fim}',
                                     labels={'indice': 'Temperatura (°C)', 'quantidade': 'Quantidade de Mortes'}, color_continuous_scale='reds')
        st.plotly_chart(fig_temperatura)

    with aba6:
        # Junção de dados de emissões com mortes
        dados_mortes_emissoes = mortes.merge(pais, left_on='id_pais', right_on='id')
        dados_mortes_emissoes = dados_mortes_emissoes[
            (dados_mortes_emissoes['nome'] == pais_selecionado) &
            (dados_mortes_emissoes['ano'] >= ano_inicio) &
            (dados_mortes_emissoes['ano'] <= ano_fim)
        ]
        dados_mortes_emissoes = dados_mortes_emissoes.merge(emissoes, left_on=['id_pais', 'ano'], right_on=['id_pais', 'ano'], suffixes=('_mortes', '_emissoes'))

        # Criar gráfico de mortes por emissões com tons de vermelho
        fig_emissoes = px.scatter(dados_mortes_emissoes, x='carvao', y='quantidade', color='ano',
                                  title=f'Mortes por Emissões de Carvão no {pais_selecionado} de {ano_inicio} a {ano_fim}',
                                  labels={'carvao': 'Emissões de Carvão (milhões de toneladas)', 'quantidade': 'Quantidade de Mortes'}, color_continuous_scale='reds')
        st.plotly_chart(fig_emissoes)

    

# Rodar as funções
Home()
graficos()
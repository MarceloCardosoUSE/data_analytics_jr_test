import streamlit as st
import sqlite3
import pandas as pd
import plotly.express as px
import altair as alt


def create_connection():
    conn = None
    try:
        conn = sqlite3.connect('teste_analytics.db')
        st.write('Conexão com o banco de dados estabelecida com sucesso.')
    except sqlite3.Error as e:
        st.error(f'Erro ao conectar-se ao banco de dados: {e}')
    return conn


def calcular_contagem_situacao_por_distrito(conn):
    
    dados = pd.read_sql_query("SELECT DISTRITO, SITUACAO FROM escolas_alunos WHERE DISTRITO IS NOT NULL AND SITUACAO IN ('ATIVA', 'CRIADA')", conn)

    
    contagem_situacao_por_distrito = dados.groupby(['DISTRITO', 'SITUACAO']).size().reset_index(name='COUNT')

    return contagem_situacao_por_distrito


def calcular_modalidade_dominante_por_distrito(conn):
    
    dados = pd.read_sql_query("SELECT DISTRITO, MODAL FROM escolas_alunos WHERE DISTRITO IS NOT NULL AND MODAL IS NOT NULL", conn)


    contagem_modalidade_por_distrito = dados.groupby(['DISTRITO', 'MODAL']).size().reset_index(name='COUNT')


    modalidade_dominante_por_distrito = contagem_modalidade_por_distrito.loc[contagem_modalidade_por_distrito.groupby('DISTRITO')['COUNT'].idxmax()]

    return modalidade_dominante_por_distrito


def calcular_contagem_nee_por_distrito(conn):

    dados = pd.read_sql_query("SELECT DISTRITO, NEE FROM escolas_alunos WHERE DISTRITO IS NOT NULL AND NEE IS NOT NULL", conn)

    nee_por_distrito = dados.groupby(['DISTRITO', 'NEE']).size()

   
    nee_por_distrito_ordenado = nee_por_distrito.groupby('DISTRITO').sum().sort_values(ascending=False)

    return nee_por_distrito_ordenado


def calcular_contagem_sexo_por_distrito(conn):

    dados = pd.read_sql_query("SELECT DISTRITO, SEXO FROM escolas_alunos WHERE DISTRITO IS NOT NULL AND SEXO IS NOT NULL", conn)


    contagem_sexo_por_distrito = dados.groupby(['DISTRITO', 'SEXO']).size().reset_index(name='COUNT')

    return contagem_sexo_por_distrito


def calcular_taxa_crescimento_media_por_distrito(conn):

    dados = pd.read_sql_query("SELECT DISTRITO, ANO, QTDE FROM escolas_alunos WHERE DISTRITO IS NOT NULL AND ANO IS NOT NULL AND QTDE IS NOT NULL", conn)


    alunos_por_distrito_ano = dados.groupby(['DISTRITO', 'ANO'])['QTDE'].sum().reset_index()
    alunos_por_distrito_ano = alunos_por_distrito_ano.sort_values(by=['DISTRITO', 'ANO'])
    alunos_por_distrito_ano['TAXA_DE_CRESCIMENTO'] = alunos_por_distrito_ano.groupby('DISTRITO')['QTDE'].pct_change()
    distritos_mais_crescentes = alunos_por_distrito_ano.groupby('DISTRITO')['TAXA_DE_CRESCIMENTO'].mean().sort_values(ascending=False)

    return distritos_mais_crescentes


conn = create_connection()


st.sidebar.title("Escolha a página")
pagina = st.sidebar.selectbox("Escolha uma página", [" Situação ATIVA por Distrito", "Modalidade Dominante por Distrito", "Contagem NEE por Distrito", "Contagem Sexo por Distrito", "Taxa de Crescimento Média por Distrito"])


if pagina == " Situação ATIVA por Distrito":
    contagem_situacao_por_distrito = calcular_contagem_situacao_por_distrito(conn)
    contagem_situacao_por_distrito_ordenado = contagem_situacao_por_distrito.sort_values(by='COUNT', ascending=False)
    st.write("### Contagem Situação por Distrito")
    st.bar_chart(contagem_situacao_por_distrito_ordenado, x='DISTRITO', y='SITUACAO')


elif pagina == "Modalidade Dominante por Distrito":
    modalidade_dominante_por_distrito = calcular_modalidade_dominante_por_distrito(conn)
    st.write("### Modalidade Dominante por Distrito")
    fig = px.pie(modalidade_dominante_por_distrito, values='COUNT', names='MODAL', title='Modalidade Dominante por Distrito')
    st.plotly_chart(fig)


elif pagina == "Contagem NEE por Distrito":
    nee_por_distrito_ordenado = calcular_contagem_nee_por_distrito(conn)
    top_10_distritos = nee_por_distrito_ordenado.head(10)
    st.write("### Top 10 Distritos com Mais Casos de NEE")
    st.bar_chart(top_10_distritos, use_container_width=True)


elif pagina == "Contagem Sexo por Distrito":
    contagem_sexo_por_distrito = calcular_contagem_sexo_por_distrito(conn)
    contagem_sexo_por_distrito_ordenado = contagem_sexo_por_distrito.sort_values(by='COUNT', ascending=False)
    st.write("### Contagem Sexo por Distrito")
    chart = alt.Chart(contagem_sexo_por_distrito_ordenado).mark_bar().encode(
        x='COUNT',
        y='DISTRITO',
        color='SEXO'
    )
    st.altair_chart(chart, use_container_width=True)


elif pagina == "Taxa de Crescimento Média por Distrito":
    distritos_mais_crescentes = calcular_taxa_crescimento_media_por_distrito(conn)
    st.write("### Distritos com Maior Taxa de Crescimento Média")
    fig = px.bar(distritos_mais_crescentes, x=distritos_mais_crescentes.index, y=distritos_mais_crescentes.values, labels={'y':'Taxa de Crescimento Média'}, title='Distritos com Maior Taxa de Crescimento Média')
    st.plotly_chart(fig)


conn.close()
import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
from langchain_openai import ChatOpenAI
from langchain_core.prompts import PromptTemplate

def formatar_brl(valor_numerico):
    """Formata um número para o padrão de moeda brasileiro (R$ 1.234,56)."""
    if pd.isna(valor_numerico):
        return "N/A"
    # Formata no padrão EN (ex: 1,234.56)
    valor_en = f"{valor_numerico:,.2f}"
    # Inverte os separadores para o padrão BR (ex: 1.234,56)
    # Usa um placeholder para não haver conflito na troca
    valor_br = valor_en.replace(",", "TEMP").replace(".", ",").replace("TEMP", ".")
    return valor_br

def interpretar_comando_llm(pergunta, openai_api_key):
    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

    prompt = PromptTemplate.from_template("""
Você é um assistente que mapeia perguntas para comandos de agregação sobre um DataFrame com colunas como VALOR TOTAL, VALOR UNITÁRIO e QUANTIDADE.

Pergunta: {pergunta}

Responda apenas com uma das opções abaixo:
- total_valor
- media_valor
- contar_notas
- contar_produtos
- max_valor
- min_valor
- desconhecido
""")

    resposta = llm.invoke(prompt.format(pergunta=pergunta)).content.strip().lower()
    return resposta


def sugestao_grafico(pergunta, openai_api_key):
    llm = ChatOpenAI(openai_api_key=openai_api_key, temperature=0)

    prompt = f"""A seguinte pergunta foi feita sobre dados de notas fiscais:

"{pergunta}"

Responda com uma das seguintes opções (em minúsculas):
- barras por município
- linha temporal
- pizza por natureza
- nenhum

Apenas retorne a opção.
"""
    return llm.invoke(prompt).content.strip().lower()


def grafico_valor_por_municipio(df):
    agrupado = df.groupby("MUNICÍPIO EMITENTE")["VALOR TOTAL"].sum().sort_values(ascending=False).head(10)
    fig, ax = plt.subplots()
    agrupado.plot(kind="barh", ax=ax)
    ax.set_title("🗺️ Top 10 municípios por valor total de notas")
    ax.set_xlabel("Valor total (R$)")
    st.pyplot(fig)


def grafico_temporal(df):
    df["DATA EMISSÃO"] = pd.to_datetime(df["DATA EMISSÃO"], errors="coerce")
    serie = df.groupby(df["DATA EMISSÃO"].dt.date)["VALOR TOTAL"].sum()
    fig, ax = plt.subplots()
    serie.plot(ax=ax)
    ax.set_title("📅 Evolução do valor total por dia")
    ax.set_ylabel("Valor total (R$)")
    st.pyplot(fig)


def grafico_natureza_operacao(df):
    contagem = df["NATUREZA DA OPERAÇÃO"].value_counts().head(5)
    fig, ax = plt.subplots()
    ax.pie(contagem, labels=contagem.index, autopct="%1.1f%%")
    ax.set_title("📄 Distribuição das naturezas de operação")
    st.pyplot(fig)


def responder_analitico(pergunta: str, df: pd.DataFrame, openai_api_key: str) -> str:
    for col in ["VALOR TOTAL", "VALOR UNITÁRIO", "QUANTIDADE"]:
        if col in df.columns and not pd.api.types.is_numeric_dtype(df[col]):
            df[col] = pd.to_numeric(df[col], errors="coerce")

    acao = interpretar_comando_llm(pergunta, openai_api_key)

    if acao == "total_valor":
        total = df['VALOR TOTAL'].sum()
        resposta = f"🧾 O valor total das notas é R$ {formatar_brl(total)}"
    elif acao == "media_valor":
        media = df['VALOR TOTAL'].mean()
        resposta = f"📊 A média do valor das notas é R$ {formatar_brl(media)}"
    elif acao == "contar_notas":
        resposta = f"📄 Foram emitidas {len(df)} notas fiscais."
    elif acao == "contar_produtos":
        total_produtos = df["QUANTIDADE"].sum()
        resposta = f"📦 Foram vendidos {total_produtos:.0f} produtos no total."
    elif acao == "max_valor":
        linha = df.loc[df["VALOR TOTAL"].idxmax()]
        resposta = f"""💰 Nota de maior valor: R$ {linha['VALOR TOTAL']:,.2f}
Emitente: {linha.get("RAZÃO SOCIAL EMITENTE", "N/A")}
Produto: {linha.get("DESCRIÇÃO DO PRODUTO/SERVIÇO", "N/A")}"""
    elif acao == "min_valor":
        linha = df.loc[df["VALOR TOTAL"].idxmin()]
        resposta = f"""💸 Nota de menor valor: R$ {linha['VALOR TOTAL']:,.2f}
Emitente: {linha.get("RAZÃO SOCIAL EMITENTE", "N/A")}
Produto: {linha.get("DESCRIÇÃO DO PRODUTO/SERVIÇO", "N/A")}"""
    else:
        return "🤖 Não consegui interpretar a pergunta. Pode reformular?"

    grafico = sugestao_grafico(pergunta, openai_api_key)
    if grafico == "barras por município":
        grafico_valor_por_municipio(df)
    elif grafico == "linha temporal":
        grafico_temporal(df)
    elif grafico == "pizza por natureza":
        grafico_natureza_operacao(df)

    return resposta

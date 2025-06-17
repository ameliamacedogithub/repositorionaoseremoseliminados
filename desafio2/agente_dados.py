import os
import pandas as pd
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain.docstore.document import Document


def carregar_arquivos_csv(destino_dir):
    arquivos_csv = [f for f in os.listdir(destino_dir) if f.endswith(".csv")]
    if len(arquivos_csv) != 2:
        raise ValueError("Esperado exatamente 2 arquivos CSV no diretório.")

    df1 = pd.read_csv(os.path.join(destino_dir, arquivos_csv[0]), dtype=str)
    df2 = pd.read_csv(os.path.join(destino_dir, arquivos_csv[1]), dtype=str)

    df1.columns = df1.columns.str.strip()
    df2.columns = df2.columns.str.strip()

    return df1, df2


def decidir_estrutura(df1, df2):
    col1 = set(df1.columns)
    col2 = set(df2.columns)

    exclusivas_df1 = col1 - col2
    exclusivas_df2 = col2 - col1

    if len(exclusivas_df1) > len(exclusivas_df2):
        return "df1"
    elif len(exclusivas_df2) > len(exclusivas_df1):
        return "df2"
    else:
        return "df1"  # Default: se forem iguais ou mesmo número de colunas exclusivas
    

def preparar_dataframe(estrutura, df1, df2):
    if estrutura == "df1":
        return df1.copy()
    elif estrutura == "df2":
        return df2.copy()
    else:
        raise ValueError("Estrutura inválida.")

    # Conversão segura das colunas numéricas
    for col in ["VALOR TOTAL", "VALOR UNITÁRIO", "QUANTIDADE"]:
        if col in df.columns:
            df[col] = (
                df[col]
                .astype(str)
                .str.replace("R$", "", regex=False)
                .str.replace(".", "", regex=False)  # Remove separadores de milhar
                .str.replace(",", ".", regex=False)  # Troca vírgula por ponto
                .str.strip()
            )
            df[col] = pd.to_numeric(df[col], errors="coerce")

    return df

def indexar_em_chroma(df, persist_dir, openai_api_key=None):
    # Garante que o diretório existe
    os.makedirs(persist_dir, exist_ok=True)

    # ⚠️ Garantir valores padrão para campos ausentes
    df = df.fillna("Não informado")

    # 🧱 Geração dos documentos
    docs = []
    for _, row in df.iterrows():
        texto = f"""
Produto: {row.get('DESCRIÇÃO DO PRODUTO/SERVIÇO', 'Não informado')}
Valor total do item: {row.get('VALOR TOTAL', 'Não informado')}
Emitente: {row.get('RAZÃO SOCIAL EMITENTE', 'Não informado')}
Município: {row.get('MUNICÍPIO EMITENTE', 'Não informado')} - {row.get('UF EMITENTE', 'Não informado')}
Destinatário: {row.get('NOME DESTINATÁRIO', 'Não informado')}
Natureza da operação: {row.get('NATUREZA DA OPERAÇÃO', 'Não informado')}
        """.strip()

        metadados = {"chave": row.get("CHAVE DE ACESSO", "sem-chave")}
        docs.append(Document(page_content=texto, metadata=metadados))

    # Split e embedding
    splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    docs_split = splitter.split_documents(docs)

    embeddings = OpenAIEmbeddings(openai_api_key=openai_api_key)
    db = Chroma.from_documents(docs_split, embedding=embeddings, persist_directory=persist_dir)

    return db


def carregar_dados(destino_dir,persist_dir, openai_api_key=None):
    df1, df2 = carregar_arquivos_csv(destino_dir)
    estrutura = decidir_estrutura(df1, df2)
    df_final = preparar_dataframe(estrutura, df1, df2)
    db = indexar_em_chroma(df_final, persist_dir, openai_api_key=openai_api_key)
    return df_final, db




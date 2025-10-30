from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings

def responder_semantico(pergunta: str, persist_dir: str, openai_api_key: str, k: int = 10) -> str:
    # Carrega o banco vetorial
    db = Chroma(persist_directory=persist_dir, embedding_function=OpenAIEmbeddings(openai_api_key=openai_api_key))

    # Faz a busca por similaridade
    resultados = db.similarity_search(pergunta, k=k)

    if not resultados:
        return "🤷 Nenhuma informação encontrada com base na pergunta."

    resposta = "📄 Resultados mais relevantes:\n\n"
    for i, doc in enumerate(resultados, 1):
        resposta += f"**{i}. Documento Relevante:**\n"
        resposta += f"```\n{doc.page_content.strip()}\n```\n\n"

    return resposta.strip()

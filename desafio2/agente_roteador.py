from agente_semantico import responder_semantico
from agente_analitico import responder_analitico
from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
import re

def heuristica_classificacao(pergunta: str) -> str:
    """Fallback simples baseado em palavras-chave."""
    pergunta_lower = pergunta.lower()
    padroes_analiticos = [
        r"média", r"soma", r"total", r"quantidade", r"valor (?:médio|total)?",
        r"maior.*valor", r"menor.*valor", r"contagem", r"número de", r"quanto"
    ]
    for padrao in padroes_analiticos:
        if re.search(padrao, pergunta_lower):
            return "analitica"
    return "semantica"

def agente_roteador(pergunta: str, df, persist_dir: str, openai_api_key: str) -> str:
    try:
        # LLM para classificar a intenção
        llm = ChatOpenAI(api_key=openai_api_key, temperature=0)
        prompt = f"""
Classifique a seguinte pergunta do usuário como um dos três tipos:
- "analitica" se envolve cálculo, soma, média, quantidade ou agregação sobre valores numéricos.
- "semantica" se é uma pergunta textual ou descritiva que depende de similaridade de texto.
- "fora_do_escopo" se não puder ser respondida com os dados de notas fiscais.

Pergunta: {pergunta}

Somente retorne uma dessas três palavras: analitica, semantica ou fora_do_escopo.
"""

        resposta = llm([HumanMessage(content=prompt)]).content.strip().lower()
        print(f"🧠 Classificação LLM: {resposta}")

    except Exception as e:
        print("⚠️ Falha na LLM, usando heurística:", e)
        resposta = heuristica_classificacao(pergunta)
        print(f"🧠 Classificação heurística: {resposta}")

    # Decisão final
    if resposta == "analitica":
        return responder_analitico(pergunta, df, openai_api_key)

    elif resposta == "semantica":
        return responder_semantico(pergunta, persist_dir, openai_api_key)
    else:
        return "🤔 Desculpe, essa pergunta está fora do escopo do sistema."

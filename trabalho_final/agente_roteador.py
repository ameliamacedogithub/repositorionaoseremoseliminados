from agente_semantico import responder_semantico
from agente_analitico import responder_analitico
from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage
from agente_ferramentas import consultar_iva_online
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

Você é um especialista em classificar perguntas de usuários sobre dados de notas fiscais.
Classifique a pergunta do usuário em uma das quatro categorias abaixo.

**Categorias:**
- "analitica": Envolve cálculo, soma, média, ou agregação sobre os dados carregados.
- "semantica": É uma pergunta textual ou descritiva sobre os dados carregados.
- "ferramenta_iva": A pergunta é especificamente sobre o imposto IVA, sua alíquota ou o cálculo dele.
- "fora_do_escopo": Não se encaixa em nenhuma das anteriores.

**Exemplos:**
- Pergunta: "Qual a soma dos valores?" -> Resposta: analitica
- Pergunta: "Fale sobre as notas da empresa 'ACME Corp'" -> Resposta: semantica
- Pergunta: "qual o valor do iva sobre 1500 reais?" -> Resposta: ferramenta_iva
- Pergunta: "Qual a alíquota de iva hoje?" -> Resposta: ferramenta_iva
- Pergunta: "Qual a previsão do tempo para amanhã?" -> Resposta: fora_do_escopo

**Pergunta do Usuário:**
"{pergunta}"

**Sua Classificação (retorne apenas uma palavra):**
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

    elif resposta == "ferramenta_iva":
        # Esta parte ainda não está no seu código original.
        # Estamos adicionando a chamada para a nova ferramenta.
        # Precisaremos passar a chave da API do Google, mas por agora vamos simplificar.
        return consultar_iva_online(pergunta, openai_api_key)

    elif resposta == "semantica":
        return responder_semantico(pergunta, persist_dir, openai_api_key)
    else:
        return "🤔 Desculpe, só consigo responder perguntas sobre os dados das notas fiscais que foram carregadas. Você pode perguntar sobre totais, médias ou buscar por produtos e empresas específicas."

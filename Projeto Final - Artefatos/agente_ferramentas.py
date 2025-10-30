# Crie este novo arquivo: agente_ferramentas.py

import os
from langchain_google_community.search import GoogleSearchAPIWrapper
import re

def consultar_iva_online(pergunta: str, openai_api_key: str):
    """
    Busca a alíquota padrão de IVA no Brasil online e aplica o cálculo se um valor for encontrado na pergunta.
    """
    print("🔎 Ativando a ferramenta de consulta de IVA...")

    # Configura a busca do Google
    # ATENÇÃO: Você precisa configurar uma API Key e um Custom Search Engine ID no Google Cloud
    # https://developers.google.com/custom-search/v1/overview
    os.environ["GCS_API_KEY"] = "SUA_GOOGLE_CLOUD_SEARCH_API_KEY"
    os.environ["GCS_CX"] = "SEU_CUSTOM_SEARCH_ENGINE_ID"
    search = GoogleSearchAPIWrapper()

    # Busca pela alíquota
    resultado_busca = search.run("valor atual alíquota padrão IVA Brasil 2025")
    print(f"🔍 Resultado da busca: {resultado_busca}")

    # Extrai o percentual do resultado da busca (exemplo simples, pode ser melhorado)
    match = re.search(r"(\d{1,2}(?:[.,]\d{1,2})?)%", resultado_busca)
    if not match:
        return "Não consegui encontrar a alíquota de IVA atual online."

    aliquota_str = match.group(1).replace(",", ".")
    aliquota = float(aliquota_str) / 100.0
    print(f"📊 Alíquota de IVA encontrada: {aliquota:.2%}")

    # Verifica se há um valor na pergunta para calcular
    valor_match = re.search(r"R\$\s*([\d.,]+)", pergunta)
    if valor_match:
        valor_str = valor_match.group(1).replace(".", "").replace(",", ".")
        valor = float(valor_str)
        iva_calculado = valor * aliquota
        return f"A alíquota de IVA encontrada foi de {aliquota:.2%}. O valor do IVA sobre R$ {valor:,.2f} é de R$ {iva_calculado:,.2f}."
    else:
        return f"A alíquota padrão de IVA encontrada online é de {aliquota:.2%}. Se quiser, me forneça um valor para eu calcular."
## 📜 Licença (MIT)

Este projeto é distribuído sob a **Licença MIT**, o que significa que você pode usar, copiar, modificar, mesclar, publicar e distribuir livremente, desde que mantenha o aviso de copyright original.

Para executar o Trabalho final, será necessário uma chave openai, ngrok e  gcs_api_key e gcs_cs. Utilize os seguintes comandos:

!git clone https://github.com/ameliamacedogithub/repositorionaoseremoseliminados

!pip install -U gdown langchain langchain-community langchain-openai chromadb openai tiktoken langchain-text-splitters streamlit langchain-openai langchain-google-community pyngrok chardet --quiet

!cp -r /content/repositorionaoseremoseliminados/"Projeto Final - Artefatos"/* /content/


destino_dir="/content/dados_nfe"
persist_dir="/content/chroma_nfe"

import os
from google.colab import userdata
# Pega a chave armazenada nos secrets do Colab
api_key = userdata.get("OPENAI_API_KEY")

# Injeta no ambiente para o LangChain reconhecer
os.environ["OPENAI_API_KEY"] = api_key
# Substitua "sua-chave" pela sua OpenAI API Key

import os
from google.colab import userdata
from pyngrok import ngrok

# 1. PEGA TODOS OS SECRETS AQUI NA CÉLULA
try:
    # Chaves da OpenAI e Google
    os.environ["OPENAI_API_KEY"] = userdata.get("OPENAI_API_KEY")
    os.environ["GCS_API_KEY"] = userdata.get("GCS_API_KEY")
    os.environ["GCS_CX"] = userdata.get("GCS_CX")

    # Chave do Ngrok
    authtoken = userdata.get('NGROK_AUTHTOKEN')
    ngrok.set_auth_token(authtoken)

    print("✅ Secrets carregados no ambiente.")

except Exception as e:
    print(f"❌ Erro ao carregar secrets: {e}")
    print("Verifique se todas as 4 chaves (OPENAI, GCS_API_KEY, GCS_CX, NGROK_AUTHTOKEN) estão salvas corretamente.")


# Mata qualquer túnel ngrok que já esteja rodando
ngrok.kill()

# Roda o app Streamlit em background
!nohup streamlit run agente_interface.py &> streamlit.log &

# Espera para o Streamlit iniciar
import time
print("Aguardando o Streamlit iniciar... ⏳")
time.sleep(5)

# Cria o túnel e mostra o link público (agora autenticado!)
public_url = ngrok.connect(8501)
print("=====================================================================================")
print(f"✅ SEU APLICATIVO ESTÁ NO AR! ACESSE AQUI: {public_url}")
print("=====================================================================================")

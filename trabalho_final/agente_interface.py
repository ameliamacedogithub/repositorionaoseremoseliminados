import streamlit as st
import os

from agente_download import baixar_e_extrair
from agente_dados import carregar_dados
from agente_roteador import agente_roteador

st.set_page_config(page_title="Sistema Inteligente de NF-e")

# Estado de controle
if "dados_carregados" not in st.session_state:
    st.session_state.dados_carregados = False

# Interface de configuração
st.sidebar.header("🔧 Configurações")

# Chave OpenAI
openai_api_key = st.sidebar.text_input("🔐 OpenAI API Key", type="password")

# Link do ZIP
url_zip = st.sidebar.text_input("📦 Link do arquivo ZIP (.csv)", "")

# Diretórios
destino_dir = st.sidebar.text_input("📂 Diretório para extração", "diretório")
persist_dir = st.sidebar.text_input("💾 Diretório do ChromaDB", "diretório")


# ✅ Define variável de ambiente para uso pelos agentes
if openai_api_key:
    os.environ["OPENAI_API_KEY"] = openai_api_key

# Botão de download e processamento
if st.sidebar.button("Baixar e processar dados"):
    if not url_zip.strip() or not openai_api_key.strip():
        st.sidebar.warning("Preencha a chave OpenAI e o link do arquivo.")
    else:
        try:
            with st.spinner("⬇️ Baixando e extraindo..."):
                baixar_e_extrair(url_zip, destino_dir)

            st.cache_resource.clear()
            st.session_state.dados_carregados = True
            st.success("✅ Arquivos baixados e extraídos.")
            st.rerun()
        except Exception as e:
            st.error(f"❌ Erro no download ou extração: {e}")
            st.stop()

# Cache do carregamento
@st.cache_resource(show_spinner="🔄 Carregando e indexando os dados...")
def carregar():
    return carregar_dados(destino_dir, persist_dir, openai_api_key)
    
# Interface principal
def main():
    st.title("Sistema Inteligente de NF-e")
     
    if not openai_api_key.strip():
        st.info("🔑 Informe sua OpenAI API Key no menu lateral.")
        return

    if not os.path.exists(destino_dir) or len([f for f in os.listdir(destino_dir) if f.endswith(".csv")]) != 2:
        st.info("📁 Aguardando o link com o arquivo .zip que contenha dois arquivos CSV.")
        return

    try:
        df, _ = carregar()
        st.session_state.dados_carregados = True
        st.success("📊 Dados carregados e indexados.")
    except Exception as e:
        st.error(f"❌ Erro ao carregar dados: {e}")
        return

    st.markdown("### ❓ Faça sua pergunta sobre as notas fiscais:")
    pergunta = st.text_input("Digite sua pergunta:")
    if st.button("Enviar"):
        if not pergunta.strip():
            st.warning("Digite uma pergunta válida.")
        else:
            resposta = agente_roteador(pergunta, df, persist_dir, openai_api_key)
            st.success("Resposta:")
            st.write(resposta)

if __name__ == "__main__":
    main()

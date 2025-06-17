# 🤖 Sistema Inteligente de Consulta a Notas Fiscais

Este projeto utiliza **agentes em Python** com interface via **Streamlit** para responder perguntas sobre notas fiscais eletrônicas (NF-e), extraídas de arquivos `.csv`. Ele utiliza **ChromaDB** como banco vetorial para busca semântica e **Pandas** para consultas analíticas.

---

## 🔧 Funcionalidades

- Interface interativa com Streamlit
- Download e extração automática de arquivo zipado do Google Drive
- Armazenamento vetorial com ChromaDB
- Respostas com base em:
  - 🔍 Similaridade semântica (produtos, empresas, destinatários)
  - 📊 Agregações analíticas (média, soma, contagem, máximo, mínimo)

---

## 🧠 Agentes

- `agente_interface.py`: Interface Streamlit para entrada do usuário
- `agente_download.py`: Faz download e extração do arquivo zip
- `agente_dados.py`: Carrega dados CSV e indexa no ChromaDB
- `agente_roteador.py`: Decide qual agente deve responder (semântico ou analítico)
- `agente_analitico.py`: Responde perguntas de análise de dados estruturados
- `agente_semantico.py`: Responde perguntas abertas com embeddings

---

## 🚀 Como executar localmente

### 1. Clone o repositório
```bash
git clone https://github.com/seu-usuario/seu-repo.git
cd seu-repo

### 2.Instale as dependências
```bash
pip install -r requirements.txt

### 3.Rode o sistema com Streamlit
```bash
streamlit run agente_interface.py

# Usa imagem base leve com Python
FROM python:3.11-slim

# Define diretório de trabalho
WORKDIR /app

# Copia os arquivos para dentro do container
COPY . .

# Instala dependências
RUN pip install --no-cache-dir -r requirements.txt

# Expõe a porta do Streamlit
EXPOSE 8501

# Comando para iniciar o app
CMD ["streamlit", "run", "agente_interface.py", "--server.port=8501", "--server.address=0.0.0.0"]

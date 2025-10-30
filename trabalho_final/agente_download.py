import os
import zipfile
import gdown

def baixar_e_extrair(url, destino_dir):
    os.makedirs(destino_dir, exist_ok=True)

    # Extrai ID do Google Drive
    file_id = url.split("/d/")[1].split("/")[0]
    gdown_url = f"https://drive.google.com/uc?id={file_id}"

    # Caminho local do arquivo ZIP
    caminho_zip = os.path.join(destino_dir, "arquivo.zip")

    print("⬇️ Baixando o arquivo ZIP...")
    gdown.download(gdown_url, caminho_zip, quiet=False)

    print("📦 Extraindo o conteúdo do ZIP...")
    with zipfile.ZipFile(caminho_zip, 'r') as zip_ref:
        zip_ref.extractall(destino_dir)

    # Remover o arquivo zip após a extração
    os.remove(caminho_zip)
    print("🧹 Arquivo ZIP removido após extração.")

    # Listar arquivos CSV resultantes
    arquivos_csv = [f for f in os.listdir(destino_dir) if f.endswith(".csv")]

    if len(arquivos_csv) != 2:
        raise ValueError(f"Erro: Esperado exatamente 2 arquivos CSV, mas foram encontrados {len(arquivos_csv)} em {destino_dir}")

    print(f"✅ Extração concluída. Foram encontrados {len(arquivos_csv)} arquivos CSV:")
    for f in arquivos_csv:
        print("-", f)

    return arquivos_csv  # pode retornar os nomes dos arquivos, se quiser usar depois

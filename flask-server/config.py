import os

# Caminho absoluto para o arquivo JSON da chave de serviço
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.getcwd(), "./credentials/stt_key.json") # Substitua pelo caminho correto
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS


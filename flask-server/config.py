import os

# Caminho absoluto para o arquivo JSON da chave de serviço
GOOGLE_APPLICATION_CREDENTIALS = os.path.join(os.getcwd(), "gerenciaderedes-463118-edbddcfc103f.json") # Substitua pelo caminho correto
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = GOOGLE_APPLICATION_CREDENTIALS

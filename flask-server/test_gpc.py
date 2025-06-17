from google.cloud import speech
import os
import config  # isso aplica o os.environ da key

def test_auth():
    try:
        client = speech.SpeechClient()
        # Testa uma chamada mínima: listar a configuração padrão
        print("✅ Autenticação bem-sucedida.")
        return True
    except Exception as e:
        print("❌ Falha na autenticação:")
        print(e)
        return False

if __name__ == "__main__":
    test_auth()

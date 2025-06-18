import os
import uuid
from werkzeug.datastructures import FileStorage
from utils.convert_to_wav import convert_to_wav

TEMP_DIR = os.path.join(os.getcwd(), "temp_audio")
os.makedirs(TEMP_DIR, exist_ok=True)

ALLOWED_EXTENSIONS = [".webm", ".wav", ".ogg"]

def process_audio_upload(file: FileStorage) -> dict:
    ext = os.path.splitext(file.filename)[1].lower()

    if ext not in ALLOWED_EXTENSIONS:
        return {
            "error": "Unsupported file type",
            "status": 415
        }

    filename = f"{uuid.uuid4()}{ext}"
    original_path = os.path.join(TEMP_DIR, filename)

    try:
        file.save(original_path)

        # converte se não for .wav
        if ext != ".wav":
            try:
                print("Original path:", original_path)
                converted_path = convert_to_wav(original_path)
                try:
                    print(f"Excluindo o arquivo: {original_path}")
                    os.remove(original_path)
                except Exception as e:
                    print(f"Erro ao excluir o arquivo: {str(e)}")
                return {
                    "message": "File received and converted",
                    "path": converted_path
                }
           
            except Exception as e:
                return {
                    "error": f"Erro ao converter para WAV: {str(e)}",
                    "status": 500
                }

        return {
            "message": "File received",
            "path": original_path
        }

    except Exception as e:
        return {
            "error": f"Failed to save file: {str(e)}",
            "status": 500
        }

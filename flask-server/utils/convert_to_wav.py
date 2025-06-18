import subprocess
import os

def convert_to_wav(input_path: str) -> str:
    """
    Converte o arquivo de áudio para formato WAV (mono, 16kHz, PCM)
    necessário para o reconhecimento da Google Cloud STT.
    Retorna o caminho do novo arquivo `.wav`.
    """
    base, _ = os.path.splitext(input_path)
    output_path = f"{base}.wav"

    try:
        subprocess.run([
            "ffmpeg", "-y",
            "-i", input_path,
            "-ac", "1",          # mono
            "-ar", "16000",      # 16 kHz
            output_path
        ], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        return output_path
    except subprocess.CalledProcessError:
        raise RuntimeError("Falha na conversão de áudio para WAV.")

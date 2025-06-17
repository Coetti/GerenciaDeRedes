import os
from google.cloud import speech
import io
import subprocess

def convert_to_wav(input_path: str) -> str:
    """
    Converte o arquivo de áudio para formato WAV (mono, 16kHz, PCM).
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

def transcribe_audio_google(wav_path: str) -> str:
    """
    Envia o arquivo wav para Google Speech-to-Text e retorna o texto transcrito.
    """
    client = speech.SpeechClient()

    with io.open(wav_path, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000,
        language_code="pt-BR"
    )

    response = client.recognize(config=config, audio=audio)

    transcripts = []
    for result in response.results:
        transcripts.append(result.alternatives[0].transcript)

    return " ".join(transcripts)

if __name__ == "__main__":
    # Caminho para o arquivo webm local
    webm_file = "test.webm"

    # Converte para wav
    wav_file = convert_to_wav(webm_file)

    # Transcreve com Google Speech-to-Text
    transcription = transcribe_audio_google(wav_file)

    print("Transcrição:")
    print(transcription)

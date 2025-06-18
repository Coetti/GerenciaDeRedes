import io
from google.cloud import speech

def transcribe_audio_google(filepath: str, language="pt-BR") -> dict:
    client = speech.SpeechClient()

    with io.open(filepath, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000, 
        language_code=language,
    )

    try:
        response = client.recognize(config=config, audio=audio)
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return {"text": transcript}
    except Exception as e:
        return {
            "error": f"Google STT failed: {str(e)}",
            "status": 500
        }

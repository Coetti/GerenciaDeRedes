from flask import request, jsonify
from services.audio_service import process_audio_upload
from services.speech_to_text_service import transcribe_audio_google
from services.dialogflow_service import detect_intent_text
from services.weather_service import fetch_current_weather
from services.calculator_service import calculator_service
import os


def handle_audio_upload(request):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    result = process_audio_upload(file)
    if "error" in result:
        return jsonify(result), result.get("status", 400)

    return jsonify(result), 200


def handle_audio_transcription(request):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    upload_result = process_audio_upload(file)
    if "error" in upload_result:
        return jsonify(upload_result), upload_result.get("status", 400)

    filepath = upload_result["path"]

    try:
        transcription = transcribe_audio_google(filepath)
        if "error" in transcription:
            return jsonify(transcription), transcription.get("status", 500)

        return jsonify({
            "message": "Success",
            "text": transcription["text"]
        })

    finally:
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao excluir o arquivo: {str(e)}")


def handle_audio_intent(request):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    upload_result = process_audio_upload(file)
    if "error" in upload_result:
        return jsonify(upload_result), upload_result.get("status", 400)

    filepath = upload_result["path"]

    try:
        transcription_result = transcribe_audio_google(filepath)
        if "error" in transcription_result:
            return jsonify(transcription_result), transcription_result.get("status", 500)

        transcribed_text = transcription_result["text"]
    finally:
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao excluir o arquivo: {str(e)}")

    dialogflow_response = detect_intent_text(transcribed_text)
    if "error" in dialogflow_response:
        return jsonify(dialogflow_response), dialogflow_response.get("status", 500)

    intent = dialogflow_response["intent"]

    result = (
        fetch_current_weather(dialogflow_response)
        if intent == "weather"
        else calculator_service(dialogflow_response)
    )

    return jsonify({
        "message": "Success",
        "transcription": transcribed_text,
        "intent": intent,
        "parameters": dialogflow_response["parameters"],
        "response_text": dialogflow_response["response_text"],
        "result": result
    })

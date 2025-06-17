from flask import Blueprint, request, jsonify
from services.audio_service import process_audio_upload
from services.speech_to_text_service import transcribe_audio_google
from services.dialogflow_service import detect_intent_text  # novo
import os
from services.calculator_service import calculate_expression

audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/upload-audio", methods=["POST"])
def upload_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    result = process_audio_upload(file)

    if "error" in result:
        return jsonify(result), result.get("status", 400)

    return jsonify(result), 200




@audio_bp.route("/upload-and-transcribe", methods=["POST"])
def upload_and_transcribe_gcloud():
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
            print(f"Excluindo o arquivo: {filepath}")
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao excluir o arquivo: {str(e)}")   


@audio_bp.route("/upload-and-transcribe-intent", methods=["POST"])
def upload_and_transcribe_intent_gcloud():
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

        dialogflow_response = detect_intent_text(transcribed_text)

        if "error" in dialogflow_response:
            return jsonify(dialogflow_response), dialogflow_response.get("status", 500)
        
        if dialogflow_response["intent"] == "soma":
            number1 = float(dialogflow_response["parameters"]["number1"])
            number2 = float(dialogflow_response["parameters"]["number2"])
            result = calculate_expression("+", number1, number2)

        return jsonify({
            "message": "Success",
            "transcription": transcribed_text,
            "intent": dialogflow_response["intent"],
            "parameters": dialogflow_response["parameters"],
            "response_text": dialogflow_response["response_text"],
            "result": result
        })

    finally:
        try:
            print(f"Excluindo o arquivo: {filepath}")
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao excluir o arquivo: {str(e)}")
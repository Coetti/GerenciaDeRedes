from flask import Blueprint, request, jsonify
from services.audio_service import process_audio_upload
from services.speech_service import transcribe_audio_google

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




@audio_bp.route("/upload-and-transcribe-gcloud", methods=["POST"])
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
    transcription = transcribe_audio_google(filepath)

    if "error" in transcription:
        return jsonify(transcription), transcription.get("status", 500)

    return jsonify({
        "message": "Success",
        "text": transcription["text"]
    })

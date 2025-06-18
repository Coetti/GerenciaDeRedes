from flask import Blueprint, request, jsonify
from controllers.audio_controller import (
    handle_audio_upload,
    handle_audio_transcription,
    handle_audio_intent
)

audio_bp = Blueprint("audio", __name__)

@audio_bp.route("/upload-audio", methods=["POST"])
def upload_audio():
    return handle_audio_upload(request)

@audio_bp.route("/upload-and-transcribe", methods=["POST"])
def upload_and_transcribe_gcloud():
    return handle_audio_transcription(request)

@audio_bp.route("/upload-and-transcribe-intent", methods=["POST"])
def upload_and_transcribe_intent_gcloud():
    return handle_audio_intent(request)

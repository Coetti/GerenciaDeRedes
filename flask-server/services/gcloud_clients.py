import os
from google.oauth2 import service_account
from google.cloud import speech
from google.cloud import dialogflow_v2 as dialogflow

STT_CREDENTIALS_PATH = os.path.join(os.getcwd(), "credentials/stt_key.json")
DIALOGFLOW_CREDENTIALS_PATH = os.path.join(os.getcwd(), "credentials/dialogflow_key.json")


stt_credentials = service_account.Credentials.from_service_account_file(STT_CREDENTIALS_PATH)
dialogflow_credentials = service_account.Credentials.from_service_account_file(DIALOGFLOW_CREDENTIALS_PATH)

def get_speech_client():
    return speech.SpeechClient(credentials=stt_credentials)

def get_dialogflow_client():
    return dialogflow.SessionsClient(credentials=dialogflow_credentials)

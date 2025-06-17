from google.cloud import dialogflow_v2 as dialogflow
from services.gcloud_clients import get_dialogflow_client
import uuid

PROJECT_ID = "gerenciaderedes-463118"  # ajuste aqui

def detect_intent_text(text: str, language_code="pt-BR") -> dict:
    client = get_dialogflow_client()
    session_id = str(uuid.uuid4())
    session = client.session_path(PROJECT_ID, session_id)

    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    try:
        response = client.detect_intent(request={"session": session, "query_input": query_input})
        return {
            "intent": response.query_result.intent.display_name,
            "parameters": dict(response.query_result.parameters),
            "response_text": response.query_result.fulfillment_text
        }
    except Exception as e:
        return {"error": f"Dialogflow error: {str(e)}", "status": 500}

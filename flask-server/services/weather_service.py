def fetch_current_weather(dialogflow_response):
    if dialogflow_response["parameters"]["city"] == "São Paulo":
        return "Clima em São Paulo"
    elif dialogflow_response["parameters"]["city"] == "Poços de Caldas":
        return "Clima em Poços de Caldas"
    elif dialogflow_response["parameters"]["city"] == "Rio de Janeiro":
        return "Clima em Rio de Janeiro"
    elif dialogflow_response["parameters"]["city"] == "Divinolândia":
        return "Clima em Divinolândia"
    return "Não sei o clima em " + dialogflow_response["parameters"]["city"]
import os
import requests
from utils.get_city_location_key import get_city_location_key
from utils.map_weather_api_response import map_weather_api_response

def fetch_current_weather(dialogflow_response):
    locationKey = ""
    if dialogflow_response["parameters"]["city"] == "São Paulo":
        locationKey = get_city_location_key("São Paulo")
        
    elif dialogflow_response["parameters"]["city"] == "Poços de Caldas":
        locationKey = get_city_location_key("Poços de Caldas")
        
    elif dialogflow_response["parameters"]["city"] == "Rio de Janeiro":
        locationKey = get_city_location_key("Rio de Janeiro")
        
    elif dialogflow_response["parameters"]["city"] == "Divinolândia":
        locationKey = get_city_location_key("Divinolândia")
    
    if locationKey == "":
        return "Nao sei o clima em " + dialogflow_response["parameters"]["city"]
    else:
        try:
            current_weather = get_daily_forecast(locationKey)
        except Exception as e:
            print(e)
        return {
                "city": dialogflow_response["parameters"]["city"],
                "weather": current_weather }

API_KEY = "TjbaDwToaC88wn6RxMKvv3OlZ0tRLzIA"
BASE_URL = "http://dataservice.accuweather.com"

def get_daily_forecast(locationKey: str) -> dict:
    url = f"{BASE_URL}/forecasts/v1/daily/1day/{locationKey}"
    params = {
        "apikey": API_KEY,
        "language": "pt-br",
        "details": "true",
        "metric": "true"
    }

    response = requests.get(url, params=params)
    mappedResponse = map_weather_api_response(response.json())
    if response.status_code != 200:
        raise Exception(f"Erro ao buscar clima atual: {response.text}")

    return mappedResponse
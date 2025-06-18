from typing import Dict

def map_weather_api_response(responseJSON: Dict) -> Dict:
    forecast = responseJSON.get("DailyForecasts", [])[0]  # Assume sempre 1 item

    data = forecast.get("Date", "").split("T")[0]
    temp_min = forecast["Temperature"]["Minimum"]["Value"]
    temp_max = forecast["Temperature"]["Maximum"]["Value"]

    chuva_dia = forecast["Day"].get("Rain", {}).get("Value", 0.0)
    chuva_noite = forecast["Night"].get("Rain", {}).get("Value", 0.0)
    quantidade_chuva = chuva_dia + chuva_noite

    precip_prob = max(
        forecast["Day"].get("PrecipitationProbability", 0),
        forecast["Night"].get("PrecipitationProbability", 0)
    )
    previsao_chuva = precip_prob > 0

    return {
        "data": data,
        "temperatura_min": temp_min,
        "temperatura_max": temp_max,
        "previsao_chuva": previsao_chuva,
        "quantidade_chuva_mm": quantidade_chuva
    }

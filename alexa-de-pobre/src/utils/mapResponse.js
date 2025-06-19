export function mapResponse(response) {
  return {
    message: "Success",
    question: response.transcription,
    answer:
      response.intent === "weather"
        ? `Atualmente na cidade de ${response.result.city}, a temperatura máxima será de ${response.result.weather.temperatura_max} graus celsius e a temperatura minima sera de ${response.result.weather.temperatura_min} graus celsius. Deve chover ${response.result.weather.quantidade_chuva_mm}mm!`
        : response.result,
    questionType:
      response.intent === "add" ||
      response.intent === "sub" ||
      response.intent === "mul" ||
      response.intent === "div"
        ? "calculator"
        : "weather",
  };
}

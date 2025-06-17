def calculate_expression(operator: str, number1: float, number2: float) -> str:
  try:
        if operator == "+":
            result = number1 + number2
            return "O resultado da soma de " + str(number1) + " e " + str(number2) + " eh: " + str(result)
        elif operator == "-":
           result = number1 - number2
           return "O resultado da subtracao de " + str(number1) + " e " + str(number2) + " eh: " + str(result)
        elif operator == "*":
           result = number1 * number2
           return "O resultado da multiplicacao de " + str(number1) + " e " + str(number2) + " eh: " + str(result)
        elif operator == "/":
           result = number1 / number2
           return "O resultado da divisao de " + str(number1) + " e " + str(number2) + " eh: " + str(result)
  except Exception as e:
    return {"error": f"Erro ao calcular: {str(e)}", "status": 500}  
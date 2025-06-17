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


def calculator_service(dialogflow_response) -> str:
   try:
      if dialogflow_response["intent"] == "add":
         number1 = float(dialogflow_response["parameters"]["number1"])
         number2 = float(dialogflow_response["parameters"]["number2"])
         result = calculate_expression("+", number1, number2)
      elif dialogflow_response["intent"] == "sub":
         number1 = float(dialogflow_response["parameters"]["number1"])
         number2 = float(dialogflow_response["parameters"]["number2"])
         result = calculate_expression("-", number1, number2)    
      elif dialogflow_response["intent"] == "mult":
         number1 = float(dialogflow_response["parameters"]["number1"])
         number2 = float(dialogflow_response["parameters"]["number2"])
         result = calculate_expression("*", number1, number2)
      elif dialogflow_response["intent"] == "div":
         number1 = float(dialogflow_response["parameters"]["number1"])
         number2 = float(dialogflow_response["parameters"]["number2"])
         if number1 == 0 or number2 == 0:
            result = "Nao eh possivel dividir por zero"
            return
         result = calculate_expression("/", number1, number2)
      else:
         result = "Operacao nao suportada."
   except Exception as e:
      print(e)
      result = "Erro ao calcular."

   return result  
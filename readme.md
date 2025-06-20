# Documentação dos Serviços - Trabalho Acadêmico

## Informações Gerais

**Disciplina:** Gerência de Redes  

**Professor:** Harison  

**Integrantes:** Gabriel Coetti, Lucas Florentino

**Data:** 20/06/2025

## Visão Geral do Projeto

Este projeto demonstra uma implementação básica de um sistema na arquitetura de `cliente-servidor`. Ele utiliza dois servidores backend `Flask` e `Node`, além de uma interface em `React`, juntamento com serviços do `Google Cloud` (`Speech-to-Text API` e `DialogFlow ES API`) para processar perguntas de áudio em linguagem natural e exibir respostas gráficas.

---

### Objetivo

O trabalho visou introduzir os alunos do 6° período do curso de Ciência da Computação - PUCMINAS Campus Poços de Caldas dessa arquitetura popular nos sistemas modernos, onde podemos ter diversos serviços isolados, mas que se comunicam através de APIs REST e protocolo HTTP/HTTPS para cooperarem por um objetivo comum. Nosso projeto foi uma tentativa de reproduzir uma versão mínima do kit de processamento de linguagem natural, inspirado no dispositivo 'Alexa', para que através de uma interface web simples, o usuário possa se comunicar por áudio, realizando uma pergunta (e.g. perguntar o clima de sua cidade), e receber uma resposta gráfica. Devido ao curto prazo de tempo para desenvolvimento, o sistema implementa uma versão muito reduzida de funcionalidades, que estão listadas abaixo.

- **Calcular a SOMA de dois números.**

  Exemplo de pergunta aceita: `Qual a soma de 6 e 4?`

- **Calcular a SUBTRAÇÃO de dois números.**

  Exemplo de pergunta aceita: `Qual a subtração de 10 e 3?`

- **Calcular a MULTIPLICAÇÃO de dois números.**

  Exemplo de pergunta aceita: `Qual a multiplicação de 7 e 5?`

- **Calcular a DIVISÃO de dois números.**

  Exemplo de pergunta aceita: `Qual a divisão de 20 por 4?`

- **Obter a previsão do tempo do dia atual.**

  Exemplo de pergunta aceita: `Qual a previsão do tempo em Poços de Caldas?`

  ***OBS**: O sistema aceita apenas as cidades de Divinolândia-SP, Poços de Caldas-MG, São Paulo-SP e Rio de Janeiro-RJ*
  
---

### Arquitetura

A arquitetura proposta representa um cenário comum do desenvolvimento web, onde utilizamos um `cliente-servidor` com `React` para o frontend e `Node/Express` para o backend, mas alido ao serviço Node, temos outros servidores de processamento, como o `Flask` para executar tarefas assíncronas, e principalmente tarefas ligadas a machine learning e/ou inteligência artificial, pela facilidade de integração aos serviços corriqueiros oferecida pelas milhares de bibliotecas Python. Abaixo podemos ver uma descrição básica da função principal de cada componente e um fluxograma demonstrando a arquitetura

- **Backend Node.js:** [Função principal - Receber a requisição do frontend e servir como proxy de acesso ao serviço de processamento do servidor Flask]

- **Backend Flask:** [Função principal - Transcrever o áudio e obter a intenção do usuário para selecionar o serviço adequado de resposta]

- **Frontend React:** [Função principal - Permitir o usuário enviar suas perguntas por áudio e enviar a requisição ao proxy Node]
  
- **Comunicação:** [Os serviços se comunicam através de **APIs REST** utilizando o protocolo **HTTP**]
  
![PythonFlask](https://github.com/user-attachments/assets/cdf190ac-b10a-467f-9681-ff00f3ea97c2)

---

## Serviço Node.js

### Descrição

Este serviço age como um proxy para acesso ao serviço de processamento hospedado no servidor Flask, através de uma API REST, ele aceita requisições provindas do client WEB em React e as encaminha para o serviço em Flask através de uma requisição HTTP.

### Tecnologias Utilizadas

- **Node.js** - Engine por trás do funcionamento do serviço

- **Express.js** - Framework para a criação rápida de servidores HTTP/APIs REST

- **Multer** - Para processamento de requisições contendo **media files**

### Arquivo Principal

- `server.js`: Contém toda a lógica do servidor Node.js

- `package.json`: Dependências e scripts do projeto

### Funcionalidades Principais

#### 1. Encaminhamentos de Arquivo de Áudio

**Descrição:** Esta funcionalidade permite receber um arquivo de áudio através de uma requisição `multipart/form-data` e o encaminha para um serviço externo de processamento, atuando como um proxy. A resposta do serviço de destino é então retornada ao cliente original.

**Endpoint:** `POST /upload-audio`  

**Parâmetros:**

- `param1`: A requisição deve ter o `Content-Type` de `multiport/form-data`.
- `file`: O arquivo de áudio a ser processado (ex: `.webm`). Este é o único campo esperado no corpo do formulário.
  

**Exemplo de uso:**

- Este exemplo mostra como um cliente (outro serviço, um site, etc.) pode chamar esta API usando `axios` em Node.js.

```javascript

const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

async function enviarAudioParaProcessamento(caminhoDoArquivo) {
  try {
    const formData = new FormData();
    formData.append('file', fs.createReadStream(caminhoDoArquivo));
    const urlDoServidor = 'http://localhost:3000/upload-audio';

    const response = await axios.post(urlDoServidor, formData, {
      headers: { ...formData.getHeaders() }
    });
    console.log('Resposta do servidor:', response.data);
  } catch (error) {
    console.error('Erro ao enviar o áudio:', error.message);
  }
}

enviarAudioParaProcessamento('./meu-audio-de-teste.webm');

```

**Detalhes da Implementação no Servidor:**

- O trecho de código abaixo mostra como esta rota está implementada internamente no servidor Express.
![Image](https://github.com/user-attachments/assets/690df9fa-b3c3-4bdc-bfe4-74696807b290)

**Resposta de Sucesso no Postman**
- No exemplo abaixo, mostra a resposta da requisição.

![Image](https://github.com/user-attachments/assets/f10ff7b3-391b-487d-ae2c-f58c0ef89bfe)

- O **`Status: 500 Internal Server Error`**, significa que o servidor (porta `3000`) recebeu o áudio do Postman com sucesso, mas **falhou ao tentar se comunicar com o servidor de destino** na rota `http://localhost:5000/upload-and-transcribe-intent`. Mas isso antes dos ajustes finais, sendo funcional após as aplicações adiante.
- O corpo da resposta (`Body`), mostrando o JSON que foi retornado pelo serviço de destino (`localhost:5000`).
### Como Executar

#### Pré-requisitos

- Node.js versão 18.x ou superior.
- npm: (geralmente vem instalado com o Node.js).
- Serviço de destino: Um outro servidor deve estar rodando em `http://localhost:5000` com a rota `POST /upload-and-transcribe-intent` para que este projeto possa funcionar corretamente.

#### Instalação

1. Clone o repositório para sua máquina local:
```bash

git clone https://github.com/Coetti/GerenciaDeRedes.git

```

2. Navegue até o diretório do projeto:
```bash

cd node-server

```

3. Instale as dependências necessárias:
  ```bash

npm install

```

#### Execução

1. Para iniciar o servidor, execute o seguinte comando no terminal:
```bash

node src/server.js

```

2. Você deverá ver a seguinte mensagem, indicando que o servidor está pronto para receber requisições:
![Image](https://github.com/user-attachments/assets/e98fcfcb-38b1-4395-b327-52efa21438c2)
  
#### Configuração

- Porta padrão: O servidor roda na porta `3000`. Este valor está definido na variável `PORT` dentro do arquivo `src/server.js`.
- Variáveis de ambiente necessárias: Atualmente, este serviço não requer varíaveis de de ambiente (`.env`).
- `DATABASE_URL`: O endereço para o qual o áudio é encaminhado está definido na variável `destinationUrl` dentro do arquivo `src/server.js`.

  

---

  

## Serviço Flask

### Descrição

Serviço responsável por receber áudios contendo perguntas, transcrevê-los em texto por meio de uma API externa, extrair a intenção do usuário e retornar uma resposta adequada. Atua como um componente de edge computing, processando e respondendo localmente às solicitações dos usuários.


### Tecnologias Utilizadas

- **Python 3.x:** Motor por trás da execução do serviço
- **Flask:** Framework para implementação rápida de servidores HTTP/APIs REST.
- **FFmpeg:** Utilitário disponível para `Windows/Linux` para o processamento e conversão de arquivos de Media.
- **Speech-to-Text API:** Serviço em Cloud oferecido pelo Google para o processamento de linguagem natural em áudio para texto.
- **DialogFlow ES API:** Serviço em Cloud também oferecido pelo Google para o processamento de textos a fim de extrair a intenção e parâmetros através da configuração de agentes.
  

### Funcionalidades Principais

#### 1. Rota par transcrever e responder uma pergunta de áudio.

**Descrição:** Rota REST de método POST que recebe um áudio em formato `.ogg`, `.webm` ou `.wav` 

**Endpoint:** `POST /upload-and-transcribe-intent`  

**Parâmetros:**

- `param1`: A requisição deve ter o `Content-Type` de `multiport/form-data`.

- `file`: O arquivo de áudio a ser processado (ex: `.webm`). Este é o único campo esperado no corpo do formulário.

**Trecho do código:**
```python
@audio_bp.route("/upload-and-transcribe-intent", methods=["POST"])
def upload_and_transcribe_intent_gcloud():
    return handle_audio_intent(request)
```

#### 2. Controller 

**Descrição:** Controller que orquestra a exucação dos serviços que processam a requisição e devolve a resposta.

**Trecho do código:**
```python
def handle_audio_intent(request):
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400
    print("request.files:", request.files)
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    upload_result = process_audio_upload(file)
    if "error" in upload_result:
        return jsonify(upload_result), upload_result.get("status", 400)

    filepath = upload_result["path"]

    try:
        transcription_result = transcribe_audio_google(filepath)
        if "error" in transcription_result:
            return jsonify(transcription_result), transcription_result.get("status", 500)

        transcribed_text = transcription_result["text"]
    finally:
        try:
            os.remove(filepath)
        except Exception as e:
            print(f"Erro ao excluir o arquivo: {str(e)}")

    dialogflow_response = detect_intent_text(transcribed_text)
    if "error" in dialogflow_response:
        return jsonify(dialogflow_response), dialogflow_response.get("status", 500)

    intent = dialogflow_response["intent"]

    result = (
        fetch_current_weather(dialogflow_response)
        if intent == "weather"
        else calculator_service(dialogflow_response)
    )

    return jsonify({
        "message": "Success",
        "transcription": transcribed_text,
        "intent": intent,
        "parameters": dialogflow_response["parameters"],
        "response_text": dialogflow_response["response_text"],
        "result": result
    })
```

O Controller orquestra a chamada de serviços com a seguinte lógica:

1. O controller verifica se a requisição possui um arquivo de key: `file`, então prossegue ou retorna um erro **HTTP 400**.
2. Então passa o arquivo ao serviço `process_audio_upload` que é responsável por utilizar o `FFmpeg` para converter o audio, que pode estar nos formatos MIME citados anteriormente, para o formato ``.wav 16K``, que é o formato esperado pelo serviço **Speech-To-Text**.
3. Com o áudio convertido, então inicia um `try-catch` invocando o serviço `transcribe_audio_google(filepath)` que irá acessar o serviço do Google e obter a transcrição do áudio em formato de texto, em caso de erro, uma resposta `HTTP 500` será retornada. Por fim, o `try-catch` executa a remoção do arquivo temporário criado.
4. Então o serviço **DialogFlow** para detecção de **intent** (i.e. A intenção do usuário) é executado, onde o texto da transcrição será enviado como parâmetro da função `detect_intent_text(transcribed_text)`.
5. Por fim a resposta obtida pelo serviço do **DialogFlow** é retornada ao serviço Node, em formato `JSON` com os seguintes atributos:
   
```python
   return jsonify({
        "message": "Success",
        "transcription": transcribed_text,
        "intent": intent,
        "parameters": dialogflow_response["parameters"],
        "response_text": dialogflow_response["response_text"],
        "result": result
    })
```

#### 3. Serviço de Transcrição de Áudio 'Speech-to-Text'.

**Descrição:** Serviço que utiliza a API disponibilizada pelo **'Google Cloud'** para transcrever um áudio em texto.

**Trecho do código:**
```python
def transcribe_audio_google(filepath: str, language="pt-BR") -> dict:
    client = get_speech_client()

    with io.open(filepath, "rb") as audio_file:
        content = audio_file.read()

    audio = speech.RecognitionAudio(content=content)

    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        sample_rate_hertz=16000, 
        language_code=language,
    )

    try:
        response = client.recognize(config=config, audio=audio)
        transcript = " ".join([result.alternatives[0].transcript for result in response.results])
        return {"text": transcript}
    except Exception as e:
        return {
            "error": f"Google STT failed: {str(e)}",
            "status": 500
        }
```

Após obter o client para a API externa, o código aguarda a execução da transcrição e devolve o texto ou um erro `HTTP 500`

#### 4. Serviço de Reconhecimento de Intent `DialogFlow ES`.

**Descrição:** Serviço que utiliza a API disponibilizada pelo **'Google Cloud'** para reconhecer a intenção do usuário e devolver uma resposta formatada.

**Trecho do código:**
```python
PROJECT_ID = "gerenciaderedes-463118"

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
```

Após obter o client para a API externa, o código aguarda a execução do reconhecimento pelo agente e então devolve uma resposta formatada conforme o trecho abaixo ou um erro `HTTP 500`. 
```python
return {
            "intent": response.query_result.intent.display_name,
            "parameters": dict(response.query_result.parameters),
            "response_text": response.query_result.fulfillment_text
        }`
```

#### 5. Serviço de Calculadora.

**Descrição:** Uma implementação de uma calculadora para as 4 operações matemáticas básicas, a função espera receber um operador e dois números como parâmetros, mas para obter os parâmetros, primeiro é necessário extrai-los da resposta do **DialogFlow**.

**Trecho do código:**

Extrai os parâmetros e chama a função de calculo:

```python
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
      elif dialogflow_response["intent"] == "mul":
         number1 = float(dialogflow_response["parameters"]["number1"])
         number2 = float(dialogflow_response["parameters"]["number2"])
         result = calculate_expression("*", number1, number2)
      elif dialogflow_response["intent"] == "div":
         number1 = float(dialogflow_response["parameters"]["number1"])
         number2 = float(dialogflow_response["parameters"]["number2"])
         if number1 == 0 or number2 == 0:
            result = "Nao eh possivel dividir por zero"
            return result
         result = calculate_expression("/", number1, number2)
      else:
         result = "Operacao nao suportada."
   except Exception as e:
      print(e)
      result = "Erro ao calcular."

   return result
```

#### 6. Serviço de Obtenção da Previsão do Tempo através da API **AccuWeather**.

**Descrição:** Serviço que utiliza a API gratuita **AccuWeather** para obter a previsão do tempo de uma localidade. Como a API depende de um parâmetro `locationKey`, que é um `ID` para a cidade no sistema externo, foi necessário mapear algumas cidades e então selecionar através do parâmetro obtido pelo **DialogFlow**.

**Trecho do código:**

Extração do parâmetro e obtenção da `locationKey`.
```python
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
```

Chamada a API externa **AccuWeather** e mapeamento da resposta obtida (filtragem dos parâmetros irrelavantes).
```python
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
```
#### 7. Exemplos de respostas HTTPs de sucesso, visualizada no Postman.

- **Pergunta:** `Qual o clima em Poços de Caldas?`

Resposta:

```JSON
{
    "intent": "weather",
    "message": "Success",
    "parameters": {
        "city": "Poços de Caldas"
    },
    "response_text": "intent:weather:parameters[city:Poços de Caldas]",
    "result": {
        "city": "Poços de Caldas",
        "weather": {
            "data": "2025-06-20",
            "previsao_chuva": true,
            "quantidade_chuva_mm": 0.0,
            "temperatura_max": 22.7,
            "temperatura_min": 9.8
        }
    },
    "transcription": "Qual o clima em Poços de Caldas"
}
```
- **Pergunta:** `Qual é o valor da divisão de 40 por 5?`

Resposta:

```JSON
{
    "intent": "div",
    "message": "Success",
    "parameters": {
        "number1": 40.0,
        "number2": 5.0
    },
    "response_text": "intent:div:parameters[40&5]",
    "result": "O resultado da divisao de 40.0 e 5.0 eh: 8.0",
    "transcription": "de vida 40 por 5"
}
```

- **Pergunta:** `Quanto é a subtração entre 10 e 4?`

Resposta:

```JSON
{
    "intent": "sub",
    "message": "Success",
    "parameters": {
        "number1": 10.0,
        "number2": 4.0
    },
    "response_text": "intent:sub:parameters[10&4]",
    "result": "O resultado da subtracao de 10.0 e 4.0 eh: 6.0",
    "transcription": "Quanto é a subtração entre 10 e 4"
}
```
### Como Executar

#### Pré-requisitos

A execução do servidor Flask exige um grande Boilerplat devido as dependências externas e natureza da execução do Python. Abaixo temos um tutorial de execução, mas tenha em mente que para o serviço funcionar será necessário setar suas próprias credenciais dos serviços externos, sendo necessário uma **IAM-Service Account** para cada serviço do **Google Cloud**, exportar suas credenciais no formato `JSON` e então salva-las no diretório `/src/credentials` com os nomes `stt_key.json` para as credenciais do serviço **Speech-to-Text** e `dialogflow_key.json` para o serviço **DialogFlow**.

_**OBS: As credenciais não foram incluídas no repositório devido ao mesmo estar listado como público. Essas credenciais permitem uso praticamente ilimitado dos serviços, o que pode acarretar em custos após exceder o crédito gratuito**_

Também será necessário criar sua conta na API de clima [AccuWeather]([URL](https://developer.accuweather.com) e obter sua `API Key` que deve ser colocada no arquivo de variáveis de ambiente `.env` com a Key: `ACCUWEATHER_API_KEY`.

Para o serviço do **DialogFlow** foi necessário configurar agentes para a detecção dos intents das perguntas. Podemos ver um exemplo de agente na **Captura de Tela** abaixo.
![photo-collage png](https://github.com/user-attachments/assets/887302f4-2841-4053-9b76-8a3f548822a0)

#### Lista de requisitos

1. Python 3.x
2. Pip
3. FFmpeg para Windows [FFmpeg](https://www.gyan.dev/ffmpeg/builds/)
4. Google Cloud Speech-to-Text [Speech-to-Text](https://cloud.google.com/speech-to-text)
5. Google Cloud DialogFlow ES [DialogFlow](https://dialogflow.cloud.google.com)
6. API AccuWeather [AccuWeather](https://developer.accuweather.com)

#### Instalação

1. Clone o repositório para sua máquina local:
```bash
git clone https://github.com/Coetti/GerenciaDeRedes.git
```
2. Navegue até o diretório do projeto:
```bash
cd flask-server
```
3.  Ative o ambiente virtual executando o script
 ```bash
  /venv/Scripts/activate
```  
4. Instale as dependências necessárias:
```bash
pip install -r ./requirements.txt
```

#### Execução

```bash
flask run
```

#### Configuração

- Porta padrão: 5000

- Variáveis de ambiente necessárias:

  - `FLASK_ENV`: development

  - `APP_KEY`: entry-point `app.py`

---


### Exemplo de Integração

```javascript

// Exemplo de como Node.js chama o Flask

const response = await fetch('http://localhost:5000/api/process', {

  method: 'POST',

  headers: { 'Content-Type': 'application/json' },

  body: JSON.stringify(data)

});

```

---

## Interface WEB React

A interface **React** não é necessária, podendo ser substituida pelo `Postman`, mas a intuito de melhorar a experiência e facilitar a demonstração, foi implementada uma interface simples que permite a captura de áudio e realiza requisições ao serviço proxy do **Node**, para então exibir as respostas em Cards visuais. A captura de tela abaixo demonstra a interface em funcioamento.
![5](https://github.com/user-attachments/assets/3c27de65-1690-4842-b42d-72c44cb7570b)

---

## Conclusões

O trabalho foi importante para praticarmos a implementação de código em diferentes linguagens/frameworks, além de reforçar conceitos da operação de sistemas `cliente-servidor`. Também pudemos observar como funcionam as `API REST` e o funcionamento de chamadas do tipo `assíncronas`. Cada vez mais a WEB funciona em sistemas com arquiteturas parecidas com esta, com servidores de proxy e microsserviços isolados, que através de políticas de filas e load balance, conseguem oferecer uma experiência satisfatória aos usuários e permitem uma escalabilidade muito superior a aplicativos monólitos. 

Além disso, este trabalho nos permitiu utilizar serviços de IA e Machine Learning disponibilizados pela plataforma do **Google Cloud**, além da integração a uma API externa **AccuWeather**, ambas são experiências que agregaram muito no nosso portfólio de ferramentas que já tivemos contato, podendo utiliza-las em trabalhos futuros e MVPs de sistemas.

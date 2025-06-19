import "./App.css";
import api from "./api";
import ResponseCard from "./components/ResponseCard";
import AudioButton from "./components/AudioButton";
import { useState } from "react";
import { mapResponse } from "./utils/mapResponse";

function App() {
  const [questions, setQuestions] = useState([]);

  const handleAudioBlob = async (audioBlob) => {
    const formData = new FormData();
    formData.append("file", audioBlob, "gravacao.webm");

    try {
      const response = await api.post("/upload-audio", formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      });
      const mappedResponse = mapResponse(response.data);
      setQuestions((prevQuestions) => [...prevQuestions, mappedResponse]);
    } catch (error) {
      console.error("Erro no envio do áudio:", error);
    }
  };

  return (
    <div className="page-container">
      <div className="main-content">
        <h1 className="title">Alexa de Pobre</h1>
        <div className="response-list">
          {questions.map((question, index) => (
            <ResponseCard key={index} data={question} />
          ))}
        </div>

        <AudioButton onAudioReady={handleAudioBlob} />
      </div>
    </div>
  );
}

export default App;

import { useEffect, useRef, useState } from "react";
import "../styles/AudioButton.css";
import { AiFillAudio, AiOutlineAudioMuted } from "react-icons/ai";

const AudioButton = ({ onAudioReady }) => {
  const [isRecording, setIsRecording] = useState(false);
  const mediaRecorderRef = useRef(null);
  const audioChunksRef = useRef([]);

  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then((stream) => {
        const recorder = new MediaRecorder(stream);

        recorder.ondataavailable = (event) => {
          if (event.data.size > 0) {
            audioChunksRef.current.push(event.data);
          }
        };

        recorder.onstop = () => {
          const audioBlob = new Blob(audioChunksRef.current, {
            type: "audio/webm",
          });
          audioChunksRef.current = [];
          onAudioReady(audioBlob);
        };

        mediaRecorderRef.current = recorder;
      })
      .catch((err) => {
        console.error("Erro ao acessar microfone:", err);
      });
  }, [onAudioReady]);

  const startRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "inactive"
    ) {
      audioChunksRef.current = [];
      mediaRecorderRef.current.start();
      setIsRecording(true);
    }
  };

  const stopRecording = () => {
    if (
      mediaRecorderRef.current &&
      mediaRecorderRef.current.state === "recording"
    ) {
      mediaRecorderRef.current.stop();
      setIsRecording(false);
    }
  };

  return (
    <div
      className={`button-container ${isRecording ? "is-recording" : ""}`}
      onMouseDown={startRecording}
      onMouseUp={stopRecording}
      onMouseLeave={stopRecording}
    >
      {isRecording ? (
        <>
          <div className="recording-text">Gravando...</div>
          <AiOutlineAudioMuted />
        </>
      ) : (
        <>
          <AiFillAudio />
        </>
      )}
    </div>
  );
};

export default AudioButton;

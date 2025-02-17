import React, { useState, useRef, useEffect } from "react";
import "./styles/SpeechRecorder.css";  // Import the CSS file

const SpeechRecorder = ({ onSpeechResult }) => {
  const [recording, setRecording] = useState(false);
  const [hasPermission, setHasPermission] = useState(null);
  const [isSupported, setIsSupported] = useState(true);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const streamRef = useRef(null);

  useEffect(() => {
    if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
      setIsSupported(false);
      return;
    }

    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(() => setHasPermission(true))
      .catch(() => setHasPermission(false));
  }, []);

  const toggleRecording = async () => {
    if (!isSupported || hasPermission === false) return;
    if (!recording) {
      try {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        streamRef.current = stream;
        const recorder = new MediaRecorder(stream);
        let chunks = [];

        recorder.ondataavailable = (event) => chunks.push(event.data);
        recorder.onstop = () => {
          const audioBlob = new Blob(chunks, { type: "audio/wav" });
          sendAudioToServer(audioBlob);
        };

        recorder.start();
        setMediaRecorder(recorder);
        setRecording(true);
      } catch (error) {
        console.error("Error accessing microphone:", error);
      }
    } else {
      mediaRecorder?.stop();
      streamRef.current?.getTracks().forEach((track) => track.stop());
      setRecording(false);
    }
  };

  const sendAudioToServer = async (blob) => {
    const formData = new FormData();
    formData.append("file", blob, "audio.wav");

    try {
      const response = await fetch("http://graphqlinteractive.tools:5005/speech-to-text", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.text) onSpeechResult(data.text);
    } catch (error) {
      console.error("Error sending audio:", error);
    }
  };

  let buttonClass = "speech-recorder-button";
  if (!isSupported) {
    buttonClass += " unsupported";
  } else if (hasPermission === false) {
    buttonClass += " disabled";
  } else if (recording) {
    buttonClass += " stop";
  } else {
    buttonClass += " start";
  }

  return (
    <button
      className={buttonClass}
      onClick={toggleRecording}
      disabled={!isSupported || hasPermission === false}
    >
      {!isSupported ? "❌ Not Supported" : hasPermission === false ? "🚫 No Mic" : recording ? "⏹️ Stop" : "🎤 Start"}
    </button>
  );
};

export default SpeechRecorder;

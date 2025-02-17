import React, { useState, useRef, useEffect } from "react";
import "./styles/SpeechRecorder.css";  // Import the CSS file

const SpeechRecorder = ({ onSpeechResult }) => {
  const [recording, setRecording] = useState(false);
  const [hasPermission, setHasPermission] = useState(null);
  const [mediaRecorder, setMediaRecorder] = useState(null);
  const streamRef = useRef(null);

  // Request microphone permission on component mount
  useEffect(() => {
    navigator.mediaDevices
      .getUserMedia({ audio: true })
      .then(() => setHasPermission(true))
      .catch(() => setHasPermission(false));
  }, []);

  // Toggle Recording (Start & Stop)
  const toggleRecording = async () => {
    if (hasPermission === false) return;

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
      streamRef.current.getTracks().forEach((track) => track.stop());
      setRecording(false);
    }
  };

  // Send Recorded Audio to Flask Server
  const sendAudioToServer = async (blob) => {
    const formData = new FormData();
    formData.append("file", blob, "audio.wav");

    try {
      const response = await fetch("http://127.0.0.1:5000/speech-to-text", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();
      if (data.text) onSpeechResult(data.text);
    } catch (error) {
      console.error("Error sending audio:", error);
    }
  };

  // Determine the correct class to apply based on state
  let buttonClass = "speech-recorder-button";
  if (hasPermission === false) {
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
      disabled={hasPermission === false}
    >
      {hasPermission === false ? "🚫 No Mic" : recording ? "⏹️ Stop" : "🎤 Start"}
    </button>
  );
};

export default SpeechRecorder;

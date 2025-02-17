import React from "react";
import "./styles/ChatMessage.css"; // Import styles

function ChatMessage({ text, sender }) {
  return (
    <div className={sender === "You" ? "my-message" : "other-message"}>
      <strong>{sender}:</strong> {text}
    </div>
  );
}

export default ChatMessage;

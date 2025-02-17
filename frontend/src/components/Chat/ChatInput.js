import React, { useState } from "react";
import "./styles/ChatInput.css"; // Import styles

function ChatInput({ onSendMessage }) {
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (input.trim()) {
      onSendMessage(input);
      setInput(""); // Clear input after sending
    }
  };

  return (
    <div className="input-container">
      <input
        type="text"
        value={input}
        onChange={(e) => setInput(e.target.value)}
        onKeyPress={(e) => e.key === "Enter" && handleSend()}
        className="input-field"
        placeholder="Type a message..."
      />
      <button onClick={handleSend} className="send-button">Send</button>
    </div>
  );
}

export default ChatInput;

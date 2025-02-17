import React from "react";
import "./styles/TypingIndicator.css"; // Make sure to create this CSS file

const TypingIndicator = () => {
  return (
    <div className="typing-indicator">
      <svg width="40" height="10" viewBox="0 0 40 10">
        <circle cx="5" cy="5" r="4" className="dot" />
        <circle cx="20" cy="5" r="4" className="dot" />
        <circle cx="35" cy="5" r="4" className="dot" />
      </svg>
    </div>
  );
};

export default TypingIndicator;

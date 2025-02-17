import React, { useState, useEffect, useRef } from "react";
import ChatMessage from "./ChatMessage";
import ChatInput from "./ChatInput";
import JsonViewer from "./JsonViewer";
import GraphQLQueryViewer from "./GraphQLQueryViewer";
import TypingIndicator from "./typing/TypingIndicator"; // Import the new typing indicator
import SpeechRecorder from "../SpeechRecorder/SpeechRecorder"; // Import SpeechRecorder
import { textMessage } from "./messageData";
import "./styles/ChatBox.css";
import ModelToggle from "../ToggleButton/ModelToggle";
function ChatBox() {
  const [messages, setMessages] = useState([{ text: textMessage, sender: "bot" }]);
  const [isTyping, setIsTyping] = useState(false); // Track if the bot is "typing"
  const messagesEndRef = useRef(null);
  const [selectedModel, setSelectedModel] = useState("Open-Ai");
  // Scrolls down to the latest message
  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const sendMessage = async (text) => {
    if (text.trim()) {
      setMessages((prevMessages) => [...prevMessages, { text, sender: "You" }]);

      // Show typing animation
      setIsTyping(true);
      
      if (text && text.trim() && text === "Could not understand audio") {
        setIsTyping(false);
        return;
      }

      try {
        const response = await fetch("http://graphqlinteractive.tools:5005/chat", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ 
            message: text,
            model: selectedModel
           }),
        });

        const data = await response.json();

        // Remove typing animation
        setIsTyping(false);

        data.responses.forEach((response) => {
          let botMessage = { sender: "Bot" };

          if (response.type === "text") {
            botMessage.text = response.message;
          } else if (response.type === "graphql") {
            botMessage.query = response.message;
          } else if (response.type === "json") {
            botMessage.json = response.message;
          }

          setMessages((prevMessages) => [...prevMessages, botMessage]);
        });

      } catch (error) {
        console.error("Error fetching response:", error);
        setIsTyping(false);
        setMessages((prevMessages) => [
          ...prevMessages,
          { text: "Error: Unable to get response from server", sender: "Bot" },
        ]);
      }
    }
  };
    // Handle speech-to-text conversion from SpeechRecorder
    const handleSpeechResult = (text) => {
      if (text.trim()) {
        sendMessage(text); // Automatically send converted speech as a message
      }
    };
  return (
    <div className="chat-container">
      <ModelToggle selectedModel={selectedModel} setSelectedModel={setSelectedModel} />
      <div className="messages-container">
        {messages.map((msg, index) => (
          <div key={index} className={`chat-message ${msg.sender === "You" ? "you" : "bot"}`}>
            <div className="message-content">
              {msg.text && <p className="message-text">{msg.text}</p>}
              {msg.query && <GraphQLQueryViewer query={msg.query} />}
              {msg.json && <JsonViewer data={msg.json} />}
            </div>
          </div>
        ))}
        {/* Show Typing Indicator if isTyping is true */}
        {isTyping && (
          <div className="chat-message bot">
            <TypingIndicator />
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <ChatInput onSendMessage={sendMessage} />
      <SpeechRecorder onSpeechResult={handleSpeechResult} />
    </div>
  );
}

export default ChatBox;

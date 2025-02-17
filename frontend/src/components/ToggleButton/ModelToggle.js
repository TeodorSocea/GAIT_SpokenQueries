import React from "react";
import "./styles/ModelToggle.css";

export default function ModelToggle({ selectedModel, setSelectedModel }) {
  const models = ["Open-Ai", "Custom"]; 

  const toggleModel = (model) => {
    setSelectedModel(model);  // Update the model in the parent (ChatBox)
  };

  return (
    <div className="model-toggle-container">
      {models.map((model) => (
        <button
          key={model}
          onClick={() => toggleModel(model)}
          className={`model-toggle-button ${selectedModel === model ? "active" : "inactive"}`}
        >
          {model}
        </button>
      ))}
    </div>
  );
}

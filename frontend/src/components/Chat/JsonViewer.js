import React from "react";
import ReactJson from "react-json-view";
import "./styles/JsonViewer.css"; // Import external CSS

const JsonViewer = ({ data, isUser }) => {
  return (
    <div className={`json-viewer-container ${isUser ? "my-message" : "other-message"}`}>
      <ReactJson src={data} theme="monokai" collapsed={false} displayDataTypes={false} />
    </div>
  );
};

export default JsonViewer;

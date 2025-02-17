import React from "react";
import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { dracula } from "react-syntax-highlighter/dist/esm/styles/prism";
import "./styles/GraphQLQueryViewer.css"; // Keep external CSS

const GraphQLQueryViewer = ({ query }) => {
  if (!query) return null;

  return (
    <div className="graphql-query-container">
      <SyntaxHighlighter language="graphql" style={dracula} wrapLongLines>
        {query}
      </SyntaxHighlighter>
    </div>
  );
};

export default GraphQLQueryViewer;

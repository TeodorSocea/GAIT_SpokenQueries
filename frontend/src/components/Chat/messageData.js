// Debug variable to control message type ("text", "graphql", or "json")
export const typeofMessage = "text"; // Change this to "text" or "json" as needed



// Define a normal text message
export const textMessage = "Welcome! Please provide a GraphQL API link to start.";

// Define a GraphQL query response
export const graphqlMessage = `
  query {
    movies(filter: { releaseYear: 2025 }, sort: { releaseDate: DESC }) {
      title
      releaseDate
    }
  }
`;

// Define a JSON response example
export const jsonMessage = {
  data: {
    movies: [
      { title: "Dune: Part Two", releaseDate: "2025-03-01" },
      { title: "Avengers: Secret Wars", releaseDate: "2025-05-01" },
    ],
  },
};

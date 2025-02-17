import requests
import re

from nlp.NLPInterface import NLPInterface


class ChatBot:
    def __init__(self, user_message, selected_model, stored_link="", stored_schema=None):
        """
        Initialize chatbot with user message and existing stored link and schema.
        """
        self.user_message = user_message.lower()  # Convert message to lowercase for easier comparison
        self.stored_link = stored_link  # Stored GraphQL link from SQLite
        self.stored_schema = stored_schema  # Stored GraphQL schema from SQLite
        self.validated_link = None  # Holds a new valid GraphQL link if found
        self.validated_schema = None  # Holds the schema if verified
        self.selected_model = selected_model  # Holds the schema if verified

        print(f"[DEBUG] ChatBot initialized with message: {self.user_message}")
        print(f"[DEBUG] ChatBot initialized with model: {self.selected_model}")
        print(f"[DEBUG] Stored GraphQL link at init: {self.stored_link}")

    def extract_links(self):
        """
        Extracts potential URLs from the user's message.
        """
        links = re.findall(r'https?://\S+', self.user_message)
        print(f"[DEBUG] Extracted links from message: {links}")
        return links

    def verify_graphql_link(self, link):
        """
        Checks if the provided link is a valid GraphQL API by sending an introspection query.
        """
        introspection_query = """
        query IntrospectionQuery {
          __schema {
            types {
              name
              fields {
                name
                type {
                  name
                  kind
                }
              }
              inputFields {
                name
                type {
                  name
                  kind
                }
              }
            }
          }
        }
        """

        try:
            print(f"[DEBUG] Verifying GraphQL link: {link}")
            response = requests.post(link, json={'query': introspection_query}, timeout=5)

            if response.status_code == 200:
                data = response.json()
                if "__schema" in data.get("data", {}):
                    print("[DEBUG] GraphQL link is valid, schema retrieved.")
                    return data["data"]["__schema"]  # Return the schema
        except requests.exceptions.RequestException:
            pass

        return None  # If request fails or schema is invalid

    def get_response(self):
        """
        Generates a response based on the user's input and the stored link.
        """
        links = self.extract_links()

        # ✅ Case 1: If user asks to "show me the schema" (whether a stored link exists or not)
        if "show me the schema" in self.user_message:
            if self.stored_schema:
                print("[DEBUG] Returning stored GraphQL schema.")
                return {
                    "responses": [
                        {"type": "text", "message": f"Here is the stored GraphQL schema for {self.stored_link}:"},
                        {"type": "json", "message": self.stored_schema}
                    ]
                }
            else:
                return {
                    "responses": [
                        {"type": "text", "message": "No GraphQL schema is stored. Please provide a GraphQL link first."}
                    ]
                }

        # ✅ Case 2: User asks something but no valid link is stored
        if not links and not self.stored_link:
            return {"responses": [{"type": "text", "message": "Please provide a GraphQL link to continue."}]}

        # ✅ Case 3: User provides multiple links
        if len(links) > 1:
            return {
                "responses": [
                    {"type": "text", "message": "You provided multiple links. Which one should I use?"},
                    {"type": "text", "message": "Links detected: " + ", ".join(links)}
                ]
            }

        # ✅ Case 4: User provides one link, but it's invalid
        if len(links) == 1:
            link = links[0]
            schema = self.verify_graphql_link(link)

            if not schema:
                return {"responses": [{"type": "text", "message": "Sorry, this is not a valid GraphQL link."}]}

            # ✅ Case 5: Link is valid → Store it and return schema
            self.validated_link = link  # Store for SQLite update
            self.validated_schema = schema
            return {
                "responses": [
                    {"type": "text", "message": f"We will use this GraphQL API: {link}"}
                    #{"type": "json", "json": schema}
                ]
            }

        # ✅ Case 6: User sends a message, and a link is already stored
        if not links and self.stored_link:
            # ✅ If they ask for the schema, return it
            if "show me the schema" in self.user_message:
                print("[DEBUG] Returning stored GraphQL schema from existing stored link.")
                return {
                    "responses": [
                        {"type": "text", "message": f"Here is the stored GraphQL schema for {self.stored_link}:"},
                        {"type": "json", "message": self.stored_schema}
                    ]
                }
            else:
                nlp_interface = NLPInterface(model_type=self.selected_model, user_input=self.user_message, schema=self.stored_schema)

                proccesed_by_nlp = nlp_interface.generate_graphql_query()

                return {
                    "responses": [
                        {"type": "text", "message": f"GraphQL API[{self.stored_link}]"},
                        #{"type": "text", "message": f"Model: {self.selected_model}"},
                        {"type": "graphql", "message": f"{proccesed_by_nlp}"}
                    ]
                }

        # Default case: Something unexpected happened
        return {"responses": [{"type": "text", "message": "Something went wrong. Please try again."}]}

from openai import OpenAI
import os


class OpenAiWrapper:
    def __init__(self, schema=None):
        self.api_key = os.environ.get("OPENAI_API_KEY")
        self.schema = schema  # Optionally pass a schema for OpenAi to use
        self.client = OpenAI(api_key=self.api_key)

    def generate_graphql_query(self, user_input):
        """Generate a GraphQL query based on user input."""
        schema_text = str(self.schema)  # Convert schema JSON to string for OpenAI

        prompt = f"""
        Given the following GraphQL schema:
        {schema_text}

        Generate a GraphQL query that matches this user request:
        "{user_input}"
        """

        response = self.client.chat.completions.create(model="gpt-4o-mini",
                                                       messages=[
                                                           {"role": "system",
                                                            "content": "You are an expert GraphQL query generator. You need to only show the generated query. Don t wrap it as a Graphql code, provided it so we can run it directly in graphql."},
                                                           {"role": "user", "content": prompt}
                                                       ])

        return response.choices[0].message.content

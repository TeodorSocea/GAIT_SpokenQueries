class Custom:
    def __init__(self, schema=None):
        self.schema = schema  # Optionally pass a schema for GraphQL query generation

    def generate_graphql_query(self, user_input):
        """Generate a GraphQL query based on user input."""
        return f"Custom response for {user_input}"
from nlp.OpenAiWrapper import OpenAiWrapper
from nlp.Custom import Custom

class NLPInterface:
    def __init__(self, model_type, user_input, schema=None):
        # Define model classes dynamically
        model_classes = {
            "Open-Ai": OpenAiWrapper,
            "Custom": Custom
        }

        if model_type not in model_classes:
            raise ValueError(f"Invalid model type: {model_type}")

        # Initialize the model (pass the schema if available)
        if model_type == "Open-Ai":
            self.model = model_classes[model_type](schema=schema)  # OpenAi requires api_key
        else:
            self.model = model_classes[model_type](schema=schema)  # Custom doesn't need an api_key

        self.user_input = user_input

    def generate_graphql_query(self):
        """Get the response from the selected model."""
        return self.model.generate_graphql_query(self.user_input)
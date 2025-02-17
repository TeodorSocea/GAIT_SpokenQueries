import openai
import json
import os
import re
import json
class OpenAIAssistant:
    def __init__(self, schema):
        """
        Initializes the OpenAIAssistant by reading instructions from a file
        and creating an Assistant via OpenAI's API.

        :param api_key: Your OpenAI API key
        :param instructions_file: Path to the instructions file (text or JSON)
        :param model: The OpenAI model to use (default: "gpt-4-turbo")
        """
        openai.api_key = os.environ.get("OPENAI_API_KEY")
        instructions_file = "instructions.txt"
        model = "gpt-4-turbo"
        # self.headers = {
        #     'OpenAI-Beta': 'assistants=v2'  # Include the header for the beta version
        # }
        self.schema = schema
        self.model = model
        self.instructions = self._load_instructions(instructions_file)
        self.assistant_id = self._create_or_fetch_assistant()
        self.thread_id = None  # Stores the thread for conversations
        #Loading schema
        self.generate_graphql_query(f"Describe the schema: {self.schema}")
    def _load_instructions(self, filename: str) -> str:
        """Loads assistant instructions from a file relative to the script's location."""
        script_dir = os.path.dirname(os.path.abspath(__file__))  # Get the script's directory
        file_path = os.path.join(script_dir, filename)  # Construct the absolute path

        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read().strip()
            return content
        except Exception as e:
            print(f"Error reading instructions file '{filename}': {e}")
            return "You are a helpful assistant."

    def _create_or_fetch_assistant(self) -> str:
        """Creates an Assistant with given instructions or fetches an existing one."""
        response = openai.beta.assistants.create(
            name="Custom AI Assistant",
            instructions=self.instructions,
            model=self.model
        )
        return response.id  # Store the assistant ID for future use

    def start_conversation(self):
        """Starts a new conversation thread."""
        response = openai.beta.threads.create()
        self.thread_id = response.id
        print(f"Started a new conversation (Thread ID: {self.thread_id})")
        #send the schema first


    def generate_graphql_query(self, user_message: str):
        """
        Sends a message to the assistant and returns the response.

        :param user_message: The user's input message
        :return: Assistant's response
        """
        if self.thread_id is None:
            self.start_conversation()


        # Add message to thread
        openai.beta.threads.messages.create(
            thread_id=self.thread_id,
            role="user",
            content=user_message,

        )

        # Run assistant to get response
        run = openai.beta.threads.runs.create(
            thread_id=self.thread_id,
            assistant_id=self.assistant_id
        )

        # Wait for completion (polling)
        while True:
            run_status = openai.beta.threads.runs.retrieve(
                thread_id=self.thread_id,  # Required argument
                run_id=run.id  # Corrected to use 'run_id' instead of just 'run.id'
            )

            if run_status.status == "completed":
                break

        # Fetch messages from the thread
        messages = openai.beta.threads.messages.list(thread_id=self.thread_id)
        response_message = messages.data[0].content[0].text.value # Latest response

        return response_message

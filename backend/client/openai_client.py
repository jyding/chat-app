import openai
from dotenv import load_dotenv
import os

class OpenAIClient:
    def __init__(self):
        # Load environment variables from the .env file
        load_dotenv()

        # Get the OpenAI API key
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key not found. Set the OPENAI_API_KEY environment variable.")

        openai.api_key = self.api_key

    def get_response(self, messages, model='gpt-4'):
        """
        Sends a list of messages to the OpenAI ChatCompletion API and returns the assistant's response.

        :param messages: A list of message dictionaries with 'role' and 'content' keys.
        :param model: The model to use for the API call.
        :return: The assistant's response as a string, or None if there's an error.
        """
        print("Messages length:", len(messages))

        # Convert Message objects to a list of dictionaries as required by the API
        formatted_messages = [
            {"role": message['role'], "content": message['content']} for message in messages
        ]

        try:
            response = openai.chat.completions.create(
                messages=formatted_messages,
                model="gpt-3.5-turbo",
            )
            # Access the assistant's message content
            return response.model_dump_json()

        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return None



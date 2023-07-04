import openai
from dotenv import load_dotenv
import os
import constants
# Load the environment variables from the .env file
load_dotenv()

openai.api_type = os.getenv("API_TYPE")
openai.api_base = os.getenv("API_BASE")
openai.api_version = os.getenv("API_VERSION")
openai.api_key = os.getenv("OPENAI_API_KEY")

def generate_response(chat_history):
    try:
        response = openai.ChatCompletion.create(
            engine="dfm_gpt", # replace this value with the deployment name you chose when you deployed the associated model.
            messages = chat_history,
            temperature=0,
            max_tokens=1000,
            top_p=0.95,
            frequency_penalty=0,
            presence_penalty=0,
            stop=None
        )
        response_message = response.choices[0].message.content
        return 200, response_message
    except Exception as e:
        print(e)
        return 501, "Error: ChatGPT failed to generate a response."
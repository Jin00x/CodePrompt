import os
import openai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv('LLM_API_KEY')

# Set the API key
openai.api_key = api_key

def call_openai_api(prompt):
    response = openai.Completion.create(
        engine="davinci-codex",
        prompt=prompt,
        max_tokens=100
    )
    return response.choices[0].text.strip()

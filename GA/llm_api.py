import os
import openai
from dotenv import load_dotenv

# Load the .env file
load_dotenv()

# Get the API key from the .env file
api_key = os.getenv('LLM_API_KEY')

# Set the API key
openai.api_key = api_key

def call_openai_api(prompt, model="gpt-4-turbo"):
    try:
        response = openai.ChatCompletion.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant for writing code."},
                {"role": "user", "content": prompt},
            ],
            max_tokens=1000,
            temperature=0.5,
        )
        # TODO: parse the only code section from the response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        print("Error on openai.ChatCompletion.create: ", e)
    
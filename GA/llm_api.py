import os
import openai
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI

env_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), ".env")
load_dotenv(env_path)

# Get the API key from the .env file
api_key = dotenv_values(env_path)["LLM_API_KEY"]
# Set the API key
openai.api_key = api_key

print("OpenAI API Key: ", api_key)
client = OpenAI(
    api_key=api_key,
)


def call_openai_api(prompt, model="gpt-4o-mini"):
    # TODO: append the return structure of the response to prompt
    prompt += f"\n"

    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for writing code.",
                },
                {"role": "user", "content": prompt},
            ],
        )
        # TODO: parse the only code section from the response
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error on openai.ChatCompletion.create: ", e)


def mutate_with_openai(
    prompt,
    mutation_instructions=(
        "Make small, random changes to the text such as replacing words with synonyms, "
        "adding minor typographical errors, or rephrasing parts of the text while preserving its meaning."
    ),
    model="gpt-4o-mini",
):
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {
                    "role": "system",
                    "content": "You are a helpful assistant for mutating text.",
                },
                {
                    "role": "user",
                    "content": f"Mutate the following text according to the instructions and the mutation rate in the text:\n\nText: {prompt}\nInstructions: {mutation_instructions}",
                },
            ],
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        print("Error while calling OpenAI API:", e)
        return None


if __name__ == "__main__":
    res = call_openai_api(
        "Write a Python function that takes a list of numbers and returns the sum of the list."
    )
    print(res)

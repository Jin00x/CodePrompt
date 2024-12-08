import os
import openai
from dotenv import load_dotenv, dotenv_values
from openai import OpenAI
import time
import threading

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

def run_thread(prompt, results, index):
    results[index] = call_openai_api(prompt)


if __name__ == "__main__":
    start = time.time()
    # res = call_openai_api(
    #     "Write a Python function that takes a list of numbers and returns the sum of the list."
    # )
    # run the call_openai_api function twice in parallel

    prompt = "Write a Python function that takes a list of numbers and returns the sum of the list."

    res = [None, None, None]
    thread1 = threading.Thread(target=run_thread, args=(prompt, res, 0))
    thread2 = threading.Thread(target=run_thread, args=("give me a short haiku", res, 1))
    thread3 = threading.Thread(target=run_thread, args=("give me a short haiku", res, 2))

    thread1.start()
    thread2.start()
    thread3.start()

    thread1.join()
    thread2.join()
    thread3.join()
    
    print(res[0])
    print("------------------------------------------")
    print(res[1])
    print("------------------------------------------")
    print(res[2])
    print(F"Time taken: {time.time() - start}")

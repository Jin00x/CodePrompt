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
    prompt = ""
    with open ("/Users/coll1ns/CS454---Team-project/linked_list/src/linked_list_src.rs") as f:
        code = f.read()
    whole_prompt = f"""
    {prompt} \n
    Code: \n
    {code} \n
    Provide the code only, without any explanation or additional text.
    """
    print(call_openai_api(whole_prompt))
    # res = call_openai_api(
    #     "Write a Python function that takes a list of numbers and returns the sum of the list."
    # )
    # run the call_openai_api function twice in parallel

    # prompts = [
    #     "Write a Python function that takes a list of numbers and returns the sum of the list.",
    #     "give me a short haiku on kaist",
    #     "give me a short haiku on korea and japan relationship",
    #     "give me a short haiku on japan's anime industry",
    #     "give me a short haiku on otaku in japan",
    #     "give me a short haiku on low korean birth rate",
    # ]

    # res = [None, None, None, None, None, None]
    # threads = []
    # for i in range(len(res)):
    #     threads.append(
    #         threading.Thread(target=run_thread, args=(prompts[i], res, i))
    #     )
    # # thread1 = threading.Thread(target=run_thread, args=(prompt, res, 0))
    # # thread2 = threading.Thread(target=run_thread, args=("give me a short haiku", res, 1))
    # # thread3 = threading.Thread(target=run_thread, args=("give me a short haiku", res, 2))

    # for thread in threads:
    #     thread.start()

    # for thread in threads:
    #     thread.join()
    # # thread1.start()
    # # thread2.start()
    # # thread3.start()

    # # thread1.join()
    # # thread2.join()
    # # thread3.join()

    # for r in res:
    #     print(r)
    #     print("------------------------------------------")
    # print(F"Time taken: {time.time() - start}")

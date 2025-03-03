from openai import OpenAI
import json

with open("config.json") as config_file:
    config = json.load(config_file)

api_key = config["api_key"]

client = OpenAI(
    api_key=api_key
)

completion = client.chat.completions.create(
    model="gpt-4o-mini",
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {
            "role": "user",
            "content": "Write a haiku about recursion in programming."
        }
    ]
)

print(completion.choices[0].message)
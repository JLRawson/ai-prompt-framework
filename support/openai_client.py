import json
import openai

def load_openai_client():
    with open("config.json") as config_file:
        config = json.load(config_file)
    api_key = config["api_key"]
    return openai.OpenAI(api_key=api_key)

def send_prompt(prompt, model="gpt-4o-mini", system_message="You are a helpful assistant."):
    client = load_openai_client()
    response = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": system_message},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

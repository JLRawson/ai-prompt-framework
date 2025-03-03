import json
import os
import openai
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser

def create_index(index_dir: str, requirements_folder: str):
    schema = Schema(title=ID(stored=True), content=TEXT)

    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
        ix = create_in(index_dir, schema)
    else:
        ix = open_dir(index_dir)

    writer = ix.writer()

    for filename in os.listdir(requirements_folder):
        file_path = os.path.join(requirements_folder, filename)
        if os.path.isfile(file_path):
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
                writer.add_document(title=filename, content=content)

    writer.commit()
    print("Indexing complete.")

def search_requirements(index_dir: str, query_str: str):
    ix = open_dir(index_dir)
    results_list = []

    with ix.searcher() as searcher:
        query = QueryParser("content", ix.schema).parse(query_str)
        results = searcher.search(query)

        for result in results:
            results_list.append(result['title'])
            # print(f"Found in: {result['title']}")

    return results_list

def generate_search_terms(relative_path):
    # Setup
    with open("config.json") as config_file:
        config = json.load(config_file)

    api_key = config["api_key"]
    client = openai.OpenAI(api_key=api_key)

    # Load default inputs from the JSON file
    def load_inputs():
        try:
            with open(f"{relative_path}/inputs.json", "r") as file:
                data = json.load(file)
                return data.get("use_case", {})  # Load "use_case" inputs
        except FileNotFoundError:
            print(f"Error: The file at {relative_path}/inputs.json was not found. Proceeding with manual input.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {relative_path}/inputs.json. Proceeding with manual input.")
            return {}

    user_inputs = load_inputs()

    # Questions to ask if values are missing
    questions = {
        "role": "What is your role in this project? (e.g., Software Engineer, Product Manager, QA Tester): ",
        "feature_name": "What is the feature name you are working on? (e.g., Invoice Processing, User Authentication): ",
        "product_description": "Briefly describe what this product does. (e.g., handles user authentication, processes payments): ",
        "use_case_description": "What is the specific use case you are implementing? (e.g., optimizing invoice scanning and data extraction): ",
        "low_number": "How many search terms should be generated? (Enter a number, e.g., 5, 7, 10): "
    }

    # Prompt for missing inputs
    for key, question in questions.items():
        if key not in user_inputs or not user_inputs[key]:
            user_inputs[key] = input(question).strip()
            if key == "low_number":
                user_inputs[key] = int(user_inputs[key])  # Ensure numerical input

    # Generate prompt dynamically
    prompt = f"""
        You are a {user_inputs['role']} that is going to start developing a use case about
        {user_inputs['feature_name']} on a product about {user_inputs['product_description']}.
        The use case you are implementing is {user_inputs['use_case_description']}.
        You are tasked with picking search terms to search for requirements
        related to the use case to reference from when creating acceptance
        criteria on the use case.
        Identify the most distinctive features of the use case and generate {user_inputs['low_number']} feature names that precisely describe its functionality. 
        Prioritize concise terms (1-2 words), such as "task prioritization" or "prioritization," while avoiding broad or generic language unrelated to specific features. 
        Ensure that the feature names are relevant to potential functionalities within the use case. List the search
        terms starting from the most relevant search term to the least, seperated by commas. 
        Do not add anything extra besides the search terms, absolutely no comments, explanations, or additional titles.
    """

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                  {"role": "user", "content": prompt}]
    )

    search_terms_response = completion.choices[0].message.content.strip()
    search_terms = [term.strip() for term in search_terms_response.split(",") if term.strip()]
    
    return search_terms

import json
import os

# Define question sets for different input keys
DEFAULT_QUESTION_SETS = {
    "prompt-one": {
        "role": "What is your role in this project? (e.g., Software Engineer, Product Manager, QA Tester): ",
        "product_type": "What type of software is this? (e.g., Web App, Mobile App, API Service, Library): ",
        "product_description": "Briefly describe what this software does. (e.g., handles user authentication, processes payments): ",
        "important_aspects": "What are the key aspects of the files that need to be summarized? (e.g., security, structure, dependencies): ",
        "additional_constraints": "Are there any specific constraints or requirements for the summary? (e.g., include security concerns, focus on performance optimizations): "
    },
    "use_case": {
        "role": "What is your role in this project? (e.g., Software Engineer, Product Manager, QA Tester): ",
        "feature_name": "What is the feature name you are working on? (e.g., Invoice Processing, User Authentication): ",
        "product_description": "Briefly describe what this product does. (e.g., handles user authentication, processes payments): ",
        "use_case_description": "What is the specific use case you are implementing? (e.g., optimizing invoice scanning and data extraction): ",
        "low_number": "How many search terms should be generated? (Enter a number, e.g., 5, 7, 10): "
   }
}


def load_or_prompt_inputs(relative_path: str, input_key: str = "prompt-one") -> dict:
    inputs_path = os.path.join(relative_path, "inputs.json")
    questions = DEFAULT_QUESTION_SETS.get(input_key, {})

    try:
        with open(inputs_path, "r") as file:
            data = json.load(file)
            user_inputs = data.get(input_key, {})
    except FileNotFoundError:
        print(f"Warning: {inputs_path} not found. Proceeding with manual input.")
        user_inputs = {}
    except json.JSONDecodeError:
        print(f"Warning: Could not decode {inputs_path}. Proceeding with manual input.")
        user_inputs = {}

    for key, question in questions.items():
        if key not in user_inputs or not user_inputs[key]:
            user_inputs[key] = input(question).strip()

    return user_inputs

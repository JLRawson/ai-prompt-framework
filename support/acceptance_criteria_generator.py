import json
import openai

def generate_acceptance_criteria(relative_path,code_files_description,acceptance_criteria_guidelines, related_requirements_results):

    with open("config.json") as config_file:
        config = json.load(config_file)

    api_key = config["api_key"]
    client = openai.OpenAI(api_key=api_key)

    def load_inputs():
        try:
            with open(relative_path + "/inputs.json", "r") as file:
                data = json.load(file)
                return data.get("use_case", {})
        except FileNotFoundError:
            print(f"Error: The file at {relative_path}/inputs.json was not found. Proceeding with manual input.")
            return {}
        except json.JSONDecodeError:
            print(f"Error: Failed to decode JSON from {relative_path}/inputs.json. Proceeding with manual input.")
            return {}
    
    user_inputs = load_inputs()

    prompt = f"""
        You are a {user_inputs['role']} working on maintaining a {user_inputs['product_description']}.
        Your team is currently working to implement a use case under the
        feature called {user_inputs['feature_name']}.
        You are tasked with suggesting acceptance criteria for the use case:
        {user_inputs['use_case_description']}
        Suggest acceptance criteria
        that in accordance to your
        guidelines.
        If at any point there is a criteria that
        must receive clarification to
        meet your guidelines, such as
        an ambiguous or untestable
        acceptance criteria, create a
        question who’s response will
        give you clarification and put
        the question under the ‘clarifying questions’ section.
        It’s crucial to keep previous
        requirements in mind, ensuring that new developments
        are consistent and complementary to the current use
        case and acceptance criteria.
        You are also provided related
        code files, use the code files to
        understand the general code
        base around the feature and
        any current limitations.
        Create a section titled “Pointers to
        start that gives other developers an idea of places to start
        in the code and potential issues
        Do not add any explanations. Only list the acceptance criteria
        under a section called “Acceptance Criteria". Do not add any titles
        to the acceptance criteria.

        Here are the related code file descriptions:
        {code_files_description}

        Here are the acceptance criteria guidelines:
        {acceptance_criteria_guidelines}

        Here are the related requirements:
        {related_requirements_results}

    """
    
    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}]
    )

    return completion.choices[0].message.content
    
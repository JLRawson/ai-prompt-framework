import os
from whoosh.index import create_in, open_dir
from whoosh.fields import Schema, TEXT, ID
from whoosh.qparser import QueryParser
from support.openai_client import send_prompt

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

def generate_search_terms(relative_path, user_inputs):

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

    search_terms_response = send_prompt(prompt)
    search_terms = [term.strip() for term in search_terms_response.split(",") if term.strip()]
    
    return search_terms

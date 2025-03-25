import os
from support.openai_client import send_prompt

def get_related_code_files(repo_summary, relative_path, user_inputs):
    prompt = f"""
        You are a {user_inputs['role']} that is going to start developing a use case about
        {user_inputs['feature_name']} on a product about {user_inputs['product_description']}.
        The use case you are implementing is {user_inputs['use_case_description']}.
        You are tasked with picking potentially related files to the use case that can
        be used to generate acceptance criteria for the use case.
        You are given a file that lists each code file’s relative path, name
        and description. Pick the top {user_inputs['low_number']} files that are most likely
        related to the use case so you can begin coding to develop the use case. In addition,
        you know the directory of the code base, for each chosen file if
        there is a highly similar file nearby and within the same folder,
        add the similar file’s path to the chosen files. Rank the chosen files
        to the according to relevancy of the use case.
        For the output, only provide the relative path of the file with its
        name included in the path. Do not add anything extra besides the
        paths, absolutely no comments, explanations, or additional titles.

        Below is file summaries and their paths:

        ```
        {repo_summary}
        ```
    """

    # print(prompt)
    raw_file_paths = send_prompt(prompt).split("\n")
    
    valid_file_paths = []
    for path in raw_file_paths:
        full_path = os.path.join(relative_path, path.lstrip("/"))
        normalized_path = full_path.replace("\\", "/")
        if os.path.exists(normalized_path):
            valid_file_paths.append(path)
    
    return valid_file_paths
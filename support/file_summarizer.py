import os
import re
from support.file_structure import get_filtered_file_paths
from support.openai_client import send_prompt

def summarize_files(relative_path, banned_extensions, banned_filenames, limit, user_inputs):

    file_paths = get_filtered_file_paths(relative_path, banned_extensions=banned_extensions, banned_filenames=banned_filenames, limit=limit)
    file_data = {}

    for file_path in file_paths: # Process each code file
        file_name = os.path.basename(file_path)
        file_extension = os.path.splitext(file_name)[1]
        full_path = relative_path + file_path

        try:
            with open(full_path, "r", encoding="utf-8") as file:
                file_content = file.read()
        except Exception as e:
            print(f"Error reading {full_path}: {e}")
            file_content = "[Error: Could not read file content]"

        max_chars = 4000  # Adjust based on model token limits
        if len(file_content) > max_chars:
            file_content = file_content[:max_chars] + "\n[Truncated for length...]"

        prompt = f"""
        You are a {user_inputs['role']} and are tasked with analyzing and summarizing a
        {file_extension} file titled {file_name}. The product you are working
        on is a {user_inputs['product_type']} software that {user_inputs['product_description']}.
        Your task is to summarize the file into 3 components: a sentence
        summary describing the file’s main purpose, a summary describing
        the file’s main purpose, and a list of the code’s files method declarations with a phrase description.
        {user_inputs['important_aspects']}. The sentence summary should start and end with <sentenceSummary> tags. 
        The paragraph summary should start and end with <paragraphSummary> tags. 
        The methods should start with <methods> and end with <methods> tags.
        {user_inputs['additional_constraints']} The output should have no additional
        wording besides the summary and methods. If it’s not a part of the summary,
        don’t write anything, not even additional notes to the user.

        Below is the content of the file:

        ```
        {file_content}
        ```
        """

        # print(f"Prompt for {file_name}:")
        # print(prompt)
        # print(f"Generating summary for {file_name}...")

        summary = send_prompt(prompt)

        sentence_summary_match = re.search(r"<sentenceSummary>(.*?)</sentenceSummary>", summary, re.DOTALL)
        paragraph_summary_match = re.search(r"<paragraphSummary>(.*?)</paragraphSummary>", summary, re.DOTALL)
        methods_match = re.search(r"<methods>(.*?)</methods>", summary, re.DOTALL)

        file_data[file_name] = {
            "path": file_path,
            "file_extension": file_extension,
            "sentence_summary": sentence_summary_match.group(1).strip() if sentence_summary_match else "",
            "paragraph_summary": paragraph_summary_match.group(1).strip() if paragraph_summary_match else "",
            "methods": methods_match.group(1).strip() if methods_match else ""
        }

    return file_data

# Example usage
if __name__ == "__main__":
    relative_path = "./tests/test_one"
    banned_extensions = [".json", ".md"]
    limit = 2

    summaries = summarize_files(relative_path, banned_extensions, limit)
    
    for file_name, attributes in summaries.items():
        print(f"\nFile: {file_name}")
        print(f"Path: {attributes['path']}")
        print(f"Extension: {attributes['file_extension']}")
        
        print("\nSentence Summary:")
        print(attributes.get("sentence_summary", "N/A"))
        
        print("\nParagraph Summary:")
        print(attributes.get("paragraph_summary", "N/A"))
        
        print("\nMethods:")
        print(attributes.get("methods", "N/A"))

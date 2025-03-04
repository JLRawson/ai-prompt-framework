import os
from support.file_identifier import get_related_code_files
from support.file_summarizer import summarize_files
from support.file_structure import get_filtered_file_paths 
from support.indexer import create_index, generate_search_terms, search_requirements 

# Step 1: Summarize the code base
relative_path = "./tests/test_one"
banned_extensions = [".json", ".md", ".toc", ".seg", ".txt", ]
banned_filenames = ["MAIN_WRITELOCK"]
limit = 2

file_paths = get_filtered_file_paths(relative_path, banned_extensions=banned_extensions, limit=limit)
summaries = summarize_files(relative_path, banned_extensions, limit)

print("==== Step 1 Results ====")

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

print("==== Step 2 Results ====")

index_directory = relative_path + "/indexed_requirements"
requirements_directory = relative_path + "/requirements"
search_term = "priority"

if not os.path.exists(index_directory):
    create_index(index_directory, requirements_directory)

search_terms = generate_search_terms(relative_path)
search_results = []
for term in search_terms:
    search_result = search_requirements(index_directory, term)
    for result in search_result:
        if result not in search_results:
            search_results.append(result)

print("Search Terms:", search_terms)
print("Search Results:", search_results)

print("==== Step 3 Results ====")


repo_summary = ""
for file_name, attributes in summaries.items():
    sentence_summary = attributes.get("sentence_summary", "N/A")
    path = attributes.get("path", "N/A")
    repo_summary += f"{path}: {sentence_summary}\n"

related_code_files = get_related_code_files(repo_summary, relative_path)

print("Related Code Files:", related_code_files)

print("==== Step 4 Results ====")

acceptance_criteria = ""

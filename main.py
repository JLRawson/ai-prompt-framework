from support.file_summarizer import summarize_files

# Step 1: Summarize the code base
relative_path = "./tests/test_one"
banned_extensions = [".json", ".md"]
limit = 2

summaries = summarize_files(relative_path, banned_extensions, limit)

print("==== Step 1 Results ====")
for file_name, attributes in summaries.items():
    print(f"\nFile: {file_name}")
    print(f"Path: {attributes['path']}")
    print(f"Extension: {attributes['file_extension']}")
    print(f"Summary: {attributes['summary']}")
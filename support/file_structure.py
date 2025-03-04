import os

def get_filtered_file_paths(base_dir, banned_extensions=[], banned_filenames=[], limit=10):
    if not os.path.exists(base_dir): 
        print(f"Error: The directory '{base_dir}' does not exist.")
        return []

    file_paths = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1]  # Extract file extension

            if file_ext in banned_extensions or file in banned_filenames:
                continue

            full_path = os.path.join(root, file)
            relative_path = os.path.relpath(full_path, base_dir)

            normalized_path = "/" + relative_path.replace("\\", "/") # Ensure consistent forward slashes

            file_paths.append(normalized_path)

            if len(file_paths) >= limit:  # Stop at file reading limit
                return file_paths
    return file_paths

# Example usage
if __name__ == "__main__":
    currrent_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(currrent_dir, "..", "tests", "test_one")
    banned_extensions = [".json", ".md", ".toc", ".seg", ".txt", ]
    banned_filenames = ["MAIN_WRITELOCK"]

    file_paths = get_filtered_file_paths(base_dir, banned_extensions, banned_filenames, limit=10)

    print("Files found in 'test_one' (excluding banned types):")
    for path in file_paths:
        print(path)

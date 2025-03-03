import os

def get_filtered_file_paths(base_dir, banned_extensions=[], limit=10):
    if not os.path.exists(base_dir): 
        print(f"Error: The directory '{base_dir}' does not exist.")
        return []

    file_paths = []
    for root, _, files in os.walk(base_dir):
        for file in files:
            file_ext = os.path.splitext(file)[1]  # Extract file extension

            if file_ext in banned_extensions:
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
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    BASE_DIR = os.path.join(CURRENT_DIR, "..", "tests", "test_one")
    BANNED_EXTENSIONS = [".json", ".md"]

    file_paths = get_filtered_file_paths(BASE_DIR, banned_extensions=BANNED_EXTENSIONS, limit=10)

    print("Files found in 'test_one' (excluding banned types):")
    for path in file_paths:
        print(path)

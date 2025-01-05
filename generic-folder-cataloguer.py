import os
import csv
from datetime import datetime

def generate_file_index(folder_path, index_file):
    """Generate a CSV index of files in the specified folder."""
    with open(index_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["absolute_file_path", "file_name", "file_size_bytes"])

        for root, _, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                file_size = os.path.getsize(file_path)
                writer.writerow([file_path, file_name, file_size])

    print(f"Index created at {index_file}")

def main():
    # List of absolute paths to catalog
    paths_to_catalog = [
        # Add the absolute paths of folders to catalog here, e.g.,
        # "/path/to/folder1",
        # "/path/to/folder2",
    ]

    if not paths_to_catalog:
        print("The list of paths to catalog is empty. Please add paths to the 'paths_to_catalog' list.")
        return

    for folder_path in paths_to_catalog:
        # Check if the folder exists
        if not os.path.exists(folder_path):
            print(f"The folder {folder_path} does not exist. Skipping...")
            continue

        # Generate the index file
        today = datetime.now().strftime("%Y%m%d")
        folder_name = os.path.basename(folder_path.rstrip(os.sep))
        index_file = os.path.join(os.getcwd(), f"{today}_{folder_name}_file_catalog.csv")
        generate_file_index(folder_path, index_file)

if __name__ == "__main__":
    main()
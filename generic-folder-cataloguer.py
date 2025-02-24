######
## Skeleton script that catalogues all files
######

import os
from datetime import datetime
import pandas as pd

def get_folder_path():
    """Gets a valid folder path from the user."""
    while True:
        folder_path = input("Please enter the folder path: ").strip()
        if os.path.exists(folder_path):
            return folder_path
        print("Error: The specified path does not exist.")


def process_folder(folder_path):
    """Recursively walks through a folder and generates a list of files and folders.

    Args:
        folder_path: The path to the folder to process.

    Returns:
        A pandas DataFrame containing the relative paths and file types.
    """
    titles = []
    rel_paths = []
    item_types = []

    for root, dirs, files in os.walk(folder_path):
        for item in dirs + files:
            # Skip files that match the pattern "YYYYMMDDHHMMSS catalog.csv"
            if item.endswith("catalog.csv"):
                continue

            full_path = os.path.join(root, item)
            relative_path = os.path.relpath(full_path, folder_path)

            if os.path.isdir(full_path):
                item_type = "folder"
            else:
                item_type = os.path.splitext(item)[1][1:] or "no extension"

            titles.append(item)
            rel_paths.append(relative_path)
            item_types.append(item_type)

    df = pd.DataFrame({
        'relative_path': rel_paths,
        'file_type': item_types
    })
    df = df.sort_values('relative_path', ignore_index=True)
    return df


def write_to_csv(df, folder_path):
    """Writes the DataFrame to a CSV file with a timestamped filename.

    Args:
        df: The pandas DataFrame to write.
        folder_path: The folder where the CSV should be saved.
    """
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    output_filename = f"{timestamp} catalog.csv"
    output_path = os.path.join(folder_path, output_filename)
    df.to_csv(output_path, index=False)
    print(f"Catalog has been saved to: {output_path}")


def main():
    """Main function to orchestrate the script."""
    folder_path = get_folder_path()
    df = process_folder(folder_path)
    write_to_csv(df, folder_path)


if __name__ == "__main__":
    main()

######
## Cataloguing script specific for my eBook library
#### assumes ebook-libraries have been pre-formatted in Calibre's library structure
#### assumes there are multiple ebook libraries in one overarching library folder
#### creates a full CSV catalogue of the library (absolute_path, book_title, book_author, number of files, hasPDF (yes/no), hasEPUB (yes/no), hasMOBI (yes/no), hasCBR (yes/no), hasCBZ (yes/no))
######

import os
import csv
from datetime import datetime

def get_folder_path(prompt):
    """Ask user for folder input and ensure it's an absolute path."""
    folder_path = input(prompt)
    if not os.path.isabs(folder_path):
        print("Please provide an absolute path.")
        return get_folder_path(prompt)
    return folder_path

def generate_ebook_index(library_path, subfolders, index_file):
    """Generate a CSV index of eBooks in the specified library subfolders."""
    with open(index_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow([
            "absolute_path", "book_id", "book_author", "total_files_in_folder",
            "PDF", "AZW3", "EPUB", "MOBI", "CBR", "CBZ"
        ])

        for subfolder in subfolders:
            subfolder_path = os.path.join(library_path, subfolder)

            if os.path.exists(subfolder_path):
                for author_folder in os.listdir(subfolder_path):
                    author_path = os.path.join(subfolder_path, author_folder)

                    if os.path.isdir(author_path):
                        for book_id_folder in os.listdir(author_path):
                            book_path = os.path.join(author_path, book_id_folder)

                            if os.path.isdir(book_path):
                                # Gather files in the book folder
                                files = os.listdir(book_path)
                                total_files = len(files)

                                # Use book ID from folder name
                                book_id = book_id_folder[:40]  # Limit book ID to 40 characters
                                book_author = author_folder[:20]  # Limit author name to 20 characters

                                # Check for file formats
                                has_pdf = any(file.lower().endswith('.pdf') for file in files)
                                has_azw3 = any(file.lower().endswith('.azw3') for file in files)
                                has_epub = any(file.lower().endswith('.epub') for file in files)
                                has_mobi = any(file.lower().endswith('.mobi') for file in files)
                                has_cbr = any(file.lower().endswith('.cbr') for file in files)
                                has_cbz = any(file.lower().endswith('.cbz') for file in files)

                                writer.writerow([
                                    book_path, book_id, book_author, total_files,
                                    "Yes" if has_pdf else "No",
                                    "Yes" if has_azw3 else "No",
                                    "Yes" if has_epub else "No",
                                    "Yes" if has_mobi else "No",
                                    "Yes" if has_cbr else "No",
                                    "Yes" if has_cbz else "No"
                                ])

    print(f"Index created at {index_file}")

def main():
    library_path = "/volume1/library" ### change this PATH to your preferred folder instead
    subfolders = [
        "books", "comics", "epulps", "kindle", "occult", "references", "textbooks"
    ]

    # Check if the library folder exists
    if not os.path.exists(library_path):
        print(f"The library folder {library_path} does not exist.")
        return

    # Generate the index file
    today = datetime.now().strftime("%Y%m%d")
    index_file = os.path.join(os.getcwd(), f"{today}_ebook_catalog.csv")
    generate_ebook_index(library_path, subfolders, index_file)

if __name__ == "__main__":
    main()

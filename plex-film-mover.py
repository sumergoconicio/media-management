######
## Plex film renamer and mover
#### assumes that downloads have been pre-formatted for archival (with IMDb matched names and years... for my archival system anyway)
#### takes films from SOURCE folder to DESTINATION folder with an first-alphabet check
#### takes the first-alphabet of the folder to insert SOURCE/Aloha into DESTINATION/A/Aloha
###### if the first word is "A " or "The ", then it takes the first-alphabet of the second word
###### only moves files if a matching folder exists in the destination folder and/or that matching folder is empty (thus avoiding unexpected files or rewriting existing files)
#### creates a full CSV catalogue of the DESTINATION for easy matching (absolute_path, film_name, release_year, number_of_video_files (mp4/mkv format))
######

import os
import shutil
import csv
from datetime import datetime

def get_folder_path(prompt):
    """Ask user for folder input and ensure it's an absolute path"""
    folder_path = input(prompt)
    if not os.path.isabs(folder_path):
        print("Please provide an absolute path.")
        return get_folder_path(prompt)
    return folder_path

def create_film_index(destination, index_file):
    """Create an index of all destination subfolders and save as a CSV."""
    with open(index_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["absolute_folder_path", "film_name", "release_year", "number_of_video_files_with_mp4_or_mkv_extension"])

        for root, dirs, _ in os.walk(destination):
            for folder in dirs:
                absolute_path = os.path.join(root, folder)

                # Extract film name and release year
                film_name = folder
                release_year = ""
                if '(' in folder and ')' in folder:
                    try:
                        release_year = folder.split('(')[-1].split(')')[0]
                    except IndexError:
                        pass

                # Count video files with .mp4 or .mkv extensions in the folder
                if os.path.isdir(absolute_path):
                    video_file_count = len([f for f in os.listdir(absolute_path) if os.path.isfile(os.path.join(absolute_path, f)) and f.lower().endswith(('.mp4', '.mkv'))])
                    if video_file_count > 0:  # Only include folders with relevant files
                        writer.writerow([absolute_path, film_name, release_year, video_file_count])

    print(f"Index created at {index_file}")

def process_folders(source, destination):
    """Process the folders in the source directory based on the rules provided"""
    # Loop through each item in the source directory
    for subfolder_name in os.listdir(source):
        source_subfolder = os.path.join(source, subfolder_name)
        
        print(f"Now trying ^^{subfolder_name}^^...")
        # Check if it's a folder
        if os.path.isdir(source_subfolder):
            # Determine the first letter or special categorization
            if subfolder_name[0].isdigit():
                first_letter = "0-9"
            elif not subfolder_name[0].isascii():
                first_letter = "Ω"  # Greek letter Omega
            elif subfolder_name.lower().startswith("a "):
                words = subfolder_name.split()
                if len(words) > 1:
                    first_letter = words[1][0].lower()  # Get the first letter of the second word
            elif subfolder_name.lower().startswith("the "):
                words = subfolder_name.split()
                if len(words) > 1:
                    first_letter = words[1][0].upper()  # Get the first letter of the second word
            else:
                first_letter = subfolder_name[0].upper()
            
            destination_first_letter_folder = os.path.join(destination, first_letter)

            # If the subfolder is empty, delete it
            if not os.listdir(source_subfolder):
                print(f"{subfolder_name} folder is empty")
                print(f"Deleting empty subfolder: {source_subfolder}")
                os.rmdir(source_subfolder)
            else:
                # Check if the first letter folder exists in the destination
                if not os.path.exists(destination_first_letter_folder):
                    print(f"^^{first_letter}^^ folder does not exist in destination")
                else:
                    # Check if the subfolder with the same name exists in the first-letter folder of the destination
                    destination_subfolder = os.path.join(destination_first_letter_folder, subfolder_name)
                    
                    if not os.path.exists(destination_subfolder):
                        print(f"^^{subfolder_name}^^ folder does not exist in {destination_first_letter_folder}")
                    else:
                        # Check if the destination subfolder is empty
                        if not os.listdir(destination_subfolder):
                            print(f"Moving files from {source_subfolder} to {destination_subfolder}")
                            # Move files from source to destination subfolder
                            for file_name in os.listdir(source_subfolder):
                                source_file = os.path.join(source_subfolder, file_name)
                                destination_file = os.path.join(destination_subfolder, file_name)
                                shutil.move(source_file, destination_file)
                        else:
                            print(f"^^{subfolder_name}^^ is not empty in destination, skipping...")
            
def main():
    # Ask user for source and destination folder paths
    #source_folder = get_folder_path("Enter the absolute path for the SOURCE folder: ")
    #destination_folder = get_folder_path("Enter the absolute path for the DESTINATION folder: ")
    source_folder = "/volume1/downloads/complete/films"
    destination_folder = "/volume1/media/films"

    # Check if both source and destination paths exist
    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist.")
        return

    if not os.path.exists(destination_folder):
        print(f"Destination folder {destination_folder} does not exist.")
        return

    # Create destination index
    today = datetime.now().strftime("%Y%m%d")
    index_file = os.path.join(os.getcwd(), f"{today}_film_catalog.csv")
    create_film_index(destination_folder, index_file)

    # Process the folders
    process_folders(source_folder, destination_folder)

if __name__ == "__main__":
    main()

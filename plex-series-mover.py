import os
import shutil
import csv
from datetime import datetime

def create_destination_index(destinations, index_file):
    """Create an index of all destination subfolders and save as a CSV."""
    with open(index_file, mode='w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["absolute_folder_path", "show_name", "total_number_of_seasons", "total_number_of_episodes"])

        for destination in destinations:
            for root, dirs, _ in os.walk(destination):
                for show_folder in dirs:
                    show_path = os.path.join(root, show_folder)
                    season_count = 0
                    episode_count = 0

                    # Iterate through seasons and count episodes
                    for season_folder in os.listdir(show_path):
                        season_path = os.path.join(show_path, season_folder)
                        if os.path.isdir(season_path) and 'season' in season_folder.lower():
                            season_count += 1
                            episode_count += len([f for f in os.listdir(season_path) if os.path.isfile(os.path.join(season_path, f)) and f.lower().endswith(('.mp4', '.mkv'))])

                    if season_count > 0 or episode_count > 0:
                        writer.writerow([show_path, show_folder, season_count, episode_count])

    print(f"Index created at {index_file}")

def move_files(source, destinations):
    """Process the folders in the source directory and move files to the destinations."""
    for show_name in os.listdir(source):
        source_show_path = os.path.join(source, show_name)

        if os.path.isdir(source_show_path):
            for season_name in os.listdir(source_show_path):
                source_season_path = os.path.join(source_show_path, season_name)

                if os.path.isdir(source_season_path):
                    for destination in destinations:
                        destination_show_path = os.path.join(destination, show_name)
                        destination_season_path = os.path.join(destination_show_path, season_name)

                        # Check if the destination season folder exists
                        if os.path.exists(destination_season_path):
                            for file_name in os.listdir(source_season_path):
                                source_file = os.path.join(source_season_path, file_name)
                                destination_file = os.path.join(destination_season_path, file_name)

                                # Move file if it doesn't already exist
                                if not os.path.exists(destination_file):
                                    shutil.move(source_file, destination_file)
                                else:
                                    print(f"File already exists, skipping: {destination_file}")

def main():
    source_folder = "/volume1/downloads/complete/shows"
    destinations = [
        "/volume1/media/series",
        "/volume1/media/documentaries/seasons",
        "/volumeUSB6/usbshare/tv1",
        "/volumeUSB5/usbshare/tv2",
        "/volumeUSB3/usbshare/tv4",
        "/volumeUSB2/usbshare/anime",
        "/volumeUSB4/usbshare/dokumentaries"
    ]

    # Create destination index
    today = datetime.now().strftime("%Y%m%d")
    index_file = os.path.join(os.getcwd(), f"{today}_series_catalog.csv")
    create_destination_index(destinations, index_file)

    # Check source folder exists
    if not os.path.exists(source_folder):
        print(f"Source folder {source_folder} does not exist.")
        return

    # Process the source folder and move files
    move_files(source_folder, destinations)

if __name__ == "__main__":
    main()

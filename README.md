# media-management
personal python scripts to manage and catalog my media

### plex-film-mover
- assumes that downloads have been pre-formatted for archival (with IMDb matched names and years... for my archival system anyway)
- takes films from SOURCE folder to DESTINATION folder with an first-alphabet check
  - takes the first-alphabet of the folder to insert SOURCE/Aloha into DESTINATION/A/Aloha
    - if the first word is "A " or "The ", then it takes the first-alphabet of the second word
  - only moves files if a matching folder exists in the destination folder and/or that matching folder is empty (thus avoiding unexpected files or rewriting existing files)
  - creates a full CSV catalogue of the DESTINATION for easy matching (absolute_path, film_name, release_year, number_of_video_files (mp4/mkv format))
 

### plex-series-mover
- assumes that downloads have been pre-formatted for archival (with IMDb matched series titles, season folders and episode titles... for my archival system anyway)
- takes TVshows from SOURCE/Show-Name/Season X/Episode X folder to one of many possible DESTINATION folders as long as there is an existing/matching Show-Name folder
- creates a full CSV catalogue of the DESTINATION folders for easy matching (absolute_path, show_name, total_number_of_seasons, total_number_of_episodes) 


### calibre-ebook-cataloguer
- assumes ebook-libraries have been pre-formatted in Calibre's library structure
- assumes there are multiple ebook libraries in one overarching library folder
- creates a full CSV catalogue of the library (absolute_path, book_title, book_author, number of files, hasPDF (yes/no), hasEPUB (yes/no), hasMOBI (yes/no), hasCBR (yes/no), hasCBZ (yes/no))


### generic-folder-cataloguer
- basic skeleton script that asks for an absolute_path as input and creates a CSV catalogue of contents as output
- feel free to modiy logic and variables to fit your desired folder structure and metadata requirements

import os
import lyricsgenius

# Initialize the Genius API
genius = lyricsgenius.Genius('StYjV27r-2epV0-KBXDLhtAPZ8qI7qvwPFR0_GFZkKcFkJYfmoVXXPuA58WrT_dD')

# Read album names from the file
with open('albums.txt', 'r') as f:
    albums_raw = f.readlines()

# Strip whitespace from each album name
ALBUMS = [album.strip() for album in albums_raw]

# Create the data directory if it doesn't exist
os.makedirs('data', exist_ok=True)

DATA_PATH = 'data'

for album_name in ALBUMS:
    album = genius.search_album(album_name, "Willie Nelson")
    
    # Create a clean album directory name
    album_dir = os.path.join(DATA_PATH, album_name.replace(" ", "_").replace("/", "_"))
    os.makedirs(album_dir, exist_ok=True)

    for song in album.tracks:
        # Fetch the lyrics
        song_lyrics = song.song.lyrics

        # Clean the song title to use it as a file name
        clean_title = song.song.title.replace(" ", "_").replace("/", "_")

        # Write lyrics to a TXT file in the album directory
        file_path = os.path.join(album_dir, f"{clean_title}.txt")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(song_lyrics)

        print(f"Lyrics for {song.song.title} saved in {album_dir}.")

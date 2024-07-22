import os
import re
import json
import nltk
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from pprint import pprint

nltk.download('wordnet')
nltk.download('stopwords')

DATA_PATH = 'data'

def get_song_list(rel_song_path):
    """
    Inputs -- str: path to song
    Outputs -- list of stemmed and lemmatized words in the song, with stop words and specified tags removed
    """
    # Compile regex patterns
    tags_pattern = re.compile(r'[\*\[\]]')  # Matches *, [, or ]
    unwanted_pattern = re.compile(r'[^\w\s]|\d')  # Matches special characters (excluding letters and digits) and digits

    # Initialize stemmer and lemmatizer
    stemmer = PorterStemmer()
    lemmatizer = WordNetLemmatizer()
    
    # Get stop words from NLTK and convert to a set for faster lookups
    stop_words = set(stopwords.words('english'))

    weird_words = set(['willie', 'nelson', 'ticket', 'anymoreembed'])

    word_list = []
    try:
        with open(rel_song_path, 'r') as f:
            lyrics = f.readlines()  # Read all lines from the file
            # Process each line to filter out stop words, tags, unwanted patterns, and words with specific prefixes
            for line in lyrics:
                words = line.lower().split()  # Split the line into words
                # Filter out words that are stop words, match the tags pattern, unwanted patterns, or start with specific prefixes
                filtered_words = [word for word in words if word 
                                  not in (stop_words and weird_words) and
                                  not tags_pattern.search(word) and
                                  not unwanted_pattern.search(word) and
                                  not word.startswith('contribut')]
                
                # Stem and lemmatize the filtered words
                #stemmed_lemmas = [lemmatizer.lemmatize(stemmer.stem(word)) for word in filtered_words]
                word_list.extend(filtered_words)  # Add stemmed and lemmatized words to the list
    except FileNotFoundError:
        print(f"Error: The file at {rel_song_path} does not exist.")
    except IOError as e:
        print(f"Error reading file {rel_song_path}: {e}")

    return word_list

def get_song_word_counts(song_list):
    """
    Inputs -- list of words from a song
    Outputs -- dictionary with word counts
    """
    counts = {}
    for word in song_list:
        if word not in counts:
            counts[word] = 1
        else:
            counts[word] += 1
    return counts

def get_album_word_counts(album_dir):
    """
    Inputs -- str: path to album directory
    Outputs -- dictionary with word counts for the entire album
    """
    album_word_count = {}

    for root, dirs, files in os.walk(album_dir):
        for file in files:
            if file.endswith('.txt'):  # Assuming song files are in .txt format
                song_path = os.path.join(root, file)
                song_list = get_song_list(song_path)
                word_counts = get_song_word_counts(song_list)

                # Aggregate word counts for the album
                for word, count in word_counts.items():
                    if word not in album_word_count:
                        album_word_count[word] = count
                    else:
                        album_word_count[word] += count
    return album_word_count

def get_whole_word_counts(data_dir):
    """
    Inputs -- str: path to data directory containing album subdirectories
    Outputs -- dictionary with album names as keys and word counts as values
    """
    whole_word_counts = {}
    
    # Iterate over each subdirectory in the data directory
    for album_name in os.listdir(data_dir):
        album_path = os.path.join(data_dir, album_name)
        if os.path.isdir(album_path):
            print(f"Processing album: {album_name}")
            album_word_counts = get_album_word_counts(album_path)
            whole_word_counts[album_name] = album_word_counts
    
    return whole_word_counts

# Example usage
data_dir = 'data'  # Replace with your actual data directory path
whole_word_counts = get_whole_word_counts(data_dir)

# Write the dictionary to a JSON file
json_file_path = 'album_word_counts.json'
with open(json_file_path, 'w', encoding='utf-8') as json_file:
    json.dump(whole_word_counts, json_file, ensure_ascii=False, indent=4)

print(f"Word counts have been written to {json_file_path}.")

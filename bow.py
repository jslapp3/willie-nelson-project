

import pandas as pd
import numpy as np

def jsons_df(json_path):
    json_df = pd.read_json(json_path)
    json_df.fillna(0, inplace=True)
    json_df = json_df.astype(int)
    return json_df

print('\nBag of Words for Each Album:\n')
album_bow = jsons_df('album_word_counts.json')
album_bow.to_csv('bag_of_words.csv')
print(album_bow)

print('\nTotal Çareer Word Count\n')
full_word_counts = pd.DataFrame(album_bow.sum(axis=1), columns=['count']).sort_values('count', ascending=False)
full_word_counts.to_csv('career_word_counts.csv')
print(full_word_counts)

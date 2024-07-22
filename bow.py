

import pandas as pd
import numpy as np

def jsons_df(json_path):
    json_df = pd.read_json(json_path)
    json_df.fillna(0, inplace=True)
    json_df = json_df.astype(int)
    return json_df

print('\nDataframe of all words and their counts in each album:\n')
album_counts = jsons_df('album_word_counts.json')
full_word_counts = pd.DataFrame(album_counts.sum(axis=1), columns=['count']).sort_values('count', ascending=False)
print(full_word_counts)

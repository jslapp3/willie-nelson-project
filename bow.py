

import pandas as pd

json_df = pd.read_json('album_word_counts.json')

print('\nDataframe of all words and their counts in each album:\n')

print(json_df)
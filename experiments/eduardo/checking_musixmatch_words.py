import numpy as np
from song_lyrics.parse import load_json_data

words, track_ids, bows = load_json_data('data/clean/mxm_dataset.json')


idx2word = {idx: w for idx, w in enumerate(words)}

# this isnt matching...
np.where(['\x96' == w for w in words])

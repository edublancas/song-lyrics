from functools import reduce
import numpy as np
import pandas as pd
from langdetect import detect

d = pd.read_feather('data/transform/mxm_dataset_1000.feather')

words = np.array([word for word in list(d) if word != 'track_id'])


def detect_language(row):
    words_with_counts = words[row > 0]

    if len(words_with_counts):
        sentence = reduce(lambda x, y: x+' '+y, words_with_counts)
        return detect(sentence)
    else:
        return np.nan


language = d.loc[:, words].apply(detect_language, axis=1)
language
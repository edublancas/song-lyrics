"""
Clustering vocabulary using word embeddings
"""
import json
import numpy as np
from scipy.spatial import distance_matrix
import pandas as pd
from song_lyrics.parse import json_glove

glove = json_glove('data/clean/embeddings_subset.json')

words = list(glove.keys())
vectors = list(glove.values())

X = np.array(vectors)
df = pd.DataFrame(dict(word=words))
dist = distance_matrix(X, X)


def find_most_similar(word, dist, df, n=20):
    idx = df[df.word == word].index.values[0]
    most_similar = np.argsort(dist[idx, :])
    return df.word[most_similar][:n].tolist()


words = ['love', 'hate', 'war', 'beach', 'joy', 'life']

mapping = {word: find_most_similar(word, dist, df) for word in words}

with open('data/transform/topics.json', 'w') as f:
    json.dump(mapping, f)

import pandas as pd
import numpy as np


def bow2vector(bow, max_words):
    """Convert a dictionary bag-of-words representation to a numpy vector
    """
    vector = np.zeros(max_words)

    for idx, count in bow.items():

        idx = int(idx)

        if idx < max_words:
            vector[idx] = count

    return vector


def glovetxt2dict(path='glove.6B.50d.txt'):
    """Load word embeddings txt file and convert to a dictionary
    """
    with open(path) as f:
        glove = f.read().splitlines()

    def process_line(l):
        tokens = l.split()

        word = tokens[0]
        values = [float(val) for val in tokens[1:]]

        return word, np.array(values)

    mapping = {k: v for k, v in (process_line(l) for l in glove)}

    return mapping


def bow2embedding(bow, words, glove, max_words):
    """
    Replace counts in a bag of words representation with an embedding
    and convert it to a numpy vector
    """
    (dim,) = list(glove.values())[0].shape

    vector = np.zeros(dim)

    # parse bag of words and replace the word index with the dense vector
    # for the sum of [count in bag of words] * [embedding] for the
    # top max_words
    for idx, count in bow.items():

        idx = int(idx)

        if idx < max_words:
            word = words[idx]
            embedding = glove[word]
            vector = vector + count * embedding

    return vector


def bows2embeddings(bows, words, track_ids, glove, max_words):
    """Convert a list of bag of words into a data DataFrame
    """
    X = np.stack([bow2embedding(bow, words, glove, max_words=max_words)
                  for bow in bows], axis=0)
    df = pd.DataFrame(X, columns=words)
    df.insert(0, 'track_id', track_ids)

    return df

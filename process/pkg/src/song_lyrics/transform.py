import logging


import pandas as pd
import numpy as np

logger = logging.getLogger(__name__)


def bow2vector(bow, max_words):
    """Convert a dictionary bag-of-words representation to a numpy vector
    """
    vector = np.zeros(max_words)

    for idx, count in bow.items():

        idx = int(idx)

        if idx < max_words:
            vector[idx] = count

    return vector


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
    def _bow2embedding(*args, i, n, **kwargs):
        if i % 1000 == 0:
            logger.info('{:,} out of {:,}...'.format(i, n))
        return bow2embedding(*args, **kwargs)

    n = len(bows)

    X = np.stack([_bow2embedding(bow, words, glove, max_words=max_words,
                                 i=i, n=n)
                  for i, bow in enumerate(bows)], axis=0)
    df = pd.DataFrame(X)
    df.insert(0, 'track_id', track_ids)

    return df

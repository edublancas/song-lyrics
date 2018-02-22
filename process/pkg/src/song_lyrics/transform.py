import logging
from operator import itemgetter


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


def bow2embedding(bow, words, glove, max_words=None, global_max=False):
    """
    Replace counts in a bag of words representation with an embedding
    and convert it to a numpy vector

    Parameters
    ----------
    bow: dict
        Bag of words in {word_index: count} format

    words: list
        List of words

    glove: dict
        Word embeddings in {word: vector} format

    max_words: int, optional
        Maximum number of words to consider. Defaults to None, which means
        all words are used

    global_max: bool, optional
        If True, max_words is determined by the popularity in the whole
        corpus, that is, taking words[:max_words], if False max_words is
        taken into account within each bag of words, defaults to False.
    """
    # TODO: verify max_words and global_max featutres
    # TODO: add featutre toselect  specific words and cutoff in bag of words
    # instead of just measuring popularity

    dim = len(list(glove.values())[0])

    vector = np.zeros(dim)

    # sort bag of words
    bow_sorted = sorted([(int(idx), count) for idx, count in bow.items()],
                        key=itemgetter(1), reverse=True)
    ids = [t[0] for t in bow_sorted]

    # parse bag of words and replace the word index with the dense vector
    # for the sum of [count in bag of words] * [embedding]
    for idx, count in bow_sorted:

        if ((max_words and global_max and idx < max_words) or
           (max_words and not global_max and idx in ids[:max_words]) or
           (max_words is None)):
            word = words[idx]
            embedding = glove[word]
            vector = vector + count * embedding

    return vector


def bows2embeddings(bows, words, track_ids, glove, max_words, global_max):
    """
    Convert a list of bag of words into a data DataFrame, this is just
    a wrapper arounf bow2embedding to handle many objects and convert
    them to a pandas.DataFrame
    """
    def _bow2embedding(*args, i, n, **kwargs):
        if i % 1000 == 0:
            logger.info('{:,} out of {:,}...'.format(i, n))
        return bow2embedding(*args, **kwargs)

    n = len(bows)

    X = np.stack([_bow2embedding(bow, words, glove, max_words=max_words,
                                 global_max=global_max, i=i, n=n)
                  for i, bow in enumerate(bows)], axis=0)
    df = pd.DataFrame(X)
    df.insert(0, 'track_id', track_ids)

    return df

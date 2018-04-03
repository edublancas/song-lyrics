import logging
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


def bow2embedding(bow, glove):
    """
    Replace counts in a bag of words representation with an embedding
    and convert it to a numpy vector

    Parameters
    ----------
    bow: dict
        Bag of words in {word: value} format

    glove: dict
        Word embeddings in {word: vector} format
    """
    logger = logging.getLogger(__name__)

    dim = len(list(glove.values())[0])
    vector = np.zeros(dim)

    # parse bag of words and replace the word with the dense vector
    # for the sum of [count/proportion in bag of words] * [embedding]
    for word, value in bow.items():
        try:
            embedding = glove[word]
        except KeyError:
            logger.exception("Coulnd't find embedding for '{}', "
                             "ignoring word...".format(word))
        else:
            vector = vector + value * embedding

    return vector


def bows2embeddings(bows, track_ids, glove):
    """
    Convert a list of bag of words into a data DataFrame, this is just
    a wrapper arounf bow2embedding to handle many objects and convert
    them to a pandas.DataFrame
    """
    logger = logging.getLogger(__name__)

    def _bow2embedding(*args, i, n, **kwargs):
        if i % 1000 == 0:
            logger.info('{:,} out of {:,}...'.format(i, n))
        return bow2embedding(*args, **kwargs)

    n = len(bows)
    X = np.stack([_bow2embedding(bow=bow, glove=glove, i=i, n=n)
                  for i, bow in enumerate(bows)], axis=0)
    df = pd.DataFrame(X)
    df.insert(0, 'track_id', track_ids)

    return df

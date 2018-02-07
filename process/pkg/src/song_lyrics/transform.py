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

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


def make_word_embeddings(train, test, we, **kwargs):
    """Make word embeddings representation
    """
    # make unigrams and keep only the top 1000 (in terms of frequency)
    X_train_, X_test_, vectorizer = make_unigrams(train, test,
                                                  **kwargs)

    vecs = np.stack([we[word] for word in vectorizer.get_feature_names()],
                    axis=0)

    X_train = np.dot(X_train_, vecs)
    X_test = np.dot(X_test_, vecs)

    return X_train, X_test, vectorizer

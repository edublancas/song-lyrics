"""
Entity resolution between the words in the Musixmatch dataset and GLOVE
"""
import logging
from fuzzywuzzy import process
from fuzzywuzzy import fuzz


# TODO: add some tests
# x = ['c', 'a', 'a', 'b', 'a', 'j', 'z']
# x[find_interval(x, 'z')]
# x[find_interval(x, 'b')]
def find_interval(words, start):
    """
    Given a list of ordered words return the indexes for the first word that
    starts with certain character up until the first word (not included)
    that starts with another character
    """
    start_idx = None
    end_idx = None

    # find start idxs
    for idx, word in enumerate(words):
        if word.startswith(start):
            start_idx = idx
            break

    if start_idx is None:
        raise ValueError("Couldn't find word starting with '{}'"
                         .format(start, word, idx))

    # find end index
    for idx, word in enumerate(words[start_idx + 1:]):
        if not word.startswith(start):
            end_idx = 1 + idx + start_idx
            break

    if end_idx is None:
        end_idx = len(words)

    return slice(start_idx, end_idx)


def match(to_match, words_glove_sorted):
    """Build a mapping between words using fuzzy matching
    """
    logger = logging.getLogger(__name__)

    mapping = dict()

    for i, word in enumerate(to_match):

        try:
            idxs = find_interval(words_glove_sorted, word[0])
        except ValueError as e:
            logger.exception('Error finding interval in word "{}" (index {})'
                             ', setting match to None...'.format(word, i))
            mapping[word] = None
        else:
            match, score = process.extractOne(word, words_glove_sorted[idxs],
                                              scorer=fuzz.ratio)

            logger.info('Matched {} with {}, score: {}'.format(word, match,
                                                               score))

            mapping[word] = match

    return mapping

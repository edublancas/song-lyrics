"""
Entity resolution between the words in the Musixmatch dataset and GLOVE
"""
import logging

from fuzzywuzzy import process

from song_lyrics.parse import load_json_data, glovetxt2dict

logging.basicConfig(level=logging.INFO)


path_to_data = '../../data/clean/mxm_dataset.json'
path_to_glove = '../../data/raw/glove.6B/glove.6B.50d.txt'

# load word embeddings
glove = glovetxt2dict(path_to_glove)

# parse json data
words, track_ids, bows = load_json_data(path_to_data)

words_glove = set(glove.keys())
words_data = set(words)

logging.info('GLOVE contains {:,} words'.format(len(words_glove)))
logging.info('Musixmatch contains {:,} words'.format(len(words_data)))

# first find exact matches
both = words_data & words_glove
# now find the ones missing (we need to match this)
to_match = words_data - both

logging.info('Exact matches: {:,}'.format(len(both)))
logging.info('To match: {:,}'.format(len(to_match)))

words_glove_sorted = sorted(list(words_glove))


def find_interval(words, start):
    start_idx = None
    end_idx = None

    # find start idxs
    for idx, word in enumerate(words):
        if word.startswith(start):
            start_idx = idx
            break

    if start_idx is None:
        raise ValueError("Couldn't find word starting with {}".format(start))

    # find end index
    for idx, word in enumerate(words[start_idx + 1:]):
        if not word.startswith(start):
            end_idx = 1 + idx + start_idx
            break

    if end_idx is None:
        end_idx = len(words)

    return slice(start_idx, end_idx)


x = ['c', 'a', 'a', 'b', 'a', 'j', 'z']
x[find_interval(x, 'z')]
x[find_interval(x, 'b')]

word = list(to_match)[0]
word


idxs = find_interval(words_glove_sorted, word[0])

process.extractOne(word, words_glove_sorted[idxs])

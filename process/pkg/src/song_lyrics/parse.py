import numpy as np
import json


def song_line(line):
    """Parse one line

    Parameters
    ----------
    line: str
        One line in the musixmatch dataset

    Returns
    -------
    dict
        track_id: Million song dataset track id, track_id_musixmatch:
        Musixmatch track id and bag_of_words: Bag of words dict in
        {word: count} format

    Notes
    -----
    Musixmatch starts words at index 1, we are shifting it so it starts at 0
    """
    elements = line.split(',')
    track_id = elements[0]
    track_id_musixmatch = elements[1]
    bag_of_words = [s.split(':') for s in elements[2:]]
    # shift index so it starts at zero
    bag_of_words_dict = {int(idx) - 1: int(count) for idx, count
                         in bag_of_words}
    return dict(track_id=track_id, track_id_musixmatch=track_id_musixmatch,
                bag_of_words=bag_of_words_dict)


def load_json_data(path_to_data):

    with open(path_to_data) as f:
        data = json.loads(f.read())

    words = data['words']
    songs = data['songs']

    # get all track ids
    track_ids = [s['track_id'] for s in songs]

    # get all bag of words
    bows = [s['bag_of_words'] for s in songs]

    return words, track_ids, bows


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

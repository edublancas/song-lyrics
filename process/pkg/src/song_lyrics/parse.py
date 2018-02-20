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


def load_json_data(path_to_data, MAX_WORDS):

    with open(path_to_data) as f:
        data = json.loads(f.read())

    words = data['words'][:MAX_WORDS]
    songs = data['songs']

    # get all track ids
    track_ids = [s['track_id'] for s in songs]

    # get all bag of words
    bows = [s['bag_of_words'] for s in songs]

    return words, track_ids, bows

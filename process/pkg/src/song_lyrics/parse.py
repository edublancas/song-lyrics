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

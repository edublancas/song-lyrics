import numpy as np

N_WORDS = 5000

with open('mxm_dataset_train.txt') as f:
    lines = f.read().splitlines()

# first 16 lines are comments

# ignore first character (%) and split words
words_all = lines[17][1:].split(',')
lines_songs = lines[18:]

# shift index so it starts at zero
words = {idx - 1: w for idx, w in enumerate(words_all, 1)}
words


def parse_song_line(line):
    elements = line.split(',')
    track_id = elements[0]
    track_id_musixmatch = elements[1]
    bag_of_words = [s.split(':') for s in elements[2:]]
    # shift index so it starts at zero
    bag_of_words_dict = {int(idx) - 1: int(count) for idx, count
                         in bag_of_words}
    return track_id, track_id_musixmatch, bag_of_words_dict


songs = [parse_song_line(line) for line in lines_songs]


# how to reduce dimensionality?
# we don't really need the exact words, we can first cluster words
# using word embeddings and merge the most similar to avoid working with
# the 5,000 dimensions

def bow2vector(bow, max_words):
    """Bag of words to vector
    """
    vector = np.zeros(max_words)

    for idx, count in bow.items():
        if idx < max_words:
            vector[idx] = count

    return vector


track_ids = [s[0] for s in songs]
bows = [s[2] for s in songs]

X = np.stack([bow2vector(bow, max_words=50) for bow in bows], axis=0)
X = X.astype('int8')

np.savetxt('words.csv', X, delimiter=',')

track_ids

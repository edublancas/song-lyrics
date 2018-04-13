from random import sample
import pandas as pd

df = pd.read_feather('data/transform/bag_of_words_top_1000.feather')

selected = sample(list(df.artist_name_), 1000)
df = df[df.artist_name_.isin(selected)]

metadata = [col for col in df.columns if col.endswith('_')]
words = [col for col in df.columns if not col.endswith('_')]


def sum_words(df):
    sums = df[words].sum(axis=0)
    return sums


def top_k_words(artist, k=10):
    return artist.sort_values(ascending=False)[:k].to_dict()


def top_genres(artist, k=3):
    return list(artist.genre_
                      .value_counts()
                      .sort_values(ascending=False)[:k]
                      .index)


def songs_per_year(artist, k=3):
    d = artist.release_year_.value_counts().to_dict()
    return {int(k): v for k, v in d.items()}


def group_info(artist_name, mappings, new_keys):
    d = {}

    for mapping, key in zip(mappings, new_keys):
        d[key] = mapping[artist_name]

    return d


artists = df.artist_name_.unique()

# top 5 songs for each artist
top_5 = (df.groupby('artist_name_')
           .apply(sum_words)
           .apply(top_k_words, axis=1)
           .to_dict())

# number of songs per artist
n_songs = (df.groupby('artist_name_')
             .apply(lambda df: df.shape[0])
             .to_dict())


# genres
genres = (df.groupby('artist_name_')
            .apply(top_genres)
            .to_dict())

years = (df.groupby('artist_name_')
           .apply(songs_per_year)
           .to_dict())


data = {}

for artist in artists:
    data[artist] = group_info(artist, [top_5, n_songs, genres, years],
                              ['top_words', 'n_songs', 'top_genres', 'years'])

"""
Generate data for interactive component
"""
from random import sample
from scipy.spatial.distance import pdist, squareform
import pandas as pd

# load bag of words and embeddings
bow = pd.read_feather('data/transform/bag_of_words_top_1000.feather')
embeddings = pd.read_feather('data/transform/embeddings.feather')

selected = sample(list(bow.artist_name_), 1000)
bow = bow[bow.artist_name_.isin(selected)]

# columns corresponding to metadata, word counts and embeddings dimensions
metadata = [col for col in bow.columns if col.endswith('_')]
words = [col for col in bow.columns if not col.endswith('_')]
dims = [col for col in embeddings.columns if col.startswith('D')]


def sum_words(df):
    """Sum word columns in a DataFrame
    """
    sums = df[words].sum(axis=0)
    return sums


def top_k_words(artist, k=10):
    """Get top k words for an artist as {word: count} mapping
    """
    return artist.sort_values(ascending=False)[:k].to_dict()


def top_genres(artist, k=3):
    """Get list of top k genres
    """
    return list(artist.genre_
                      .value_counts()
                      .sort_values(ascending=False)[:k]
                      .index)


def songs_per_year(artist, k=3):
    """Get songs per year in a {year: count} mapping
    """
    d = artist.release_year_.value_counts().to_dict()
    return {int(k): v for k, v in d.items()}


def group_info(artist_name, mappings, new_keys):
    """Group artist info in a single mapping
    """
    d = {}

    for mapping, key in zip(mappings, new_keys):
        d[key] = mapping[artist_name]

    return d


def artist_distance(embeddings):
    """
    Given an embeddings, return a DataFrame with the distances between
    artists
    """
    embeddings_only = embeddings.loc[:, ['artist_name_'] + dims]
    artist_vectors = embeddings_only.groupby('artist_name_').mean()

    dist = squareform(pdist(artist_vectors.values))
    distances = pd.DataFrame(dist, index=artist_vectors.index,
                             columns=artist_vectors.index)

    return distances


def most_similar_artists(artist_name, distance_matrix, k=10):
    return list(distance_matrix[artist_name].sort_values()[1:k+1].index)


# get list of unique artists
artists = bow.artist_name_.unique()

# top 5 songs for each artist
top_5 = (bow.groupby('artist_name_')
         .apply(sum_words)
         .apply(top_k_words, axis=1)
         .to_dict())

# number of songs per artist
n_songs = (bow.groupby('artist_name_')
           .apply(lambda df: df.shape[0])
           .to_dict())

# top 3 genres
genres = (bow.groupby('artist_name_')
          .apply(top_genres)
          .to_dict())

# songs per year
years = (bow.groupby('artist_name_')
         .apply(songs_per_year)
         .to_dict())


# find most similar artists
distances = artist_distance(embeddings)
similar = {artist: most_similar_artists(artist, distances)
           for artist in artists}

# build dataset
data = {}

for artist in artists:
    data[artist] = group_info(artist, [top_5, n_songs, genres, years, similar],
                              ['top_words', 'n_songs', 'top_genres',
                               'years', 'similar_artists'])

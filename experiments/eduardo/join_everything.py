import pandas as pd

mxm = pd.read_feather('data/transform/mxm_dataset.feather')
mxm_tracks = mxm[['track_id']]

unique_tracks = pd.read_feather('data/transform/unique_tracks.feather')
unique_artists = pd.read_feather('data/transform/unique_artists.feather')
artist_location = pd.read_feather('data/transform/artist_location.feather')
tracks_per_year = pd.read_feather('data/transform/tracks_per_year.feather')


df = mxm_tracks.merge(unique_tracks, how='left', on='track_id')
df = df.merge(tracks_per_year[['track_id', 'year']], how='left')

df = df.merge(unique_artists[['artist', 'artist_id']], how='left',
              left_on='artist_name', right_on='artist')
df = df.merge(artist_location[['artist_id', 'latitude', 'longitude',
                               'location']], how='left', on='artist_id')

# ?
sum(df.artist_id.isna())

# save this
df.head()


df.year.value_counts()
df.location.value_counts()
df.artist_name.value_counts()

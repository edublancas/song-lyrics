import pandas as pd

location = pd.read_csv('subset_artist_location.txt', sep='<SEP>',
                       names=['artist_id', 'lat', 'long', 'track_id',
                              'artist'])

location[location.artist == 'Grand Funk']


per_year = pd.read_csv('subset_tracks_per_year.txt', sep='<SEP>',
                       names=['year', 'track_id', 'artist', 'song'])

per_year.head()

# some songs do not appear cause the do not have year information
per_year[per_year.track_id == 'TRAKZMB128F427B44F']

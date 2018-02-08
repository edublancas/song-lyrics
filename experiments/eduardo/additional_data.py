import pandas as pd

artist_location = pd.read_feather('artist_location.feather')
tracks_per_year = pd.read_feather('tracks_per_year.feather')
unique_artists = pd.read_feather('unique_artists.feather')
unique_tracks = pd.read_feather('unique_tracks.feather')

unique_tracks.head()

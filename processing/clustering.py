"""
python -m bnpy.Run /path/to/dataset.csv DPMixtureModel Gauss VB --K 8
"""
import numpy as np
from sklearn.cluster import KMeans

kmeans = KMeans(n_clusters=15, random_state=0).fit(X)

(idxs, ) = np.where(kmeans.labels_ == 3)

track_ids = pd.Series(track_ids)

track_ids[idxs]

X_small = X[idxs, :]
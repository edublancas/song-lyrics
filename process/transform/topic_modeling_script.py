#!/usr/bin/env python

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm

print('Load bag_of_words_top_1000.feather')
bag_of_words_top_1000 = pd.read_feather('../../data/transform/bag_of_words_top_1000.feather')


def corpus_topics_top_words(model, features, no_top_words):
    topic_dict = {}
    for topic_idx, topic in enumerate(model.components_):
        topic_dict[topic_idx] = [features[i] for i in topic.argsort()[:-no_top_words - 1:-1]]
    return topic_dict

def song_topics(model, song):
    topic_dict = []
    for topic_idx, topic in enumerate(model.components_):
        topic_dict.append(sum(topic*song))
    return topic_dict


print('Identify topics within model')
from sklearn.decomposition import LatentDirichletAllocation

mxm_25_top1000 = LatentDirichletAllocation(n_topics=25, random_state=0)
mxm_25_top1000.fit(bag_of_words_top_1000.iloc[:,16:])


print('Identify per/song topic weights')
top_per_topic_words = corpus_topics_top_words(mxm_25_top1000,bag_of_words_top_1000.iloc[:,16:].columns.values, 10)

#save per/song topic results to df
song_topic_weights = np.zeros([len(bag_of_words_top_1000.iloc[:,16:]),25])
temp = bag_of_words_top_1000.iloc[:,16:]
for i in tqdm(range(len(bag_of_words_top_1000))):
    song_weights = pd.Series(song_topics(mxm_25_top1000, temp.iloc[i]))
    song_topic_weights[i] = song_weights


initial_topic_names = list(range(25))
song_topic_weights_df = pd.DataFrame(data =song_topic_weights, columns=initial_topic_names)
song_topic_weights_df['track_id'] = bag_of_words_top_1000['track_id_']
df_topic_weights_reduced_df = song_topic_weights_df[['track_id',11,15,20]]
df_topic_weights_reduced_df.columns = 'track_id', 'love','death','religion'


#Top words in each topic
topic_words = {}
topic_words['love'] = top_per_topic_words[11]
topic_words['death'] = top_per_topic_words[15]
topic_words['religion'] = top_per_topic_words[20]
print(topic_words)


bag_of_words_top_1000['love'] = df_topic_weights_reduced_df['love']
bag_of_words_top_1000['religion'] = df_topic_weights_reduced_df['religion']
bag_of_words_top_1000['death'] = df_topic_weights_reduced_df['death']


# # Transform

original_top_1000 = pd.read_feather('../../data/transform/bag_of_words_top_1000.feather')

bag_of_words_top_1000_topics = bag_of_words_top_1000


#scale by word count
bag_of_words_top_1000_topics['sum'] = original_top_1000.iloc[:,16:].sum(axis=1)
bag_of_words_top_1000_topics['love'] = bag_of_words_top_1000_topics['love']/bag_of_words_top_1000_topics['sum']
bag_of_words_top_1000_topics['religion'] = bag_of_words_top_1000_topics['religion']/bag_of_words_top_1000_topics['sum']
bag_of_words_top_1000_topics['death'] = bag_of_words_top_1000_topics['death']/bag_of_words_top_1000_topics['sum']
bag_of_words_top_1000_topics.drop('sum', axis=1, inplace=True)


#rank and scale between 0 and 1
rank_order = np.array(range(len(bag_of_words_top_1000_topics)))/(len(bag_of_words_top_1000_topics)-1)

bag_of_words_top_1000_topics = bag_of_words_top_1000_topics.sort_values(by='religion')
bag_of_words_top_1000_topics = bag_of_words_top_1000_topics.reset_index(drop=True)
bag_of_words_top_1000_topics['religion'] = rank_order

bag_of_words_top_1000_topics = bag_of_words_top_1000_topics.sort_values(by='death')
bag_of_words_top_1000_topics = bag_of_words_top_1000_topics.reset_index(drop=True)
bag_of_words_top_1000_topics['death'] = rank_order

bag_of_words_top_1000_topics = bag_of_words_top_1000_topics.sort_values(by='love')
bag_of_words_top_1000_topics = bag_of_words_top_1000_topics.reset_index(drop=True)
bag_of_words_top_1000_topics['love'] = rank_order


#yearly topics
print('Identify topic weights each year')
bag_with_year = bag_of_words_top_1000_topics[bag_of_words_top_1000_topics['release_year_'].notnull()].reset_index()

weights_yearly_clean = {}
weights_yearly_clean['song_count'] = [0] * len(bag_with_year['release_year_'].unique())
weights_yearly_clean['love'] = [0] * len(bag_with_year['release_year_'].unique())
weights_yearly_clean['death'] = [0] * len(bag_with_year['release_year_'].unique())
weights_yearly_clean['religion'] = [0] * len(bag_with_year['release_year_'].unique())
weights_yearly_clean['year'] = [0] * len(bag_with_year['release_year_'].unique())

for i, val in enumerate(bag_with_year['release_year_'].unique()):
    temp = bag_with_year[bag_with_year['release_year_']==val]
    weights_yearly_clean['song_count'][i] = len(temp)
    weights_yearly_clean['year'][i] = val
    weights_yearly_clean['love'][i] = temp.love.mean()
    weights_yearly_clean['death'][i] = temp.death.mean()
    weights_yearly_clean['religion'][i] = temp.religion.mean()

topics_per_year = pd.DataFrame(weights_yearly_clean).sort_values(by='year').reset_index(drop=True)


#artist weights
print('Identify topic weights for each artist ()')
weights_artist_clean = {}
weights_artist_clean['love'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())
weights_artist_clean['death'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())
weights_artist_clean['religion'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())
weights_artist_clean['artist_id'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())
weights_artist_clean['artist_name'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())
weights_artist_clean['longitude'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())
weights_artist_clean['latitude'] = [0] * len(bag_of_words_top_1000_topics.artist_id_.unique())

for i, val in tqdm(enumerate(bag_of_words_top_1000_topics.artist_id_.unique())):
    temp = bag_of_words_top_1000_topics[bag_of_words_top_1000_topics.artist_id_==val]
    weights_artist_clean['artist_id'][i] = val
    weights_artist_clean['artist_name'][i] = temp.artist_name_.iloc[0]
    weights_artist_clean['longitude'][i] = temp.longitude_.iloc[0]
    weights_artist_clean['latitude'][i] = temp.latitude_.iloc[0]
    weights_artist_clean['love'][i] = temp.love.mean()
    weights_artist_clean['death'][i] = temp.death.mean()
    weights_artist_clean['religion'][i] = temp.religion.mean()

topics_per_artist = pd.DataFrame(weights_artist_clean).sort_values(by='artist_name').reset_index(drop=True)

topics_per_artist.to_feather('../../data/transform/artist_topic_weights.feather')
topics_per_year.to_feather('../../data/transform/year_topic_weights.feather')


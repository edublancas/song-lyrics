# Load utility functions
source('lib/functions.R')

# Set the working directory to the current directory
setwd('./')

# Required packages
packages<-c('feather','tidyverse','data.table','tidytext', 'stringr')

# Load required pakages (install and load if packages is not currently installed)
print('Loading required packages')
installNeededPackages(packages)

# Read the final songs dataset feather file
print('Reading bag_of_words_clean.feather')
songsDataClean<-read_feather('data/transform/bag_of_words.feather')

# Wrangle the songDataClean to get the words for each artist and convert to data.table
print('Getting words per artist')
artist_words<-songsDataClean %>% select(16:ncol(songsDataClean)) %>% 
  filter(!is.na(artist_id_) & str_trim(artist_id_)!='') %>%
  group_by(artist_id_) %>% 
  summarise_all(sum) %>% ungroup() %>% gather(word,freq,-artist_id_) %>% 
  data.table(key='freq') %>% filter(freq>0) %>% data.table(key='word')

# Get the afinn lexicon sentiments and convert them to a data.table
print('Getting affin lexicon sentiments')
sentiments<-data.table(get_sentiments('afinn'),key='word')

# Inner join artist word data set with the sentiments dataset
print('Joining artist words with the sentiments')
artist_word_sentiment <- artist_words[sentiments,nomatch=0]

# Get the average sentiment per artist and write it to file
print('Calculating mean sentiment score per artist')
setkey(artist_word_sentiment,artist_id_)
artist_sentiment<-artist_word_sentiment[,list(meanScore=sum(score*freq)/sum(freq)),by=list(artist_id_)]

# Write result to disk
print('Writing result to data/transform/artist_sentiment_mean_score.feather')
write_feather(artist_sentiment,'data/transform/artist_sentiment_mean_score.feather')

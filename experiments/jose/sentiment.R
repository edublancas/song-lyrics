require(data.table)
require(dplyr)
require(stringr)
require(tidytext)
require(feather)

setwd('~/Documents/DataScience/Classes/Visualization/song-lyrics/')
words<-read_feather('data/transform/mxm_dataset.feather')
track<-read_feather('data/transform/unique_tracks.feather')
artist<-read_feather('data/transform/artist_location.feather')
year<-read_feather('data/transform/tracks_per_year.feather')
genre<-read.table('~/Documents/msd_beatunes_map_genre.cls',header = FALSE,stringsAsFactors = FALSE,sep = '$',quote = '?')
names(genre)<-c('track_id','genre')
names(year)[1]<-'released_year'

songsData <- track %>% left_join(genre) %>% left_join(year[,1:2]) %>% inner_join(words)

with(wordcloud::wordcloud(songsData,freq,max.words = 200))

unwords_df<-data.frame(id=2:ncol(words),word=names(words)[-1],stringsAsFactors = FALSE)
words_df_clean<-words_df %>% anti_join(stop_words) %>% inner_join(sentiments)
words_clean<-words[,c(1,unique(words_df_clean$id))]

words_clean %>% select(-1) %>% summarise_all(sum) %>% tidyr::gather(key=word,value=freq) %>%
with(wordcloud::wordcloud(word,freq,max.words = 200))


stop_words_dt<-data.table(stop_words,key='word')
tidyWords<-words %>% tidyr::gather(key=word,value=freq,-track_id) %>% data.table(key = word)
tidyWordsClean<-tidyWords[!stop_words_dt]
dim(sentiments)

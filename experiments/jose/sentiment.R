require(feather)
require(scales)
require(stringr)
require(tidyverse)
require(ggplot2)
require(tidytext)
require(data.table)

setwd('~/Documents/DataScience/Classes/Visualization/song-lyrics/')

songsDataClean <- read_feather('data/transform/bag_of_words_clean.feather')

songsDataEng <- songsDataClean %>% filter(language_=='en')

wordCount <- songsDataEng %>% select(-c(1:16)) %>% summarise_all(sum)
  
songsDataEng <- songsDataEng %>% select(-which(wordCount==0)+16)


songsDataEng %>% select(-c(1:16)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
  with(wordcloud::wordcloud(words,freq,max.words = 200))

wordsClean<- data.frame(id=8:ncol(songsDataEng),word=names(songsDataEng[-c(1:7)]),stringsAsFactors = FALSE) %>% anti_join(stop_words)

songsDataEngClean<-songsDataEng[,c(1:7,unique(wordsClean$id))]

songsDataEngClean %>% select(-c(1:7)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
with(wordcloud::wordcloud(words,freq,max.words = 200))

songsDataEngClean %>% select(-c(1:7)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
  with(wordcloud::wordcloud(words,freq,max.words = 200))

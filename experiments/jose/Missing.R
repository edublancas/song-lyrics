require(feather)
require(scales)
require(stringr)
require(tidyverse)
require(ggplot2)
require(tidytext)

setwd('~/Documents/DataScience/Classes/Visualization/song-lyrics/')

songsData<-read_feather('data/transform/bag_of_words.feather')
language<-read_feather('data/transform/language.feather')

metadata<-select(songsData,1:16)
names(metadata)<-gsub('_$','',names(metadata))
metadata %>% summarise_all(function(x){sum(is.na(x) | str_trim(x)=='')/length(x)}) %>% 
  gather(key = Variable,value=Missing) %>%
  ggplot(aes(reorder(Variable,-Missing),Missing)) + geom_col(fill='lightblue',colour='black') + scale_y_continuous(labels = percent) +
  labs(x='Variables',y='Missing Values') + coord_flip() + 
  geom_text(aes(label=paste0(round(Missing*100,1),'%')),hjust=-.1,size=3)

extracat::visna(metadata,sort = 'b')

metadata %>% select(language,artist_mbid,location,release_year,genre) %>% group_by(language) %>% 
  summarise_all(function(x){sum(is.na(x))/length(x)}) %>% ungroup() %>% 
  gather(variable,missing_rate,-language) %>% 
  ggplot(aes(y=language,x=variable,fill=missing_rate)) + geom_tile(colour='white') + 
  theme_bw() + scale_fill_gradientn(name="Missing Rate",labels=percent,
                                    colours = c('lightyellow','yellow','orange','darkred'))

wordList<-read.table('data/raw/mxm_reverse_mapping_new.txt',sep = '|',header = FALSE,stringsAsFactors = FALSE,quote = '"')
names(wordList)<-c('steammedWord','unsteammedWord')
wordList$unsteammedWord<-str_trim(wordList$unsteammedWord)
steammedWords<-data.frame(id=2:ncol(musicXmatch),steammedWord=names(musicXmatch)[-1],stringsAsFactors = FALSE)

songsDataEng <- songsData %>% filter(language_=='en')

wordCount <- songsDataEng %>% select(-c(1:16)) %>% summarise_all(sum)

songsDataEng <- songsDataEng %>% select(-c(which(wordCount==0)+16))

songsDataEng %>% select(-c(1:16)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
  with(wordcloud::wordcloud(words,freq,max.words = 300))

wordsClean<- data.frame(id=17:ncol(songsDataEng),word=names(songsDataEng[-c(1:16)]),
                        stringsAsFactors = FALSE) %>% anti_join(stop_words)

songsDataEngClean<-songsDataEng[,c(1:16,unique(wordsClean$id))]

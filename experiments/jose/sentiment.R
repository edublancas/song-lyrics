require(feather)
require(scales)
require(stringr)
require(tidyverse)
require(tidytext)
require(data.table)
require(reshape2)

setwd('~/Documents/DataScience/Classes/Visualization/song-lyrics/')

songsDataClean <- read_feather('data/transform/bag_of_words_clean.feather')

songsDataEng <- songsDataClean %>% filter(language_=='en')

wordCount <- songsDataEng %>% select(-c(1:16)) %>% summarise_all(sum)

songsDataEng <- songsDataEng %>% select(-which(wordCount==0)+16)

# word cloud
songsDataEng %>% select(-c(1:16)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
  with(wordcloud::wordcloud(words,freq,max.words = 200))

# Word cloud with sentiment
songsDataClean %>% select(-c(1:16)) %>% summarise_all(sum) %>% 
  tidyr::gather(key=word,value=freq) %>% inner_join(get_sentiments('bing')) %>% 
  acast(word ~ sentiment,value.var = 'freq') %>% apply(2,function(x){ifelse(is.na(x),0,x)}) %>%
  wordcloud::comparison.cloud(colors = c("#F8766D", "#00BFC4"),max.words = 100,random.order = F)

# Sentiment per year
songsDataClean %>% select(9,17:ncol(songsDataEng)) %>% filter(!is.na(release_year_)) %>% 
  group_by(release_year_) %>% summarise_all(sum) %>% ungroup() %>%
  tidyr::gather(key=word,value=freq,-release_year_) %>% filter(freq>0) %>%
  inner_join(get_sentiments('nrc')) %>%
  group_by(release_year_,sentiment) %>% summarise(freq=sum(freq)) %>%
  ggplot(aes(x=release_year_,y=(freq)/1000,group=sentiment,colour=fct_reorder(sentiment,freq,.desc = TRUE))) + 
    xlim(1960,2010) + geom_line() + theme_bw() + 
    labs(colour='Sentiment',y='Frequency (Thousands)',x='Song Release Year')

# Sentiment per year faceted by 15 most frequent genres in dataset
songsDataClean %>% select(9,10,17:ncol(songsDataEng)) %>% 
  filter(!is.na(release_year_) & genre_ %in% names(sort(table(songsDataClean$genre_),decreasing = TRUE)[1:15])) %>% 
  group_by(genre_,release_year_) %>% summarise_all(sum) %>% ungroup() %>%
  tidyr::gather(key=word,value=freq,-genre_,-release_year_) %>% filter(freq>0) %>%
  inner_join(get_sentiments('nrc')) %>%
  group_by(genre_,release_year_,sentiment) %>% summarise(freq=sum(freq)) %>%
  ggplot(aes(x=release_year_,y=freq,group=sentiment,colour=fct_reorder(sentiment,freq,.desc = TRUE))) + 
    xlim(1960,2010) + geom_line() + theme_bw() +
    labs(colour='Sentiment',y='Frequency (Thousands)',x='Song Release Year') +
    facet_wrap(~genre_,scales = 'free_y',ncol = 3)

genrePopularArtist<-songsDataEng %>% filter(genre_ %in% names(sort(table(songsDataClean$genre_),decreasing = TRUE)[1:15])) %>%
  select(7,10,15:ncol(songsDataEng)) %>%
  plyr::ddply(.variables='genre_',
               .fun=function(x)
                {
                  y <- x %>% group_by(artist_id_) %>% summarise(popularity=max(artist_familiarity_)) %>%
                    arrange(desc(popularity))
                  y <- y[1:10,'artist_id_',drop=FALSE]
                  return(inner_join(x,y,by='artist_id_'))
                }
              ) %>% tidyr::gather(key=word,value=freq,-c(1:4)) %>% filter(freq>0) %>%
  inner_join(get_sentiments('afinn')) %>% group_by(genre_,artist_id_,artist_name_) %>%
  summarise(meanSentiment=sum(freq*score)/sum(freq))

ggplot(genrePopularArtist,aes(y=meanSentiment,x=artist_name_)) + geom_point(size=2) + 
    coord_flip() + facet_wrap(~genre_,scales = 'free_y',ncol = 2) + theme_bw() + 
    theme(panel.grid.major.y=element_blank()) + geom_segment(aes(xend=artist_name_),yend=-4)
  


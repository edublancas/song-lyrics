require(data.table)
require(dplyr)
require(stringr)
require(tidytext)
require(feather)
require(ggplot2)
require(scales)
require(textcat)

setwd('~/Documents/DataScience/Classes/Visualization/song-lyrics/')

musicXmatch<-read_feather('data/transform/mxm_dataset.feather')
msd<-read_feather('data/transform/unique_tracks.feather')
#artist<-read_feather('data/transform/artist_location.feather')
msdYear<-read_feather('data/transform/tracks_per_year.feather')
tagtraum<-read.table('~/Documents/msd_beatunes_map_genre.cls',header = FALSE,stringsAsFactors = FALSE,sep = '$',quote = '?')
names(tagtraum)<-c('track_id','genre')
names(msdYear)[1]<-'released_year'
wordList<-read.table('experiments/jose/mxm_reverse_mapping_new.txt',sep = '|',header = FALSE,stringsAsFactors = FALSE,quote = '"')
names(wordList)<-c('steammedWord','unsteammedWord')
wordList$unsteammedWord<-str_trim(wordList$unsteammedWord)
steammedWords<-data.frame(id=2:ncol(musicXmatch),steammedWord=names(musicXmatch)[-1],stringsAsFactors = FALSE)
unsteammedWords<-steammedWords %>% inner_join(wordList)
difference<-unsteammedWords[unsteammedWords$steammedWord != unsteammedWords$unsteammedWord,]
difference[grep("'$",difference$unsteammedWord),3]<-str_replace(difference[grep("'$",difference$unsteammedWord),3],pattern = "'",'g')
difference[difference$unsteammedWord=="'em",3]<-'them'
difference[difference$unsteammedWord=="'til",3]<-'until'
difference[difference$unsteammedWord=="'bout",3]<-'about'
difference[difference$unsteammedWord=="'fore",3]<-'before'
unsteammedWords[unsteammedWords$id %in% difference$id,3]<-difference[,3]
names(musicXmatch)[2:5001]<-unsteammedWords$unsteammedWord

millionSongs <- msd %>% left_join(msdYear[,1:2]) %>% left_join(tagtraum)

millionSongs %>% summarise_all(function(x){sum(is.na(x) | str_trim(x)=='')/nrow(millionSongs)}) %>% tidyr::gather(key = Variable,value=Missing) %>%
  ggplot(aes(reorder(Variable,-Missing),Missing)) + geom_col(fill='lightblue',colour='black') + geom_text(aes(label=paste0(round(Missing*100,3),'%')),vjust=-.2) + scale_y_continuous(labels = percent) +
  labs(x='Variables',y='Missing Values')

songsData <- millionSongs %>% inner_join(musicXmatch)
songsData$inputedLanguage<-NA

detectLanguage<-function(row){
  wordCols<-which(row[7:5006]>0)+6
  words<-names(songsData)[wordCols]
  sentence<-paste(words,collapse = ' ')
  return(cld2::detect_language(sentence))
}
for(i in 1:nrow(songsData)){
  if(is.na(songsData[i,5007])){
    songsData[i,5007]<-detectLanguage(songsData[i,])
  }
  print(i)
}

songsData <- songsData[,c(1:6,5007,7:5006)]

write_feather(songsData,'experiments/jose/songsData.feather')

songsDataEng <- songsData %>% filter(language=='en')

wordCount <- songsDataEng %>% select(-c(1:7)) %>% summarise_all(sum)
  
songsDataEng <- songsDataEng %>% select(-which(wordCount==0)+7)


songsDataEng %>% select(1:6) %>% summarise_all(function(x){sum(is.na(x) | str_trim(x)=='')/nrow(millionSongs)}) %>% tidyr::gather(key = Variable,value=Missing) %>%
  ggplot(aes(reorder(Variable,-Missing),Missing)) + geom_col(fill='lightblue',colour='black') + geom_text(aes(label=paste0(round(Missing*100,1),'%')),vjust=-.2) + scale_y_continuous(labels = percent) +
  labs(x='Variables',y='Missing Values')

songsDataEng %>% select(-c(1:7)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
  with(wordcloud::wordcloud(words,freq,max.words = 300))

wordsClean<- data.frame(id=8:ncol(songsDataEng),word=names(songsDataEng[-c(1:7)]),stringsAsFactors = FALSE) %>% anti_join(stop_words)

songsDataEngClean<-songsDataEng[,c(1:7,unique(wordsClean$id))]

songsDataEngClean %>% select(-c(1:7)) %>% summarise_all(sum) %>% tidyr::gather(key=words,value=freq) %>%
with(wordcloud::wordcloud(words,freq,max.words = 200))

stop_words_dt<-data.table(stop_words,key='word')
tidyWords<-words %>% tidyr::gather(key=word,value=freq,-track_id) %>% data.table(key = word)
tidyWordsClean<-tidyWords[!stop_words_dt]
dim(sentiments)

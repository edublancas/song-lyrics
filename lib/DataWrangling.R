# Set the working directory to the current directory
setwd('./')

# Load utility functions
source('lib/functions.R')

# Required packages
packages<-c('feather','tidytext','stringr','tidyverse')

# Load required pakages (install and load if packages is not currently installed)
print('Loading required packages')
installNeededPackages(packages)

# Read the final songs dataset feather file
print('Reading bag_of_words.feather')
songsData<-read_feather('data/transform/bag_of_words.feather')

# Dataset with the list of words as rows
words<-data.frame(id=17:ncol(songsData),word=names(songsData)[-c(1:16)],stringsAsFactors = FALSE)

# Cleaning some of the words
print('Cleaning words')
words[grep("'$",words$word),2]<-str_replace(words[grep("'$",words$word),2],pattern = "'",'g')
words[words$word=="'em",2]<-'them'
words[words$word=="'til",2]<-'until'
words[words$word=="'bout",2]<-'about'
words[words$word=="'fore",2]<-'before'
words[words$word=="'cause",2]<-'because'

# Removing stop words
print('Removing stop words')
words <- words %>% anti_join(stop_words,by='word')
songsDataClean <- songsData[,c(1:16,words$id)]
names(songsDataClean)[17:ncol(songsDataClean)]<-words$word

# Dealing with repeated words
print('Dealing with repeated words')
repeatedWords<-names(songsDataClean)[duplicated(names(songsDataClean))]
for(w in repeatedWords){
  index<-grep(w,names(songsDataClean)) 
  songsDataClean[index[1]]<-apply(songsDataClean[,index],1,sum)
  songsDataClean[index[-1]]<-NULL
}

# Save file to disk
print('Saving result to data/transform/bag_of_words_clean.feather')
write_feather(songsDataClean,'data/transform/bag_of_words_clean.feather')
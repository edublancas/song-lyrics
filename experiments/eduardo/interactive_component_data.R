library(feather)
library(dplyr)

sum_words <- function(df, cols){
    data.frame(t(colSums(df[, cols])))
}

df <- read_feather('data/transform/bag_of_words_top_1000.feather')

selected <- sample(unique(df$artist_name_), 100)
df <- df %>% filter(artist_name_ %in% selected)

columns <- colnames(df)
columns_metadata <- columns[endsWith(columns, '_')]
columns_lyrics <- columns[!endsWith(columns, '_')]

by_artist <- df %>% group_by(artist_name_)


sums <- by_artist %>% do(sum_words(., columns_lyrics))

get_top_words <- function(df, k=20){
    counts <- as.numeric(w[, 2:nrow(df)])
    indexes <- order(counts, decreasing=TRUE)[1:k]

    words <-colnames(w)[indexes]
    top <- counts[indexes]

    return(top)
}


names(top) <- words

# number of songs
n_songs <- by_artist %>% summarize(n = n()) %>%
            arrange(desc(n)) %>%
            mutate(rank = dense_rank(desc(n)))

# top words
# most similar artists
# songs per year
# metadata: genre (table with songs by genre), location, language (table)

head(per_artist_songs, 20)

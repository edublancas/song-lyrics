library(feather)
library(dplyr)

# columns to use for grouping: year, genre (only top), artist (only top),
# duration also use track_id for distances

bow <- read_feather('data/transform/bag_of_words_top_100.feather')

genres_ <- table(bow$genre_)

length(genres_[genres_ >= 10])


bow %>% group_by(genre_) %>% summarise(n=n())

sort(table(bow$genre_), decreasing=TRUE)[0:10]

# TODO: check artist_name vs artist_id
length(unique(bow$artist_id_))
length(unique(bow$artist_name_))

head(bow)
colnames(bow)

apply_to_words <- function(df, fn, threshold){
    if(nrow(df) >= threshold){
        df_words <- select(df, -ends_with('_'))
        return(data.frame(t(fn(df_words))))
    }

    return(data.frame())
}


# group and summarize operations (sum, mean)

res <- bow %>% group_by(release_year_) %>% do(apply_to_words(., colMeans))

genre_means <- bow %>% group_by(genre_) %>% do(apply_to_words(., colMeans, 10))
artist_means <- bow %>% group_by(artist_name_) %>% do(apply_to_words(., colMeans, 10))

dim(res)
head(res)
head(res_)

# compute a distances matrix
distances <- function(df, row_names){
    df <- data.frame(df)
    df <- df[!is.na(df[[row_names]]), ]
    rownames(df) <- df[[row_names]]
    m <- as.matrix(dist(df, diag=TRUE, upper=TRUE))
    return(m)
}

closest <- function(m, row_name, n) sort(m[row_name, ])[0:n]
farest <- function(m, row_name, n) sort(m[row_name, ], decreasing=TRUE)[0:n]

m <- distances(res, 'release_year_')
m['1925', '1924']

closest(m, '1924', 5)
farest(m, '1924', 5)


# distance matrix of artists is too big.. maybe filter by artists with > x
# songs?
m_ <- distances(artist_sum, 'artist_name_')


m <- distances(genre_means, 'genre_')
closest(m, 'Rock', 10)
farest(m, 'Rock', 10)

m <- distances(artist_means, 'artist_name_')
closest(m, 'Pink Floyd', 20)
farest(m, 'Pink Floyd', 10)

# top words for artist
artist <- data.frame(filter(artist_means, artist_name_ == 'Oasis'))
artist <- as.numeric(artist[1, 2:101])
names(artist) <- colnames(artist_means[1, 2:101])
sort(artist, decreasing=TRUE)


d <- filter(bow, artist_name_ == 'Oasis', title_ == 'Songbird')
t(select(d, -ends_with('_')))

filter(bow, artist_name_ == 'Oasis', tu > 0)$tu
filter(bow, artist_name_ == 'Oasis', tu > 0)$title_


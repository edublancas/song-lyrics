library(feather)
library(dplyr)

# columns to use for grouping: year, genre, artist, duration
# also use track_id for distances
# TODO: check artist_name vs artist_id

bow <- read_feather('data/transform/bag_of_words_top_100.feather')

head(bow)
colnames(bow)

apply_to_words <- function(df, fn){
    df_words <- select(df, -ends_with('_'))
    data.frame(t(fn(df_words)))
}


# group and summarize operations (sum, mean)
artist_sum <- bow %>% group_by(artist_name_) %>% do(apply_to_words(., colSums))

res <- bow %>% group_by(release_year_) %>% do(apply_to_words(., colMeans))
res_ <- bow %>% group_by(release_year_) %>% do(apply_to_words(., colSums))

res <- bow %>% group_by(genre_) %>% do(apply_to_words(., colSums))

head(res)
head(res_)

# compute a distances matrix
distances <- function(df, row_names){
    df <- data.frame(df)
    df <- df[!is.na(res$release_year_), ]
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


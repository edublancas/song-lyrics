library(rjson)

# compute distances matrix from the embeddings json file
embeddings_distances <- function(path_to_embeddings){
    # load data
    embeddings <- fromJSON(file=path_to_embeddings)
    embeddings <- lapply(embeddings, as.numeric)
    dimensions <- length(embeddings[[1]])
    words <- names(embeddings)

    # convert data to a matrix where every row is the embedding for a word
    m <- t(matrix(unlist(embeddings), nrow=dimensions))

    # compute distance matrix
    distances <- as.matrix(dist(m))
    rownames(distances) <- words
    colnames(distances) <- words

    return(distances)
}


# find k closest words to a given word
closest_k <- function(distances, word, k=10){
    topic <- names(sort(distances[word, ])[1:k])
    return(topic)
}

load_topic <- function(topic, df){
    inter <- intersect(names(topic), colnames(df))
    return(df[, inter])
}
library(rjson)

# generate a matrix plot
plot_matrix <- function(data, grouping_column=1){
    data <- data.frame(data)
    data <- data[!is.na(data[[grouping_column]]), ]
    rownames(data) <- data[[grouping_column]]

    distances <- as.matrix(dist(data))
    distances <- melt(as.matrix(distances), varnames = c("row", "col"))

    ggplot(distances, aes(x=row, y=col)) +
        geom_tile(aes(fill=value), color="white") + 
        coord_fixed() +
        theme(axis.text.x = element_text(angle=45, hjust=1))
}



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


load_topic <- function(topic, df, metadata_cols, mean=TRUE){
    inter <- intersect(topic, colnames(df))

    if(mean){
        df_topic <- data.frame(rowMeans(df[, inter]))
        names(df_topic)[1] <- paste(topic[1], 'topic', sep='_')
    }else{
        df_topic <- df[, inter]
    }

    df_res <- cbind(df_topic, df[, metadata_cols])

    return(df_res)
}
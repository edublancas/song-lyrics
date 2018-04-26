library(rjson)


top_k_words <- function(df, cols, row=1, k=10){
    # given a bow data frame, return the top word for some song
    counts <- as.numeric(songs[row, cols])
    names(counts) <- cols
    return(sort(counts, decreasing=TRUE)[1:k])
}

# take the mean of some columns
mean_words <- function(df, cols){
    data.frame(t(colMeans(df[, cols])))
}


# compute pairwise distances
pairwise_distances <- function(data, grouping_column=1, only_upper_half=TRUE,
                               sort=TRUE, groups=3){
    data <- data.frame(data)
    data <- data[!is.na(data[[grouping_column]]), ]
    rownames(data) <- data[[grouping_column]]

    if(sort){
        set.seed(0)
        cols <- 1:ncol(data)
        cols <- cols[cols != grouping_column]

        group <- kmeans(data[, cols], centers=groups, nstart=5)$cluster
        group_sorted <- names(sort(group))

        data <- data[group_sorted, ]
    }

    distances <- as.matrix(dist(data))

    if(only_upper_half){
        distances[lower.tri(distances, diag=FALSE)] <- NA
    }

    distances <- melt(as.matrix(distances), varnames = c("row", "col"))
    distances <- distances[!is.na(distances$value), ]

    colnames(distances) <- c("row", "col", "Distance")
    
    return(distances)
}


# generate a matrix plot
plot_matrix <- function(data, title, grouping_column=1, only_upper_half=TRUE,
                        sort=TRUE, groups=3){

    distances <- pairwise_distances(data, grouping_column, only_upper_half,
                                    sort, groups)

    ggplot(distances, aes(x=row, y=col)) +
        geom_tile(aes(fill=Distance), color="white") + 
        coord_fixed() +
        theme(axis.text.x = element_text(angle=45, hjust=1, size=11)) +
        xlab("") +
        ylab("") +
        ggtitle(title)
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
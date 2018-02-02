# Scoping the song lyrics project

## What kind of questions we want to be able to answer?

* How does sentiment in lyrics varies by year?
* What are the most similar songs?
* Which are the most happy/sad song?
* How different are lyrics from the same artist?
* Which artists are most similar to each other?

## Which data representation we need to answer such questions?

We need to represent lyrics as vectors to compute similarity, sentiment analysis, etc. We can try a simple bag of words representation so that other people can start on the visualization part, then, we can try a more sophisticated representation such as word embeddings.

For similarity, we can cluster lyrics. Depending on how fast we can fit the model we may be able to try different ones and explore results, would also be a good idea to use nonparametric clustering to see how many "natural" groups we find.

## How can we get that representation?

* Bag of words is pretty simple, the dataset is already in that format
* Word embeddings needs more work

## Potential problems

* Bag of words representation may not be good enough
* Clustering may take to long to run

## Project outline

* Data exploration
    - Get the data
    - Explore, see what's in there, spot problems
* Bag of words representation
    - Represent all lyrics as vectors using bag of words representation
    - Try to cluster using this representation
    - Try to so sentiment analysis with this representation
    - Evaluate results - is this representation good enough?
* Word embeddings
    - Represent lyrics as real-valued vectors using word embeddings
    - Cluster
    - Sentiment analysis
    - Evaluate results
* Plotting
    - Once we have reasonable results we can start making nice plots/interactive visualizations for the final delivery
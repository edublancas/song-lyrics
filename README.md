# Song lyrics project

Exploratory Data Analysis and Visualization, Columbia University, Spring 2018.

## Project overview

WIP

## Folder structure

* `data/` - Data is dumped here, not included in the repository
* `process/` - Scripts for downloading and processing the data (Python 3)
    - `process/pkg/` - Small Python package with utility functions
    - `process/download/` - Getting the raw data
    - `process/clean/` - Cleaning the raw data
    - `process/transform/` - Code for generating various song vector representations
    - `process/cluster/` - Clustering songs
* `experiments/` - Notebooks/scripts that we used to explore the data
* `viz/` - Visualizations (R)

## Data

We are using the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/), specifically the [musiXmatch dataset](https://labrosa.ee.columbia.edu/millionsong/musixmatch) which contains lyics data for 237,662 tracks.

## Quickstart

## 0. Software requirements

* Install [miniconda](https://github.com/edublancas/commons/blob/master/repos/conda.md)
* Install [R](https://www.r-project.org/)

Create conda environment and requirements for the project:

```shell
conda create --name=song-lyrics python=3
pip install -r requirements.txt
```

Install R requirements:

    * rjson
    * dplyr
    * ggplot2
    * feather
    * reshape2

## 1. Get raw data

```shell
git clone https://github.com/edublancas/song-lyrics
cd song-lyrics

# this will create a new data/ folder in the current
# working directory raw data will be stored in data/raw
./process/download/get_data
```

## 2. Process data

```shell
# install the python package
pip install -e process/pkg

# parse txt files and convert them to json
mkdir data/clean
./process/clean/txt2json data/raw/mxm_dataset_train.txt \
    data/clean/mxm_dataset_train.json
./process/clean/txt2json data/raw/mxm_dataset_test.txt \
    data/clean/mxm_dataset_test.json

# join the two json files
./process/clean/join_json data/clean/mxm_dataset_train.json \
    data/clean/mxm_dataset_test.json data/clean/mxm_dataset.json

# convert json data to bag of words representation
mkdir data/transform

# all 5000 words (~10GB file)
./process/transform/bag_of_words data/clean/mxm_dataset.json \
    data/transform/mxm_dataset.feather

# top 1000  words but normalized (counts converted to proportions)
./process/transform/bag_of_words data/clean/mxm_dataset.json \
    data/transform/mxm_dataset_100_normalized.feather \
    --max_words 1000 --normalize

# just top 50
./process/transform/bag_of_words data/clean/mxm_dataset.json \
    --max_words 50 data/transform/mxm_dataset_50.feather

# export track metadata
./process/clean/export_track_metadata data/raw/AdditionalFiles/track_metadata.db data/transform/mxm_dataset_50.feather data/transform/track_metadata.feather


# At this point you should have a lot of .feather files in data/transform/
# let's start exploring those with ggplot2. put your findings in the
# experiments/[your name]/ folder (only include Rmd or jnb files, not html
# pdf, etc)


# building word embeddings vocabulary by subsetting the GLOVE dataset
# for exact matches in the musixmatch dataset and fuzzy matching the remaining
# words
./process/clean/subset_embeddings data/clean/mxm_dataset.json \
    data/raw/glove.6B/glove.6B.50d.txt data/clean/embeddings_subset.json

# use word embeddings to represent songs, each song is represented as the
# sum of the count * embedding vectors for every word, run --help
# for more info
./process/transform/word_embeddings data/clean/embeddings_subset.json \
    data/transform/mxm_embeddings.feather
```

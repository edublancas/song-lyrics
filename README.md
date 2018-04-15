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
    * wordcloud
    * knitr

## 1. Get raw data

```shell
git clone https://github.com/edublancas/song-lyrics
cd song-lyrics

# this will create a new data/ folder in the current
# working directory raw data will be stored in data/raw
./process/download/get_data
```

GLOVE gives some problems when trying to download it using `wget`, it's better to download it manually, put data un `data/raw`: https://nlp.stanford.edu/projects/glove/

## 2. Process data

```shell
./bootstrap
```

This will generate the files that we will be working with:
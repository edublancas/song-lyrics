# Song lyrics project

Exploratory Data Analysis and Visualization, Columbia University, Spring 2018.

## Project overview

WIP

## Folder structure

* `data/` - Data is dumped here, not included in the repository
* `processing/` - Scripts for downloading and processing the data (Python 3)
    - `processing/download/` - Getting the raw data
    - `processing/clean/` - Cleaning the raw data
    - `processing/transform/` - Code for generating various song vector representations
    - `processing/cluster/` - Clustering songs
* `viz/` - Scripts for for generating visualizations (R)

## Data

We are using the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/), specifically the [musiXmatch dataset](https://labrosa.ee.columbia.edu/millionsong/musixmatch) which contains lyics data for 237,662 tracks.

## Quickstart

```shell
git clone https://github.com/edublancas/song-lyrics
cd song-lyrics

./get_data
```

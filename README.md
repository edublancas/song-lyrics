# Song lyrics project

Exploratory Data Analysis and Visualization, Columbia University, Spring 2018.

## Project overview

We explored song lyrics data from the Musixmatch + Million Songs dataset to derive conclusions about trends in song lyrics and music across time and geography. We asked questions to explore different facets of the dataset and identified some interesting trends.

## Folder structure

* `data/` - Data is dumped here, not included in the repository
* `experiments/` - Notebooks/scripts that we used to explore the data
* `lib/` - R utility functions used in the project
* `process/` - Scripts for downloading and processing the data (Python 3)
    - `process/pkg/` - Python package with utility functions
    - `process/clean/` - Cleaning the raw data
    - `process/transform/` - Code for generating various song vector representations
    - `process/cluster/` - Clustering songs
* `report/` - Report files

## Data

We are using the [Million Song Dataset](https://labrosa.ee.columbia.edu/millionsong/), specifically the [musiXmatch dataset](https://labrosa.ee.columbia.edu/millionsong/musixmatch) which contains lyics data for 237,662 tracks.

## Quickstart

```shell
git clone https://github.com/edublancas/song-lyrics
cd song-lyrics
```

## 0. Software requirements

This project requires Python 3 and R.

To install Python and R required packages:

```shell
make requirements
```

## 1. Get raw data

The following command fetches all the datasets we used, it will create a new data/ folder in the current working directory raw data will be stored in data/raw.


```shell
make get_data
```

Note: [GLoVe](https://nlp.stanford.edu/projects/glove/) gives some problems when trying to download it using `wget`, it's better to download it manually, put the uncompressed data in  `data/raw`.

## 2. Process data

This script runs all the cleaning, processing we did on the data and it outputs the final datasets we used in the report and the interactive component.

```shell
make bootstrap
```

## 3. Build report

Build the final report.

```shell
make report
```


## 4. Interactive component

The interactive component, built in d3, allows you to explore data points such as sentiment scores, topic scores and similar artists for the top artists in the One Million Songs + Musixmatch dataset.

[Click here](http://bl.ocks.org/valmikkpatel/raw/450a721204f0f3788133c045f700278f/) to view the interactive component. Or it can be viewed after downloading this folder and running a local server.

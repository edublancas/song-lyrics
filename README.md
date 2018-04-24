# Song lyrics project

Exploratory Data Analysis and Visualization, Columbia University, Spring 2018.

## Project overview

TODO: add executive summary here

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

TODO: add instructions
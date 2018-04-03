./process/transform/bag_of_words data/clean/mxm_dataset.json \
    data/transform/mxm_100.feather \
    --max_words 100

./process/transform/bag_of_words data/clean/mxm_dataset.json \
    data/transform/mxm_100_sw.feather \
    --max_words 100 --keep_stopwords


./process/transform/join data/transform/mxm_100.feather \
    data/transform/track_metadata.feather \
    data/transform/bow_100.feather


./process/transform/join data/transform/mxm_100_sw.feather \
    data/transform/track_metadata.feather \
    data/transform/bow_100_sw.feather
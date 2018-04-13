import json
from fuzzywuzzy import process, fuzz

with open('data/clean/mxm_dataset.json') as f:
    mxm = json.load(f)

words = mxm['words']

"'til" in words

process.extract("cos", words, limit=2, scorer=fuzz.ratio)
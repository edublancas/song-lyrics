import json
from fuzzywuzzy import process, fuzz

with open('data/clean/mxm_dataset.json') as f:
    mxm = json.load(f)

words = mxm['words']

"'til" in words

process.extract("cos", words, limit=2, scorer=fuzz.ratio)

c = sorted([w for w in words if w.startswith("'")])
c

[i for i, w in enumerate(words) if w in c]

sorted([w for w in words if w.endswith("in'")])

sorted([w for w in words if w.endswith("ing")])

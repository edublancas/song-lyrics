
%%timeit -r 1
[bow2embedding(bow, words, glove, max_words=MAX_WORDS) for bow in bows[:10000]]
# 2 mins 40

from joblib import Parallel, delayed

bow2embedding(bows[0], words, glove, max_words=MAX_WORDS)


%%timeit
Parallel(n_jobs=4)(delayed(bow2embedding)(bow, words, glove, max_words=MAX_WORDS)
        for bow in bows[:100])


from functools import partial
import multiprocessing

_bow2embedding = partial(bow2embedding, words=words, glove=glove, max_words=MAX_WORDS)

pool = multiprocessing.Pool(8)

%%timeit -r 1
pool.map(_bow2embedding, bows[:10000])
# 3minutes


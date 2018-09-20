# The X Fakes (HackZurich 2018)
Get your news verified by the people you trust

## Prerequisites
```
pip install nltk gensim flask flask_restful flask_jsonpify flask_cors newspaper
```

```
>>> import nltk
>>> nltk.download('punkt')
```

Download at least a [slimmed-down
version](https://github.com/eyaler/word2vec-slim/blob/master/GoogleNews-vectors-negative300-SLIM.bin.gz) of pre-trained word embeddings (the full one is fine as well) and unpack it under `./model` subdirectory.

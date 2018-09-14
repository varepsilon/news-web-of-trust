# news-web-of-trust
Get your news verified by the people you trust

## Prerequisites
```
pip install nltk gensim
```

```
>>> import nltk
>>> nltk.download('punkt')
```

Download at least [slimmed-down
version](https://github.com/eyaler/word2vec-slim/blob/master/GoogleNews-vectors-negative300-SLIM.bin.gz) of pre-trained word embeddings and unpack it under `./model` subdirectory.

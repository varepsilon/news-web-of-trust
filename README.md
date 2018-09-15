# news-web-of-trust
Get your news verified by the people you trust

## Prerequisites
```
pip install nltk gensim flask flask_restful flask_jsonpify flask_cors fcache html2text
```

```
>>> import nltk
>>> nltk.download('punkt')
```

Download at least [slimmed-down
version](https://github.com/eyaler/word2vec-slim/blob/master/GoogleNews-vectors-negative300-SLIM.bin.gz) of pre-trained word embeddings and unpack it under `./model` subdirectory.

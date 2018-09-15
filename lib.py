#  Collection of library functions

from __future__ import print_function

import sys

import numpy as np
import scipy

import nltk
import gensim


DEBUG = True


class Doc2Vec:
    def __init__(self, model_path):
        ''' This initialization is slow. Make sure you don't call it often'''
        self.model = gensim.models.KeyedVectors.load_word2vec_format(
                model_path, binary=True)

    def get_vector(self, document):
        ''' Return the float vector corresponding to the string `document` '''
        word_vectors = []
        oov_words = set()
        for word in nltk.tokenize.word_tokenize(document)[:60]:
            try:
                word_vectors.append(self.model.wv[word])
            except KeyError:
                oov_words.add(word)
                continue
        if DEBUG:
            print('OOV words:', oov_words, file=sys.stderr)
        # pad with zero vectors for short documents
        word_vectors.extend([np.zeros(300) for i in range(60 - len(word_vectors))])
        return np.concatenate(word_vectors)

    @staticmethod
    def sim(v1, v2):
        ''' Compute similarity (from 0 to 1) between float vectors v1 and v2 '''
        return 1 - scipy.spatial.distance.cosine(v1, v2)

if __name__ == '__main__':
    print('======= RUNNING TESTS / SANITY CHECKS ===========')
    doc2vec = Doc2Vec('./model/GoogleNews-vectors-negative300-SLIM.bin')
    docs = ['Donald Trump was elected US president',
            'Hilary Clinton turned out to be a lizard!',
            'Hilary Clinton lost the United States elections',
            ]
    for i in range(len(docs)):
        for j in range(i, len(docs)):
            d1 = docs[i]
            d2 = docs[j]
            print('sim([{}],[{}]) = {}'.format(
                    d1, d2,
                    doc2vec.sim(doc2vec.get_vector(d1), doc2vec.get_vector(d2))))

    with open('./testdata/cleaned_news.txt') as test_data:
        # Run this in the DEBUG mode to see what are the OOV words
        vec = doc2vec.get_vector(test_data.read())


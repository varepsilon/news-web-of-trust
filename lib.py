#!/usr/bin/env python

#  Collection of library functions

import numpy as np
import nltk
import gensim
import scipy

class Doc2Vec:
    def __init__(self, model_path):
        self.model = gensim.models.KeyedVectors.load_word2vec_format(
                model_path, binary=True)

    def get_vector(self, document):
        sum_vec = 0
        l = 0
        for word in nltk.tokenize.word_tokenize(document):
            try:
                sum_vec += self.model.wv[word]
                l += 1
            except KeyError:
                continue
        return sum_vec / l

    @staticmethod
    def sim(w1, w2):
        return 1 - scipy.spatial.distance.cosine(w1, w2)

if __name__ == '__main__':
    doc2vec = Doc2Vec('./model/GoogleNews-vectors-negative300-SLIM.bin')
    docs = ['Donald Trump was elected US president',
            'Hilary Clinton turned out to be a lizard!',
            'Hilary Clinton lost the United States elections',
            ]
    for i in range(len(docs)):
        for j in range(i + 1, len(docs)):
            d1 = docs[i]
            d2 = docs[j]
            print('sim([{}],[{}])= {}'.format(
                    d1, d2,
                    doc2vec.sim(doc2vec.get_vector(d1), doc2vec.get_vector(d2))))

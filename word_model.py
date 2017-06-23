# -*- coding: utf-8 -*-

import sys
import numpy as np
#sys.path.insert(0, '/home/johnlee/Research/morse/fasttext/fasttext') #DEBUGGING PURPOSE
import fasttext
from gensim.models.keyedvectors import KeyedVectors

class WORDMODEL(object):
    # __slots__ = ['model', 'words','type']
    def __init__(self, type, data, batch):

        self.type = type
        self.batch = batch
        if type == "fasttext":
            print "loading fasttext model"
            self.model = fasttext.load_model(data)
            print "Model Loaded"
            if batch != -1:
                self.words = (list(self.model.words))[:batch]
            else:
                self.words = list(self.model.words)
        elif type == "word2vec":

            binv = True
            if ".vec" in data:
                binv = False

            print "loading word2vec model"
            self.model = KeyedVectors.load_word2vec_format(data, binary=binv,
                                                           unicode_errors='ignore')
            print "Model Loaded"


        print "loading done"

    def get_vector(self, words):
        """get vector of the word"""
        dict = {}
        print "Creating Vector dictionary"
        for word in words:
            dict[word] = np.array(self.model[word], dtype=np.float32)
        return dict

    def get_words(self):
        """ get the list of words """
        words = []
        final_words = []
        if self.batch != -1 and self.batch < len(self.model.vocab):
            for (k, obj) in self.model.vocab.iteritems():
                words.append((k, obj.count))

            print "Sorting Start"

            # words = sorted(words, key=lambda x: x[1], reverse=True)

            for i in range(self.batch):
                final_words.append((words[i])[0])

            print "Sorting Done"

        else:
            for (k, _) in self.model.vocab.iteritems():
                words.append(k)
        return final_words



if __name__ == "__main__":


    word_rep = vectorize_word('word2vec','wiki.en.vec', -1, 100)
    vector =   word_rep.get_vector('king')
    print len(vector)

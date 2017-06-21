# -*- coding: utf-8 -*-

import sys
#sys.path.insert(0, '/home/johnlee/Research/morse/fasttext/fasttext') #DEBUGGING PURPOSE
import fasttext
from gensim.models.keyedvectors import KeyedVectors

class WORDMODEL(object):

    def __init__(self, type, data, batch):

        self.type = type
        if type == "fasttext":
            print "loading fasttext model"
            self.model = fasttext.load_model(data)
            if batch != -1:
                self.words = (list(self.model.words))[:batch]
            else:
                self.words = list(self.model.words)
        elif type == "word2vec":

            print "loading word2vec model"
            self.model = KeyedVectors.load_word2vec_format(data, binary=False)

            self.words = []
            if batch != -1:
                counter = 0
                for (k, _) in self.model.vocab.iteritems():
                    counter += 1
                    if counter == batch:
                        break
                    self.words.append(k)
            else:
                for (k, _) in self.model.vocab.iteritems():
                    self.words.append(k)

        print "loading done"

    def get_vector(self, word):
        """get vector of the word"""
        return self.model[unicode(word, "utf-8")]

    def get_words(self):
        """ get the list of words """
        return self.words



if __name__ == "__main__":


    word_rep = vectorize_word('word2vec','wiki.en.vec', -1)
    vector =   word_rep.get_vector('king')
    print len(vector)

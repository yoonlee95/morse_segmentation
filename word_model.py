# -*- coding: utf-8 -*-

import sys
#sys.path.insert(0, '/home/johnlee/Research/morse/fasttext/fasttext') #DEBUGGING PURPOSE
import fasttext
from gensim.models.keyedvectors import KeyedVectors

class WORDMODEL(object):

    def __init__(self, type, data, batch):

        if type == "fasttext":
            print "loading fasttext model"
            print data
            self.model = fasttext.load_model("")
            # self.words =  self.model.words[:batch]
            self.words = (list(self.model.words))[:batch]

        elif type == "word2vec":

            print "loading word2vec model"
            self.model = KeyedVectors.load_word2vec_format(data, binary=False)

            counter = 0
            self.words = []
            for (k, _) in self.model.vocab.iteritems():
                counter += 1
                if counter == batch:
                    break
                self.words.append(k)
                print k

        print "loading done"




    def get_vector(self, word):
        return self.model[unicode(word,"utf-8")]
    def get_words(self):
        return self.words



if __name__ == "__main__":


    word_rep = vectorize_word('word2vec','wiki.en.vec')


    vector =   word_rep.get_vector('king')
    print len(vector)

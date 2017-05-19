import fasttext
# from gensim.keyedvectors import KeyedVectors
# import gensim
from gensim.models.keyedvectors import KeyedVectors
# import word2vec
class vectorize_word(object):

    def __init__(self, type, data):

        if type == "fasttext":
            print "loading fasttext model"
            self.model = fasttext.load_model(data)
            print "loading done"
        #data structure for storing neighbers of the current word
        elif type == "word2vec":
            print "loading word2vec model"
            self.model = KeyedVectors.load_word2vec_format(data, binary=False)

            print "loading done"



    def get_vector(self, word):
        return self.model[word]



if __name__ == "__main__":


    word_rep = vectorize_word('word2vec','wiki.en.vec')


    vector =   word_rep.get_vector('king')
    print len(vector)

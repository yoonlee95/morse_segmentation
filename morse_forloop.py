import pickle
from Queue import *
from tree import ALPHABETTREE
from wordGroup import WORDGROUP


with open('googlenews_vocab.pkl', 'rb') as f:
    data = pickle.load(f)

print "pickle file loaded"
data = data[:10]
print data
print len(data)

list = []
# for word_1 in data:
#     for word_2 in data:
        
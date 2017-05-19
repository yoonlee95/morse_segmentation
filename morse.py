#!/usr/bin/env python

import os
import morse_structure
import morse_structure_reverse
import numpy as np
from calc_distance2 import get_distance_parallel
from vectorize_word import vectorize_word
import pickle

__author__ = "Jong Yoon(John) Lee"
__license__ = "MIT"
__version__ = "alpha"
__email__ = "jlee642@illinois.edu"


VOCAB_DATA = 'googlenews_vocab.pkl'

WORD_REPR = 'fasttext'
WORD_REPR_DATA = 'wiki.en.bin'

SAVE_PICKLE = True
MODE = "PREFIX"                #select between PREFIX and SUFFIX
DICT = 'pkloutput1m/'

#make directory if it doesnt exist
if not os.path.exists(DICT):
    os.makedirs(DICT)

print "initialize data"
with open(VOCAB_DATA, 'rb') as f:
    FULL_DATA = pickle.load(f)

r_orth = {}
r_sem = {}
w_sem = {}
loc_sem = {}
ss_sem = {}

BATCH_SIZE = 1000000
BATCH = FULL_DATA[:BATCH_SIZE]
print "initalizing word-vec dataset"

WORD_REP = vectorize_word(WORD_REPR, WORD_REPR_DATA)

#CREATE SUPPORT SET
if MODE == "SUFFIX":
    SEGMENTED_WORD = morse_structure.getsegmentation(BATCH)
else:
    for index in range(BATCH_SIZE):
        if len(BATCH[index]) > 0:
            BATCH[index] = BATCH[index][::-1]
    SEGMENTED_WORD = morse_structure_reverse.getsegmentation(BATCH)


#CALCULATE THE SCORES(LOCAL ,GLOBAL) FOR THE SUPPORT SETS
for rule, words in SEGMENTED_WORD.iteritems():
    w_1 = []
    w_2 = []
    if len(words) > 1:

        for word in words:
            w_1.extend(WORD_REP.get_vector(word[0]))
            w_2.extend(WORD_REP.get_vector(word[1]))
        count, cos = get_distance_parallel(np.asarray(w_1, dtype=np.float32),
                                    np.asarray(w_2, dtype=np.float32))

        len_w = len(words)

        total = len_w * len_w
        total_count = np.sum(count)
        # print "RULE: " + str(rule)+ " Score: " + str(total_count) + "/" + str(total)



        #Save to pickle
        if SAVE_PICKLE is True:

            r_orth[rule] = len(w_1)/300

            r_sem[rule] = 1.0 * total_count/total

            #Get Local store
            for index, word in enumerate(words):

                loc_sem[word] = 1.0 *count[index]/float(len_w)
                # print loc_sem[word]
                # print count[index]
                # print len_w
                w_sem[word] = cos[index]

            support_set = []
            for word in words:
                support_set.append(word)
            ss_sem[rule] = support_set

if SAVE_PICKLE is True:
    pickle.dump(r_orth, open(DICT+"r_orth.pkl", "wb"))
    pickle.dump(r_sem, open(DICT+"r_sem.pkl", "wb"))
    pickle.dump(w_sem, open(DICT+"w_sem.pkl", "wb"))
    pickle.dump( loc_sem, open( DICT+"loc_sem.pkl", "wb"))
    pickle.dump(ss_sem, open(DICT+"ss_sem.pkl", "wb"))



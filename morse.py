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
PICKLE_PARTITION_SIZE = 200000 # depends on the system RAM memory
MODE = "SUFFIX"                #select between PREFIX and SUFFIX
DICT = 'pkloutput_1m_partition_2/'

#make directory if it doesnt exist
if not os.path.exists(DICT) and SAVE_PICKLE == True:
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

#CREATE SUPPORT SET

if MODE == "SUFFIX":
    print "SUFFIX TREE BUILD"
    SEGMENTED_WORD = morse_structure.getsegmentation(BATCH)
else:
    for index in range(BATCH_SIZE):
        if len(BATCH[index]) > 0:
            BATCH[index] = BATCH[index][::-1]
    print "PREFIX TREE BUILD"
    SEGMENTED_WORD = morse_structure_reverse.getsegmentation(BATCH)


print "initalizing word-vec dataset"
WORD_REP = vectorize_word(WORD_REPR, WORD_REPR_DATA)

counter = 0
partition_index = 0
pkl_saved = False
#CALCULATE THE SCORES(LOCAL ,GLOBAL) FOR THE SUPPORT SETS
for rule, words in SEGMENTED_WORD.iteritems():
    w_1 = []
    w_2 = []
    if len(words) > 1:
        counter += 1
        pkl_saved = False

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
            
            if counter % PICKLE_PARTITION_SIZE == 0 and counter != 0:
                print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"+ str(PICKLE_PARTITION_SIZE) + ")"
                pickle.dump(r_orth, open(DICT+"r_orth"+str(partition_index)+".pkl", "wb"))
                pickle.dump(r_sem, open(DICT+"r_sem"+str(partition_index)+".pkl", "wb"))
                pickle.dump(w_sem, open(DICT+"w_sem"+str(partition_index)+".pkl", "wb"))
                pickle.dump( loc_sem, open( DICT+"loc_sem"+str(partition_index)+".pkl", "wb"))
                pickle.dump(ss_sem, open(DICT+"ss_sem"+str(partition_index)+".pkl", "wb"))
                partition_index += 1

                r_orth = {}
                r_sem = {}
                w_sem = {}
                loc_sem = {}
                ss_sem = {}
                pkl_saved = True
            
if SAVE_PICKLE is True and pkl_saved is not True:
    print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"+ str(PICKLE_PARTITION_SIZE) + ") FINAL"
    pickle.dump(r_orth, open(DICT+"r_orth"+str(partition_index)+".pkl", "wb"))
    pickle.dump(r_sem, open(DICT+"r_sem"+str(partition_index)+".pkl", "wb"))
    pickle.dump(w_sem, open(DICT+"w_sem"+str(partition_index)+".pkl", "wb"))
    pickle.dump( loc_sem, open( DICT+"loc_sem"+str(partition_index)+".pkl", "wb"))
    pickle.dump(ss_sem, open(DICT+"ss_sem"+str(partition_index)+".pkl", "wb"))




#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import numpy as np
import pickle
import json

from calc_distance2 import get_distance_parallel
from vectorize_word import vectorize_word
import morse_structure
import morse_structure_reverse
import sys  

# sys.setdefaultencoding('utf-8')

__author__ = "Jong Yoon(John) Lee"
__license__ = "MIT"
__version__ = "alpha"
__email__ = "jlee642@illinois.edu"
    
def start_morse(word_repr_model, batch_size, pickle_partition_size, mode, output_dict, base_word, edit_distance):

    # WORD_REPR = 'fasttext'
    WORD_REPR = 'word2vec'

    print "INIT WORD MODEL"
    WORD_REP = vectorize_word(WORD_REPR, word_repr_model, batch_size)
    print "FINISHED LOADING MODEL"
    BATCH =  WORD_REP.get_words()


    r_orth = {}
    r_sem = {}
    w_sem = {}
    loc_sem = {}
    ss_sem = {}


    #CREATE SUPPORT SET

    if mode == "SUFFIX":
        print "SUFFIX TREE BUILD"
        SEGMENTED_WORD = morse_structure.getsegmentation(BATCH,base_word,edit_distance)
        # for k, v in SEGMENTED_WORD.iteritems():
        #     print k, v
    else:
        for index in range(len(BATCH)):
            if len(BATCH[index]) > 0:
                BATCH[index] = BATCH[index][::-1]
        print "PREFIX TREE BUILD"
        SEGMENTED_WORD = morse_structure_reverse.getsegmentation(BATCH,base_word, edit_distance)

    print "Number of Support Set: " + str(len(SEGMENTED_WORD))
    del BATCH

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
                # w_1.extend(WORD_REP.get_vector(word[0].decode("utf-8", 'ignore')))
                # w_2.extend(WORD_REP.get_vector(word[1].decode("utf-8", 'ignore')))
                w_1.extend(WORD_REP.get_vector(word[0].encode('utf-8')))
                w_2.extend(WORD_REP.get_vector(word[1].encode('utf-8')))
            count, cos = get_distance_parallel(np.asarray(w_1, dtype=np.float32),
                                               np.asarray(w_2, dtype=np.float32))

            len_w = len(words)

            total = len_w * len_w
            total_count = np.sum(count)

            #Save to pickle

            r_orth[rule] = len(w_1)/300

            r_sem[rule] = 1.0 * total_count/total

            #Get Local store
            for index, word in enumerate(words):

                loc_sem[word] = 1.0 *count[index]/float(len_w)
                w_sem[word] = cos[index]

            support_set = []
            for word in words:
                support_set.append(word)
            ss_sem[rule] = support_set
            
            if counter % pickle_partition_size == 0:
                print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"+ str(pickle_partition_size) + ")"
                pickle.dump(r_orth, open(output_dict+"/r_orth_"+str(partition_index)+".pkl", "wb"))
                pickle.dump(r_sem, open(output_dict+"/r_sem_"+str(partition_index)+".pkl", "wb"))
                pickle.dump(w_sem, open(output_dict+"/w_sem_"+str(partition_index)+".pkl", "wb"))
                pickle.dump( loc_sem, open( output_dict+"/loc_sem_"+str(partition_index)+".pkl", "wb"))
                pickle.dump(ss_sem, open(output_dict+"/ss_sem_"+str(partition_index)+".pkl", "wb"))
                partition_index += 1

                r_orth = {}
                r_sem = {}
                w_sem = {}
                loc_sem = {}
                ss_sem = {}
                pkl_saved = True
                
    if pkl_saved is not True:
        print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"+ str(pickle_partition_size) + ") FINAL"
        pickle.dump(r_orth, open(output_dict+"/r_orth_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(r_sem, open(output_dict+"/r_sem_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(w_sem, open(output_dict+"/w_sem_"+str(partition_index)+".pkl", "wb"))
        pickle.dump( loc_sem, open( output_dict+"/loc_sem_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(ss_sem, open(output_dict+"/ss_sem_"+str(partition_index)+".pkl", "wb"))



if __name__ == '__main__':
    start_morse('wiki.en.bin', 100000, 100000, 'SUFFIX', './test_1/',1,4)
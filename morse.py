#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys  

import numpy as np
import pickle
import json

from calc_distance import get_distance_parallel
from word_model import WORDMODEL
import morse_structure
import morse_structure_reverse

__author__ = "Jong Yoon(John) Lee"
__license__ = "MIT"
__version__ = "alpha"
__email__ = "jlee642@illinois.edu"

def start_morse(model_file, config):
    """ make support set and calculate score

    Args:
        model_file (str): path to model file

    Returns:
        config (object) : config file for morse

    """

    print "INIT WORD MODEL"
    wmodel = WORDMODEL(config['model_type'], model_file, config['batch_size'])
    print "FINISHED LOADING MODEL"

    batch = wmodel.get_words()

    r_orth = {}
    r_sem = {}
    w_sem = {}
    loc_sem = {}
    ss_sem = {}

    #CREATE SUPPORT SET
    if config['mode'] == "SUFFIX":
        print "SUFFIX TREE BUILD"
        support_set = morse_structure.getsegmentation(batch, config['base_word'],
                                                      config['edit_distance'])
    else:
        print "PREFIX TREE BUILD"
        for index, _ in enumerate(batch):
            if len(batch[index]) > 0:
                batch[index] = batch[index][::-1]
        support_set = morse_structure_reverse.getsegmentation(batch, config['base_word'],
                                                              config['edit_distance'])

    print "Number of Support Set: " + str(len(support_set))
    del batch

    counter = 0
    partition_index = 0

    pkl_saved = False

    pickle_partition_size = config['partition_size']
    output_dict = config['output_dir']

    #CALCULATE THE SCORES(LOCAL ,GLOBAL) FOR THE SUPPORT SETS
    for rule, words in support_set.iteritems():
        w_1 = []
        w_2 = []
        if len(words) > 1:
            counter += 1
            pkl_saved = False

            for word in words:
                w_1.extend(wmodel.get_vector(word[0].encode('utf-8')))
                w_2.extend(wmodel.get_vector(word[1].encode('utf-8')))
            count, cos = get_distance_parallel(np.asarray(w_1, dtype=np.float32),
                                               np.asarray(w_2, dtype=np.float32))

            len_w = len(words)
            total = len_w * len_w
            total_count = np.sum(count)
            r_orth[rule] = len(w_1)/300
            r_sem[rule] = 1.0 * total_count/total
            for index, word in enumerate(words):

                loc_sem[word] = 1.0 *count[index]/float(len_w)
                w_sem[word] = cos[index]

            support_set = []
            for word in words:
                support_set.append(word)
            ss_sem[rule] = support_set

            if counter % pickle_partition_size == 0:
                print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"\
                                               + str(pickle_partition_size) + ")"
                pickle.dump(r_orth, open(output_dict+"/r_orth_"+str(partition_index)+".pkl", "wb"))
                pickle.dump(r_sem, open(output_dict+"/r_sem_"+str(partition_index)+".pkl", "wb"))
                pickle.dump(w_sem, open(output_dict+"/w_sem_"+str(partition_index)+".pkl", "wb"))
                pickle.dump(loc_sem, open(output_dict+"/loc_sem_"+str(partition_index)+".pkl"))
                pickle.dump(ss_sem, open(output_dict+"/ss_sem_"+str(partition_index)+".pkl", "wb"))
                partition_index += 1

                r_orth = {}
                r_sem = {}
                w_sem = {}
                loc_sem = {}
                ss_sem = {}
                pkl_saved = True

    if pkl_saved is not True:
        print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"\
                                 + str(pickle_partition_size) + ") FINAL"
        pickle.dump(r_orth, open(output_dict+"/r_orth_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(r_sem, open(output_dict+"/r_sem_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(w_sem, open(output_dict+"/w_sem_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(loc_sem, open(output_dict+"/loc_sem_"+str(partition_index)+".pkl", "wb"))
        pickle.dump(ss_sem, open(output_dict+"/ss_sem_"+str(partition_index)+".pkl", "wb"))



if __name__ == '__main__':
    CONFIG = json.loads(open('./default-config').read())
    start_morse('wiki.en.bin', CONFIG)

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys  
import time

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

def start_morse(model_file, config, mode):
    """ make support set and calculates score

    This function will use the input model and create the according support set
    and score files. This function will output 5 different types of partitioned
    files with appropriate index.

    Args:
        model_file (str): path to model file
        config (object) : config file for morse
        mode (str)) : <SUFFIX> or <PREFIX> mode to calcualte

    Returns:
        partition_index : final index of the partitioned data

    """

    print "INIT WORD MODEL"
    wmodel = WORDMODEL(config['external_model_type'], model_file, config['batch_size'])
    print "FINISHED LOADING MODEL"

    batch = wmodel.get_words()
    vec = wmodel.get_vector(batch)

    del wmodel


    r_orth = {}
    r_sem = {}
    w_sem = {}
    loc_sem = {}
    ss = {}
    file_start_string = ""

    #CREATE SUPPORT SET
    if mode == "SUFFIX":
        print "SUFFIX TREE BUILD"
        file_start_string = "/SUF"

        support_set = morse_structure.getsegmentation(batch, config['suffix_base_word'],
                                                      config['suffix_edit_dist'])
    elif mode == "PREFIX":
        print "PREFIX TREE BUILD"
        file_start_string = "/PRE"

        for index, _ in enumerate(batch):
            if len(batch[index]) > 0:
                batch[index] = batch[index][::-1]
        support_set = morse_structure_reverse.getsegmentation(batch, config['prefix_base_word'],
                                                              config['prefix_edit_dist'])
    else:
        print "WRONG MODE"
        print "NEEDS TO BE <SUFFIX> or <PREFIX>"
        exit()

    print "Number of Support Set: " + str(len(support_set))
    del batch

    counter = 0
    partition_index = 0

    pkl_saved = False

    pickle_partition_size = config['partition_size']
    output_dict = config['ss_score_output_dir']

    #CALCULATE THE SCORES(LOCAL ,GLOBAL) FOR THE SUPPORT SETS
    for rule, words in support_set.iteritems():
        w_1 = []
        w_2 = []
        if len(words) > 5:
            counter += 1
            pkl_saved = False

            w_1 = np.concatenate([vec[word[0]] for word in words])
            w_2 = np.concatenate([vec[word[1]] for word in words])
            count, cos = get_distance_parallel(w_1, w_2)

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
            ss[rule] = support_set

            if counter % pickle_partition_size == 0 and pickle_partition_size != -1:
                print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"\
                                               + str(pickle_partition_size) + ")"
                pickle.dump(r_orth, open(output_dict+file_start_string+"_r_orth_"+
                                         str(partition_index)+".pkl", "wb"),
                            protocol=2)
                pickle.dump(r_sem, open(output_dict+file_start_string+"_r_sem_"+
                                        str(partition_index)+".pkl", "wb"),
                            protocol=2)
                pickle.dump(w_sem, open(output_dict+file_start_string+"_w_sem_"+
                                        str(partition_index)+".pkl", "wb"),
                            protocol=2)
                pickle.dump(loc_sem, open(output_dict+file_start_string+"_loc_sem_"+
                                          str(partition_index)+".pkl", "wb"),
                            protocol=2)
                pickle.dump(ss, open(output_dict+file_start_string+"_ss_"+
                                     str(partition_index)+".pkl", "wb"),
                            protocol=2)
                partition_index += 1

                r_orth = {}
                r_sem = {}
                w_sem = {}
                loc_sem = {}
                ss = {}
                pkl_saved = True

    if pkl_saved is not True:
        print "PARTITION : "+ str(partition_index) + " COMPLETE (SIZE:"\
                                 + str(pickle_partition_size) + ") FINAL"
        pickle.dump(r_orth, open(output_dict+file_start_string+"_r_orth_"+
                                 str(partition_index)+".pkl", "wb"),
                    protocol=2)
        pickle.dump(r_sem, open(output_dict+file_start_string+"_r_sem_"+
                                str(partition_index)+".pkl", "wb"),
                    protocol=2)
        pickle.dump(w_sem, open(output_dict+file_start_string+"_w_sem_"+
                                str(partition_index)+".pkl", "wb"),
                    protocol=2)
        pickle.dump(loc_sem, open(output_dict+file_start_string+"_loc_sem_"+
                                  str(partition_index)+".pkl", "wb"),
                    protocol=2)
        pickle.dump(ss, open(output_dict+file_start_string+"_ss_"+
                             str(partition_index)+".pkl", "wb"),
                    protocol=2)

    del vec
    del support_set

    del r_orth
    del r_sem
    del w_sem
    del loc_sem
    del ss

    return partition_index



if __name__ == '__main__':
    CONFIG = json.loads(open('./default-config.json').read())
    start_morse('ssg.300.bin', CONFIG, 'SUFFIX')

#!/usr/bin/python

import os.path
import sys
import getopt
import subprocess
import json

from language_to_iso639 import find_translation
from morse import start_morse
from Model_Creator import model_creator

WEB_BASE = "https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki."
VEC = ".vec"
CONFIG_FILE_NAME = "default-config.json"
MODEL_DIR = "./model"

def parse_input(argv, config):
    """ parse input file and updates the config file

    Args:
        argv (list): input argument from user
        config (dictionary): config dictionary

    Returns:
       NONE

    """
    try:
        opts, _ = getopt.getopt(argv, "l:b:p:s:o:m:t:e:h", ["pw=", "pe=", "sw=", "se="])
    except getopt.GetoptError:
        print "Input argument Invalid: "
        print "Valid inputs are Shown below"
        print """train.py
          FASTTEXT MODEL mode(default mode):
          -l <input language>       Language to run Morse Segmentation

          External MODEL Mode(when <external mode> is used)
          -e <external model dir>   Directory of the external model
          -t <model type>           model to load the external model (<fasttext> or <word2vec>)

          General Configuations:
          -b <batch size>           Number of words to segment from model( -1 for full dataset)
          -p <partition size>       Number of words to group as a partition( -1 for no partition)

          -m  <external mode>       <True> or <False> value if external model is going to be used

          Output Directories:
          -s <ss, score directory>  Output directory for the  support set and scores
          -o <model output dir>     Output directory for the model

          PREFIX Rules:
          --pw <base word>           Minimum length of a word
          --pe <edit distance>       Maximum edit distance a word can have beween another word in a SS 

          SUFFIX Rules:
          --sw <base word>           Minimum length of a word
          --se <edit distance>       Maximum edit distance a word can have beween another word in a SS"""

        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print """train.py
            FASTTEXT MODEL mode(default mode):
            -l <input language>       Language to run Morse Segmentation

            External MODEL Mode(when <external mode> is used)
            -e <external model dir>   Directory of the external model
            -t <model type>           model to load the external model (<fasttext> or <word2vec>)

            General Configuations:
            -b <batch size>           Number of words to segment from model( -1 for full dataset)
            -p <partition size>       Number of words to group as a partition( -1 for no partition)

            -m  <external mode>       <True> or <False> value if external model is going to be used

            Output Directories:
            -s <ss, score directory>  Output directory for the  support set and scores
            -o <model output dir>     Output directory for the model

            PREFIX Rules:
            --pw <base word>           Minimum length of a word
            --pe <edit distance>       Maximum edit distance a word can have beween another word in a SS 

            SUFFIX Rules:
            --sw <base word>           Minimum length of a word
            --se <edit distance>       Maximum edit distance a word can have beween another word in a SS"""

            exit()
        elif opt in "-l":
            config['language'] = arg
        elif opt in "-b":
            config['batch_size'] = int(arg)
        elif opt in "-p":
            config['partition_size'] = int(arg)
        elif opt in "-t":
            if arg in ["fasttext", "word2vec"]:
                config['external_model_type'] = arg
            else:
                print "model type has to be <fasttext> or <word2vec>"
                sys.exit(2)
        elif opt in "-o":
            config['model_output_dir'] = arg
        elif opt in "-s":
            config['ss_score_output_dir'] = arg
        elif opt in "--pw":
            config['prefix_base_word'] = int(arg)
        elif opt in "--pe":
            config['prefix_edit_dist'] = int(arg)
        elif opt in "--sw":
            config['suffix_base_word'] = int(arg)
        elif opt in "--se":
            config['suffix_edit_dist'] = int(arg)
        elif opt in "-m":
            bol = arg.lower()
            if bol == 'true':
                config['external_mode'] = True
            elif bol == 'false':
                config['external_mode'] = False
            else:
                print "External Mode takes an argument of <True> or <False>"
                sys.exit(2)

        elif opt in "-e":
            config['external_model_dir'] = arg

def download_model(config):
    """ Download Model from fasttext(facebook) repository

    Args:
        config (object): config file for morse segmentation

    Returns:
        model_file (str) : relative model directory

    """
    #Get the iso639 from of the language
    iso639 = find_translation(config['language'])

    print "Language", config['language']
    print "ISO-639:", iso639

    #Create Model dir if there isnt
    if not os.path.exists(MODEL_DIR):
        os.makedirs(MODEL_DIR)

    model_file = "./model/wiki."+iso639+".vec"

    if not os.path.exists(model_file):
        print "DOWNLOADING MODEL"
        print subprocess.check_output(['wget', WEB_BASE+iso639+".vec", '-P', './model/'])
        # print "UNZIPPI1NG MODEL"
        # print subprocess.check_output(['unzip', './model/wiki.'+iso639+".zip", '-d', "./model/"])
        # print "MODEL INSTALLED"
        # print subprocess.check_output(['rm', './model/wiki.'+iso639+".zip"])
        # print subprocess.check_output(['rm', './model/wiki.'+iso639+".bin"])
    return model_file

def print_config(config):
    """print config parameter"""

    if config['external_mode'] is False:
        print("INPUT PARAMETER:\n\
        LANGUAGE : {}\n\
        PREFIX BASE WORD : {}\n\
        PREFIX EDIT DISTANCE : {}\n\n\
        SUFFIX BASE WORD : {}\n\
        SUFFIX EDIT DISTANCE : {}\n\n\
        BATCH SIZE : {}\n\
        PARTITION SIZE : {}\n\
        SS SCORE DIRECTORY : {}\n\
        MODEL DIRECTORY : {}".format(config['language'], config['prefix_base_word'],
                                     config['prefix_edit_dist'], config['suffix_base_word'],
                                     config['suffix_edit_dist'], config['batch_size'],
                                     config['partition_size'], config['ss_score_output_dir'],
                                     config['model_output_dir']))
    else:
        print("INPUT PARAMETER:\n\
        EXTERNAL MODEL DIR : {}\n\
        MODEL TYPE : {}\n\
        PREFIX BASE WORD : {}\n\
        PREFIX EDIT DISTANCE : {}\n\n\
        SUFFIX BASE WORD : {}\n\
        SUFFIX EDIT DISTANCE : {}\n\n\
        BATCH SIZE : {}\n\
        PARTITION SIZE : {}\n\
        SS SCORE DIRECTORY : {}\n\
        MODEL DIRECTORY : {}".format(config['external_model_dir'], config['external_model_type'],
                                     config['prefix_base_word'], config['prefix_edit_dist'],
                                     config['suffix_base_word'],
                                     config['suffix_edit_distance'], config['batch_size'],
                                     config['partition_size'], config['ss_score_output_dir'],
                                     config['model_output_dir']))

def main(argv):
    """Main code to lanch code for morse segmentation """

    # Load default config
    config = json.loads(open(CONFIG_FILE_NAME).read())

    # update config file to user input
    parse_input(argv, config)
    print_config(config)

    if config['external_mode'] is False:
        model_file = download_model(config)

        # Note: not really a extenal model type.
        # word2vec is used for fasttext .vec file interperation
        config['external_model_type'] = 'word2vec'
    else:
        model_file = config['external_model_dir']


    #Create output directory if it doesnt exit
    if not os.path.exists(config['ss_score_output_dir']):
        os.makedirs(config['ss_score_output_dir'])
    if not os.path.exists(config['model_output_dir']):
        os.makedirs(config['model_output_dir'])

    suffix_index = start_morse(model_file, config, "SUFFIX")
    prefix_index = start_morse(model_file, config, "PREFIX")

    model_creator(config['ss_score_output_dir'], config['model_output_dir'], prefix_index, suffix_index)

if __name__ == "__main__":
    main(sys.argv[1:])



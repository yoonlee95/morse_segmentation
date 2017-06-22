#!/usr/bin/python

import os.path
import sys
import getopt
import subprocess
import json

from pprint import pprint

from language_to_iso639 import find_translation
from morse import start_morse

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
        opts, _ = getopt.getopt(argv, "l:b:p:m:t:o:hw:e:")
    except getopt.GetoptError:
        print "Input argument Invalid: "
        print "Valid inputs are Shown below"
        print """main.py
          -l <input language>       Language to run morse segmentation on
          -b <batch size>           Number of words to segment from model( -1 for full dataset)
          -p <partition size>       Number of words to group as a partition( -1 for no partition)
          -m <mode>                 segment type (<SUFFIX> or <PREFIX>)
          -t <model type>           SELECT mode (<fasttext> or <word2vec>)
          -o <output directory>     Output directory
          -w <base word>            minimum length of a word
          -e <edit distance>        maximum edit distance a word can have beween another word in a SS""" 
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print """main.py
            -l <input language>       Language to run morse segmentation on
            -b <batch size>           Number of words to segment from model( -1 for full dataset)
            -p <partition size>       Number of words to group as a partition( -1 for no partition)
            -m <mode>                 Segment type (<SUFFIX> or <PREFIX>)
            -t <model type>           Select mode (<fasttext> or <word2vec>)
            -o <output directory>     Output directory
            -w <base word>            Minimum length of a word
            -e <edit distance>        Maximum edit distance a word can have beween another word in a SS""" 
            exit()
        elif opt in "-l":
            config['language'] = arg
        elif opt in "-b":
            config['batch_size'] = int(arg)
        elif opt in "-p":
            config['partition_size'] = int(arg)
        elif opt in "-m":
            if arg in ["SUFFIX", "PREFIX"]:
                config['mode'] = arg
            else:
                print "model type has to be <SUFFIX> or <PREFIX>"
                sys.exit(2)

        elif opt in "-t":
            if arg in ["fasttext", "word2vec"]:
                config['model_type'] = arg
            else:
                print "model type has to be <fasttext> or <word2vec>"
                sys.exit(2)
        elif opt in "-o":
            config['output_dir'] = arg
        elif opt in "-w":
            config['base_word'] = int(arg)
        elif opt in "-e":
            config['edit_distance'] = int(arg)
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

    print("INPUT PARAMETER:\n\
    BASE WORD : {}\n\
    BATCH SIZE : {}\n\
    EDIT DISTANCE : {}\n\
    LANGUAGE : {}\n\
    MODE : {}\n\
    MODEL TYPE : {}\n\
    OUTPUT DIRECTORY : {}\n\
    PARTITION SIZE : {}".format(config['base_word'], config['batch_size'],
                                config['edit_distance'], config['language'], config['mode'],
                                config['model_type'], config['output_dir'],
                                config['partition_size']))

def main(argv):
    """Main code to lanch code for morse segmentation """

    # Load default config
    config = json.loads(open(CONFIG_FILE_NAME).read())

    # update config file to user input
    parse_input(argv, config)
    print_config(config)


    model_file = download_model(config)

    #Create output directory if it doesnt exit
    if not os.path.exists(config['output_dir']):
        os.makedirs(config['output_dir'])

    start_morse(model_file, config)

if __name__ == "__main__":
    main(sys.argv[1:])



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
        opts, _ = getopt.getopt(argv, "l:b:p:m:t:o:hw:e:", ["em=", "ed=", "ext="])
    except getopt.GetoptError:
        print "Input argument Invalid: "
        print "Valid inputs are Shown below"
        print """main.py
          -l <input language>        Language to run morse segmentation on
          -b <batch size>            Number of words to segment from model( -1 for full dataset)
          -p <partition size>        Number of words to group as a partition( -1 for no partition)
          -m <mode>                  Segment type (<SUFFIX> or <PREFIX>)
          -o <output directory>      Output directory
          -w <base word>             Minimum length of a word
          -e <edit distance>         Maximum edit distance a word can have beween another word in a SS 

          -em  <external mode>       <True> or <False> value if external model is going to be used

          External MODEL Mode Arguments( when <external mode> is used)

          -ed  <external model dir>  Directory of the external model
          -t <model type>            SELECT mode (<fasttext> or <word2vec>)"""
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print """main.py
            -l <input language>       Language to run morse segmentation on
            -b <batch size>           Number of words to segment from model( -1 for full dataset)
            -p <partition size>       Number of words to group as a partition( -1 for no partition)
            -m <mode>                 Segment type (<SUFFIX> or <PREFIX>)
            -o <output directory>     Output directory
            -w <base word>            Minimum length of a word
            -e <edit distance>        Maximum edit distance a word can have beween another word in a SS

            --em  <external mode>       <True> or <False> value if external model is going to be used

            External MODEL Mode Arguments( when <external mode> is used)

            --ed  <external model dir>  Directory of the external model
            -t <model type>             External model type (<fasttext> or <word2vec>)"""
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
        elif opt in "--em":
            bol = arg.lower()
            if bol == 'true':
                config['external_mode'] = True
            elif bol == 'false':
                config['external_mode'] = False
            else:
                print "External Mode takes an argument of <True> or <False>"
                sys.exit(2)

        elif opt in "--ed":
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

    if config['external_mode'] == False:
        print("INPUT PARAMETER:\n\
        LANGUAGE : {}\n\
        MODE : {}\n\n\
        BASE WORD : {}\n\
        EDIT DISTANCE : {}\n\n\
        BATCH SIZE : {}\n\
        PARTITION SIZE : {}\n\
        OUTPUT DIRECTORY : {}".format(config['language'], config['mode'], config['base_word'],
                                      config['edit_distance'], config['batch_size'],
                                      config['partition_size'], config['output_dir']))
    else:
        print("INPUT PARAMETER:\n\
        EXTERNAL MODEL DIR : {}\n\
        MODEL TYPE : {}\n\
        MODE : {}\n\n\
        BASE WORD : {}\n\
        EDIT DISTANCE : {}\n\n\
        BATCH SIZE : {}\n\
        PARTITION SIZE : {}\n\
        OUTPUT DIRECTORY : {}".format(config['external_model_dir'], config['model_type'],
                                      config['mode'], config['base_word'],
                                      config['edit_distance'], config['batch_size'],
                                      config['partition_size'], config['output_dir']))

def main(argv):
    """Main code to lanch code for morse segmentation """

    # Load default config
    config = json.loads(open(CONFIG_FILE_NAME).read())

    # update config file to user input
    parse_input(argv, config)
    print_config(config)

    if config['external_mode'] is False:
        model_file = download_model(config)
        config['model_type'] = 'word2vec'
    else:
        model_file = config['external_model_dir']


    #Create output directory if it doesnt exit
    if not os.path.exists(config['output_dir']):
        os.makedirs(config['output_dir'])

    start_morse(model_file, config)

if __name__ == "__main__":
    main(sys.argv[1:])



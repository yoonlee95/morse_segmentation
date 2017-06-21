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

def parse_input(argv, config):
    """ parse input file and updates the config file

    Args:
        argv (list): input argument from user
        config (dictionary): config dictionary

    Returns:
       NONE

    """
    try:
        opts, args = getopt.getopt(argv,"l:b:p:m:t:", ["ifile=", "ofile="])
    except getopt.GetoptError:
        print 'test.py -i <inputfile> -o <outputfile>'
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print 'test.py -i <inputfile> -o <outputfile>'
            sys.exit()
        elif opt in ("-i", "--ifile"):
            inputfile = arg
        elif opt in ("-o", "--ofile"):
            outputfile = arg
    print 'Input file is "', inputfile
    print 'Output file is "', outputfile

    
def main(argv):

    # Load default config
    config = json.loads(open(CONFIG_FILE_NAME).read())
    pprint(config)

    # update config file to user input
    parse_input(argv, config)


    #Get the iso639 from of the language
    iso639 = find_translation(config['language'])

    print "Language", config['language']
    print "ISO-639:", iso639

    model_file = "./model/wiki."+iso639+".vec"
    model_zip = "./model/wiki."+iso639+".zip"
    print SETTING
    print model_file

    if not os.path.exists(model_file):
        if not os.path.exists(model_zip):
            print "DOWNLOADING MODEL"
            print subprocess.check_output(['wget',WEB_BASE+iso639+".zip", '-P', './model/'])
        print "UNZIPPI1NG MODEL"
        print subprocess.check_output(['unzip','./model/wiki.'+iso639+".zip",'-d' ,"./model/"])
        print "MODEL INSTALLED"
        print subprocess.check_output(['rm','./model/wiki.'+iso639+".zip"])
        print subprocess.check_output(['rm','./model/wiki.'+iso639+".bin"])

    #Create output directory if it doesnt exit
    if not os.path.exists(config['output_dir']):
        os.makedirs(config['output_dir'])

    start_morse(model_file, config['batch_size'], config['partition_size'], config['mode'], config['output_dir'], config['base_word'], config['edit_distance'])

if __name__ == "__main__":
    main(sys.argv[1:])



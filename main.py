from language_to_iso639 import find_translation
import json
from morse import start_morse
from pprint import pprint
import os.path
import subprocess

WEB_BASE = "https://s3-us-west-1.amazonaws.com/fasttext-vectors/wiki."   #ab.zip"

CONFIG_FILE =open("config.json").read()

CONFIG = json.loads(CONFIG_FILE)
pprint(CONFIG)


#Get the iso639 from of the language
iso639 = find_translation(CONFIG['language'])

print "Language" , CONFIG['language']
print "ISO-639:" , iso639

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
if not os.path.exists(CONFIG['output_dir']):
    os.makedirs(CONFIG['output_dir'])

start_morse(model_file, CONFIG['batch_size'], CONFIG['partition_size'], CONFIG['mode'], CONFIG['output_dir'], CONFIG['base_word'], CONFIG['edit_distance'])



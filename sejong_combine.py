# -*- coding: utf-8 -*-

import codecs
import cPickle as pickle
import sys
from sklearn.model_selection import KFold

def contain_basecase(text):
    for i in text:
         if ord(i) < 128 and ord(i) != 32:
            return 0
         if ord(i) >= 0xE384B1 and ord(i) <= 0xE385A3:
            print text
            return 0
    return 1
def word_form_changed(raw, segment):
    for i in raw:
        if i not in segment:
            return 0
    return 1


    
sejong_raw = []
f = codecs.open("sejong_raw.txt", encoding='utf-8')
for line in f:
	sejong_raw.append((line.rstrip()))

sejong_segment = []
f = codecs.open("sejong_segmented.txt", encoding='utf-8')
for line in f:
	sejong_segment.append((line.rstrip()))



file = codecs.open("cleaned_combined_sejong.txt", "w", "utf-8")
# for i in range( 50):
for i in range( len(sejong_raw) ):
    if contain_basecase(sejong_segment[i]) and word_form_changed(sejong_raw[i], sejong_segment[i]):
        file.write(sejong_raw[i] + " " + sejong_segment[i] + "\n")
file.close()


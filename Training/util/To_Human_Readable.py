# -*- coding: utf-8 -*-

import os
import sys
import pickle

# DIR = '../test_3/'
if len(sys.argv) != 2:
    print "Input Argument Missing : Input_Dir"
    exit()
DIR = sys.argv[1]

if not os.path.exists('human_readable'):
    os.makedirs('human_readable')

ss_file = open('human_readable/ss_sem_H.txt', 'w')
rule_file = open('human_readable/rule_H.txt', 'w')
cos_file = open('human_readable/cos_H.txt', 'w')


for i in range(0,5):

    ss_sem = open(DIR + '/SUF_ss_'+str(i)+'.pkl', 'rb')
    r_sem = open(DIR + '/SUF_r_sem_'+str(i)+'.pkl', 'rb')
    r_orth = open(DIR + '/SUF_r_orth_'+str(i)+'.pkl', 'rb')
    w_sem = open(DIR + '/SUF_w_sem_'+str(i)+'.pkl', 'rb')
    mydict1 = pickle.load(ss_sem)
    mydict2 = pickle.load(r_sem)
    mydict3 = pickle.load(r_orth)
    mydict4 = pickle.load(w_sem)

    for i in mydict1:
        ss = mydict1[i]
        # string = u'(' + unicode(i[0]) +u','+ unicode(i[1]) + u') : ', u' [' + u','.join([u"(" + unicode(s[0])+u","+unicode(s[1]) + u")" for s in ss]) + u']'
        string = unicode(i[0]) +u','+ unicode(i[1]) + u' : ' 
        string += u'[' + u','.join([u"(" + unicode(s[0])+u","+unicode(s[1]) + u")" for s in ss]) + u']'
        string += u'\r\n'
        ss_file.write(string.encode('utf8'))
    for i in mydict2:
        string = unicode(i[0]) +u','+ unicode(i[1]) 
        string += u' : score: '+str(mydict2[i]) + ' size: ' + str(mydict3[i])
        string += u'\r\n'
        rule_file.write(string.encode('utf8'))

    for i in mydict4:
        string = unicode(i[0]) +u','+ unicode(i[1]) 
        string += u' : '+str(mydict4[i]) 
        string += u'\r\n'
        cos_file.write(string.encode('utf8'))




ss_file.close()
rule_file.close()
cos_file.close()

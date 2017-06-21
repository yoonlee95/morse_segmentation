# -*- coding: utf-8 -*-

import pickle

ss_file = open('ss_sem_H.txt', 'w')

for i in range(0,26):

    ss_sem = open('ss_sem_'+str(i)+'.pkl', 'rb')
    mydict1 = pickle.load(ss_sem)

    for i in mydict1:
        ss = mydict1[i]
        string = unicode(i[0]) +u','+ unicode(i[1]) 
        string += u' [' + u','.join([u"(" + unicode(s[0])+u","+unicode(s[1]) + u")" for s in ss]) + u']'
        string += u'\r\n'
        ss_file.write(string.encode('utf8'))



ss_file.close()

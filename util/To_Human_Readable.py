# -*- coding: utf-8 -*-

import pickle

ss_file = open('ss_sem_H.txt', 'w')
r_sem_file = open('r_sem_H.txt', 'w')

for i in range(0,26):

    ss_sem = open('ss_sem_'+str(i)+'.pkl', 'rb')
    r_sem = open('ss_sem_'+str(i)+'.pkl', 'rb')
    mydict1 = pickle.load(ss_sem)
    mydict2 = pickle.load(r_sem)

    for i in mydict1:
        ss = mydict1[i]
        string = unicode(i[0]) +u','+ unicode(i[1]) 
        string += u' [' + u','.join([u"(" + unicode(s[0])+u","+unicode(s[1]) + u")" for s in ss]) + u']'
        string += u'\r\n'
        ss_file.write(string.encode('utf8'))
    for i in mydict2:
        string = unicode(i[0]) +u','+ unicode(i[1]) 
        string = mydict2[i]
        string += u'\r\n'
        r_sem_file.write(string.encode('utf8'))



ss_file.close()
r_sem_file.close()

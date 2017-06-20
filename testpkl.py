# -*- coding: utf-8 -*-

import pickle


r_1 = u'' 
r_2 = u'와' 

w_1 = u'선교부'
w_2 =  u'선교부와'
for i in range(0,26):
    r_sem = open('korean_output_1m/r_sem_'+str(i)+'.pkl', 'rb')
    # pkl_file = open('ss_sem_'+str(i)+'.pkl', 'rb')
    loc_sem = open('korean_output_1m/loc_sem_'+str(i)+'.pkl', 'rb')
    r_orth = open('korean_output_1m/r_orth_'+str(i)+'.pkl', 'rb')
    w_sem = open('korean_output_1m/w_sem_'+str(i)+'.pkl', 'rb')
    # pkl_file = open('korean_output_full_4_combined/ss_sem_combined.pkl', 'rb')
    mydict1 = pickle.load(r_sem)
    mydict2 = pickle.load(loc_sem)
    mydict3 = pickle.load(r_orth)
    mydict4 = pickle.load(w_sem)
    r_sem.close()
    loc_sem.close()
    r_orth.close()
    w_sem.close()

    if (r_1, r_2) in mydict3:
        print "r_orth"
        print mydict3[(r_1,r_2)]
    if (r_1,r_2) in mydict1:
        print "r_sem"
        print mydict1[(r_1,r_2)]

    if (w_1,w_2) in mydict2:
        print "loc_sem"
        print mydict2[(w_1,w_2)]


    if (w_1,w_2) in mydict4:
        print "w_sem"
        print mydict4[(w_1,w_2)]

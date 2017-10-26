# -*- coding: utf-8 -*-

import pickle

FILE_BASE="../korean_500k_p_1_2_s_1_3/"
LOC = "SUF"

r_1 = u'' 
r_2 = u'약' 

# w_1 = u'여한'
# w_2 =  u'여한이'
for i in range(0,26):
    r_sem = open(FILE_BASE + LOC + '_r_sem_'+str(i)+'.pkl', 'rb')
    # loc_sem = open(FILE_BASE + LOC + '_loc_sem_'+str(i)+'.pkl', 'rb')
    r_orth = open(FILE_BASE + LOC + '_r_orth_'+str(i)+'.pkl', 'rb')
    ss = open(FILE_BASE + LOC + '_ss_'+str(i)+'.pkl', 'rb')
    # w_sem = open(FILE_BASE + LOC + '_w_sem_'+str(i)+'.pkl', 'rb')
    # pkl_file = open('korean_output_full_4_combined/ss_sem_combined.pkl', 'rb')
    mydict1 = pickle.load(r_sem)
    # mydict2 = pickle.load(loc_sem)
    mydict3 = pickle.load(r_orth)
    # mydict4 = pickle.load(w_sem)
    mydict5 = pickle.load(ss)
    r_sem.close()
    # loc_sem.close()
    r_orth.close()
    # w_sem.close()

    if (r_1, r_2) in mydict3:
        print "r_orth"
        print mydict3[(r_1,r_2)]
    if (r_1,r_2) in mydict1:
        print "r_sem"
        print mydict1[(r_1,r_2)]

    if (r_1,r_2) in mydict5:
        print "ss"
        x =  mydict5[(r_1,r_2)]
        string = u'[' + u','.join([u"(" + unicode(s[0])+u","+unicode(s[1]) + u")" for s in x]) + u']'
        print string

    # if (w_1,w_2) in mydict2:
    #     print "loc_sem"
    #     print mydict2[(w_1,w_2)]
    # if (w_1,w_2) in mydict4:
    #     print "w_sem"
    #     print mydict4[(w_1,w_2)]









    # counter = 0
    # for key,value in mydict2.iteritems():
    #     counter += 1
    #     # if counter > 30:
    #     #     break
    #     if key[0] == r_1 and key[1] == r_2:
    #         print key[0],key[1] , value
    #         # for j in value:
    #         #     if j[0] == u'선교부' and  j[1] == u'선교부와':
    #         #     # if j[0] ==  u'청와대' and j[1] == u'청와대와':
    #         #         # print key[0],key[1] 
    #         #         # print "hello"
    #         #         print j[0], j[1]
                

    # print key[0], key[1]
    # list = []
    # for i in value:
    #     print i[0], i[1]
    #     # list.append(i)

#     print i[1]
#     print ""
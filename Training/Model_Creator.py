# coding: utf-8

import cPickle as pickle
import sys

def model_creator(scores_pre_path, scores_suf_path):
    output_dict = {}

    path = scores_suf_path

    print "let the games begin"
    loc_sem = pickle.load(open(path + "/loc_sem.pkl"))
    print "loc_sem loaded"
    r_sem = pickle.load(open(path + "/r_sem.pkl"))
    print "r_sem loaded"
    r_orth = pickle.load(open(path + "/r_orth.pkl"))
    print "r_orth loaded"
    w_sem = pickle.load(open(path + "/w_sem.pkl"))
    print "w_sem loaded"
    ss_sem = pickle.load(open(path + "/ss_sem.pkl"))
    print "ss_sem loaded"


    total = len(ss_sem.keys())
    temp = 0
    for counter, rule in enumerate(ss_sem.keys()):
        if ((counter - temp) > 0.01*total):
            print float(counter)/total
            temp = counter
        hr = r_sem[rule]
        sss = r_orth[rule]
    	for instance in ss_sem[rule]:
            word1 = instance[0]
            word2 = instance[1]
            dis = loc_sem[instance]
            w_sem_val = w_sem[instance]
            rule_appended = ("suf", rule[0], rule[1])
            if word1 in output_dict:
                output_dict[word1].append((hr, sss, rule_appended, word2, rule_appended[1], w_sem_val, dis))
            else:
                output_dict[word1] = [(hr, sss, rule_appended, word2, rule_appended[1], w_sem_val, dis)]
            if word2 in output_dict:
                output_dict[word2].append((hr, sss, rule_appended, word1, rule_appended[2], w_sem_val, dis))
            else:
                output_dict[word2] = [(hr, sss, rule_appended, word1, rule_appended[2], w_sem_val, dis)]
    
    path = scores_pre_path

    print "let the games begin"
    loc_sem = pickle.load(open(path + "/loc_sem.pkl"))
    print "loc_sem loaded"
    r_sem = pickle.load(open(path + "/r_sem.pkl"))
    print "r_sem loaded"
    r_orth = pickle.load(open(path + "/r_orth.pkl"))
    print "r_orth loaded"
    w_sem = pickle.load(open(path + "/w_sem.pkl"))
    print "w_sem loaded"
    ss_sem = pickle.load(open(path + "/ss_sem.pkl"))
    print "ss_sem loaded"


    total = len(ss_sem.keys())
    temp = 0
    for counter, rule in enumerate(ss_sem.keys()):
        if ((counter - temp) > 0.01*total):
            print float(counter)/total
            temp = counter
        hr = r_sem[rule]
        sss = r_orth[rule]
    	for instance in ss_sem[rule]:
            word1 = instance[0]
            word2 = instance[1]
            dis = loc_sem[instance]
            w_sem_val = w_sem[instance]
            rule_appended = ("pre", rule[0], rule[1])
            if word1 in output_dict:
                output_dict[word1].append((hr, sss, rule_appended, word2, rule_appended[1], w_sem_val, dis))
            else:
                output_dict[word1] = [(hr, sss, rule_appended, word2, rule_appended[1], w_sem_val, dis)]
            if word2 in output_dict:
                output_dict[word2].append((hr, sss, rule_appended, word1, rule_appended[2], w_sem_val, dis))
            else:
                output_dict[word2] = [(hr, sss, rule_appended, word1, rule_appended[2], w_sem_val, dis)]

    total = len(output_dict.keys())
    temp = 0
    output_dict_v2 = {}
    for counter, word in enumerate(output_dict.keys()):
        if ((counter - temp) > 0.01*total):
            print float(counter)/total
            temp = counter
        temp_list = []
        sorted_list = sorted(output_dict[word], key=lambda x: x[0] + x[1] + x[5] + x[6], reverse = True)
        for tup in sorted_list:
            if tup[2][1]=="" or tup[2][2]=="":
                temp_list.append(tup)
        for tup in sorted_list:
            if tup[2][1]!="" and tup[2][2]!="":
                temp_list.append(tup)
        output_dict_v2[word] = temp_list
    pickle.dump(output_dict_v2, open("model.pkl", "w"), protocol = 2)


scores_pre_path = "scores_pre"
scores_suf_path = "scores_suf"

model_creator(scores_pre_path, scores_suf_path)

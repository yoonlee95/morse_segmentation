# coding: utf-8

import cPickle as pickle
import sys

def model_creator(ss_sem_path, output_path, prefix_index, suffix_index):
    output_dict = {}
    print "CREATING MODEL"

    print "LOADING SUFFIX DATA"
    try:
        ss_sem = pickle.load(open(ss_sem_path + "/SUF_ss_0.pkl"))
        loc_sem = pickle.load(open(ss_sem_path + "/SUF_loc_sem_0.pkl"))
        r_sem = pickle.load(open(ss_sem_path + "/SUF_r_sem_0.pkl"))
        r_orth = pickle.load(open(ss_sem_path + "/SUF_r_orth_0.pkl"))
        w_sem = pickle.load(open(ss_sem_path + "/SUF_w_sem_0.pkl"))
    except:
        print "ss_score files cant be found"
        exit()

    if suffix_index -1 > 0:
        for index in range(1, suffix_index):
            ss_sem.update(pickle.load(open(ss_sem_path + "/SUF_ss_"+str(index)+".pkl")))
            loc_sem.update(pickle.load(open(ss_sem_path + "/SUF_loc_sem_"+str(index)+".pkl")))
            r_sem.update(pickle.load(open(ss_sem_path + "/SUF_r_sem_"+str(index)+".pkl")))
            r_orth.update(pickle.load(open(ss_sem_path + "/SUF_r_orth_"+str(index)+".pkl")))
            w_sem.update(pickle.load(open(ss_sem_path + "/SUF_w_sem_"+str(index)+".pkl")))

    print "CREATING SUFFIX MODEL"

    total = len(ss_sem.keys())
    temp = 0
    for counter, rule in enumerate(ss_sem.keys()):
        if ((counter - temp) > 0.01*total):
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
    
    del ss_sem
    del loc_sem
    del r_sem
    del r_orth
    del w_sem
    print "LOADING PREFIX DATA"
    try:
        ss_sem = pickle.load(open(ss_sem_path + "/PRE_ss_0.pkl"))
        loc_sem = pickle.load(open(ss_sem_path + "/PRE_loc_sem_0.pkl"))
        r_sem = pickle.load(open(ss_sem_path + "/PRE_r_sem_0.pkl"))
        r_orth = pickle.load(open(ss_sem_path + "/PRE_r_orth_0.pkl"))
        w_sem = pickle.load(open(ss_sem_path + "/PRE_w_sem_0.pkl"))
    except:
        print "ss_score files cant be found"
        exit()

    if suffix_index -1 > 0:
        for index in range(1, prefix_index):
            ss_sem.update(pickle.load(open(ss_sem_path + "/PRE_ss_"+str(index)+".pkl")))
            loc_sem.update(pickle.load(open(ss_sem_path + "/PRE_loc_sem_"+str(index)+".pkl")))
            r_sem.update(pickle.load(open(ss_sem_path + "/PRE_r_sem_"+str(index)+".pkl")))
            r_orth.update(pickle.load(open(ss_sem_path + "/PRE_r_orth_"+str(index)+".pkl")))
            w_sem.update(pickle.load(open(ss_sem_path + "/PRE_w_sem_"+str(index)+".pkl")))

    print "CREATING PREFIX MODEL"


    total = len(ss_sem.keys())
    temp = 0
    for counter, rule in enumerate(ss_sem.keys()):
        if ((counter - temp) > 0.01*total):
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

    del ss_sem
    del loc_sem
    del r_sem
    del r_orth
    del w_sem

    total = len(output_dict.keys())
    temp = 0
    print "FINAL STAGE OF MODEL BUILDING"

    output_dict_v2 = {}
    for counter, word in enumerate(output_dict.keys()):
        if ((counter - temp) > 0.01*total):
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
    del output_dict
    print "Saving MODEL"
    pickle.dump(output_dict_v2, open(output_path+"/model.pkl", "wb"), protocol=2)




if __name__ == "__main__":
    model_creator("./ss_score_output", "./model_output",  13, 4)

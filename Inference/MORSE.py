# coding: utf-8

import cPickle as pickle
import sys
import random

def find_str(s, char):
    index = 0

    if char in s:
        c = char[0]
        for ch in s:
            if ch == c:
                if s[index:index+len(char)] == char:
                    return index

            index += 1

    return -1

def generate_all_ss(shorter):
        all_ss = []
        for head in range(len(shorter)-1):
                for tail in range(head+1, len(shorter)+1):
                        sc = shorter[head:tail]
                        all_ss.append((sc, len(sc), head, tail))
        all_ss_sorted = sorted(all_ss, key = lambda x:x[1], reverse = True)
        return all_ss_sorted

def find_lcs(shorter, longer):
        all_ss = generate_all_ss(shorter)
        for ss in all_ss:
                curr_ss = ss[0]
                head = ss[2]
                tail = ss[3]
                ind = find_str(longer, curr_ss)
                if ind != -1:
                        return (ind-head, ind+len(shorter) - head - 1)
        return -1

def get_full_bounds(init_word, pre_bounds, suff_bounds):
        bounds = pre_bounds + [len(init_word) - sum(pre_bounds + suff_bounds)] + suff_bounds
        s=0
        new_bounds = [0]
        for b in bounds:
                s += b
                new_bounds.append(s)
        segs = []
        for i in range(len(new_bounds)-1):
                string = init_word[new_bounds[i]:new_bounds[i+1]]
                segs.append(string)
        return segs

def segment_word(word, words_to_rule_dict, sss_cutoff, hr_cutoff, cs_cutoff, pw_cutoff, all_rules, with_replacement):

        prefixes = []
        suffixes = []

	word = word.decode("utf-8")

	init_word = word

        temp_word = ""

	head = 0
	tail = len(word)-1

	pre_bounds = []
	suff_bounds = []

        while(True):

                if word == temp_word:
                        break

                temp_word = word

                if word in words_to_rule_dict:
			lrules = words_to_rule_dict[word]
			#random.shuffle(lrules)
                        for tup in lrules:
                                if tup[1] > sss_cutoff and tup[0]>hr_cutoff and (tup[2][1] == "" or tup[2][2] == "" or all_rules) and tup[5] > cs_cutoff and tup[5]!=-1 and tup[6] > pw_cutoff:
                                        if len(tup[3]) < len(word):

                                                affix = tup[4]

                                                if tup[2][0] == "pre":
							if not(with_replacement):
                                                        	prefixes.append(affix)
                                                        	word = word[len(affix):]
							else:
								ht = find_lcs(tup[3], init_word)
								if ht != -1:
									(curr_head, curr_tail) = ht
									if curr_head > head:
										prefixes.append(affix)
										head = head + len(affix)
										pre_bounds.append(len(affix))
								word = tup[3]
                                                elif tup[2][0] == "suf":
							if not(with_replacement):
                                                        	suffixes.insert(0,affix)
                                                        	word = word[:-len(affix)]
							else:
								ht = find_lcs(tup[3], init_word)
								if ht != -1:
									(curr_head, curr_tail) = ht
									if curr_tail < tail :
										suffixes.insert(0,affix)
										tail = tail - len(affix)
										suff_bounds.insert(0,len(affix))
								word = tup[3]

                                                break

	if not(with_replacement):
        	return prefixes + [word] + suffixes
	else:
		#return get_full_bounds(init_word, pre_bounds, suff_bounds)
        	return prefixes + [word] + suffixes

def segment_word_full(word, words_to_rule_dict, sss_cutoff, hr_cutoff, cs_cutoff, pw_cutoff, all_rules, with_replacement):

	predicted_morphs = []
	gen_splits = word.split("'")
	word = gen_splits[0]
	gen_part = []
	if len(gen_splits) == 2:
		gen_part = ["'" + gen_splits[1]]

	compounds = word.split("-")
	for comp in compounds:
		predicted_morphs += segment_word(comp, words_to_rule_dict, sss_cutoff, hr_cutoff, cs_cutoff, pw_cutoff, all_rules, with_replacement) + ["-"]
	if predicted_morphs[-1] == "-":
		predicted_morphs = predicted_morphs[:-1]
	predicted_morphs = predicted_morphs + gen_part

	return predicted_morphs

model = pickle.load(open("model.pkl"))
sss_cutoff = 45
hr_cutoff = 0.1
cs_cutoff = 0.1
pw_cutoff = -100
all_rules = True
with_replacement = True
infile = open(sys.argv[1])
outfile = open(sys.argv[2], "w")
for line in infile:
	word = line.strip()
	morphs = segment_word_full(word, model, sss_cutoff, hr_cutoff, cs_cutoff, pw_cutoff, all_rules, with_replacement)
	#outfile.write(" ".join(morphs) + "\n")
	for morph in morphs:
		outfile.write(morph.encode("utf-8") + " ")
	outfile.write("\n")
outfile.close()

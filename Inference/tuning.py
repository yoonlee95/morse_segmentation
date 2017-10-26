# -*- coding: utf-8 -*-

import codecs
import cPickle as pickle
import sys
from MORSE import *
from sklearn.model_selection import KFold

def morphs_to_boundaries(morphemes):
        boundaries = []
        count = 0
        for morph in morphemes:
                boundaries.append(str(count))
                count += len(morph)
        boundaries.append(str(count))
        return boundaries[1:-1]

def eval_our_segmentor_PRFA(dataset_lines, output_dict, params, all_rules, with_r):

	pred_bs = []
	gold_bs = []

	[sss_cutoff, hr_cutoff, cs_cutoff, pw_cutoff] = params

	TP = 0
	TN = 0
	FP = 0
	FN = 0
	corr = 0
	tots = 0
	nsegments = 0

	for line in dataset_lines:
		word = line.split()[0]
		gen_splits = word.split("'")
		gen_splits = []
		gen_splits.append(word)


		# gen_splits = [i.encode("utf-8") for i in gen_splits]

		word = gen_splits[0]
		gen_part = []
		if len(gen_splits) == 2:
			gen_part = ["'" + gen_splits[1]]
                gold_morphs = line.split()[1:]
		if "aa" in gold_morphs:
			continue
		tots += 1
		predicted_morphs = []
		compounds = word.split("-")
		for comp in compounds:
                	predicted_morphs += segment_word(comp, output_dict, sss_cutoff, hr_cutoff, cs_cutoff, pw_cutoff, all_rules, with_r) + ["-"]
		if predicted_morphs[-1] == "-":
			predicted_morphs = predicted_morphs[:-1]
		predicted_morphs = predicted_morphs + gen_part
		#print line
		#print predicted_morphs
		# print gold_morphs, predicted_morphs
		nsegments += len(predicted_morphs)
		if predicted_morphs == gold_morphs:
			corr += 1
			gold_bounds = morphs_to_boundaries(gold_morphs)
			predicted_bounds = morphs_to_boundaries(predicted_morphs)
		pred_bs.append(predicted_bounds)
		gold_bs.append(gold_bounds)

		currTP = len(set(predicted_bounds) & set(gold_bounds))
		currFP = len(set(predicted_bounds) - set(gold_bounds))
		currTN = len(word) - currTP - currFP - 1
		currFN = len(set(gold_bounds) - set(predicted_bounds))
		TP += currTP
		TN += currTN
		FP += currFP
		FN += currFN

	Precision = float(TP)/((TP + FP) + 0.0001)
	Recall = float(TP)/((TP + FN) + 0.0001)
	F1 = 2*(Precision*Recall)/((Precision + Recall) + 0.0001)
	Acc = float(corr)/tots
	#print "Number of Segmentations = ", nsegments

	pickle.dump(pred_bs, open("pred_bs.pkl", "w"), protocol = 2)
	pickle.dump(gold_bs, open("gold_bs.pkl", "w"), protocol = 2)

	return (Precision, Recall, F1, Acc)

def tune(dataset_lines, model, all_rules, with_r, metric, hr_off = False, sss_off = False, cs_off = False, pw_off = False):

	metric_index = ["P", "R", "F", "A"].index(metric)

	params = []

	max_value = 0

	hr_loop = [float(i)/100 for i in range(0,100, 5)]
	sss_loop = [float(i)/1 for i in range(0,50, 5)]
	cs_loop = [float(i)/100 for i in range(0,50, 5)]
	pw_loop = [float(i)/100 for i in range(0,100, 5)]

	if hr_off:
		hr_loop = [-2]
	if sss_off:
		sss_loop = [-2]
	if cs_off:
		cs_loop = [-2]
	if pw_off:
		pw_loop= [-2]

	P = []
	R = []
	F = []

	for hit_rate in hr_loop:
		for sss_cutoff in sss_loop:
			for cs_cutoff in cs_loop:
				for pw_cutoff in pw_loop:
					params_curr = [sss_cutoff, hit_rate, cs_cutoff, pw_cutoff]
					full_score =  eval_our_segmentor_PRFA(dataset_lines, model, params_curr, all_rules, with_r)
					score = full_score[metric_index]
					P.append(full_score[0])
					R.append(full_score[1])
					F.append(full_score[2])
					if score > max_value:
						max_value = score
						params = params_curr
						print max_value
						print params

	return params

tuning_set_path = sys.argv[1]
model_path = sys.argv[2]

tuning_set_lines = []
f = codecs.open(tuning_set_path, encoding='utf-8')
for line in f:
	# print (line)
	tuning_set_lines.append((line))
# tuning_set_lines = open(tuning_set_path).readlines()

all_rules = True
with_r = True

metric = "F"

model = pickle.load(open(model_path))

best_parameter =  tune(tuning_set_lines, model, all_rules, with_r, metric, pw_off = False)
print "best Parameter: " , best_parameter


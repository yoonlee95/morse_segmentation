import pickle
import os

DICT = 'korean_output_full_4_rev_combined/'
# FILE = 'loc_sem_'
FILES = ['ss_sem_','w_sem_', 'r_sem_', 'r_orth_', 'loc_sem_']
#FILES = [ 'r_orth_', 'loc_sem_']
combined = {}
count = 0
countcombin = 0
for FILE in FILES:
    for i in range(341):
        pkl_file = open('korean_output_rev_full_4/'+FILE+str(i)+'.pkl', 'rb')
        hi = pickle.load(pkl_file)
        pkl_file.close()

        combined.update(hi)
	

    if not os.path.exists(DICT):
        os.makedirs(DICT)
	

    pickle.dump( combined, open( DICT + FILE + "combined.pkl", "wb"))
    print FILE + " DONE"

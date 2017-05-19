import pickle

pkl_file = open('pkloutput100k/loc_sem.pkl', 'rb')
mydict2 = pickle.load(pkl_file)
pkl_file.close()


print mydict2
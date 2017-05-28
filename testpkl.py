import pickle

pkl_file = open('korean_output_full_4/ss_sem_1.pkl', 'rb')
# pkl_file = open('korean_output_full_4_combined/ss_sem_combined.pkl', 'rb')
mydict2 = pickle.load(pkl_file)
pkl_file.close()

print type(mydict2)
for i in mydict2:
    print i[0], i[1]
#     print i[1]
#     print ""
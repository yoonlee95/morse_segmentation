# -*- coding: utf-8 -*-

import pickle
from Queue import *
from tree_structure import ALPHABETTREE
from wordGroup import WORDGROUP
import time

def contain_ascii(text):
    for i in text:
         if ord(i) < 128:
#        if (ord(i) < 0x3130 or ord(i) > 0xD79E ):
            # print text
            # k = []
            # for i in text:
            #      k.append(i)
            # print k

            return 1

    return 0
def getsegmentation(data, base_word_len, edit_dist):
    word_segmentation = {}

    ROOT = ALPHABETTREE(None, '', 0)
    neighbor_nodes = Queue()

    counter = 0
    progress = len(data)/10
    #for all words in the pickle data
    for word in data:
        counter += 1
        if counter % progress == 0:
            print("BUILT "+str(counter/progress*10)+ " % of DATA")

        # if contain_ascii(word) == 1 :
        #     # print word
        #     continue
        # word = word.lower()

        cur_node = ROOT
        #####################################################
        #traverse the tree using the letters of the word#####
        #Create new nodes if neccesary.                 #####
        #####################################################
        word_len = len(word)

        for pos, letter in enumerate(word):

            cur_node = cur_node.traverse_alphabet(letter)



        #Remove duplicates
        if cur_node.get_word() != "":
            # print cur_node.get_word()
            continue

        #3#####################################################
        ## reset traverse_node to staring to scanning range####
        ## Gets the nodes to explore with depth it should#####
        #######################################################



        prev_node = cur_node
        traverse_node = prev_node
        pos = traverse_node.get_position()
        # print pos
        if pos < base_word_len:
            pass
        elif pos == base_word_len:
            #add extended words
            for node in cur_node.get_next_alphabets():
                neighbor_nodes.put((node, base_word_len, 1))

        else:
            for i in range(edit_dist-1):

                prev_node = traverse_node
                traverse_node = traverse_node.get_prev_pos()
                pos = traverse_node.get_position()

                #Rule: base word word needs to be >= 3

                #add the stems of the word
                for node in traverse_node.get_next_alphabets():
                    if node is not prev_node:
                        #add branches
                        neighbor_nodes.put((node, pos, i+2))
                    else:
                        cur_word = node.get_word()

                        #check if the cur_word is not empty
                        if cur_word:
                            segmentation = ("", word[pos+1:])
                            if not word_segmentation.has_key(segmentation):
                                word_segmentation[segmentation] = [] 
                            word_segmentation[segmentation].append((cur_word, word))

                if pos < base_word_len + 1:
                    break



            cur_word = traverse_node.get_word()
            pos = traverse_node.get_position()

            if cur_word:
                segmentation =("", word[pos:])
                if not word_segmentation.has_key(segmentation):
                    word_segmentation[segmentation] = [] 
                word_segmentation[segmentation].append((cur_word, word))
                # cur_word_group.add_word(cur_group.get_word())

            end_node = traverse_node.get_prev_pos()
            if pos-1 >= base_word_len:

                cur_word = end_node.get_word()
                if cur_word:
                    segmentation = ("", word[pos-1:])
                    if not word_segmentation.has_key(segmentation):
                        word_segmentation[segmentation] = [] 
                    word_segmentation[segmentation].append((cur_word, word))

            #add extended words
            pos = cur_node.get_position()
            for node in cur_node.get_next_alphabets():
                neighbor_nodes.put((node, pos, 1))

        cur_node.set_word(word)
        ###############################################
        #Get all the word objects created by the graph#
        ###############################################

        while neighbor_nodes.empty() == False:

            node, start, level = neighbor_nodes.get()

            # add the words to the proper data structures
            cur_word = node.get_word()
            if cur_word:

                cur_word_len = node.get_position()


                d_1 = cur_word[start:]
                d_2 = word[start:]



                if cur_word_len > word_len:
                    segmentation = (d_2, d_1)

                    if not word_segmentation.has_key(segmentation):
                        word_segmentation[segmentation] = []

                    word_segmentation[segmentation].append((word, cur_word))
                elif word_len > cur_word_len:
 
                    segmentation = (d_1, d_2)
                    if not word_segmentation.has_key(segmentation):
                        word_segmentation[segmentation] = []

                    word_segmentation[segmentation].append((cur_word, word))
                else:
                    if d_1 < d_2:
                        segmentation = (d_1, d_2)
                        if not word_segmentation.has_key(segmentation):
                            word_segmentation[segmentation] = []

                        word_segmentation[segmentation].append((cur_word, word))
                    else:
                        segmentation = (d_2, d_1)
                        if not word_segmentation.has_key(segmentation):
                            word_segmentation[segmentation] = []

                        word_segmentation[segmentation].append((word, cur_word))


            #add next level if should
            if level < edit_dist:
                neighbors = node.get_next_alphabets()

                for neighbor in neighbors:
                    neighbor_nodes.put((neighbor, start, level+1))




    print "Created graph."
    # for key,value in word_segmentation.iteritems():
        # if len(value) > 1:
            # print key , value

    return word_segmentation
    

if __name__ == "__main__":
    import timeit
    setup = "from __main__ import getsegmentation"


    with open('googlenews_vocab.pkl', 'rb') as f:
        full_data = pickle.load(f)

    print "pickle file loaded"

    d = full_data[:500]


    # for index in range(100000):
    #     d[index] = d[index][::-1]
    # d = len(full_data)
    # d = ['discriminating', 'discriminatory', 'discrimination', 'discriminate','discriminates',  'discriminated']
    d = [ 'aaaaaa', 'aaaaaab','aaaaaabb',  'aaaaaabbb', 'aaaaaabbbb', 'aaaaaabbbbb', 'aaaaaabbbbbb', 'aaaaaabbbbbbb','aa','aaa','aaaa','aaaaaac','aaaaa']
    # d = ['aaa','aaa']
    # i = [['aaaaaab','aaaaaa' ],['aaaaaabb','aaaaaa' ],['aaaaaabbb','aaaaaa' ],['aaaaaabbbb','aaaaaa' ],['aaaaaabbbbb','aaaaaa' ],['aaaaaabbbbbb','aaaaaa' ],['aaaaabbbbb','aaaaaa' ],['aaaaaabbbbbbb','aaaaaa']]
    # d = ['aaaccc','aaabbbb']

    # print d
    # for i in d:
    #     if i == "discrimination":
    #         print "found"
    # d = ["discriminate","discrimination"]
    # getsegmentation(d)
    # for d in i:
    #     d = [d[1][3:], d[0][3:]]
    #     print "-----------------"
    #     print d
    time =  timeit.timeit("getsegmentation("
    +str(d)+")", setup=setup, number = 1)/1
    print time



    # for key,value in word_segmentation.iteritems():
    #     print key ,value
    # print "discriminate" in d
    # print "discrimination" in d

    # list = []
    # for size in range(80):

    #     data_len = size * 5000
    #     d = full_data[:data_len]
    
    #     time =  timeit.timeit("getsegmentation("
    #     +str(d)+")", setup=setup, number = 5)/5
    #     print time

    #     list.append((data_len, time))

    # print list

    # measure process time

    # measure wall time
    # t0 = time.time()
    # getsegmentation()
    # print time.time() - t0, "seconds wall time"
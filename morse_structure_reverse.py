import pickle
from Queue import *
from tree_structure import ALPHABETTREE
from wordGroup import WORDGROUP
import time

def getsegmentation(data):
    word_segmentation = {}

    ROOT = ALPHABETTREE(None, '', 0)
    neighbor_nodes = Queue()

    #for all words in the pickle data
    for word in data:


        cur_node = ROOT
        #####################################################
        #traverse the tree using the letters of the word#####
        #Create new nodes if neccesary.                 #####
        #####################################################
        word = word.lower()
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
        if pos < 3:
            pass
        elif pos == 3:
            #add extended words
            for node in cur_node.get_next_alphabets():
                neighbor_nodes.put((node, 3, 1))

        else:
            for i in range(5):

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
                            r_word = word[pos+1:]
                            r_word = r_word[::-1]
                            segmentation = ("", r_word)
                            if not word_segmentation.has_key(segmentation):
                                word_segmentation[segmentation] = [] 
                            word_segmentation[segmentation].append((cur_word[::-1], word[::-1]))

                if pos < 4:
                    break



            cur_word = traverse_node.get_word()
            pos = traverse_node.get_position()

            if cur_word:
                r_word = word[pos:]
                r_word = r_word[::-1]
                segmentation =("", r_word)
                if not word_segmentation.has_key(segmentation):
                    word_segmentation[segmentation] = [] 
                word_segmentation[segmentation].append((cur_word[::-1], word[::-1]))
                # cur_word_group.add_word(cur_group.get_word())

            end_node = traverse_node.get_prev_pos()
            if pos-1 >= 3:

                cur_word = end_node.get_word()
                if cur_word:
                    r_word = word[pos-1:]
                    r_word = r_word[::-1]
                    segmentation = ("", r_word)
                    if not word_segmentation.has_key(segmentation):
                        word_segmentation[segmentation] = [] 
                    word_segmentation[segmentation].append((cur_word[::-1], word[::-1]))

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
                d_1 = d_1[::-1]
                d_2 = word[start:]
                d_2 = d_2[::-1]



                if cur_word_len > word_len:
                    segmentation = (d_2, d_1)

                    if not word_segmentation.has_key(segmentation):
                        word_segmentation[segmentation] = []

                    word_segmentation[segmentation].append((word[::-1], cur_word[::-1]))
                elif word_len > cur_word_len:
 
                    segmentation = (d_1, d_2)
                    if not word_segmentation.has_key(segmentation):
                        word_segmentation[segmentation] = []

                    word_segmentation[segmentation].append((word[::-1], cur_word[::-1]))
                else:
                    if d_1 < d_2:
                        segmentation = (d_1, d_2)
                        if not word_segmentation.has_key(segmentation):
                            word_segmentation[segmentation] = []

                        word_segmentation[segmentation].append((word[::-1], cur_word[::-1]))
                    else:
                        segmentation = (d_2, d_1)
                        if not word_segmentation.has_key(segmentation):
                            word_segmentation[segmentation] = []

                        word_segmentation[segmentation].append((word[::-1], cur_word[::-1]))



            #add next level if should
            if level < 6:
                neighbors = node.get_next_alphabets()

                for neighbor in neighbors:
                    neighbor_nodes.put((neighbor, start, level+1))




    print "Created graph."
    # for key,value in word_segmentation.iteritems():
    #     print key ,value
    #     # count += len(value)

    return word_segmentation

if __name__ == "__main__":
    import timeit
    setup = "from __main__ import getsegmentation"


    with open('googlenews_vocab.pkl', 'rb') as f:
        full_data = pickle.load(f)

    print "pickle file loaded"

    d = full_data[:100000]


    for index in range(100000):
        if len(d[index]) > 0:
            d[index] = d[index][::-1]
    # d = len(full_data)
    # d = ['discriminating', 'discriminatory', 'discrimination', 'discriminate','discriminates',  'discriminated']
    # d = [ 'aaaaaa', 'aaaaaab','aaaaaabb',  'aaaaaabbb', 'aaaaaabbbb', 'aaaaaabbbbb', 'aaaaaabbbbbb', 'aaaaaabbbbbbb','aa','aaa','aaaa','aaaaaac','aaaaa']
    # d = ['aaa','aaa']
    # i = [['aaaaaab','aaaaaa' ],['aaaaaabb','aaaaaa' ],['aaaaaabbb','aaaaaa' ],['aaaaaabbbb','aaaaaa' ],['aaaaaabbbbb','aaaaaa' ],['aaaaaabbbbbb','aaaaaa' ],['aaaaabbbbb','aaaaaa' ],['aaaaaabbbbbbb','aaaaaa']]
    # d = ['aaa','aaabbb']

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
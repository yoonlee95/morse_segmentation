import pickle
from Queue import *
from tree import ALPHABETTREE
from wordGroup import WORDGROUP
import time

def getsegmentation(data):
    # data = ['aaaabbb', 'aaaaaaa']

    ROOT = ALPHABETTREE(None, '', 0)

    #for all words in the pickle data
    for word in data:

        # print "------"
        # print word

        cur_node = ROOT
        #####################################################
        #traverse the tree using the letters of the word#####
        #Create new nodes if neccesary.                 #####
        #####################################################
        word = word.lower()
        for pos, letter in enumerate(word):

            cur_node = cur_node.traverse_alphabet(letter)


        #create worgroup for the current word
        cur_word_group = WORDGROUP(word)
        cur_node.set_word_group(cur_word_group)

        #3#####################################################
        ## reset traverse_node to staring to scanning range####
        ## Gets the nodes to explore with depth it should#####
        #######################################################


        # print word
        neighbor_nodes = Queue()

        prev_node = cur_node
        traverse_node = prev_node.get_prev_pos()

        if traverse_node.get_position() == 2:
            pass

        else:
            for i in range(5):

                pos =  traverse_node.get_position()
                # print pos
                #Rule: base word word needs to be >= 3


                if pos < 3:
                    break

                if i == 4 or pos == 3:
                    cur_group = traverse_node.get_word_group()
                    if cur_group is not None:

                        cur_group.add_word(word)
                        cur_word_group.add_word(cur_group.get_word())

                    end_node = traverse_node.get_prev_pos()
                    if end_node.get_position() >= 3:

                        cur_group = end_node.get_word_group()
                        if cur_group is not None:

                            cur_group.add_word(word)
                            cur_word_group.add_word(cur_group.get_word())


                #add the stems of the word
                for node in traverse_node.get_next_alphabets():
                    if node is not prev_node:
                        #add branches
                        neighbor_nodes.put((node, i+2))
                    elif i != 0:
                        #add stems of the word
                        cur_group = node.get_word_group()
                        if cur_group is not None:

                            cur_group.add_word(word)
                            cur_word_group.add_word(cur_group.get_word())

                prev_node = traverse_node
                traverse_node = traverse_node.get_prev_pos()

            #add extended words
        for node in cur_node.get_next_alphabets():
            neighbor_nodes.put((node, 1))



        ###############################################
        #Get all the word objects created by the graph#
        ###############################################

        while neighbor_nodes.empty() == False:

            node, level = neighbor_nodes.get()

            # add the words to the proper data structures
            cur_group = node.get_word_group()
            if cur_group is not None:

                cur_group.add_word(word)

                # print cur_group.get_list()

                cur_word_group.add_word(cur_group.get_word())

            #add next level if should
            if level < 6:
                neighbors = node.get_next_alphabets()

                for neighbor in neighbors:
                    neighbor_nodes.put((neighbor, level+1))




    print "Created graph."

    nodes = Queue()

    nodes.put(ROOT)
    

    # for i in range(6+steps):
    while nodes.empty() == False:

        node = nodes.get()

        # add the words to the proper data structures
        cur_group = node.get_word_group()

        # if cur_group is not None:
            # print cur_group.get_word().encode('ascii', 'ignore')   , cur_group.get_list()

        nextnodes = node.get_next_alphabets()

        for nextnode in nextnodes:
            nodes.put(nextnode)
    print "segmentation done"




    

if __name__ == "__main__":
    import timeit
    setup = "from __main__ import getsegmentation"


    with open('googlenews_vocab.pkl', 'rb') as f:
        full_data = pickle.load(f)

    print "pickle file loaded"

    d = full_data[:1000000]
    # d = len(full_data)
    # d = ['discriminating', 'discriminatory', 'discrimination', 'discriminate','discriminates',  'discriminated']
    # d = [ 'aaaaaa', 'aaaaaab','aaaaaabb',  'aaaaaabbb', 'aaaaaabbbb', 'aaaaaabbbbb', 'aaaaaabbbbbb', 'aaaaaabbbbbbb','aa','aaa','aaaa']

    # print d
    # for i in d:
    #     if i == "discrimination":
    #         print "found"
    # d = ["discriminate","discrimination"]
    # getsegmentation(d)
    time =  timeit.timeit("getsegmentation("
    +str(d)+")", setup=setup, number = 1)/1
    print time
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
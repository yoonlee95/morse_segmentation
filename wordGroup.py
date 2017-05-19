
class WORDGROUP(object):

    def __init__(self, word):


        #data structure for storing neighbers of the current word
        self.num = 0
        self.neighber_list = []

        #set the wordgroup word
        self.word = word


    def get_word(self):
        return self.word

    def add_word(self, word):

        self.neighber_list.append(word)
        self.num += 1

    def get_list(self):

        return self.neighber_list
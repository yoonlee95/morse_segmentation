class ALPHABETTREE(object):

    def __init__(self, parent, letter, position):

        self.prev_alphabet = parent
        self.position = position
        self.letter = letter


        #create an empty dictionary for next alphabet
        self.next_alphabet = {}

        self.word_group = None

    def get_position(self):
        return self.position

    def get_prev_pos(self):
        return self.prev_alphabet

    def get_info(self):
        """ return letter and position """

        return (self.letter, self.position)

    def set_word_group(self, group):
        """ set group for the current word """
        self.word_group = group

    def get_word_group(self):
        """ set group for the current word """
        return self.word_group

    def get_next_alphabets(self):
        """ set all the next letters that we found """
        return self.next_alphabet.values()
    def traverse_alphabet(self, alphabet):

        if self.next_alphabet.has_key(alphabet):
            return self.next_alphabet[alphabet]
        else:

            #create next alphabet object if there isnt one
            letter = ALPHABETTREE(self, alphabet, self.position + 1)

            self.next_alphabet[alphabet] = letter
            return letter



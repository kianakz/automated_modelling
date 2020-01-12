from operator import *

class Nogood:
    def __init__(self, ID, unsorted_seq_lits, red, paths):
        """
        :param ID: string (digit)
        :param unsorted_seq_lits: list of Literals
        :param red: int
        :param paths: string
        """
        self.unsorted_seq_lits = unsorted_seq_lits
        self.ID = ID
        self.red = red
        self.paths = paths
        self.seq_lits = self.unsorted_seq_lits
        # self.seq_lits = self.sort_nogood()
        self.name = ""
        self.__calculate_name__()
        self.name = self.get_name()
        self.params = []
        self.__calculate_params__()
        self.params = self.get_params()

    def __repr__(self):
        return self.name

    def __calculate_params__(self):
        self.params = []
        for lit in self.seq_lits:
            self.params += lit.get_params()

    def __calculate_name__(self):
        self.name = ""
        for seq_lit in self.seq_lits:
            self.name += seq_lit.get_literal_str() + " "

    def get_name(self):
        return self.name

    def get_ID(self):
        return self.ID

    def get_seq_lits(self):
        return self.seq_lits

    def get_red(self):
        return self.red

    def get_paths(self): #the line number in the path file
        return self.paths

    def sort_nogood(self):
        """
        Sorts the literals in a nogood based on their name, operator, index and value
        :param no_good: String
        :return: String
        """
        seq_lits = sorted(self.unsorted_seq_lits, key=attrgetter('variable_names', 'operators', 'params_int'))
        return seq_lits

    def get_params(self):

        return self.params




from Pattern import *
import operator
from copy import *
from functions import *
from Globals import *
#from get_input_data import *


if not ignore_data_file:
    from get_input_data import *

class Fact:
    def __init__(self, pattern):
        """
        :param pattern: An instance of a Pattern class
        :param var_type_dim: String (type of dimension e.g. PIZZA)
        :param var_type_enum: String (type of enum associated to the var_type_dim e.g. VOUCHER)
        """

        self.pattern_name = pattern.get_name()
        self.pattern = pattern
        self.var_types = pattern.get_var_types()

        self.max_percentage_single_fact = []
        self.max_map_whole_fact = []
        self.max_fact_whole_fact = []

        self.max_percentage_single_fact_parameter = []
        self.max_map_whole_fact_parameter = []
        self.max_fact_whole_fact_parameter = []

        self.maps = tuple(pattern.get_maps())  # pattern.get_maps() returns a list, I converted to tuple to be immutable
        self.calculate_facts_pattern_max_nogood()

    def calculate_single_fact_each_nogood(self, map1, var1, var2):
        """
        :param map1: dict, maps variables to the values, it corresponds to a single nogood
        :param var1: Char, represents a pattern variable
        :param var2: Char, represents a pattern variable
        :return: str: represents a binary relationship between var1 and var2 (=, <, >)
        e.g "var1 > var2"
        """
        fact_str_each_nogood = ""
        if map1[var1] < map1[var2]:
            fact_str_each_nogood += var1 + "<" + var2
        elif map1[var1] > map1[var2]:
            fact_str_each_nogood += var1 + ">" + var2
        elif map1[var1] == map1[var2]:
            fact_str_each_nogood += var1 + "=" + var2
        fact_str_each_nogood += " "
        return fact_str_each_nogood

    def get_percentage_of_nogoods_with_the_same_single_fact(self, fact1, var1, var2):
        """
        :param map1: dict, maps variables to the values, it corresponds to a single nogood
        :param var1: Char, represents a pattern variable
        :param var2: Char, represents a pattern variable
        :return: represents the percentage of nogoods that a fact is true for
        """
        n_nogoods = len(self.maps)
        n_nogood_same_facts = 0
        maps_test = ""
        for m1 in range(0, n_nogoods):  # each nogood
            fact2 = self.calculate_single_fact_each_nogood(self.maps[m1], var1, var2)  # fact for the first nogood
            if fact1 == fact2:
                n_nogood_same_facts += 1
                maps_test += json.dumps(self.maps[m1]) + " "
        percentage = float(n_nogood_same_facts) / float(n_nogoods) * 100.0
        return percentage

    def calculate_single_fact_each_nogood_parameter(self, map1, var1, var2, param):
        """
        :param map1: dict, maps variables to the values, it corresponds to a single nogood
        :param var1: Char, represents a pattern variable
        :param var2: Char, represents a pattern variable
        :param param: str: represents a model parameter
        :return: str: represents a binary relationship between param[var1] and param[var2] (=, <, >)
        e.g "param[var1] > param[var2]"
        """
        try:
            index = param_names.index(param)
            param_list = param_values[index]
            fact_str_each_nogood = ""
            if param_list[int(map1[var1])-1] < param_list[int(map1[var2])-1]:
                fact_str_each_nogood += param + "[" + var1 + "]" + " < " + param + "[" + var2 + "]"
            elif param_list[int(map1[var1])-1] > param_list[int(map1[var2])-1]:
                fact_str_each_nogood += param + "[" + var1 + "]" + " > " + param + "[" + var2 + "]"
            elif param_list[int(map1[var1])-1] == param_list[int(map1[var2])-1]:
                fact_str_each_nogood += param + "[" + var1 + "]" + " = " + param + "[" + var2 + "]"
            fact_str_each_nogood += " "
            return fact_str_each_nogood
        except:
            x=1



    def get_percentage_of_nogoods_with_the_same_single_fact_parameter(self, fact1, var1, var2, param1):
        """
        :param map1: dict, maps variables to the values, it corresponds to a single nogood
        :param var1: Char, represents a pattern variable
        :param var2: Char, represents a pattern variable
        :param param1: str, represents a model parameter
        :return: percentages of the nogoods that a fact is true for
        """
        n_nogoods = len(self.maps)
        n_nogood_same_facts = 0
        maps_test = ""
        if fact1 == "null":
            return "null"
        for m1 in range(0, n_nogoods):  # each nogood
            fact2 = self.calculate_single_fact_each_nogood_parameter(self.maps[m1], var1, var2, param1)  # fact for the first nogood
            if fact1 == fact2:
                n_nogood_same_facts += 1
                maps_test += json.dumps(self.maps[m1]) + " "
        percentage = float(n_nogood_same_facts) / float(n_nogoods) * 100.0

        return percentage

    def calculate_facts_pattern_max_nogood(self):
        self.max_percentage_single_fact = []
        self.max_map_whole_fact = []
        self.max_fact_whole_fact = []

        self.max_percentage_single_fact_parameter = []
        self.max_map_whole_fact_parameter = []
        self.max_fact_whole_fact_parameter = []

        n_nogoods = len(self.maps)
        all_objects_of_same_type = self.pattern.get_all_objects_of_the_same_type()
        parameters_indexed_by_objects = self.pattern.get_parameters_indexed_by_objects()
        corresponding_types = self.pattern.get_var_types_no_rep()

        # just variables
        for l in range(0, len(all_objects_of_same_type)):  # all objects of the same type
            tuples = [obj for obj in all_objects_of_same_type[l] if
                      type(obj) == tuple]  # all the parameters that have the
            # same enum type as vars (all the tuples)
            vars = [obj for obj in all_objects_of_same_type[l] if
                    is_variable(obj)]  # all the variables of the same type
            for obj1 in range(0, len(vars)):  # for variables of the same type
                var_1 = vars[obj1]
                for obj2 in range(obj1 + 1, len(vars)):  # compare each pair of variables together and pass it to CONACQ
                    var_2 = vars[obj2]
                    fact1 = self.calculate_single_fact_each_nogood(self.maps[0], var_1, var_2)  # fact for the first nogood
                    temp_max_percentage_whole_fact = self.get_percentage_of_nogoods_with_the_same_single_fact(fact1, var_1, var_2)# fact for the first nogood
                    temp_max_map_whole_fact = copy(self.maps[0])
                    temp_max_fact_whole_fact = copy(fact1)
                    for m1 in range(0, n_nogoods):  # to find the fact with the maximum percentage
                        fact1 = self.calculate_single_fact_each_nogood(self.maps[m1], var_1, var_2)  # fact for the first nogood
                        percentage = self.get_percentage_of_nogoods_with_the_same_single_fact(fact1, var_1, var_2)
                        if percentage > temp_max_percentage_whole_fact:
                            temp_max_percentage_whole_fact = self.get_percentage_of_nogoods_with_the_same_single_fact(fact1, var_1, var_2)
                            temp_max_map_whole_fact = copy(self.maps[m1])
                            temp_max_fact_whole_fact = copy(fact1)
                    self.max_percentage_single_fact.append(temp_max_percentage_whole_fact)
                    self.max_map_whole_fact.append(temp_max_map_whole_fact)
                    self.max_fact_whole_fact.append(temp_max_fact_whole_fact)
                    # compute the facts for all the variables indexed by the objects of the same type
                    for p in range(0, len(parameters_indexed_by_objects[l])):  # parameters indexed by lth type
                        try:
                            param1 = parameters_indexed_by_objects[l][p]

                            fact1 = self.calculate_single_fact_each_nogood_parameter(self.maps[0], var_1, var_2, param1)  # fact for the first nogood

                            if fact1 != "null":
                                temp_max_percentage_whole_fact_parameter = self.get_percentage_of_nogoods_with_the_same_single_fact_parameter(fact1, var_1, var_2, param1)  # fact for the first nogood
                                temp_max_map_whole_fact_parameter = copy(self.maps[0])
                                temp_max_fact_whole_fact_parameter = copy(fact1)
                        except Error:
                            continue
                        for m1 in range(0, n_nogoods):
                            fact1 = self.calculate_single_fact_each_nogood_parameter(self.maps[m1], var_1, var_2, param1)  # fact for the first nogood
                            if fact1 != "null":
                                percentage = self.get_percentage_of_nogoods_with_the_same_single_fact_parameter(fact1, var_1, var_2, param1)
                                if percentage > temp_max_percentage_whole_fact_parameter:
                                    temp_max_percentage_whole_fact_parameter = self.get_percentage_of_nogoods_with_the_same_single_fact_parameter(
                                        fact1, var_1, var_2, param1)
                                    temp_max_map_whole_fact_parameter = copy(self.maps[m1])
                                    temp_max_fact_whole_fact_parameter = copy(fact1)
                        self.max_percentage_single_fact_parameter.append(temp_max_percentage_whole_fact_parameter)
                        self.max_map_whole_fact_parameter.append(temp_max_map_whole_fact_parameter)
                        self.max_fact_whole_fact_parameter.append(temp_max_fact_whole_fact_parameter)

    def get_max_percentage_single_fact(self):
        return self.max_percentage_single_fact

    def get_max_map_whole_fact(self):
        return self.max_map_whole_fact

    def get_max_fact_whole_fact(self):
        return self.max_fact_whole_fact

    def get_max_percentage_whole_fact_parameter(self):
        return self.max_percentage_whole_fact_parameter

    def get_max_map_whole_fact_parameter(self):
        return self.max_map_whole_fact_parameter

    def get_max_fact_whole_fact_parameter(self):
        return self.max_fact_whole_fact_parameter

    def get_max_percentage_single_fact_parameter(self):
        return self.max_percentage_single_fact_parameter

    def get_max_map_whole_fact_parameter(self):
        return self.max_map_whole_fact_parameter

    def get_max_fact_whole_fact_parameter(self):
        return self.max_fact_whole_fact_parameter

    def get_fact_str(self):
        fact_str = ""
        fact_str_param = ""
        num_fact = len(self.max_percentage_single_fact)
        num_fact_param = len(self.max_percentage_single_fact_parameter)
        top_5_indices = sorted(range(len(self.max_percentage_single_fact)),
                                     key=lambda x: self.max_percentage_single_fact[x])[-5:]
        #for f in range(0, num_fact):
        for f in top_5_indices:
            if self.max_fact_whole_fact[f] == None or self.max_fact_whole_fact[f] == "null":
                continue
            fact_str += str(self.max_percentage_single_fact[f]) + ": " + str(self.max_map_whole_fact[f]) + ": " + \
                        str(self.max_fact_whole_fact[f]) + " | "

        top_5_indices_param = sorted(range(len(self.max_percentage_single_fact_parameter)), key=lambda x: self.max_percentage_single_fact_parameter[x])[-5:]
        #for f2 in range(0, num_fact_param):

        #print len(self.max_percentage_single_fact_parameter)

        for f2 in top_5_indices_param:
            if self.max_fact_whole_fact_parameter[f2] == None or self.max_map_whole_fact_parameter[f2] == "null":
                continue
            #print(self.max_percentage_single_fact_parameter[f2])
            fact_str_param += str(self.max_percentage_single_fact_parameter[f2]) + ": " + str(self.max_map_whole_fact_parameter[f2]) + ": " + \
                        str(self.max_fact_whole_fact_parameter[f2]) + " | "
        return fact_str + fact_str_param


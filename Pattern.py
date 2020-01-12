"""
This module contains a Pattern class.
@since            29th May 2018
@input            none
@output           none
@errorHandling    none
@knownBugs        none
"""

from Literal import *
from collections import OrderedDict
import copy
from functions import *
from Type1 import *


# TODO: Add some functions to make testing easier: like add a map by just giving the map argument


class Pattern:
    def __init__(self, n_IDs, p_seq_lits, p_nums, p_reds, p_paths):
        """
        :param n_IDs: list of string
        :param p_seq_lits: list of Literals
        :param p_nums: list of lists of char
        e.g.
        pattern: how[A]!=3 how[B]!=3
        p_nums: [['1', '9'], ['2', '4']]: each list corresponds to a nogood under the pattern
        :param p_reds: list of integers: e.g [345, 123]
        :param p_paths: list of strings: e.g. ['|12|3|12|10|', '|23|18|23|45| |26|7|26|34|']
        @complexity: O(N) (best and worst case)
        """
        self._param_type = []
        self.const_types = []
        self.tuple_var_type = []
        self.p_seq_lits = p_seq_lits  # list of Literals
        self.p_negate_lits = [] # list of negation of literals
        self.p_nums = p_nums  # constants to be mapped to the variables
        self.paths = []  # list of string
        self.p_reds = []  # list of reduction in search space
        self.p_reds += p_reds  # combines the 2 lists
        self.n_IDS = n_IDs
        self.sum_reduction = 0
        self.variable_names = []  # name of the decision variables appearing in the pattern
        self.params = []  # parameters appearing in the pattern (e.g. how[A]=3 => self.params = ['A', '3'])
        self.indices_of_params = []  # position of each parameter in self.params
        self.constants = []  # constants appearing in the pattern (e.g. how[1]=2 => self.constants = ['1', '2'])
        self.indices_of_consts = []  # position of each constant
        self.variables = []  # The variables of pattern => self.variables = ['A', 'B']
        self.indices_of_variables = []  # position of each variable
        self.p_maps = []  # list of dictionaries, each dictionary maps variables to constants
        self.name = ""  # name of the pattern which is calculated based on the variables
        self.operator_str = ""  # stores all the operators appearing in the pattern
        self.__calculate_param_var_const__()  # calculates self.params, self.indices_of_params, self.constants,
        # self.indices_of_consts, self.variables and self.indices_of_variables
        self.__calculate_name__()  # updates self.name
        self.__calculate_operators__()  # updates self.operator_str
        self.__calculate_variable_names__()  # updates self.variable_names
        self.constants = self.get_constants()  # updates self.constants
        self.indices_of_consts = self.get_indices_of_consts()  # returns index of each consts
        self.params = self.get_params()  # returns the parameters of the pattern
        self.indices_of_params = self.get_indices_of_params()  # returns the indices of params
        self.variables = self.get_variables()  # returns the variables e.g. how[A]=B how[C]=B => ['A', 'B', 'C', 'B']
        self.variables_no_duplicates = list(OrderedDict.fromkeys(self.variables))  # e.g.
        # how[A]=B how[C]=B => ['A', 'B', 'C'] this is needed for maps
        self.indices_of_variables = self.get_indices_of_vars()  # position of each variable
        for p_num in self.p_nums:  # map self.p_nums to the variables
            self.p_maps.append(dict(zip(self.variables_no_duplicates, p_num)))
        for red in self.p_reds:
            self.sum_reduction += red
        self.paths += p_paths  # list of constraints
        self.var_types = []
        self.var_types_no_reps = []
        self.var_types_each_pattern_variables = []
        self.all_objects_of_the_same_type = []  # list of list [[objects_t1], [objects_t2]]
        self.parameters_indexed_by_objects = []
        self.__calculate_var_types__()
        self.__calculate_things_to_compare__()
        self.pattern_negate_str = "" # String: negation of the pattern
        self.pattern_negate_str = self.negate_pattern()
        self.map_param_type = {}
        self.map_pvar_type = {}

    def __repr__(self):
        return self.name

    def find_types_enum(self):
        """
        :return: All the enum types that appear in the pattern
        e.g. how[1]=2 =>
        """
        types_enum = []
        for name in self.variable_names:
            types_enum = set(types_enum) | set(get_type(name, "enum_type"))
        return list(types_enum)

    def get_map_var_type(self):
        var_types = self.get_var_types()
        self.map_param_type = {self.params[p]: var_types[p] for p in range(0, len(self.params))}
        map_keys = self.map_param_type.keys()
        self.map_pvar_type = copy.deepcopy(self.get_map_param_type())
        for dicti in self.map_pvar_type.keys():
            if not is_variable(dicti):
                del self.map_pvar_type[dicti]
        return self.map_pvar_type

    def get_map_param_type(self):
        var_types = self.get_var_types()        
        self.map_param_type = {self.params[p]: var_types[p] for p in range(0, len(self.params))}
        return self.map_param_type

    def find_types_dim(self):
        """
        :return: All the enum types that appear in the pattern
        e.g. how[1]=2 =>
        """
        types_dim = []
        for name in self.variable_names:
            types_dim = types_dim + get_type(name, "dims")
        return list(set(types_dim))

    # "e.g get_type("how","enum_type"), get_type("how","dims")"

    def add_map(self, n_IDs, nums, red, paths):
        """
        :param n_IDs: list of string
        :param nums: list of lists of char
        :param red: list of integers
        :param paths: list string
        :return: null
        @complexity: O(N)
        """
        self.n_IDS += n_IDs  # combine n_IDs from the newly added nogoods with the existing ones self.n_IDS
        for num in nums:  # updates self.p_nums and self.p_maps
            self.p_nums.append(num)
            self.p_maps.append(dict(zip(self.variables_no_duplicates, num)))  # updates self.p_maps
        self.p_reds += red  # updates self.p_reds
        self.paths += paths  # updates self.paths
        for r in red:
            self.sum_reduction += r  # updates total sum reduction for pattern

    def __calculate_name__(self):
        """
        updates self.name
        :return: null
        @complexity: worst and best case: O(N)
        """
        self.name = ""
        for lit in self.p_seq_lits:  # iterates through the literals and gets the name for
            #  each of them to be appended to self.name
            self.name += lit.get_literal_str() + " "
        self.name = self.name[:len(self.name)-1]

    def __calculate_param_var_const__(self):
        """
        This function updates self.params, self.indices_of_params, self.constants, self.indices_of_consts,
         self.variables and self.indices_of_variables
        It iterates through the literals and extract the parameters, afterwards, it checks if the parameter is digit
        in that case it would be added to the self.constants. Otherwise, it would be added to self.variables.
        :return: Null
        @complexity: O(N)
        """
        self.params = []  # parameters appearing in the pattern (e.g. how[A]=3 => self.params = ['A', '3'])
        self.indices_of_params = []
        self.constants = []  # constants appearing in the pattern (e.g. how[1]=2 => self.constants = ['1', '2'])
        self.indices_of_consts = []  # position of each constants in each literal
        self.variables = []
        self.indices_of_variables = []
        for lit in self.p_seq_lits:
            self.params += lit.get_params()  # returns the parameters in each literal
            self.indices_of_params += lit.get_params_indices()
        for p in range(0, len(self.params)):  # for each parameter it checks whether it's a constant or a variable
            if not is_variable(self.params[p]):
                self.constants.append(self.params[p])
                self.indices_of_consts.append(self.indices_of_params[p])
            else:
                self.variables.append(self.params[p])
                self.indices_of_variables.append(self.indices_of_params[p])

    def __calculate_things_to_compare__(self):
        types_in_p = self.get_var_types_no_rep()
        self.all_objects_of_the_same_type = []  # list of list [[objects_t1], [objects_t2]]
        self.parameters_indexed_by_objects = []
        for t1 in range(0, len(types_in_p)):
            object_of_the_same_type = [] # vars and enums
            T1 = Type1(types_in_p[t1])
            p_vars_with_Type_t = self.get_vars_for_a_type(types_in_p[t1])[0]  # it returns a list of two lists [[variables], [their indexes]]
            object_of_the_same_type += p_vars_with_Type_t
            parameters_with_the_same_enum_as_T1 = T1.get_m_params_enum_is_t()  # parameters with the same enum as T1
            self.parameters_indexed_by_objects.append(T1.get_m_params_dim_is_t())
            dim_types_of_parameters_with_the_same_enum_as_T1 = T1.get_related_type()  # each element corresponds to
            for i in range(0, len(parameters_with_the_same_enum_as_T1)):
                if dim_types_of_parameters_with_the_same_enum_as_T1[i] in types_in_p:
                    related_vars = self.get_vars_for_a_type(dim_types_of_parameters_with_the_same_enum_as_T1[i])[0]
                    object_of_the_same_type.append((parameters_with_the_same_enum_as_T1, related_vars))
            self.all_objects_of_the_same_type.append(object_of_the_same_type)
        objects_of_a_same_type = []  # p_vars_with_Type_t + enums with type t


    def __calculate_operators__(self):
        """
        updates self.operator_str
        For each literal in lit.get_operators() it gets the operator and adds it to the self.operator_str
        e.g self.name = "how[1]=2 how[7]>=123" => self.operator_str = "=>="
        :return: null
        @complexity:
        """
        self.operator_str = ""
        for lit in self.p_seq_lits:
            ops = lit.get_operators()
            self.operator_str += ''.join(x for x in ops)

    def __calculate_variable_names__(self):
        """
        :return: self.variable_names: a list consisting of the name of decision variables appearing in the pattern
        e.g.
        self.name = "how[1]=3 used=[2] how[5]=3"
        self.variable_names = ['how', 'used', 'how']
        @complexity: O(N^2)
        """
        self.variable_names = []
        for lit in self.p_seq_lits:
            self.variable_names += lit.get_variable_names()

    def __calculate_var_types__(self):
        self.var_types = []
        for lit in self.p_seq_lits:
            self.var_types += lit.get_var_types()

    def get_var_types_for_each_pattern_variable(self):
        """
        To remove the types of the constants
        :return:
        """
        return self.var_types_each_pattern_variables

    def get_var_types(self):
        """
        :return: list of variable types in the pattern e.g. ["'u'PIZZA", "'u'VOUCHER"]
        """
        return self.var_types

    def get_var_types_no_rep(self):
        self.var_types_no_reps = list(set(tuple(self.var_types)))
        return self.var_types_no_reps

    def negate_pattern(self):
        """
        :return: String: which is a negation of the pattern
        Example: pattern: how[1]!=2 how[2]!=4, this function returns: how[1]=2 /\ how[2]=4
        """
        self.pattern_negate_str = ""
        dicts_op_neg = {">=": "<", "<=": ">", "!=": "=", ">": "<=", "<": ">=", "==": "!=", "=": "!=", "+": "-"}
        lits = self.p_seq_lits
        length_lit = len(lits)
        for l in range(0, length_lit):  # Replace the negated operator for each literal
            lit_org = lits[l].get_literal_str().replace("@", "")  # To get literals without @
            ops = lits[l].get_operators()
            for op in ops:
                lit_org = lit_org.replace(op, dicts_op_neg[op])
            if l == length_lit - 1:
                self.pattern_negate_str += lit_org
            else:
                self.pattern_negate_str += lit_org + " /\ "
        return self.pattern_negate_str

    def negate_pattern_all_enum(self):
        """
        :return: String: which is a negation of the pattern
        Example: pattern: how[1]!=2 how[2]!=4, this function returns: how[1]=2 /\ how[2]=4
        """
        self.pattern_negate_str = ""
        dicts_op_neg = {">=": "<", "<=": ">", "!=": "=", ">": "<=", "<": ">=", "==": "!=", "=": "!=", "+": "-"}
        lits = self.p_seq_lits
        length_lit = len(lits)
        self.const_types = []
        for p in range(0, len(self.params)):
            if isDigit(self.params[p]):
                self.const_types.append(self.var_types[p])
        num_consts_in_each_previous_literal = 0
        for l in range(0, length_lit):  # Replace the negated operator for each literal
            lit_org = lits[l].get_literal_str()
            ops = lits[l].get_operators()
            consts = lits[l].get_consts()
            consts_indices = lits[l].get_consts_indices()
            # To replace the how[1]=@A how[2]=@B to how[PIZZA[1]]!=A /\ how[PIZZA[2]]!=B
            enums = get_enums_in_model()
            c = len(consts)-1
            while c >= 0:  # iterate over consts and consts_indices in reverse order, so that
                type_of_const = self.const_types[c + num_consts_in_each_previous_literal]

                if type_of_const in enums:
                    lit_org = lit_org[:consts_indices[c]] + type_of_const + "[" + consts[c] + "]" + \
                              lit_org[consts_indices[c] + len(consts[c]):]
                c -= 1
            lit_org = lit_org.replace("@", "")  # To get literals without @
            num_consts_in_each_previous_literal = len(consts) + num_consts_in_each_previous_literal
            for op in ops:
                lit_org = lit_org.replace(op, dicts_op_neg[op])
            if l == length_lit - 1:
                self.pattern_negate_str += lit_org
            else:
                self.pattern_negate_str += lit_org + " /\ "
        return self.pattern_negate_str


            # def replace_consts_with_enum_neg(self):
    #     pattern_negate_str_enum = self.pattern_negate_str
    #     pizza_params = self.get_params_for_a_type("PIZZA")[0]
    #     voucher_params = self.get_params_for_a_type("VOUCHER")[0]
    #     print voucher_params
    #     for p in pizza_params:
    #         if isDigit(p):
    #             pattern_negate_str_enum = self.pattern_negate_str.replace(p, "PIZZA[" + p + "]")
    #     for v in voucher_params:
    #         if isDigit(v):
    #             pattern_negate_str_enum = self.pattern_negate_str.replace(v, "VOUCHER[" + v + "]")
    #     return pattern_negate_str_enum

        # self.p_negate_lits
        # self.get_seq_lits()
        # self.get_operators()

    def get_params(self):
        """
        :return: self.params: list of char
        e.g.
        self.name = "how[A]=3 used=[2] how[5]=3"
        self.params = ['A', '3', '2', '5', '3']
        @complexity: O(N)
        """
        return self.params

    def get_indices_of_params(self):
        """
        :return: list of int (stores the position of each param from the beginning of each literal)
        e.g.
        self.name = "how[A]!=3 how[B]!=3"
        self.params = [4, 8, 4, 8]
        """
        return self.indices_of_params

    def get_variables(self):
        """
        :return: self.variables: list of char
        e.g.
        self.name = "how[A]!=3 how[B]!=3"
        self.variables = ['A', 'B']
        """
        return self.variables

    def get_variables_no_duplicates(self):
        """
        :return: list of char
        """
        return self.variables_no_duplicates

    def get_indices_of_vars(self):
        """
        :return: list of int (position of each variable)
        e.g.
        self.name = "how[A]!=3 how[B]!=3"
        self.indices_of_variables = [4, 4]
        """
        return self.indices_of_variables

    def get_constants(self):
        """
        :return: list of char (digits in the pattern name)
         e.g.
        self.name = "how[A]!=3 how[B]!=3"
        self.indices_of_variables = ['3', '3']
        """
        return self.constants

    def get_indices_of_consts(self):
        """
        :return: A list of integer
        Description: position of each constant which is calculated from the beginning of each literal
        e.g.
        self.name: how[A]!=3 how[B]!=3
        self.indices_of_consts: [8, 8]
        """
        return self.indices_of_consts

    def get_operators(self):
        """
        :return: string
        All the operators such as (!=<>) appearing in the pattern
        e.g.
        self.name: how[A]!=3 how[B]>3 how[B]<=3
        self.operator_str: "!=><="
        """
        return self.operator_str

    def get_sum_reduction(self):
        """
        :return: int (sum of elements of self.p_reds)
        """
        return self.sum_reduction

    def get_variable_names(self):
        """
        :return: list of string
        e.g.
        self.name: how[A]!=3 used[B]=true
        self.operator_str: ["how", "used"]
        """
        return self.variable_names

    def get_name(self):
        """
        :return: string (name of the pattern)
        """
        return self.name

    def get_name_original(self):
        """
        :return: string (name of the pattern)
        """
        new_name = self.name
        new_name = new_name.replace("@","")
        return new_name

    def get_seq_lits(self):
        """
        :return: list of Literal
        """
        return self.p_seq_lits

    def get_reds(self):
        """
        :return: list of int (each element corresponds to a nogood under the pattern)
        """
        return self.p_reds

    def get_IDS(self):
        """
        :return: list of string
        """
        return self.n_IDS

    def get_maps(self):
        """
        :return: list of dict
        """
        return self.p_maps

    def get_pnums(self):
        """
        :return: list of list of char
        e.g.
        self.p_nums = [['1', '9'], ['2', '4']]
        """
        return self.p_nums

    def get_paths(self):
        """
        :return: list of string (each string corresponds to paths for each nogood)
        """
        return self.paths

    def get_params_for_a_type(self, var_type):
        """
        :param var_type: String: "PIZZA", "VOUCHER"
        :return: [,] a list of variables and constants with the type var_type and a list with the literal numbers
        """
        params_of_a_type = []
        lit_nums = []
        var_types = self.get_var_types()
        for p in range(0, len(self.params)):
            if var_types[p] == var_type and self.params[p] not in params_of_a_type:
                params_of_a_type.append(self.params[p])
                lit_nums.append(p)
        return [params_of_a_type, lit_nums]

    def get_vars_for_a_type(self, var_type):
        """
        :param var_type: String: "PIZZA", "VOUCHER"
        :return: [,] a list of variables and constants with the type var_type and a list with the literal numbers
        """
        vars_of_a_type = []
        lit_nums = []
        var_types = self.get_var_types()
        # a temperory fix for x[neigh[2,2],neigh[1,4]]=6 => it extracts the types as [u'int', u'int', u'int']
        while len(var_types) < len(self.params):
            var_types.append(u'int')

        for p in range(0, len(self.params)):
            if var_types[p] == var_type and self.params[p] not in vars_of_a_type and is_variable(self.params[p]):
                vars_of_a_type.append(self.params[p])
                lit_nums.append(p)
        return [vars_of_a_type, lit_nums]

    ############################################
    def calculate_permutables(self, var_type_dim, var_type_enum):
        """
        calculates all the possible value and index permutations and updates permutation lists
        :param var_type: type of variable to compute the permutation for (e.g. Pizza, Voucher)
        :return: Null
        """
        self.permutable_lits = []
        self.params_dim_lit_num = self.get_params_for_a_type(var_type_dim) # All the parameters with the type var_type_dim
        self.params_dim = self.params_dim_lit_num[0]
        self.lit_nums = self.params_dim_lit_num[1]
        self.params_enum = self.get_params_for_a_type(var_type_enum)[0]  # All the parameters with the type var_type_enum
        len_dim = len(self.params_dim)
        len_enum = len(self.params_enum)
        if len_dim == len_enum:
            for d1 in range(0, len_dim):
                dim1 = self.params_dim[d1]
                enum1 = self.params_enum[d1]
                for d2 in range(d1+1, len_dim):
                    dim2 = self.params_dim[d2]
                    enum2 = self.params_enum[d2]
                    # if lit1.getOperator() != lit2.getOperator():
                    # continue
                    if (not(isDigit(dim1)) and not(isDigit(enum1)) and
                        not(isDigit(dim2)) and not(isDigit(enum2))) or \
                            enum1 == enum2 or dim1 == dim2:
                        if (d1, d2) not in self.permutable_lits:
                            self.permutable_lits.append((d1, d2))
                    #else:


        else:
            print "Error: len_dim != len_enum for pattern " + self.name
        print self.permutable_lits



        # for l in range(0, len(self.p_seq_lits)):
        #     lit1 = self.p_seq_lits[l]
        #     for h in range(l + 1, len(self.p_seq_lits)):
        #         lit2 = self.p_seq_lits[l]
        #         value1 = lit1.getValue()
        #         value2 = lit2.getValue()
        #         index1 = lit1.getIndex()
        #         index2 = lit2.getIndex()
        #         if value1 == 'false' or value2 == 'false' or lit1.getOperator() != lit2.getOperator():
        #             continue
        #         if isDigit(index1) and isDigit(index2) or isDigit(value1) and isDigit(value2):
        #             continue
        #         if not (isDigit(index1)) and not (isDigit(index2)) and index1 != index2 and not (
        #         isDigit(value1)) and not (isDigit(value2)) and value1 != value2:  # both values are variable
        #             # n = value_vars.index(value1)
        #             # m = value_vars.index(value2)
        #             if (l, h) not in self.permutable_lits:
        #                 self.permutable_lits.append((l, h))  # literal i and j are interchangeable
        #
        #         else:
        #             for i in range(0, len(self.maps)):  # find the no-goods which have value or index permutation
        #             #     if not (isDigit(value1)) and not (isDigit(value2)):
        #             #         if not (isDigit(index1)) and isDigit(index2) and self.maps[i][
        #             #             index1] == index2:  # if a no-good hase same index for literal 1 and 2
        #             #             n = value_vars.index(value1)
        #             #             m = value_vars.index(value2)
        #             #             if i not in self.ng_permutable_val:
        #             #                 self.ng_permutable_val.append(i)
        #             #             if (n, m) not in self.perm_ng_val:
        #             #                 self.perm_ng_val.append((n, m))
        #             #         elif not (isDigit(index2)) and isDigit(index1) and self.maps[i][index2] == index1:
        #             #             n = value_vars.index(value1)
        #             #             m = value_vars.index(value2)
        #             #             if i not in self.ng_permutable_val:
        #             #                 self.ng_permutable_val.append(i)
        #             #             if (n, m) not in self.perm_ng_val:
        #             #                 self.perm_ng_val.append((n, m))
        #                 if not (isDigit(index1)) and not (isDigit(index2)):
        #                     if not (isDigit(value1)) and isDigit(value2) and self.maps[i][
        #                         value1] == value2:  # if value1 is a variable but value2 is a constant
        #                         n = index_vars.index(index1)
        #                         m = index_vars.index(index2)
        #                         if i not in self.ng_permutable_index:
        #                             self.ng_permutable_index.append(i)
        #                         if (n, m) not in self.perm_ng_index:
        #                             self.perm_ng_index.append((n, m))
        #                     if not (isDigit(value2)) and isDigit(value1) and self.maps[i][
        #                         value2] == value1:  # if value1 is a variable but value2 is a constant
        #                         n = index_vars.index(index1)
        #                         m = index_vars.index(index2)
        #                         if i not in self.ng_permutable_index:
        #                             self.ng_permutable_index.append(i)
        #                         if (n, m) not in self.perm_ng_index:
        #                             self.perm_ng_index.append((n, m))
        #

    def get_lit_permutation(self):
        return self.permutable_lits

    def get_perm_ng_val(self):
        return self.perm_ng_val

    def get_ng_permutable_val(self):
        return self.ng_permutable_val

    def get_perm_ng_index(self):
        return self.perm_ng_index

    def get_ng_permutable_index(self):
        return self.ng_permutable_index

    def permute(self, set1, num, t1):
        temp = set1[num]
        ind1 = t1[0]
        ind2 = t1[1]
        intermediate = temp[ind1]
        temp[ind1] = temp[ind2]
        temp[ind2] = intermediate
        set1[num] = temp
        return set1

    def recurse(self, set1, num, perm):
        if num > 0:
            temp1 = []
            p1 = self.recurse(set1, num - 1, perm)
            temp1 = temp1 + copy.deepcopy(p1)
            self.permute(set1, num, perm)
            p2 = self.recurse(set1, num - 1, perm)
            temp1 = temp1 + copy.deepcopy(p2)
            return temp1
        else:
            temp1 = []
            p1 = self.permute(set1, num, perm)
            temp1.append(copy.deepcopy(p1))
            p2 = self.permute(set1, num, perm)
            temp1.append(copy.deepcopy(p2))
            return temp1

    def calculate_dim_map_permutation(self):
        """
        :return: A list of list of value maps which includes all the permutations
        e.g = [[ng1_map_perm1, ng2_map_perm1], [ng1_map_perm1, ng2_map_perm2], [ng1_map_perm2, ng2_map_perm1], [ng1_map_perm2, ng2_map_perm2]
        e.g = if a pattern has 9 elements => it returns a list of 512 combination of no-goods
        """
        self.calculate_permutables()
        num = self.get_num()
        set_index = self.get_index()
        perm_ng_index = self.get_perm_ng_index()
        index_variables = self.get_index_vars()
        maps = []
        map_list = []
        ng_permutable = self.get_ng_permutable_index()
        ng_not_permutable = []
        for i in range(0, len(set_index)):  # set_value corresponds to no-good but contains only the indices
            if i not in ng_permutable:
                ng_not_permutable.append(i)  # index of the no-goods that are not permutable
        new_set_index_ng = []
        self.temp11 = []
        if len(perm_ng_index) == 0:  # No permutation just adding the original map
            for s in set_index:
                maps.append(copy.deepcopy(dict(zip(index_variables, s))))
            map_list.append(copy.deepcopy(maps))
        else:
            for k in range(0, len(ng_permutable)):  # All the permutable no-goods are added to the new_set_value_ng
                new_set_index_ng.append(set_index[ng_permutable[k]])

            for j in range(0, len(perm_ng_index)):
                permutations = self.recurse(new_set_index_ng, len(new_set_index_ng) - 1,
                                            perm_ng_index[
                                                j])  # All permutations of permutable no-goods are calculated
                for i in range(0, len(
                        permutations)):  # To create map for all the permutations and add all the non-permutable no-goods to the set also
                    maps = []
                    for n in range(0, len(permutations[i])):
                        maps.append(copy.deepcopy(dict(zip(index_variables, permutations[i][n]))))
                    for m in ng_not_permutable:
                        maps.append(copy.deepcopy(dict(zip(index_variables, set_index[m]))))
                    map_list.append(copy.deepcopy(maps))
        return map_list

    # These functions are for fact calculation
    def get_all_objects_of_the_same_type(self):

        return self.all_objects_of_the_same_type

    def get_parameters_indexed_by_objects(self):

        return self.parameters_indexed_by_objects













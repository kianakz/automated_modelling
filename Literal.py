"""
This module contains a class of Literal
@since            8th may 2018
@input            none
@output           none
@errorHandling    none
@knownBugs        none
"""
from functions import *
import re
import Globals

# param_in_bracket_re = re.compile(r"((?<=@)[a-zA-Z]|\d+)[\],\)]")

param_in_bracket_re = re.compile(r"((?<=@)[a-zA-Z]|\d+)[\],\)]")

# (?<=@) A look-behind (coded as (?<=someregex)) is a zero-width match, so it asserts, but does not capture the match.
# it captures any alphabet after the @, or any digit which is before (]),)
# e.g. how[@b] = how[1] => it matches b and 1.


# e.g. 'XI:72|13-72|48:(j=138):builtins.mzn:312|9-312|35'<=350 => param_in_bracket = [138]
# e.g. how[1,2] => param_in_bracket = [1,2]

if Globals.flag_all_conts_positive:
    btw_op_re = re.compile(r"[^+=><!-]+")
else:
    btw_op_re = re.compile(r"[^+=><!]+")
# matches everything before, after or between operators
# e.g. order[succ[211]+5]=7, matches ['order[succ[211]', '5]', '7']


class Literal:
    def __init__(self, literal_str):
        """
        :param literal_str: String
        @complexity: O(N)
        """
        self.literal_str = literal_str  # string
        self.in_bracket = []  # indices e.g. literal_str = "how[2]=4+order[A]" self.in_bracket = ['2', 'A']
        self.in_bracket_indices = []  # starting positions of the elements of self.in_bracket
        self.other_params = []  # other parameters that are not in the bracket
        self.other_params_indices = []  # position of each other_params
        self.consts = []
        self.consts_indices = []
        self.params = []  # all the parameters in the literal
        self.params_indices = []  # lists of chars: all the digits or variable appearing in the literal_str
        self.variable_names = []  # list of strings: e.g. literal_str = "how[2]=4+order[A]" =>
        # self.variable_names = ['how', 'order']
        self.var_types = []
        self.params_int = []  # if the param is a digit it's converted to int
        self.__calculate_variable_names__()  # updates self.variable_names
        self.variable_names = self.get_variable_names()
        self.operators = self.get_operators()  # contains the operators in a literal e.g.
        self.matches_btw_op = []

    def __repr__(self):
        return self.literal_str

    def update(self):
        """
        It should be called after creating a Literal object to calculate and update params.
        This is done to improve the speed of copying the literals of the old pattern to the new pattern, in pattern_functions.py
        in line 18. Because self.params will be changed in the new_pattern. It shouldn't be copied then modified.
        @Complexity: O(N)
        """
        self.__calculate_params__()
        self.params = self.get_params()
        for x in self.params:
            if isDigit(x):
                self.params_int.append(int(x))
        self.params_indices = self.get_params_indices()
        self.__calculate_types__()

    def __calculate_params__(self):
        """
        updates self.params, self.params_indices, self.in_bracket and self.in_bracket_indices
        @complexity: O(N)
        """
        iterator = param_in_bracket_re.finditer(self.literal_str)  # find anything within brackets (the smallest)
        # e.g. succ[succ[A]]=> finds A
        self.in_bracket = []  # indices e.g. literal_str = "how[2]=4 + order[A]" self.in_bracket = ['2', 'A']
        self.in_bracket_indices = []  # starting positions of the elements of self.in_bracket
        self.other_params = []  # other parameters that are not in the bracket
        self.other_params_indices = []
        self.params = []  # all the parameters in the literal
        self.params_indices = []  # lists of chars: all the digits or variable appearing in the literal_str
        self.consts = []
        self.consts_indices = []
        for match in iterator:
            self.in_bracket_indices.append(match.start())
            str_in_bracket = match.group(1)
            self.in_bracket.append(str_in_bracket)
            if isDigit(str_in_bracket):
                self.consts_indices.append(match.start())
                self.consts.append(str_in_bracket)
        str_btw_ops = btw_op_re.finditer(self.literal_str)  # all the strings before or after an operator
        self.matches_btw_op = []
        for match in str_btw_ops:
            str_match = match.group()
            self.matches_btw_op.append(str_match)
            if self.literal_str[match.start()] == '@' and len(str_match[0:]) == 2:  # if the str is a character or a digit
                if isDigit(str_match):
                    self.consts_indices.append(match.start())
                    self.consts.append(str_match)
                self.other_params_indices.append(match.start()+1)
                self.other_params.append(str_match[1:])
            if str_match == 'false' or str_match == 'true':  # if the str is a character or a digit
                self.other_params_indices.append(match.start())
                self.other_params.append(str_match)
            elif isDigit(str_match):
                if isDigit(str_match):
                    self.consts_indices.append(match.start())
                    self.consts.append(str_match)
                self.other_params_indices.append(match.start())
                self.other_params.append(str_match)

        self.params_indices += self.in_bracket_indices  # position of each param that's in bracket
        self.params_indices += self.other_params_indices  # position of each params that's not in bracket
        self.params += self.in_bracket
        self.params += self.other_params

    def __calculate_types__(self):
        self.var_types = []
        for str_btw_op in self.matches_btw_op:
            var_name = re.findall(r"(?<!@)[a-zA-Z]{1,}", str_btw_op)  # it matches all the characters,
            if "false" in var_name:
                var_name.remove("false")
            if "true" in var_name:
                var_name.remove("true")
            # var_name = re.findall(r"(?<!@)[a-zA-Z]{1,}", str_btw_op)  # it matches all the characters,
            # but not the variables (which starts with @)
            if not var_name:
                self.var_types += types_enum
            else:
                main_name = var_name[0]
                types_enum = get_type(main_name, "enum_type")  # reads the type from the .type file
                if types_enum == 'Variable name not in Json':
                    print "error:"
                    print 'Variable name ' + main_name + " not in Json"

                types_dims = get_type(main_name, "dims")
                self.var_types += types_dims
        # to fix a bug
        while len(self.var_types) < len(self.params):
            self.var_types.append(u"int")
        return self.var_types

    def __calculate_variable_names__(self):
        """
        :return: list of string (variable names appearing in the literal)
        @complexity: O(N)? not sure about complexity of regex
        """
        # self.variable_names = re.findall(r"[a-zA-Z]{1,}", self.literal_str)  # finds the words with length > 1 ({2,})

        self.variable_names = re.findall(r"(?<!@)[a-zA-Z]{1,}", self.literal_str)  # finds the words with length > 1

        # ({1,} that doesn't start with @)
        # ?<! negative lookahead () for the current location

        # The following code is to find variable name for "XI:72|13-72|48:(j=26):builtins.mzn:312|9-312|35<=112".
        # If self.literal_str = "XI:72|13-72|48:(j=26):builtins.mzn:312|9-312|35<=112" =>
        # self.variable_names = "XI:72|13-72|48::builtins.mzn:312|9-312|35"
        if "false" in self.variable_names:
            self.variable_names.remove("false")
        if "true" in self.variable_names:
            self.variable_names.remove("true")
        if len(self.literal_str) > 2:
            if self.literal_str[0:2] == 'XI':
                start = self.literal_str.find('(')
                end = self.literal_str.find(')') + 1
                str_btw_paranthesis = self.literal_str[start:end]
                str_test_wo_loop_index = self.literal_str.replace(str_btw_paranthesis, '')
                btw_op_re = re.findall(r"[^+=><!]+", str_test_wo_loop_index)

                if btw_op_re[0] != "false" and btw_op_re[0] != "true":
                    self.variable_names = btw_op_re[0]

    def get_params(self):
        """
        :return: self.params: list of characters (digits or single characters appearing in the literal)
        the first elements are the ones in the brackets followed by the other parameters
        @complexity: O(1)
        """
        return self.params

    # def get_consts(self):
    #     self.consts = [p for p in self.params if not is_variable(p)]
    #     return self.consts

    def get_consts(self):
        return self.consts

    def get_consts_indices(self):
        return self.consts_indices

    def get_var_types(self):
        return self.var_types

    def get_params_indices(self):
        """
        :return: self.params_indices: list of integers (starting position of each element in self.params)
        @complexity: O(1)
        """
        return self.params_indices

    def get_operators(self):
        """
        Finds and return all the Literal's operator.
        e.g.  if the literal is "how[1]!=7", getOperator() returns "!="
        @return a list of operators of the literal
        """
        ops = [">=", "<=", "!=", ">", "<", "==", "=", "+"]
        words = self.literal_str.split()
        signs = []
        for li in words:
            for op in ops:
                while li.find(op) != -1:
                    ind = li.index(op)
                    l = len(op)
                    sign = li[ind:ind + l]
                    signs.append(sign)
                    li = li[:li.find(sign)] + li[li.find(sign)+l:]
        return signs

    def get_variable_names(self):
        """
        :return: a list of strings containing variable names
        @complexity: O(1)
        """
        return self.variable_names

    def get_literal_str(self):
        """
        :return: returns the full name of the literal
        @complexity: O(1)
        """
        return self.literal_str

    def set_variable(self, new_value, index, length):
        """
        :param new_value: a new character which replaces the old one
        :param index: starting position of the old character
        :param length: length of the old character
        """
        self.literal_str = self.literal_str[:index] + new_value + self.literal_str[index + length:]
        self.__calculate_params__()  # updates self.params and self.params_indices
        self.__calculate_variable_names__()  # updates self.variable_names


def convert_str_to_literals(str1):
    """
    :param str1: a string containing literals
    :return: a list of Literal objects
    converts str1 into
    """
    str_split = str1.split()
    literals = []
    for lit_str in str_split:
        lit = Literal(lit_str)
        lit.update()
        literals.append(lit)
    return literals



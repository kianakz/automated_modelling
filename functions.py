"""
This module consists of the functions which are used in this project.
"""

import json
import Globals
import re


def is_variable(parameter):  # if the parameter is a character it returns true, otherwise it returns false
    if len(parameter) == 1 and not isDigit(parameter):
        return True
    else:
        return False


def get_type(variable_name, type1):
    """
    :param variable_name: string
    :param type1: string (should be either "enum_type" or "dims")
    :return: list of string (type of variable)
    """
    json_file = json.loads(open(Globals.ifile_type).read())
    variable_dict = json_file['var_types']['vars']
    variable_names = variable_dict.keys()
    if variable_name in variable_names:
        variable_details = variable_dict[variable_name]  # e.g. {"type" : "bool", "dim" : 1, "dims" : ["VOUCHER"]}
        if type1 in variable_details.keys():
            if type(variable_details[type1]) == list:
                return variable_details[type1]
            else:
                return [variable_details[type1]]
        elif type1 == "enum_type":  # if there is no enum_type for the variable
            return [variable_details["type"]]

        elif type1 == "dims":  # if there is no dim type: for example:
            return [variable_details["type"]]

    else:
        return ["Variable name not in Json"]


def get_type_names(variable_name, type1):
    """
    :param variable_name: string e.g how
    :param type1: string (should be either "enum_type" or "dims")
    :return: list of string (type of variable)
    """
    types = json.loads(open(Globals.ifile_type).read())
    if variable_name in types['var_types']['vars'].keys():
        variable_details = types['var_types']['vars'][variable_name]
        if type1 in variable_details.keys():
            if type(variable_details[type1]) == list:
                return variable_details[type1]
            else:
                return [variable_details[type1]]
        else:
            return ["i"]
    else:
        return ["i"]

def get_enums_in_model():
    """
    :param variable_name: string e.g how
    :param type1: string (should be either "enum_type" or "dims")
    :return: list of string (type of variable)
    """
    types = json.loads(open(Globals.ifile_type).read())
    return types["var_types"]["enums"]

    # if variable_name in types['var_types']['vars'].keys():
    #     variable_details = types['var_types']['vars'][variable_name]
    #     if type1 in variable_details.keys():
    #         if type(variable_details[type1]) == list:
    #             return variable_details[type1]
    #         else:
    #             return [variable_details[type1]]
    #     else:
    #         return ["i"]
    # else:
    #     return ["i"]


def get_m_paramter_indexed_by_a_type(type1):
    # TODO: Return a parameter indexed by a type (e.g. type1 = PIZZA => return = Price)
    parameter = ""
    return parameter


def deepish_copy(org):
    out = dict().fromkeys(org)
    for k, v in org.iteritems():
        try:
            out[k] = v.copy()  # dicts, sets
        except AttributeError:
            try:
                out[k] = v[:]  # lists, tuples, strings, unicode
            except TypeError:
                out[k] = v  # ints
    return out


def test_deepish_copy():
    o1 = dict(name=u"blah", id=1, att0=(1, 2, 3), att1=range(10), att2=set(range(10)))
    o2 = deepish_copy(o1)
    assert o2 == o1, "not equal, but should be"
    del o2['att1'][-1]
    assert o2 != o1, "are equal, shouldn't be"


def isDigit(num):
    """
    Checks if a string is number or not
    :param num: string
    :return: boolean
    """
    if len(num) > 0:
        if num[0] == "-" and num[1:].isdigit():
            return True
        elif num.isdigit():
            return True
        else:
            return False


def generate_sign(s):
    """
    :param s: String
    :return: String (The operator in the literal)
    """
    ops = [">=", "<=", "!=", ">", "<", "==","="]
    l = 0
    sign = ""
    literals = s.split()
    for literal in literals:
        for op in ops:
            if literal.find(op) != -1:
                index = literal.find(op)
                l = len(op)
                sign += literal[index:index+l]
                break
    return sign


def find_occurrences(s1, s2):
    """
    Finds occurrences of a string inside another string
    :param s1: the string
    :param s2: the small string within string
    :return: The starting index of all the occurrences of s1 in s2
    """
    return [m.start() for m in re.finditer(s2, s1)]


def find_occurrences_char(s, ch):
    """
    Finds occurrences of a character inside another string
    :param s: the string
    :param ch: the character to be found in string
    :return: The starting index of all the occurrences of ch in s
    """

    return [i for i, letter in enumerate(s) if letter == ch]


def find_occurrences_list(list, element):
    """
    Finds occurrences of a character inside another string
    :param s: the string
    :param ch: the character to be found in string
    :return: The starting index of all the occurrences of ch in s
    """
    return [i for i, letter in enumerate(list) if letter == element]


def replace_nth(string, sub, wanted, n):
    where = [m.start() for m in re.finditer(sub, string)][n-1]
    before = string[:where]
    after = string[where:]
    after = after.replace(sub, wanted, 1)
    new_string = before + after
    return new_string


def get_keys_by_value(dict_Of_elements, value_to_Find):
    list_Of_keys = list()
    list_Of_items = dict_Of_elements.items()
    for item in list_Of_items:
        if item[1] == value_to_Find:
            list_Of_keys.append(item[0])
    return list_Of_keys






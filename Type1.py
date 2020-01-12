"""
This module contains one class Type1.
This class represents an enum type in the MiniZinc model. For example, for the free pizza problem it
can be: ['PIZZA', 'VOUCHER'].
Assumptions: type var_int in Json means that it is a variable
"""

from Globals import *
import json
from functions import *


class Type1:
    """
    This class represents an enum type in the MiniZinc model. For example, for the free pizza problem it
    can be: ['PIZZA', 'VOUCHER'].
    """
    def __init__(self, t):
        self.t = t
        self.m_params_dim_is_t = []
        self.m_params_enum_is_t = []
        self.m_params_enum_is_t_dim = []  # t2 which is related to t1 => e.g. Imagine we have a parameter
        # map_pizza_voucher, which maps pizzas to the vouchers. In this case self.m_params_enum_is_t = map_pizza_voucher
        #  (since its enum_type is t) and self.m_params_enum_is_t_dim = 'VOUCHER' since voucher is the index of
        # map_pizza_voucher, so 'VOUCHER' is a type related to "PIZZA"
        self.related_types = []  # types that are related to t (it is basically self.m_params_enum_is_t_dim without
        # repetition)
        self.__calculate__()

    def __calculate__(self):
        """
        Updates self.m_params_dim_is_t, self.m_params_enum_is_t and self.m_params_enum_is_t_dim
        """
        json_file = json.loads(open(ifile_type).read())
        variable_dict = json_file['var_types']['vars']  # A dictionary which maps variables and parameters to their
        # related info
        variable_dict_tuples = variable_dict.items()  # A list of tuples (each tuple is a dictionary item) =

        # [(key1, value1), (key2, value2)]
        m_vars_params = ""

        for item_tuple in variable_dict_tuples:
            m_vars_param = item_tuple[0]   # model variable or parameter
            info = item_tuple[1]  # all the info about dimension and type of the model variable or parameter
            m_vars_param
            each_info = info.items()  # converts the dict into a list of tuples (for iterating through the dictionary)
            [value_of_type_for_m_vars_params] = [x[1] for x in each_info if x[0] == u'type']  # type of m_vars_param
            is_m_var = False  # if m_vars_param is variables it will be set to true
            if 'var' in value_of_type_for_m_vars_params:  # checks if is_m_var is a variable (if it is a variable,
                # the type has a var substring like 'var_int')
                is_m_var = True

            if not is_m_var:  # We only need the types for model parameters
                if (u'dim', 1) and (u'dims', [self.t]) in each_info:  # it finds a model parameter that is
                    # indexed by the type t
                    self.m_params_dim_is_t.append(m_vars_param)
                if (u'enum_type', self.t) in each_info:  # finds a model parameter that has the enum_type t
                    self.m_params_enum_is_t.append(m_vars_param)
                    [dim] = [x[1] for x in each_info if x[0] == u'dims']
                    self.m_params_enum_is_t_dim.append(dim[0])

    def get_m_params_dim_is_t(self):
        """
        :return: list of model parameters indexed by t
        """
        return self.m_params_dim_is_t

    def get_m_params_enum_is_t(self):
        """
        :return: list of model parameters with the enum_type t
        """
        return self.m_params_enum_is_t

    def get_related_type(self):
        """
        :return: list of model dims of the parameters with the enum_type t
        e.g.:
        map_pizza_voucher is a parameter: dims = "PIZZA" and enum = "VOUCHER"
        t = "VOUCHER"
        this returns "PIZZA"
        """
        return self.m_params_enum_is_t_dim

    def get_type_name(self):
        return self.t

# t = Type1("VOUCHER")
# print t.get_related_type()
# print t.get_m_params_enum_is_t()
# print t.get_m_params_dim_is_t()


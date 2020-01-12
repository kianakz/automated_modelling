"""
This module reads the prices from the input.txt file
"""
import os
from Globals import *


param_names = []  # Stores values of a parameter from the input data file (int)
param_values = []
parameter_str = ""  # Stores values of a parameter from the input data file (str)
param_name_val_map = {}
with open(ifile_input_data_file_dir, "r") as f:
    for line in f:
        par_name, value_str = line.split('=')
        par_name = par_name.replace(" ", "")
        value_str = value_str.replace(";", "")
        value_str = value_str.replace(" ", "")
        value_str = value_str.replace("\n", "")
        value_str = value_str.replace("[", "")
        value_str = value_str.replace("]", "")
        value_str = value_str.split(',')
        if value_str == [""]:
            continue
        try:
            value = map(int, value_str)
            #print value
            param_names.append(par_name)
            param_values.append(value)
        except:
            continue
param_name_val_map = dict(zip(param_names, param_values))
print param_name_val_map
#parameter_name = "price"



# just for testing
# param_names.append("map_pizza_voucher")
# param_values.append([1, 2, 3, 4, 5, 4, 2, 1, 3, 3, 4])
# line = ifile.readline()
# line = line[:len(line)] #to remove the \n from the last number
# parameter_str = line.split(',')
# for p in range(0, len(parameter_str)):
#     parameter_str.append(int(p))

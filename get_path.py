import os
import Globals


def get_paths():
    path_file = open(Globals.ifile_path, "r")
    lines = path_file.readlines()
    line_num_arr = []
    nums = []
    for line in lines:
        line_nums = [s for s in line.split() if s.isdigit()] #extract the line numbers from each line
        if len(line_nums) > 0:
            line_num = line_nums[0]
            line_num_arr.append(line_num)
            index = line.rfind(".mzn") + len(".mzn")
            ctr = 0
            num = ""
            for c in line[index:]:
                if c == '|':
                    ctr += 1
                if ctr < 5:
                    num += c
            num += "\t"
            nums.append(num)
    num_path = dict(zip(line_num_arr, nums))
    return num_path


def get_path(line_numbers):
    line_numbers = line_numbers.split()
    paths = ""
    num_path = get_paths()
    for line_number in line_numbers:
        if line_number not in num_path.keys():
            continue
        if num_path[line_number] not in paths:
            paths += num_path[line_number] + " "
    return paths




from pattern_functions import *
from Nogood import *
from Literal import *
from Fact import *

#lits1 = convert_str_to_literals("XI:72|13-72|48:(j=106):builtins.mzn:312|9-312|35<=49")
#lits2 = convert_str_to_literals("XI:72|13-72|48:(j=26):builtins.mzn:312|9-312|35<=12")
# types = get_type('a', 'dims')
# types = get_type('a', 'enum_type')
# print types
#convert_str_to_literals('a[STEPS[3],5]!=a[STEPS[4],5] a[3,5]!=4 a[4,5]==4')
# print get_type('a', 'dims')

# lits1 = convert_str_to_literals('a[STEPS[3],5]!=a[STEPS[4],5] a[3,5]!=4+a[4,5]')
# print lits1[1].get_var_types()
# print lits1[1].get_params()


# print lits1
# str1 = "a[STEPS[3],5]!=a[STEPS[4],5]"
# print str1

# components = re.findall(r"(\[\],|+=><!)", str1)
# print components
#
# lits1 = convert_str_to_literals('a[STEPS[3],5]!=a[STEPS[4],5] a[7,8]==9')
# lits2 = convert_str_to_literals('a[5,5]!=5 a[4,5]==4')

# list1 = ["A", "B", "C", "D"]
# list2 = ["1", "2", "3", "4"]
# list3 = ["a", "b", "c", "d"]

# dict1 = dict(zip(list1, list2,list3))
# dict2 = {"kiana": {"aus": "25"}
# }
# # my_dict = {a: {p: l} for l in list3 for p in list2 for a in list1}
# # print my_dict
#
# animal, property = ['dolphin', 'panda', 'koala'], ['habitat', 'diet', 'lifespan']
#
# my_dict = {a: {p: {} for p in property}  for a in animal}
# print my_dict
# print dict2["kiana"]["aus"]


# lits1 = convert_str_to_literals('how[1]=2')
# lits1[0].update()
# print lits1[0].get_var_types()
# lits2 = convert_str_to_literals('a[STEPS[3],5]!=a[STEPS[6],5] a[2,13]!=5 a[3,13]==5')

# x[1,5]<=2 x[2,5]<=2 x[neigh[3,1],neigh[3,2]]=2 x[neigh[3,1],neigh[3,2]]=3

lits1 = convert_str_to_literals('how[3]!=2, how[1]!=-2')

lits2 = convert_str_to_literals('how[2]!=3, how[5]!=-3')
# lits1 = convert_str_to_literals('a[3,2]=4')
# lits2 = convert_str_to_literals('a[6,5]=9')
n = Nogood("23", lits1, 123, "|2|3|4|5|")
p1 = Pattern(["24"], lits2, [], [200], ["|2|3|4|5|"])
p2 = generate_pattern(p1, n)
#print p2.negate_pattern_all_enum()
#print p2.get_vars_for_a_type("int")
print p2
print p2.get_vars_for_a_type("pizza")

print p2.find_types_enum()
print p2.find_types_dim()

f = Fact(p2)
print f.get_fact_str()


# print p2.get_params()
# print p2.get_var_types()

# print p2.get_all_objects_of_the_same_type()
# print p2.get_parameters_indexed_by_objects()

#how[10]!=-3 how[@A]!=3

#p2.calculate_things_to_compare()

# print p2.get_map_var_type()
# print p2.get_var_types()

# print p2.get_name_original()

# # p3 = Pattern(["24"], lits3, [], [200], ["|2|3|4|5|"])
# print p2
# patterns = []
# patterns.append(p3)
# patterns.append(p2)
# print pattern_exists(patterns, p2)

# print p2.get_maps()
# print p2.get_params()
# print n
# print p1
# print p2
# print p1.get_params()

#
# assert (p1.get_name() == "how[1]!=3 how[9]!=3"), "Failed get_name() for p1"
# assert (p2.get_name() == "how[@A]!=3 how[@B]!=3"), "Failed get_name() for p2"
#
# assert (p1.get_pnums() == []), "Failed get_pnums() for p1"
# assert (p2.get_pnums() == [['1', '9'], ['2', '4'], ['1', '3']]), "Failed get_pnums() for p2"
#
# assert (p1.get_maps() == []), "Failed get_maps() for p1"
# assert (p2.get_maps() == [{'A': '1', 'B': '9'}, {'A': '2', 'B': '4'}, {'A': '1', 'B': '3'}]), "Failed get_maps() for p2"
#
# assert (p1.get_params() == ['1', '3', '9', '3']), "Failed get_params() for p1"
# assert (p2.get_params() == ['A', '3', 'B', '3']), "Failed get_params() for p2"
#
# assert (p1.get_operators() == "!=!="), "Failed get_operators() for p1"
# assert (p2.get_operators() == "!=!="), "Failed get_operators() for p2"
#
# assert (p1.get_indices_of_params() == [4, 8, 4, 8]), "Failed get_indices_of_params() for p1"
# assert (p2.get_indices_of_params() == [5, 9, 5, 9]), "Failed get_indices_of_params() for p2"
#
# assert (p1.get_constants() == ['1', '3', '9', '3']), "Failed get_constants() for p1"
# assert (p2.get_constants() == ['3', '3']), "Failed get_constants() for p2"
#
# assert (p1.get_indices_of_consts() == [4, 8, 4, 8]), "Failed get_indices_of_consts() for p1"
# assert (p2.get_indices_of_consts() == [8, 8]), "Failed get_indices_of_consts() for p2"
#
# assert (p1.get_variables() == []), "Failed get_variables() for p1"
# assert (p2.get_variables() == ['A', 'B']), "Failed get_variables() for p2"
#
# assert (p1.get_indices_of_vars() == []), "Failed get_indices_of_vars() for p1"
# assert (p2.get_indices_of_vars() == [4, 4]), "Failed get_indices_of_vars() for p2"

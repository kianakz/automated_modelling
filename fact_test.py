from Fact import *
from pattern_functions import *
from Nogood import *

lits2 = convert_str_to_literals('how[6]!=-1 how[1]!=2 how[3]!=-1 how[1]!=2')
lits1 = convert_str_to_literals('how[7]!=-1 how[8]!=3 how[6]!=-2 how[1]!=2')
n = Nogood("23", lits1, 123, "|2|3|4|5|")
p1 = Pattern(["24"], lits2, [], [200], ["|2|3|4|5|"])
p2 = generate_pattern(p1, n)
maps = p2.get_maps()
p_enum_types = p2.find_types_enum()
p_dim_types = p2.find_types_dim()
#p2.add_map(['203'], [{'1', '3', '2', '3', '2', '1', '3'}], [20], "")
f = Fact(p2)


print p2.get_all_objects_of_the_same_type()
print p2.get_parameters_indexed_by_objects()

print p2
print p2.get_maps()
print f.get_fact_str()

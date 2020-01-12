from Fact import *
from pattern_functions import *
from Nogood import *
from Literal import *
from functions import *

# lits1 = convert_str_to_literals("how[2]!=3 how[4]!=3")
# lits2 = convert_str_to_literals("how[5]!=3 how[9]!=3")
# n = Nogood(23, lits1, 123, "|2|3|4|5|")
# p1 = Pattern([23], lits2, [], [345], ["|2|3|4|5|"])
# p2 = Pattern([23], lits2, [], [345], ["|2|3|4|5|"])
# p3 = generate_pattern(p1, n)
#print p3.get_name()

#print get_type("how", "enum_type")
print get_type("x", "enum_type")
print get_type("x", "dims")



#print get_type("how", "dims")
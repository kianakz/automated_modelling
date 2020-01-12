from Nogood import *
from Literal import *
from functions import *

lits = convert_str_to_literals("how[10]!=-3 how[1]=1 how[1]=2 how[4]!=-3 how[5]>0 how[5]=-4 "
                        "how[6]>0 how[6]=-4 how[7]>0 how[7]=-4 how[8]=-4 how[8]>0 how[9]=-4 objective>=350")
ng = Nogood(21, lits, 123, "|12|3|4|5")
print ng.get_name()
for lit in lits:
    print lit.get_variable_names()
    print lit.get_params()
    
"""
This module consists of the functions related to the pattern class.
"""
from Pattern import *
from functions import *
import copy

eval_flag = True


def generate_pattern(pattern, nogood):
    """
    pattern and nogood should have the same length, variables and operators
    :param pattern: an object of pattern
    :param nogood: an object of nogood
    :return: a new pattern containing the maps (of pattern and nogood)
    """
    seq_lit_p = pattern.get_seq_lits()
    seq_lit_n = nogood.get_seq_lits()
    param_types = pattern.get_var_types()

    #seq_lit_newp = copy.deepcopy(seq_lit_p)  # copies the literals corresponding to the seq_lit_p to the new pattern literals
    seq_lit_newp = []
    for lit in seq_lit_p:
        new_lit = Literal(lit.get_literal_str())
        new_lit.update()
        seq_lit_newp.append(new_lit)

    reds_p = pattern.get_reds()
    red_n = nogood.get_red()
    reds_newp = list(reds_p)
    reds_newp.append(red_n)
    paths_p = pattern.get_paths()
    paths_n = nogood.get_paths()
    paths_new_p = []
    for c in paths_p:
        paths_new_p.append(c)  # adding the paths corresponding to the old pattern to the new pattern
    paths_new_p.append(paths_n)  # adding the paths corresponding to the nogood to the new pattern
    n_id = nogood.get_ID()
    p_nids = pattern.get_IDS()
    #newp_ids = deepish_copy(p_nids)
    newp_ids = list(p_nids)
    newp_ids.append(n_id)
    p_maps = pattern.get_maps()
    new_pattern_maps = []
    x = 'A'
    list_consts = []  # to store the tuples in nogood and pattern which are being replaced by a variable
    list_var_new_p = []
    list_params_p = []  # params in the pattern that are replaced
    list_consts_n = []  # consts in the nogood that are replaced
    list_consts_new_p = [] * len(p_maps)  # contains all the constants corresponding to the pattern and nogood
    list_all_consts = []
    dict_rep_type_var = {}  # e.g. dict_rep_type_var[rep][type]= 'A'

    """
    For each literal if the parameters of nogood and pattern are different they are replaced by a variable
    """
    for i in range(0, len(seq_lit_p)):
        if x > 'Z':
            x = 'a'
        elif x > 'z':
            x = 'A'
        params_pattern = seq_lit_newp[i].get_params()  # constants or variables e.g how[1]=b => [1,b]
        consts_nogood = seq_lit_n[i].get_params()
        param_types_lit = seq_lit_newp[i].get_var_types()
        if len(params_pattern) == len(consts_nogood):
            for j in range(0, len(consts_nogood)):
                indices_of_params = seq_lit_newp[i].get_params_indices()
                if params_pattern[j] != consts_nogood[j]:
                    rep_tuple = (consts_nogood[j], params_pattern[j])

                    if ((rep_tuple, param_types_lit[j]) in dict_rep_type_var.keys()  # if the same consts are being replaced they should be
                        ):
                        #  replaced by the same variable
                        # param_types[j] == dict_var_type[map_const_var[rep_tuple]]):  # replacing the same type with the same
                        #  variable
                        # e.g. ng1: how[1]=2 used[1]=3
                        #      ng2: how[3]=2 used[4]=3
                        # if type of index of how is pizza and type of index of used is pizza the pattern will be:
                        # p: how[A]=2 used[A]=3
                        # Otherwise: p: how[A]=2 used[B]=3
                        try:
                            if seq_lit_newp[i].get_literal_str()[indices_of_params[j] - 1] == '@':
                                seq_lit_newp[i].set_variable(dict_rep_type_var[(rep_tuple, param_types_lit[j])], indices_of_params[j], len(params_pattern[j]))
                            else:
                                seq_lit_newp[i].set_variable('@' + dict_rep_type_var[(rep_tuple, param_types_lit[j])], indices_of_params[j],
                                                             len(params_pattern[j]))
                        except:
                            print seq_lit_newp[i]
                            print j
                            print indices_of_params

                    else:
                        list_consts_n.append(consts_nogood[j])
                        list_params_p.append(params_pattern[j])
                        list_consts.append(rep_tuple)
                        list_var_new_p.append(x)
                        dict_rep_type_var.update({(rep_tuple, param_types_lit[j]): x})

                        # for v in range(0, len(list_var_new_p)):
                        #     dict_rep_type_var.update({(list_consts[v], param_types[v]): list_var_new_p[v]})

                        if seq_lit_newp[i].get_literal_str()[indices_of_params[j]-1] == '@':
                            seq_lit_newp[i].set_variable(x, indices_of_params[j], len(params_pattern[j]))
                        else:
                            seq_lit_newp[i].set_variable('@' + x, indices_of_params[j], len(params_pattern[j]))
                        x = chr(ord(x) + 1)
                        if x > 'Z':
                            x = 'a'
                        elif x > 'z':
                            x = 'A'

    """
    replaces all the variables in the map of old pattern by their value 
    """
    """
    list_consts_new_p stores all the constants corresponding to the old pattern
    e.g.
    newp = how[A]=B
    oldp = how[A]=1 maps =[{A:4}, {A:5}]
    list_consts_new_p = [[4,1], [5,1]]
    """
    for i in range(0, len(p_maps)):  # p_maps: maps corresponding to the old pattern
        list_consts_new_p.append([])

    for i in range(0, len(list_params_p)):
        param = list_params_p[i]
        if isDigit(param):  # checks if param is variable or a constant
            if len(p_maps) > 0:  # if there are maps under the old pattern
                for j in range(0, len(p_maps)):
                    list_consts_new_p[j].append(param)
        elif len(param) == 1:
            for j in range(0, len(p_maps)):
                list_consts_new_p[j].append(p_maps[j][param])
    for list_const in list_consts_new_p:
        new_pattern_maps.append(dict(zip(list_var_new_p, list_const)))
    if len(p_maps) == 0:  # if there isn't any map under the old pattern
        new_pattern_maps.append(dict(zip(list_var_new_p, list_params_p)))  # if there is no variable
        list_all_consts.append(list_params_p)
    else:
        list_all_consts += list_consts_new_p
    new_pattern_maps.append(dict(zip(list_var_new_p, list_consts_n)))
    list_all_consts.append(list_consts_n)
    new_pattern = Pattern(newp_ids, seq_lit_newp, list_all_consts, reds_newp, paths_new_p)
    return new_pattern


def pattern_exists(patterns, p):
    """
    :param patterns: List of all the existing patterns
    :param p: An object of a pattern to check if it exists
    :return: If the pattern doesn't exist it returns false, otherwise the index of pattern would be returned
    """
    lit_seq_new_p = p.get_seq_lits()
    new_p_var_names = p.get_variable_names()
    p_var = p.get_variables()
    p_var_set = set(p_var)
    indices_of_vars_new_p = p.get_indices_of_vars()
    constants_newp = p.get_constants()
    indices_of_consts_newp = p.get_indices_of_consts()
    for i in range(0, len(patterns)):
        flag_continue = False
        old_pattern_names = patterns[i].get_variable_names()
        if new_p_var_names != old_pattern_names:
            continue
        lit_seq_existing_p = patterns[i].get_seq_lits()
        if len(lit_seq_existing_p) != len(lit_seq_new_p):
            continue
        pattern_var = patterns[i].get_variables()
        if len(p_var) != len(pattern_var):
            continue
        pattern_var_set = set(pattern_var)
        if len(p_var_set) != len(pattern_var_set):
            continue
        if p.get_name() == patterns[i].get_name():
            return i
        indices_of_vars_existing_p = patterns[i].get_indices_of_vars()
        constants_pattern = patterns[i].get_constants()
        indices_of_consts_pattern = patterns[i].get_indices_of_consts()
        if (len(p_var) == len(pattern_var) and indices_of_vars_new_p == indices_of_vars_existing_p
                and indices_of_consts_pattern == indices_of_consts_newp and constants_newp == constants_pattern):
            flag_continue = False
            for v in range(0, len(p_var)):
                occ_var_newp = find_occurrences_list(p_var, p_var[v])
                occ_var_existingp = find_occurrences_list(pattern_var, pattern_var[v])
                if occ_var_newp != occ_var_existingp:
                    flag_continue = True
                    break
                     # return -1
            if not flag_continue:
                return i
    return -1


def get_cluster_str(p, delimiter):
    """
    :param p: a pattern object
    :param delimiter: a char (the delimeter of output file)
    :return: A string: containing the form of:
    reduction_c1, maps_c1, paths_c1\n,,reduction_c2, maps_c2, paths_c2
    Important : Each time you add another columns before the cluster (a new data): cluster_str += delimiter  + str(sum_red_cluster) + delimiter + map_str + delimiter + list_paths[c] + '\n' + delimiter \
                       + delimiter + delimiter
    Add one delimiter in the end
    """
    maps = p.get_maps()
    ng_ids = p.get_IDS()
    ng_reds = p.get_reds()
    p_paths = p.get_paths()
    set_paths = set(p_paths)
    list_paths = list(set_paths)
    list_paths.sort(key=len)
    clusters = []
    for s in range(0, len(list_paths)):
        clusters.append([])
        for n in range(0, len(ng_ids)):
            if p_paths[n] == list_paths[s]:
                map_str = ''
                map_str += ng_ids[n]
                if len(maps) > 0:
                    map_str += ':'
                    map_str += '['
                    map_str += ''.join('{} = {} '.format(key, val) for key, val in maps[n].items())
                    map_str += ']'
                clusters[s].append((map_str, ng_reds[n]))
    cluster_str = ''
    for c in range(0, len(clusters)):
        map_str = '"'
        sum_red_cluster = 0
        for tuple in clusters[c]:
            map_str += tuple[0] + ' '   # change to \n if the delimiter is ,
            sum_red_cluster += tuple[1]
        map_str += '"'
        cluster_str += delimiter + str(sum_red_cluster) + delimiter + map_str + delimiter + list_paths[c] + '\n' + delimiter \
                       + delimiter + delimiter + delimiter + delimiter + delimiter + delimiter
    return cluster_str

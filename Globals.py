import os
import re
delimiter = '$'

# File names
# direct = "C:\Docs\projects\generate-pattern\\free_pizza_enum"


direct = "C:\Docs\projects\\autoprofile_0.1\\newExperiments\\2018\\vrplc"
mzn_model_name = "vrplc_service.mzn"
data_file_name = "vrplc9_5_10_s3.dzn"

model_name = re.search(r'(.*?).mzn', mzn_model_name).group(1)
data_name = re.search(r'(.*?).dzn', data_file_name).group(1)

fixed_original_name = model_name + "_" + data_name + "_" + "result_fixed_original.tsv"
fixed_renamed_name = model_name + "_" + data_name + "_" + "result_fixed_renamed.tsv"
fixed_renamed_simplified_name = model_name + "_" + data_name + "_" + "result_fixed_renamed_simplified.tsv"

alternating_original_name = model_name + "_" + data_name + "_" + "result_alternating_original.tsv"
alternating_renamed_name = model_name + "_" + data_name + "_" + "result_alternating_renamed.tsv"
alternating_simplified_name = model_name + "_" + data_name + "_" + "result_alternating_renamed_simplified.tsv"


input_type_file_name = model_name + ".type"
#input_type_file_name = "freepizza_enum_org.type"
path_file_name = model_name + ".paths"

#nogood_file_name = "mario_mario_medium_1_result_alternating_renamed_simplified.txt"
nogood_file_name = model_name + " " + data_name + " fixed + alternating.txt"

#nogood_file_name = "concert-cap.mznc2018.02_dominance_breaking(fixed search with a random order).txt"
solutions_for_model_with_pattern_name = "sols_" + model_name + " " + data_name
model_with_pattern_name = model_name + "_with_pattern.mzn"
solutions_for_model_with_negated_pattern_name = model_name + "_with_negated_pattern.mzn"

#nogood_file_name = "original_freepizza_pizza_paper_10_result_fixed.tsv"

#output_file_name_alternating = model_name + "_" + data_name + "_" + "result_alternating.tsv"
#output_file_name_fixed = model_name + "_" + data_name + "_" + "result_fixed.tsv"

ofile_statistics_simplification_dir = os.path.join(direct, "statistics_simplification" + model_name + data_name + ".txt")
ofile_statistics_dir = os.path.join(direct, "statistics" + model_name + data_name + ".txt")
ofile_result_dir = os.path.join(direct, "results" + model_name + data_name + ".txt")
ofile_solutions_for_model_with_pattern_dir = os.path.join(direct, solutions_for_model_with_pattern_name)
#ofile_solutions_for_model_with_pattern_after_counting_dir = os.path.join(direct, "sols_pizza10_after_counting.dzn")
ofile_test_dir = os.path.join(direct, "output_test.txt")

ofile_model_with_pattern_dir = os.path.join(direct, model_with_pattern_name)
ofile_solutions_for_model_with_negated_pattern_dir = os.path.join(direct, solutions_for_model_with_negated_pattern_name)

ifile_model_with_pattern_dir = os.path.join(direct, model_with_pattern_name)
ifile_original_model_dir = os.path.join(direct, mzn_model_name)

ifile_CONACQ_model_dir = "conacq_same_as_paper_template.mzn"
ifile_CONACQ_model_dir_parameter = "conacq_same_as_paper_template_parameter.mzn"

ifile_input_data_file_dir = os.path.join(direct, data_file_name)
ifile_nogood = os.path.join(direct, nogood_file_name)
#ifile_param = os.path.join(direct, "input.txt")
ifile_path = os.path.join(direct, path_file_name)
ifile_type = os.path.join(direct, input_type_file_name)


ifile_fixed_original_dir = os.path.join(direct, fixed_original_name)
ifile_fixed_renamed_dir = os.path.join(direct, fixed_renamed_name)
ifile_fixed_renamed_simplified_dir = os.path.join(direct, fixed_renamed_simplified_name)

ifile_alternating_original_dir = os.path.join(direct, alternating_original_name)
ifile_alternating_renamed_dir = os.path.join(direct, alternating_renamed_name)
ifile_alternating_renamed_simplified_dir = os.path.join(direct, alternating_simplified_name)



solver = "Gecode"
# For CONACQ
# parameter = [70, 10, 60, 65, 30, 100, 75, 40, 45, 20]
n = 10
#TODO: should read all the possible variables from the type file
# Flags
flag_all_conts_positive = True  # if flag_all_conts_positive is true, the parameters are all positive and negative sign
# is ignored e.g. how[1]= -2 => self.param = ['1', '2']
# if the flag is false:  e.g. how[1]= -2 => self.param = ['1', '-2']
eval_flag = True  # if this flag is true all the expressions in nogood will be evaluated and replaced by the result.
# e.g. a[1+2] => if eval_flag = True a[3]
ignore_data_file = True



import numpy as np
from relative_dose_1d.tools import text_to_list, get_data

lista = text_to_list("6FFF_calculated_Eclipse.txt")

array = get_data("6FFF_calculated_Eclipse.txt", start_word = "Field 1")

new_array = array[0::8,:]
#print(new_array)

np.savetxt("6FF_clinical_calc_profile.txt", new_array, fmt='%.6f', delimiter="\t")
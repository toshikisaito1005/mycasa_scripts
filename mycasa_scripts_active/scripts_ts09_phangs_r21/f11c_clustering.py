import numpy as np

dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"


#####################
### Main Procedure
#####################
txtdata = np.loadtxt(dir_data + "eps/ngc0628_parameter_matched_res.txt")

# get data
xydata = np.c_[txtdata[:,14], txtdata[:,15]] # parsec
# calculate distance matrix
all_diffs = np.expand_dims(xydata, axis=1) - np.expand_dims(xydata, axis=0)
distance = np.sqrt(np.sum(all_diffs ** 2, axis=-1))

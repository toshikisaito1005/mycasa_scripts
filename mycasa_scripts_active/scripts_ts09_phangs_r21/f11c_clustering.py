import numpy as np


#####################
### Directory
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"


#####################
### Main Procedure
#####################
txtdata = np.loadtxt(dir_data + "eps/ngc0628_parameter_matched_res.txt")

### get data
xydata = np.c_[txtdata[:,14], txtdata[:,15]] # parsec
r21mask = txtdata[:,13]
### choose data
xydata_high = xydata[r21mask==1]
xydata_mid = xydata[r21mask==0]
xydata_low = xydata[r21mask==-1]
### calculate distance matrix
all_diffs = np.expand_dims(xydata_high, axis=1) - np.expand_dims(xydata_high, axis=0)
distance_high = np.sqrt(np.sum(all_diffs**2, axis=-1))
#
all_diffs = np.expand_dims(xydata_mid, axis=1) - np.expand_dims(xydata_mid, axis=0)
distance_mid = np.sqrt(np.sum(all_diffs**2, axis=-1))
#
all_diffs = np.expand_dims(xydata_low, axis=1) - np.expand_dims(xydata_low, axis=0)
distance_low = np.sqrt(np.sum(all_diffs**2, axis=-1))
#
### calcurate function
list_dist = np.log10(np.logspace(np.log10(1), np.log10(10000), 21))
list_func = []
for i in list_dist"
num_zero_high = len(distance_high[distance_high==0])

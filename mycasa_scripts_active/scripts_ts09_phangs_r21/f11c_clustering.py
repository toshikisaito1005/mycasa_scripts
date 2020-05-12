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
list_log_dist = np.log10(np.logspace(np.log10(1), np.log10(10000), 21))
list_num = []
for this_log_dist in list_log_dist:
	num_zero_high = len(distance_high[distance_high==0])
	this_num = len(distance_high[distance_high<=10**this_log_dist]/2 - num_zero_high)
	list_num.append(this_num)
#
list_num = np.array(list_num)
#
### plot
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=17, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:5,0:8])
ax2 = plt.subplot(gs[6:11,0:8])
ax3 = plt.subplot(gs[12:17,0:8])
ax1.grid(axis="x")
ax2.grid(axis="x")
ax3.grid(axis="x")
ax1.set_xlabel("Distance (kpc)")
ax2.set_xlabel("Distance (kpc)")
ax3.set_xlabel("Distance (kpc)")
plt.rcParams["font.size"] = 16


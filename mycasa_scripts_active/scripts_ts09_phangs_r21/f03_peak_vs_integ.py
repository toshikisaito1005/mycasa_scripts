import os
import re
import sys
import glob
import scipy


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	galname = gals[i]
	dir_r21 = dir_proj + galname + "_parameter_matched_res.txt"

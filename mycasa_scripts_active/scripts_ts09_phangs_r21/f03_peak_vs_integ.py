import os
import re
import sys
import glob
import scipy


#####################
### parameters
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628","ngc3627","ngc4321"]


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	galname = gals[i]
	dir_
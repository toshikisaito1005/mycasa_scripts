import os
import re
import sys
import glob
import scipy
import numpy as np

#####################
### Parameter
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
galaxy = ["eso267"]

#####################
### Main Procedure
#####################
for i in range(len(galaxy)):
	this_galaxy = galaxy[i]
	this_mom0 = glob.glob(dir_proj + this_galaxy + "*_mom0.fits")[0]
	# get box
	shape = imhead(this_mom0,mode="list")["shape"]
	box = "0,0," + str(shape[0]) + "," + str(shape[1])
	# get beam and pixel size
	
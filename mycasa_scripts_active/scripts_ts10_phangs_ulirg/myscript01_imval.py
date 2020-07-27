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
	this_header = imhead(this_mom0,mode="list")
	shape = this_header["shape"]
	box = "0,0," + str(shape[0]-1) + "," + str(shape[1]-1)
	# K_to_Jy conversion factor
	this_beamsize = this_header["beammajor"]["value"] # arcsec
	this_pixelsize = abs(this_header["cdelt1"]) * 3600 * 180 / np.pi # arcsec
	K_to_Jy = 1 / (1.222e6 / this_beamsize**2 / 230.53800**2)
	# imval


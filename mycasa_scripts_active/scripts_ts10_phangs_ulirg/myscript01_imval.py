import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.cm as cm
import matplotlib.patches as mpatches


#####################
### Parameter
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = ['eso267', 'eso297g011', 'eso297g012', 'eso319', 'eso507', 'eso557', 'ic4518e', 'ic4518w', 'ic5179', 'iras06592', 'irasf10409', 'irasf17138', 'mcg02', 'ngc1614', 'ngc2369', 'ngc3110', 'ngc3256', 'ngc5257', 'ngc6240']

#####################
### Main Procedure
#####################
list_m0 = []
list_ew = []
for i in range(len(galaxy)):
	this_galaxy = galaxy[i]
	print("# working on " + this_galaxy)
	this_mom0 = glob.glob(dir_proj + this_galaxy + "*_mom0.fits")[0]
	this_ew = glob.glob(dir_proj + this_galaxy + "*_ew.fits")[0]
	# get box
	this_header = imhead(this_mom0,mode="list")
	shape = this_header["shape"]
	box = "0,0," + str(shape[0]-1) + "," + str(shape[1]-1)
	# K_to_Jy conversion factor
	this_beamsize = this_header["beammajor"]["value"] # arcsec
	this_pixelsize = abs(this_header["cdelt1"]) * 3600 * 180 / np.pi # arcsec
	this_beamsize_per_pix = this_beamsize / this_pixelsize
	gridsize = (int(shape[0] / this_beamsize_per_pix), int(shape[1] / this_beamsize_per_pix))
	# imval mom0
	this_data = imval(this_mom0, box=box)
	x = this_data["coords"][:,:,0].flatten()
	y = this_data["coords"][:,:,1].flatten()
	z_m0 = this_data["data"].flatten()
	# imval ew
	this_data = imval(this_ew, box=box)
	z_ew = this_data["data"].flatten()
	# hexbin
	fig, ax = plt.subplots(1, 1)
	hex_m0 = ax.hexbin(x, y, C=z_m0, gridsize=gridsize)
	hex_m0 = np.log10(hex_m0.get_array())
	hex_ew = ax.hexbin(x, y, C=z_ew, gridsize=gridsize)
	hex_ew = np.log10(hex_ew.get_array())
	# plt.savefig(dir_eps+"test.png",dpi=200)
	# output
	np.savetxt(dir_eps+"scatter_"+this_galaxy+".txt",np.c_[hex_m0,hex_ew])

os.system("rm -rf *.last")

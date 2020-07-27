import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.patches as mpatches


#####################
### Parameter
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
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
	# gridsize
	gridsize = shape[0]
	# imval
	this_data = imval(this_mom0, box=box)
	x = this_data["coords"][:,:,0].flatten()
	y = this_data["coords"][:,:,1].flatten()
	z = this_data["data"].flatten()
	# plot
	fig, ax = plt.subplots(1, 1)
	ax.hexbin(x, y, C=z)
	plt.savefig(dir_eps+"test.png",dpi=200)
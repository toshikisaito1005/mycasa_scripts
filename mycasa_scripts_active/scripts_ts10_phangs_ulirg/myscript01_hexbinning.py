import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.cm as cm
import matplotlib.patches as mpatches
from astropy import units as u
from astropy.coordinates import SkyCoord


#####################
### Parameter
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
phangs = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_proj + "../data_phangs/*mom0*")]
#galaxy = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_proj + "*mom0*")]
galaxy = ['eso267','eso297g011','eso297g012','eso319','eso507','eso557','ic4518e','ic4518w','ic5179','iras06592','irasf10409','irasf17138','mcg02-33-098','ngc1614','ngc2369','ngc3110','ngc3256','ngc5257','ngc6240']
centers = [["12:14:12.821 -47:13:42.928"], # eso267
		   ["01:36:23.387 -37:19:17.643"], # eso297g011
		   ["01:36:24.154 -37:20:25.853"], # eso297g012
		   ["11:27:54.085 -41:36:52.241"], # eso319
		   ["13:02:52.366 -23:55:17.740"], # eso507
		   ["06:31:47.198 -17:37:15.765"], # eso557
		   ["14:57:45.268 -43:07:56.000"], # ic4518e (center?)
		   ["14:57:41.127 -43:07:55.035"], # ic4518w
		   ["22:16:09.141 -36:50:36.965"], # ic5179
		   ["06:59:40.268 -63:17:53.018"], # iras06592
		   ["10:43:07.660 -46:12:44.866"], # irasf10409
		   ["17:16:35.793 -10:20:40.758"], # irasf17138
		   ["13:02:19.649 -15:46:04.058"], # mcg02-33-098 (center?)
		   ["04:34:00.026  -8:34:45.100"], # ngc1614
		   ["07:16:37.676 -62:20:36.598"], # ngc2369
		   ["10:04:02.086  -6:28:29.288"], # ngc3110
		   ["10:27:51.204 -43:54:16.627"], # ngc3256 (center?)
		   ["13:39:52.916   0:50:24.481"], # ngc5257
		   ["16:52:58.893   2:24:03.792"], # ngc6240
		   ]
scales = [365,345,345,325,425,425,325,325,225,445,425,345,305,305,205,325,185,445,485]


#####################
### Main Procedure
#####################
#for i in range(len(galaxy)):
for i in [0]:
	this_galaxy = galaxy[i]
	print("# working on " + this_galaxy)
	this_center = centers[i][0]
	this_scale = scales[i]
	# get enter in degree
	c = SkyCoord(this_center, unit=(u.hourangle, u.deg))
	ra_center, dec_center = c.ra.deg, c.dec.deg
	# get images
	this_mom0 = glob.glob(dir_proj + this_galaxy + "*_mom0.fits")[0]
	this_ew = glob.glob(dir_proj + this_galaxy + "*_ew.fits")[0]
	# get box
	this_header = imhead(this_mom0,mode="list")
	shape = this_header["shape"]
	box = "0,0," + str(shape[0]-1) + "," + str(shape[1]-1)
	# determine hex size
	this_beamsize = this_header["beammajor"]["value"] # arcsec
	this_pixelsize = abs(this_header["cdelt1"]) * 3600 * 180 / np.pi # arcsec
	this_beamsize_per_pix = this_beamsize / this_pixelsize
	gridsize = (int(shape[0] / this_beamsize_per_pix), int(shape[1] / this_beamsize_per_pix))
	# imval mom0
	this_data = imval(this_mom0, box=box)
	x = this_data["coords"][:,:,0].flatten() * 180/np.pi - ra_center
	y = this_data["coords"][:,:,1].flatten() * 180/np.pi - dec_center
	r = np.sqrt(x**2 + y**2) * this_scale/1000 # radius in kpc units
	z_m0 = this_data["data"].flatten()
	# imval ew
	this_data = imval(this_ew, box=box)
	z_ew = this_data["data"].flatten()
	# hexbin
	fig, ax = plt.subplots(1, 1)
	hex_m0 = ax.hexbin(x, y, C=z_m0, gridsize=gridsize)
	hex_m0 = hex_m0.get_array()
	hex_ew = ax.hexbin(x, y, C=z_ew, gridsize=gridsize)
	hex_ew = hex_ew.get_array()
	hex_r = ax.hexbin(x, y, C=r, gridsize=gridsize)
	hex_r = hex_r.get_array()
	#plt.savefig(dir_eps+"hex_"+this_galaxy+".png",dpi=200)
	# output
	np.savetxt(dir_eps+"scatter_"+this_galaxy+".txt",np.c_[hex_m0,hex_ew,hex_r])

"""
for i in range(len(phangs)):
	this_galaxy = phangs[i]
	print("# working on " + this_galaxy)
	this_mom0 = glob.glob(dir_proj + "../data_phangs/" + this_galaxy + "*_mom0*.fits")[0]
	this_ew = glob.glob(dir_proj + "../data_phangs/" + this_galaxy + "*_ew*.fits")[0]
	# get box
	this_header = imhead(this_mom0,mode="list")
	shape = this_header["shape"]
	box = "0,0," + str(shape[0]-1) + "," + str(shape[1]-1)
	# determine hex size
	this_beamsize = this_header["beammajor"]["value"] # arcsec
	this_pixelsize = abs(this_header["cdelt1"]) * 3600 * 180 / np.pi # arcsec
	this_beamsize_per_pix = this_beamsize / this_pixelsize
	gridsize = (int(shape[0] / this_beamsize_per_pix), int(shape[1] / this_beamsize_per_pix))
	# imval mom0
	this_data = imval(this_mom0, box=box)
	x = this_data["coords"][:,:,0].flatten()
	y = this_data["coords"][:,:,1].flatten()
	z_m0 = this_data["data"].flatten()
	z_m0[np.isnan(z_m0)] = 0
	# imval ew
	this_data = imval(this_ew, box=box)
	z_ew = this_data["data"].flatten()
	z_ew[np.isnan(z_ew)] = 0
	# hexbin
	fig, ax = plt.subplots(1, 1)
	hex_m0 = ax.hexbin(x, y, C=z_m0, gridsize=gridsize)
	hex_m0 = hex_m0.get_array()
	hex_ew = ax.hexbin(x, y, C=z_ew, gridsize=gridsize)
	hex_ew = hex_ew.get_array()
	# output
	np.savetxt(dir_eps+"scatter_"+this_galaxy+".txt",np.c_[hex_m0,hex_ew])
"""

os.system("rm -rf *.last")

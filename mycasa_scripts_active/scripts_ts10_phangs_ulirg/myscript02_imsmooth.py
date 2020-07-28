import os
import re
import sys
import glob
import scipy
import math
import numpy as np


#####################
### Parameter
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = ['ic4518e', 'ic4518w', 'ic5179', 'iras06592', 'ngc1614', 'ngc5257']
beam = "0.8arcsec"

#####################
### Main Procedure
#####################
dir_smooth = dir_proj + "../data_0p8/"
done = glob.glob(dir_smooth)
if not done:
	os.mkdir(dir_smooth)

list_m0 = []
list_ew = []
for i in range(len(galaxy)):
	this_galaxy = galaxy[i]
	print("# working on " + this_galaxy)
	this_mom0 = glob.glob(dir_proj + this_galaxy + "*_mom0.fits")[0]
	### imsmooth
	outfile = dir_smooth + this_mom0.split("/")[-1].replace(".fits","_smooth.image")
	os.system("rm -rf " + outfile + "_tmp")
	imsmooth(imagename = this_mom0,
		targetres = True,
		major = beam,
		minor = beam,
		pa = "0deg",
		outfile = outfile + "_tmp")
	### imrebin
	beamsize = float(beam.replace("arcsec",""))
	pixelsize = abs(imhead(outfile+"_tmp",mode="list")["cdelt1"]) * 3600*180/np.pi
	factor = math.floor(beamsize/pixelsize/4.0)
	#
	os.system("rm -rf " + outfile)
	imrebin(imagename = outfile + "_tmp",
		outfile = outfile,
		factor = [factor, factor])
	os.system("rm -rf " + outfile + "_tmp")


os.system("rm -rf *.last")

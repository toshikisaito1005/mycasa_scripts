import numpy as np
import os
import glob
import pyfits
import shutil

dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
this_proj = "sim01"
robust = 0.5


##############################
### def
##############################
def dirty_map(
	vis,
	imagename,
	robust,
	width="",
	start="",
	imsize=512,
	phasecenter="",
	weighting="briggs",
	):
	"""
	"""
	#
	os.system("rm -rf " + imagename + "*")
	#
	tclean(
		vis = vis,
		imagename = imagename,
		field = "",
		specmode = "cube",
		restfreq = "230.53800GHz",
		outframe = "LSRK",
		width = width,
		start = start,
		niter = 0,
		threshold = "",
		cyclefactor = 4,
		interactive = False,
		imsize = imsize,
		cell = "1.0arcsec",
		phasecenter = phasecenter,
		weighting = weighting,
		robust = robust,
		gridder = "mosaic",
		deconvolver = "multiscale",
		scales = [0,2,5],
		nchan = nchan,
		cycleniter = 50,
		usemask = "user",
		restoringbeam = "common",
		startmodel = "",
		mask = "",
		)


##############################
### main
##############################
"""
# initialize
os.system("rm -rf " + this_proj)
os.system("rm -rf " + this_proj+"_*m")
os.system("rm -rf " + dir_project + "/" + this_proj+"_*m")
os.mkdir(this_proj)

# path to the mocksky FITS file
dir_mocksky = dir_project + "sim_images/"
this_skymodel = glob.glob(dir_mocksky + image_mocksky)[0]

# make 12m ms
print("### making simulted 12m ms")
run_simobserve("12m", this_skymodel, this_proj+"_12m")

# make 7m ms
print("### making simulted 7m ms")
run_simobserve("7m", this_skymodel, this_proj+"_7m")

# mv to the working directory
#
os.mkdir(dir_project + this_proj)
ms_12m = glob.glob(this_proj + "_12m/*.ms")[0]
os.system("cp -r " + ms_12m + " " + dir_project + this_proj)
#
ms_7m = glob.glob(this_proj + "_7m/*.ms")[0]
os.system("cp -r " + ms_7m + " " + dir_project + this_proj)
#
os.system("mv " + this_proj+"_* " + dir_project)
"""

#
os.system("rm -rf *.last")

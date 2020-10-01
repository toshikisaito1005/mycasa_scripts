import numpy as np
import os
import glob
import pyfits
import shutil
import math


dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
this_proj = "sim01"


##############################
### def
##############################
def dirty_continuum(
	vis,
	imagename,
	fov, # arcsec
	cell, # arcsec
	weighting="briggs",
	robust=0.5,
	):
	"""
	"""
	# calc imsize
	imsize_tmp = (fov + 46.85) / cell
	imsize = 2**int(math.ceil(np.log2(imsize_tmp)))
	#
	default("tclean")
	tclean(
		vis         = vis,
		imagename   = imagename,
		field       = "",
		specmode    = "mfs",
		restfreq    = "230.53800GHz",
		niter       = 0,
		threshold   = "",
		interactive = False,
		cell        = cell,
		imsize      = imsize,
		phasecenter = "",
		weighting   = weighting,
		robust      = robust,
		gridder     = "mosaic",
		deconvolver = "mtmfs",
		usemask     = "user",
		restoration = False,
		startmodel  = "",
		mask        = "",
		)


##############################
### main
##############################
# concat
vis_12m = glob.glob(dir_project + this_proj + "/*12m*.ms")[0]
vis_7m = glob.glob(dir_project + this_proj + "/*7m*.ms")[0]
#
dirty_continuum(
	vis,
	imagename,
	fov=120,
	cell=0.25)



#
os.system("rm -rf *.last")

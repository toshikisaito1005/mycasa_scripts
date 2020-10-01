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
	print("# imsize = " + str(imsize))
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
print("### concat")
vis_12m = glob.glob(dir_project + this_proj + "/*12m.ms")[0]
vis_7m = glob.glob(dir_project + this_proj + "/*7m.ms")[0]
vis_12m7m = vis_12m.replace("12m","12m+7m")
os.system("rm -rf " + vis_12m7m)
concat(vis=[vis_12m,vis_7m], concatvis=vis_12m7m)

# dirty map
print("### dirty map creation: 7m")
imagename = dir_project + this_proj + "/sim01_7m"
dirty_continuum(vis_7m, imagename, fov=120, cell=1.0)

print("### dirty map creation: 12m")
imagename = dir_project + this_proj + "/sim01_12m"
dirty_continuum(
	vis_7m,
	imagename,
	fov=120,
	cell=0.25)

print("### dirty map creation: 7m")
imagename = dir_project + this_proj + "/sim01_12+7m"
dirty_continuum(
	vis_7m,
	imagename,
	fov=120,
	cell=0.25)

#
os.system("rm -rf *.last")

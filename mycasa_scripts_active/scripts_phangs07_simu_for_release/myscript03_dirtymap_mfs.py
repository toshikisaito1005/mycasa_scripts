import numpy as np
import os
import glob
import pyfits
import shutil
import math


dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
phasecenter = "J2000 12h21m54.947s 4d28m15.258s"


##############################
### def
##############################
def clean_continuum(
	vis,
	imagename,
	fov, # arcsec
	cell, # arcsec
	phasecenter,
	weighting="briggs",
	robust=0.5,
	):
	"""
	"""
	# calc imsize
	cellfloat = float(cell.replace("arcsec",""))
	imsize_tmp = (fov + 46.85) / cellfloat
	imsize = 2**int(math.ceil(np.log2(imsize_tmp)))
	print("# imsize = " + str(imsize))
	#
	tclean(
		vis         = vis,
		imagename   = imagename,
		field       = "",
		specmode    = "mfs",
		restfreq    = "230.53800GHz",
		niter       = 1000,
		threshold   = "1mJy",
		interactive = False,
		cell        = cell,
		imsize      = imsize,
		phasecenter = phasecenter,
		weighting   = weighting,
		robust      = robust,
		gridder     = "mosaic",
		deconvolver = "hogbom",
		usemask     = "pb",
		pbmask      = 0.8,
		restoration = True,
		pblimit     = 0.5,
		)


##############################
### main
##############################
#
vis_12m = glob.glob(dir_project + this_proj + "/" + this_proj + "_12m.ms")[0]
vis_7m = glob.glob(dir_project + this_proj + "/" + this_proj + "_7m.ms")[0]

# 7m-only dirty map
print("### dirty map creation: 7m")
imagename = dir_project + this_proj + "/" + "image_sim01_7m"
os.system("rm -rf " + imagename + "*")
clean_continuum(vis_7m, imagename, fov=this_fov, cell="1.0arcsec", phasecenter=phasecenter)

# 12m-only dirty map
print("### dirty map creation: 12m")
imagename = dir_project + this_proj + "/" + "image_sim01_12m"
os.system("rm -rf " + imagename + "*")
clean_continuum(vis_12m, imagename, fov=this_fov, cell="0.4arcsec", phasecenter=phasecenter)

# concat
print("### concat")
vis_12m7m = vis_12m.replace("12m","12m+7m")
os.system("rm -rf " + vis_12m7m)
concat(vis=[vis_12m,vis_7m], concatvis=vis_12m7m)

# 12m+7m dirty map
print("### dirty map creation: 12m+7m")
imagename = dir_project + this_proj + "/" + "image_sim01_12+7m"
os.system("rm -rf " + imagename + "*")
clean_continuum(vis_12m7m, imagename, fov=this_fov, cell="0.4arcsec", phasecenter=phasecenter)

#
os.system("rm -rf *.last")

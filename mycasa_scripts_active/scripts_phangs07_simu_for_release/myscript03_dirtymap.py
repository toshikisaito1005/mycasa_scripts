import numpy as np
import os
import glob
import pyfits
import shutil
import math


dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
this_proj = "sim01"
phasecenter = "J2000 12h21m54.947s 4d28m15.258s"


##############################
### def
##############################
def dirty_continuum(
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
	default("tclean")
	tclean(
		vis         = vis,
		imagename   = imagename,
		field       = "",
		specmode    = "mfs",
		restfreq    = "230.53800GHz",
		niter       = 100,
		threshold   = "10mJy",
		interactive = False,
		cell        = cell,
		imsize      = imsize,
		phasecenter = phasecenter,
		weighting   = weighting,
		robust      = robust,
		gridder     = "mosaic",
		deconvolver = "mtmfs",
		usemask     = "pb",
		pbmask      = 0.8,
		restoration = False,
		startmodel  = "",
		pblimit     = 0.5,
		)


##############################
### main
##############################
# concat
print("### concat")
vis_12m = glob.glob(dir_project + this_proj + "/" + this_proj + "_12m.ms")[0]
vis_7m = glob.glob(dir_project + this_proj + "/" + this_proj + "_7m.ms")[0]
vis_12m7m = vis_12m.replace("12m","12m+7m")
os.system("rm -rf " + vis_12m7m)
concat(vis=[vis_12m,vis_7m], concatvis=vis_12m7m)

# 7m-only dirty map
print("### dirty map creation: 7m")
imagename = "image_sim01_7m"
os.system("rm -rf " + imagename + "*")
os.system("rm -rf " + dir_project + this_proj + "/" + imagename + "*")
dirty_continuum(vis_7m, imagename, fov=120, cell="1.0arcsec", phasecenter=phasecenter)
os.system("mv " + imagename + " " + dir_project + this_proj)

# 12m-only dirty map
print("### dirty map creation: 12m")
imagename = "image_sim01_12m"
os.system("rm -rf " + imagename + "*")
os.system("rm -rf " + dir_project + this_proj + "/" + imagename + "*")
dirty_continuum(vis_12m, imagename, fov=120, cell="0.4arcsec", phasecenter=phasecenter)
os.system("mv " + imagename + " " + dir_project + this_proj)

# 12m+7m dirty map
print("### dirty map creation: 12m+7m")
imagename = "image_sim01_12+7m"
os.system("rm -rf " + imagename + "*")
os.system("rm -rf " + dir_project + this_proj + "/" + imagename + "*")
dirty_continuum(vis_12m7m, imagename, fov=120, cell="0.4arcsec", phasecenter=phasecenter)
os.system("mv " + imagename + " " + dir_project + this_proj)

#
os.system("rm -rf *.last")

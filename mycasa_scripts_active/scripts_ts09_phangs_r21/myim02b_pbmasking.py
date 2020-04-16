import os
import glob
import numpy as np
import scripts_phangs_r21 as r21


dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_ready/"


#####################
### Main Procedure
#####################
co10images = glob.glob(dir_data + "ngc*co10*.image")
co21images = glob.glob(dir_data + "ngc*co21*.image")
co10pbmasks = glob.glob(dir_data + "ngc*co10*.pbmask")
co21pbmasks = glob.glob(dir_data + "ngc*co21*.pbmask")

for i in range(len(co10images)):
	beam = co10images[i].split("/")[-1].split("_")[-1].replace(".image","").replace("p",".")
	# combine mask
	combinepbmask = co10pbmasks[i] + ".combined"
	os.system("rm -rf " + combinepbmask + "_tmp")
	immath(
		imagename = [co10pbmasks[i], co21pbmasks[i]],
		expr = "iif( IM0>=1.0, IM1, 0.0)",
		outfile = combinepbmask + "_tmp",
		)
	makemask(mode = "copy",
		inpimage = combinepbmask + "_tmp",
		inpmask = combinepbmask + "_tmp",
		output = combinepbmask + ":mask0",# + "_tmp_mask:mask0",
		overwrite = True)
	# mask images
	os.system("rm -rf " + co10images[i] + ".masked")
	immath(
		imagename = [combinepbmask, co10images[i]],
		expr = "IM0*IM1",
		outfile = co10images[i] + ".masked",
		)
	os.system("rm -rf " + co21images[i] + ".masked")
	immath(
		imagename = [combinepbmask, co21images[i]],
		expr = "iif( IM0>=1.0, IM1, 0.0)",
		outfile = co21images[i] + ".masked",
		)
	# header
	imhead(imagename = co10images[i] + ".masked",
		mode = "del",
		hdkey = "beammajor")
	imhead(imagename = co10images[i] + ".masked",
		mode = "put",
		hdkey = "beammajor",
		hdvalue = beam + "arcsec")
	imhead(imagename = co10images[i] + ".masked",
		mode = "put",
		hdkey = "beamminor",
		hdvalue = beam + "arcsec")
	imhead(imagename = co21images[i] + ".masked",
		mode = "del",
		hdkey = "beammajor")
	imhead(imagename = co21images[i] + ".masked",
		mode = "put",
		hdkey = "beammajor",
		hdvalue = beam + "arcsec")
	imhead(imagename = co21images[i] + ".masked",
		mode = "put",
		hdkey = "beamminor",
		hdvalue = beam + "arcsec")
	# rename
	os.system("rm -rf " + co10images[i])
	os.system("mv " + co10images[i] + ".masked" + " " + co10images[i])
	os.system("rm -rf " + co21images[i])
	os.system("mv " + co21images[i] + ".masked" + " " + co21images[i])
	#
	os.system("rm -rf " + )

os.system("rm -rf *.last")

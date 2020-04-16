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
	# combine mask
	combinepbmask = co10pbmasks + ".combined"
	os.system("rm -rf " + combinepbmask)
	immath(imagename = )
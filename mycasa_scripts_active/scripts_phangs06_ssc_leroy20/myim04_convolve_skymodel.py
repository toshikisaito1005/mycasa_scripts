import os
import sys
import glob
import datetime


##############################
### parameters
##############################
dir_proj = "/Users/saito/data/myproj_active/proj_phangs06_ssc/v3p4_tpeak/"


##############################
### main
##############################
skymodels = glob.glob(dir_proj + "*.skymodel")
skymodels.sort()

for i in range(len(skymodels)):
	galname = skymodels[i].split("/")[-1].split("_")[0]
	dir_gal = dir_proj + "../sim_phangs/sim_" + galname + "/"
	# smooth
	imsmoith(imagename = skymodels[i],
		)

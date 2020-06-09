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
	print("### processing " + galname + " " + str(i) + "/" + str(len(skymodels)))
	dir_gal = dir_proj + "../sim_phangs/sim_" + galname + "/"
	# smooth
	print("# smooth skymodel " + galname)
	outfile = dir_gal + "sim_" + galname + "_skymodel.smooth"
	os.system("rm -rf " + outfile)
	imsmooth(imagename=skymodels[i], targetres=True, major="10.0arcsec", minor="10.0arcsec", pa="0deg", outfile=outfile)
	# smooth
	imagenames = glob.glob(dir_gal + "sim_*.image")
	for j in range(len(imagenames)):
		print("# smooth sim image " + str(j) + " " + galname)
		outfile = imagenames[j].replace(".image",".smooth")
		os.system("rm -rf " + outfile)
		imsmooth(imagename=imagenames[j], targetres=True, major="10.0arcsec", minor="10.0arcsec", pa="0deg", outfile=outfile)

os.system("rm -rf *.last")

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

#for i in range(len(skymodels)):
for i in [26]:
	galname = skymodels[i].split("/")[-1].split("_")[0]
	print("### processing " + galname + " " + str(i) + "/" + str(len(skymodels)))
	dir_gal = dir_proj + "../sim_phangs/sim_" + galname + "/"
	# smooth
	print("# smooth skymodel " + galname)
	outfile = dir_gal + "sim_" + galname + "_skymodel.smooth"
	os.system("rm -rf " + outfile + "*")
	imsmooth(imagename=skymodels[i], targetres=True, major="10.0arcsec", minor="10.0arcsec", pa="0deg", outfile=outfile+"_tmp")
	#
	# cut
	thres = str(imstat(outfile+"_tmp")["max"][0] * 0.01)
	immath(imagename=outfile+"_tmp", expr="iif(IM0>"+thres+",IM0,0.0)", outfile=outfile)
	os.system("rm -rf " + outfile + "_tmp")
	skymodel = outfile
	#
	os.system("rm -rf " + outfile + ".fits")
	exportfits(imagename=outfile, fitsimage=outfile+".fits")
	os.system("rm -rf " + outfile)
	importfits(fitsimage=outfile+".fits", imagename=outfile, defaultaxes=True, defaultaxesvalues=["RA","Dec","Frequency","Stokes"])
	os.system("rm -rf " + outfile + ".fits")
	#
	# smooth
	imagenames = glob.glob(dir_gal + "sim_*.image.pbcor")
	for j in range(len(imagenames)):
		print("# smooth sim image " + str(j) + " " + galname)
		outfile = imagenames[j].replace(".image.pbcor",".smooth")
		os.system("rm -rf " + outfile + "*")
		imsmooth(imagename=imagenames[j], targetres=True, major="10.0arcsec", minor="10.0arcsec", pa="0deg", outfile=outfile+"_tmp")
		#
		done = glob.glob(skymodel.replace(".smooth","_regrid.smooth"))
		if not done:
			imregrid(imagename=skymodel,template=outfile+"_tmp",output=skymodel.replace(".smooth","_regrid.smooth"))
		#
		immath(imagename=[outfile+"_tmp",skymodel.replace(".smooth","_regrid.smooth")], expr="iif(IM1>"+thres+",IM0,0.0)", outfile=outfile)
		os.system("rm -rf " + outfile + "_tmp")

os.system("rm -rf *.last")

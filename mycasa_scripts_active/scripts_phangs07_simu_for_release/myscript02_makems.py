import numpy as np
import os
import glob
import pyfits
import shutil

dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"
image_mocksky = "simulated_sky.fits"
this_proj = "sim01"


##############################
### def
##############################
def run_simobserve(
	array,
	skymodel,
	project,
	totaltime="6h",
	):
	"""
	"""
	print(skymodel)
	if array=="12m":
		antennalist = "alma.cycle5.1.cfg"
		imsize = np.round(21*300/230.53800*2)
		mapsize = [imsize, imsize]
		pointingspacing = np.round(21*300/230.53800/2., 2)
	elif array=="7m":
		antennalist = "aca.cycle5.cfg"
		imsize = np.round(21*300/230.53800*12./7.*2)
		mapsize = [imsize, imsize]
		pointingspacing = np.round(21*300/230.53800*12./7./2., 2)
	#
	default('simobserve')
	simobserve()
	antennalist     = antennalist
	skymodel        = skymodel
	project         = project
	indirection     = ""
	incell          = ""
	mapsize         = mapsize
	incenter        = ""
	inbright        = ""
	setpointings    = True
	integration     = "10s"
	graphics        = "none"
	obsmode         = "int"
	totaltime       = totaltime
	#thermalnoise    = ""
	pointingspacing = pointingspacing
	overwrite       = True
	simobserve()


##############################
### main
##############################
# initialize
os.system("rm -rf " + this_proj)
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
os.system("mv " + this_proj+"_* " + dir_project)

#
os.system("rm -rf *.last")

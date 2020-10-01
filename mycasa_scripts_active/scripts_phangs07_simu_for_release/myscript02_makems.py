import numpy as np
import os
import glob
import pyfits
import shutil

dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"

##############################
### def
##############################
def run_simobserve(
	array,
	skymodel,
	project,
	mapsize=["",""],
	totaltime="6h",
	):
	"""
	"""
	#
	if array=="12m":
		antennalist = "alma.cycle5.1.cfg"
		pointingspacing = str(np.round(21*300/230.53800/2., 2)) + "arcsec"
	elif array=="7m":
		antennalist = "aca.cycle5.cfg"
		pointingspacing = str(np.round(21*300/230.53800*12./7./2., 2)) + "arcsec"
	#
	default("simobserve")
	simobserve(
		antennalist     = antennalist,
		skymodel        = skymodel,
		project         = project,
		indirection     = "",
		incell          = "",
		mapsize         = ["",""],
		incenter        = "",
		inbright        = "",
		setpointings    = True,
		integration     = "10s",
		graphics        = "file",
		obsmode         = "int",
		totaltime       = totaltime,
		#thermalnoise    = "",
		pointingspacing = pointingspacing,
		overwrite       = True,
		)


##############################
### main
##############################
# initialize
os.system("rm -rf " + this_proj)
os.system("rm -rf " + this_proj+"_*m")
os.system("rm -rf " + dir_project + "/" + this_proj)
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
#
os.mkdir(dir_project + this_proj)
ms_12m = glob.glob(this_proj + "_12m/*.ms")[0]
new_ms_12m_name = this_proj + "_12m.ms"
os.system("cp -r " + ms_12m + " " + dir_project + this_proj + "/" + new_ms_12m_name)
#
ms_7m = glob.glob(this_proj + "_7m/*.ms")[0]
new_ms_7m_name = this_proj + "_7m.ms"
os.system("cp -r " + ms_7m + " " + dir_project + this_proj + "/" + new_ms_7m_name)
#
os.system("mv " + this_proj+"_* " + dir_project + this_proj)

#
os.system("rm -rf " + this_proj)
os.system("rm -rf *.last")

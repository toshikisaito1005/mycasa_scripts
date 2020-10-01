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
	totaltime="6h",,
	):
	"""
	"""
	if array=="12m":
		antennalist = "alma.cycle5.1.cfg"
		imsize = np.round(21*300/230.53800*2)
		mapsize = [imsize, imsize]
		
	elif:
		antennalist = "aca.cycle5.cfg"
		imsize = np.round(21*300/230.53800*12./7.*2)
		mapsize = [imsize, imsize]
	#
	default('simobserve')
	antennalist        =  antennalist
	skymodel           =  skymodel
	project            =  project
	indirection        =  ""
	incell             =  ""
	mapsize            =  mapsize
	incenter           =  ""
	inbright           =  ""
	setpointings       =  True
	integration        =  "10s"
	graphics           =  "none"
	obsmode            = "int"
	totaltime          =  totaltime
	#thermalnoise       =  ""
	pointingspacing    =  pointingspacing
	overwrite          =  True
	simobserve()


##############################
### main
##############################
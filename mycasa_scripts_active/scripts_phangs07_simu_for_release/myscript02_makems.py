import numpy as np
import os
import glob
import pyfits
import shutil

dir_project = "/Users/saito/data/myproj_active/proj_phangs07_simu_for_release/"


##############################
### def
##############################
def set_simobserve_param(
	):
	"""
	"""
	default('simobserve')
	antennalist        =  "aca.cycle5.cfg"
	skymodel           =  skymodels[i]
	project            =  dir_this
	indirection        =  ""
	incell             =  ""
	mapsize            =  ["",""]
	incenter           =  ""
	inbright           =  ""
	setpointings       =  True
	integration        =  "10s"
	graphics           =  "none"
	obsmode            = "int"
	totaltime          =  "4h"
	#thermalnoise       =  ""
	pointingspacing    =  "0.4arcmin"
	overwrite          =  True


##############################
### main
##############################
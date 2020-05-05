import os, re, sys, glob
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
plt.ioff()


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"


#####################
### functions
#####################
def function(x, a, b):
	"""
	"""
	return a * x + b


#####################
### Main Procedure
#####################
fits_mom0  = glob.glob(dir_proj)
fits_noise = 
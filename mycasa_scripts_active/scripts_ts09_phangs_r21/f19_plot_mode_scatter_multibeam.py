import os, re, sys, glob
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats
plt.ioff()

#
import scripts_phangs_r21 as r21


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galname = "ngc0628"
freqco10 = 115.27120
freqco21 = 230.53800
percentile = 84

nbins_n0628 = [40, 30, 20, 10, 10]
beams = ["04p0","08p0","12p0","16p0","20p0"]


#####################
### functions
#####################
def get_best_params(
	txtfile,
	):
	"""
	"""
	data = np.loadtxt(txtfile)
	best_params = np.median(data, axis=0)

	return best_params


#####################
### main
#####################
##
txt_n0628_co10 = glob.glob(dir_proj + "eps/bootstrap_co10_models_ngc0628_??p0.txt")
txt_n0628_co21 = glob.glob(dir_proj + "eps/bootstrap_co21_models_ngc0628_??p0.txt")
txt_n3627_co10 = glob.glob(dir_proj + "eps/bootstrap_co10_models_ngc3627_??p0.txt")
txt_n3627_co21 = glob.glob(dir_proj + "eps/bootstrap_co21_models_ngc3627_??p0.txt")
txt_n4321_co10 = glob.glob(dir_proj + "eps/bootstrap_co10_models_ngc4321_??p0.txt")
txt_n4321_co21 = glob.glob(dir_proj + "eps/bootstrap_co21_models_ngc4321_??p0.txt")

##
for i in range(len(nbins_n0628)):
	n0628_best_params = get_best_params(txt_n0628_co10[i])





import os, re, sys, glob
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
plt.ioff()

#
import scripts_phangs_r21 as r21


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

def Jy2Kelvin(
	data,
	beam,
	obsfreq_GHz,
	):
	"""
	"""
    J2K = 1.222e6 / beam / beam / obsfreq_GHz**2
    data = np.array(data) * J2K


#####################
### Main Procedure
#####################
co10_mom0  = dir_proj + "ngc0628_co10/co10_04p0.moment0"
co10_noise = dir_proj + "ngc0628_co10/co10_04p0.moment0.noise"
co21_mom0  = dir_proj + "ngc0628_co21/co21_04p0.moment0"
co21_noise = dir_proj + "ngc0628_co21/co21_04p0.moment0.noise"

# get beam
beamstr = co10_mom0.split("/")[-1].replace(".moment0","").split("_")[-1].replace("p",".")
beamfloat = float(beamstr)
#
# get data
data_co10_mom0  = r21.import_data(co10_mom0, mode="data")
data_co10_noise = r21.import_data(co10_noise, mode="data")
data_co21_mom0  = r21.import_data(co21_mom0, mode="data")
data_co21_noise = r21.import_data(co21_noise, mode="data")
#
# select data
cut_all = np.where((data_co10_mom0>0) & (data_co10_noise>0) & (data_co21_mom0>0) & (data_co21_noise>0))
#
data_co10_mom0 = data_co10_mom0[cut_all]
data_co10_noise = data_co10_noise[cut_all]
data_co21_mom0 = data_co21_mom0[cut_all]
data_co21_noise = data_co21_noise[cut_all]
#
# Jy-to-Kelvin








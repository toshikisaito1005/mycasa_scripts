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
freqco10 = 115.27120
freqco21 = 230.53800


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

	return data


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
data_co10_mom0  = data_co10_mom0[cut_all]
data_co10_noise = data_co10_noise[cut_all]
data_co21_mom0  = data_co21_mom0[cut_all]
data_co21_noise = data_co21_noise[cut_all]
#
# Jy-to-Kelvin
log_co10_mom0_k  = np.log10(Jy2Kelvin(data_co10_mom0, beamfloat, freqco10))
log_co10_noise_k = np.log10(Jy2Kelvin(data_co10_noise, beamfloat, freqco10))
log_co21_mom0_k  = np.log10(Jy2Kelvin(data_co21_mom0, beamfloat, freqco21))
log_co21_noise_k = np.log10(Jy2Kelvin(data_co21_noise, beamfloat, freqco21))

# plot
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=8, ncols=18)
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,10:18])
ax1.grid(axis="both")
ax2.grid(axis="both")
plt.rcParams["font.size"] = 16




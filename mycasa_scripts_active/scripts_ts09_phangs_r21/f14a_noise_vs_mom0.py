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

def getdata(
	co10_mom0,
	co10_noise,
	co21_mom0,
	co21_noise,
	freqco10,
	freqco21,
	):
	"""
	"""
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

	return log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k


#####################
### Main Procedure
#####################
co10_mom0  = dir_proj + "ngc0628_co10/co10_04p0.moment0"
co10_noise = dir_proj + "ngc0628_co10/co10_04p0.moment0.noise"
co21_mom0  = dir_proj + "ngc0628_co21/co21_04p0.moment0"
co21_noise = dir_proj + "ngc0628_co21/co21_04p0.moment0.noise"

log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = \
	getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21)

# print
print("### co10 data properties")
print("# 84% mom-0 = " + str(np.round(np.percentile(10**log_co10_mom0_k,84),2)) + " K.km/s")
print("# median mom-0 = " + str(np.round(np.mean(10**log_co10_mom0_k),2)) + " K.km/s")
print("# 16% mom-0 = " + str(np.round(np.percentile(10**log_co10_mom0_k,	6),2)) + " K.km/s")
print("# mean noise = " + str(np.round(np.mean(10**log_co10_noise_k),2)) + " K.km/s")
#
print("### co21 data properties")
print("# 84% mom-0 = " + str(np.round(np.percentile(10**log_co21_mom0_k,84),2)) + " K.km/s")
print("# median mom-0 = " + str(np.round(np.mean(10**log_co21_mom0_k),2)) + " K.km/s")
print("# 16% mom-0 = " + str(np.round(np.percentile(10**log_co21_mom0_k,	6),2)) + " K.km/s")
print("# mean noise = " + str(np.round(np.mean(10**log_co21_noise_k),2)) + " K.km/s")

# plot
figure = plt.figure(figsize=(10,8))
gs = gridspec.GridSpec(nrows=9, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:4,0:8])
ax2 = plt.subplot(gs[5:9,0:8])
ax1.grid(axis="both")
ax2.grid(axis="both")
ax1.set_xscale("log")
ax2.set_xscale("log")
ax1.set_yscale("log")
ax2.set_yscale("log")
plt.rcParams["font.size"] = 16

# ax1
ax1.scatter(10**log_co10_mom0_k, 10**log_co10_noise_k, c="black", alpha=0.5)

# ax2
ax2.scatter(10**log_co21_mom0_k, 10**log_co21_noise_k, c="black", alpha=0.5)

#
plt.savefig(dir_proj + "eps/fig_noise_vs_mom0.png",dpi=200)

os.system("rm -rf *.last")

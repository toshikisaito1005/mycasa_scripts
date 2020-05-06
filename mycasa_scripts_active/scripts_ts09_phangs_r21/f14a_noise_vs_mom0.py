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
nbins = 40


#####################
### functions
#####################
def function(x, a, b):
	"""
	"""
	return a * x + b

def func_lognorm(x, a, b, c):
    return a*np.exp(-(np.log(x)-b)**2/(2*c**2))

def fit_lognorm(func_lognorm, data_x, data_y, guess):
    """
    fit data with func1
    """
    popt, pcov = curve_fit(func_lognorm,
                           data_x, data_y,
                           p0=guess)
    best_func = func_lognorm(data_x,popt[0],popt[1],popt[2])
    residual = data_y - best_func
                           
    return popt, residual

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

def print_things(
	log_co10_mom0_k,
	log_co10_noise_k,
	log_co21_mom0_k,
	log_co21_noise_k,
	):
	"""
	"""
	p84_co10 = np.round(np.percentile(10**log_co10_mom0_k,84),2)
	p50_co10 = np.round(np.mean(10**log_co10_mom0_k),2)
	p16_co10 = np.round(np.percentile(10**log_co10_mom0_k,16),2)
	p84_co21 = np.round(np.percentile(10**log_co21_mom0_k,84),2)
	p50_co21 = np.round(np.mean(10**log_co21_mom0_k),2)
	p16_co21 = np.round(np.percentile(10**log_co21_mom0_k,16),2)
	# print
	print("### co10 data properties (K.km/s)")
	print("# mom-0 84%    = " + str(p84_co10))
	print("# mom-0 median = " + str(p50_co10))
	print("# mom-0 16%    = " + str(p16_co10))
	print("# noise mean   = " + str(np.round(np.mean(10**log_co10_noise_k),2)))
	#
	print("### co21 data properties (K.km/s)")
	print("# mom-0 84%    = " + str(p84_co21))
	print("# mom-0 median = " + str(p50_co21))
	print("# mom-0 16%    = " + str(p16_co21))
	print("# noise mean   = " + str(np.round(np.mean(10**log_co21_noise_k),2)))

	return p84_co10, p50_co10, p16_co10, p84_co21, p50_co21, p16_co21

def calcbins(
	log_co_mom0_k,
	log_co_noise_k,
	nbins,
	):
	"""
	"""
	xbins = np.linspace(log_co_mom0_k.min(), log_co_mom0_k.max(), nbins)
	list_log_noise_mean = []
	for i in range(len(xbins)-1):
		cut_all = np.where((log_co_mom0_k>xbins[i]) & (log_co_mom0_k<xbins[i+1]))
		noise_cut = 10**log_co_noise_k[cut_all]
		noise_mean = np.round(np.mean(noise_cut),2)
		list_log_noise_mean.append(np.log10(noise_mean))

	xbins = np.delete(xbins + (xbins[1]-xbins[0])/2., -1)

	return xbins, list_log_noise_mean


#####################
### Main Procedure
#####################
###
co10_mom0  = dir_proj + "ngc0628_co10/co10_04p0.moment0"
co10_noise = dir_proj + "ngc0628_co10/co10_04p0.moment0.noise"
co21_mom0  = dir_proj + "ngc0628_co21/co21_04p0.moment0"
co21_noise = dir_proj + "ngc0628_co21/co21_04p0.moment0.noise"
#
log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = \
	getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21)
#
p84_co10, p50_co10, p16_co10, p84_co21, p50_co21, p16_co21 = \
	print_things(log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k)
#

### plot noise vs mom-0
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:4,0:8])
ax2 = plt.subplot(gs[5:9,0:8])
ax1.grid(axis="both")
ax2.grid(axis="both")
ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
ax2.set_xlabel("CO(2-1) mom-0 (K.km/s)")
ax1.set_ylabel("CO(1-0) mom-0 noise (K.km/s)")
ax2.set_ylabel("CO(2-1) mom-0 noise (K.km/s)")
plt.rcParams["font.size"] = 16

# ax1
ax1.scatter(log_co10_mom0_k, log_co10_noise_k, c="black", alpha=0.5)
xbins_co10, list_log_noise_co10_mean = calcbins(log_co10_mom0_k, log_co10_noise_k, nbins)
ax1.scatter(xbins_co10, list_log_noise_co10_mean, c="red", alpha=1.0, s=70)
np.savetxt(dir_proj + "eps/ngc0628_4p0_lognoise_co10_bin.txt", np.array(np.c_[xbins_co10, list_log_noise_co10_mean]), fmt="%.3f")

# ax2
ax2.scatter(log_co21_mom0_k, log_co21_noise_k, c="black", alpha=0.5)
xbins_co21, list_log_noise_co21_mean = calcbins(log_co21_mom0_k, log_co21_noise_k, nbins)
ax2.scatter(xbins_co21, list_log_noise_co21_mean, c="red", alpha=1.0, s=70)
np.savetxt(dir_proj + "eps/ngc0628_4p0_lognoise_co21_bin.txt", np.array(np.c_[xbins_co21, list_log_noise_co21_mean]), fmt="%.3f")

#
plt.savefig(dir_proj + "eps/fig_noise_vs_mom0.png",dpi=200)


### model co10 mom-0 distribution
#
data_histo = np.histogram(log_co10_mom0_k, bins=nbins, range=range_co10_input)

popt, residual = fit_lognorm(func_lognorm, data_histo[0], np.delete(data_histo[1],-1), [0.5,0.5,0.5])
mu, sigma = popt[1], popt[2]
mean_lognorm = np.exp(mu + (sigma**2)/2.)


### plot obs and model mom-0
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:4,0:8])
ax2 = plt.subplot(gs[5:9,0:8])
ax1.grid(axis="both")
ax2.grid(axis="both")
ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
ax2.set_xlabel("CO(2-1) mom-0 (K.km/s)")
plt.rcParams["font.size"] = 16

# ax1
#ax1.hist(log_co10_mom0_k, color="black", alpha=0.5, bins=nbins, range=range_co10_input, lw=0)
#ax1.hist(co10_mom0_k_model, color="red", alpha=0.5, bins=nbins, lw=0, range=range_co10_input)
ax1.plot(data_histo[0], func_lognorm(data_histo[0],*popt), lw=6, alpha=0.5)
#
ax1.set_xlim(range_co10_input)
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_mom0.png",dpi=200)
#
os.system("rm -rf *.last")

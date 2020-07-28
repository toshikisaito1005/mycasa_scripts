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
nbins = [40, 30, 20, 10, 10]
percentile = 84

beams = ["04p0","08p0","12p0","16p0","20p0"]


#####################
### functions
#####################
def weighted_percentile(
    data,
    percentile,
    weights=None,
    ):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    if weights==None:
        w_median = np.percentile(data,percentile*100)
    else:
        data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
        s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
        midpoint = percentile * sum(s_weights)
        if any(weights > midpoint):
            w_median = (data[weights == np.max(weights)])[0]
        else:
            cs_weights = np.cumsum(s_weights)
            idx = np.where(cs_weights <= midpoint)[0][-1]
            if cs_weights[idx] == midpoint:
                w_median = np.mean(s_data[idx:idx+2])
            else:
                w_median = s_data[idx+1]

    return w_median

def get_binned_dist(x,y,binrange):
	"""
	"""
	n, _ = np.histogram(x, bins=10, range=binrange)
	sy, _ = np.histogram(x, bins=10, range=binrange, weights=y)
	sy2, _ = np.histogram(x, bins=10, range=binrange, weights=y*y)
	mean = sy / n
	std = np.sqrt(sy2/n - mean*mean)
	binx = (_[1:] + _[:-1])/2

	return binx, mean, std

def func1(x, a, b, c):
	"""
	"""
	return a * np.exp(-(x-b)**2 / (2*c**2))

def func_co10_vs_co21(x, a, b):
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
	percentile,
	):
	"""
	"""
	xbins = np.linspace(log_co_mom0_k.min(), log_co_mom0_k.max(), nbins)
	list_log_noise_mean = []
	for i in range(len(xbins)-1):
		cut_all = np.where((log_co_mom0_k>xbins[i]) & (log_co_mom0_k<xbins[i+1]))
		noise_cut = 10**log_co_noise_k[cut_all]
		noise_mean = np.round(np.percentile(noise_cut,percentile),2)
		list_log_noise_mean.append(np.log10(noise_mean))

	xbins = np.delete(xbins, -1) # np.delete(xbins + (xbins[1]-xbins[0])/2., -1)

	return xbins, list_log_noise_mean

def plotter_noise(
	dir_proj,
	log_co10_mom0_k,
	log_co10_noise_k,
	log_co21_mom0_k,
	log_co21_noise_k,
	nbins,
	percentile,
	galname,
	):
	"""
	"""
	# preparation
	figure = plt.figure(figsize=(10,10))
	gs = gridspec.GridSpec(nrows=9, ncols=8)
	plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
	ax1 = plt.subplot(gs[0:4,0:8])
	ax2 = plt.subplot(gs[5:9,0:8])
	ax1.grid(axis="both")
	ax2.grid(axis="both")
	ax1.set_xlim([0.3,1.7])
	ax2.set_xlim([-0.4,1.7])
	ax1.set_xlabel("log $I_{CO(1-0)}$ (K km s$^{-1}$)")
	ax2.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
	ax1.set_ylabel("log 1 sigma error (K km s$^{-1}$)")
	ax2.set_ylabel("log 1 sigma error (K km s$^{-1}$)")
	plt.rcParams["font.size"] = 20
	plt.rcParams["legend.fontsize"] = 16
	#
	# ax1
	ax1.scatter(log_co10_mom0_k, log_co10_noise_k, c="black", alpha=0.5)
	xbins_co10, list_log_noise_co10_mean = calcbins(log_co10_mom0_k, log_co10_noise_k, nbins, percentile)
	ax1.scatter(xbins_co10, list_log_noise_co10_mean, c="red", alpha=1.0, s=70)
	#np.savetxt(dir_proj + "eps/ngc0628_4p0_lognoise_co10_bin.txt", np.array(np.c_[xbins_co10, list_log_noise_co10_mean]), fmt="%.3f")
	#
	# ax2
	ax2.scatter(log_co21_mom0_k, log_co21_noise_k, c="black", alpha=0.5)
	xbins_co21, list_log_noise_co21_mean = calcbins(log_co21_mom0_k, log_co21_noise_k, nbins, percentile)
	ax2.scatter(xbins_co21, list_log_noise_co21_mean, c="red", alpha=1.0, s=70)
	#np.savetxt(dir_proj + "eps/ngc0628_4p0_lognoise_co21_bin.txt", np.array(np.c_[xbins_co21, list_log_noise_co21_mean]), fmt="%.3f")
	#
	#
	plt.savefig(dir_proj + "eps/fig_noise_vs_mom0_"+galname+".png",dpi=200)

	return xbins_co10, xbins_co21

def add_scatter(
	data_log,
	sigma,
	):
	"""
	"""
	# create noise
	num_data = len(data_log)
	data_log_w_noise = np.log10(10**data_log + np.random.normal(0.0, sigma, num_data))

	return np.array(data_log_w_noise)

def add_noise(
	best_lognorm_co10,
	log_co10_noise_k,
	xbins_co10,
	best_lognorm_co21,
	log_co21_noise_k,
	xbins_co21,
	):
	"""
	"""
	list_output_co10 = []
	list_output_co21 = []
	for i in range(len(xbins_co10)):
		for j in range(len(xbins_co21)):
			# create binned data
			if i<=len(xbins_co10)-2:
				if j<=len(xbins_co10)-2:
					cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co10<xbins_co10[i+1]) & (best_lognorm_co21>=xbins_co21[j]) & (best_lognorm_co21<xbins_co21[j+1]))
				else:
					cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co10<xbins_co10[i+1]) & (best_lognorm_co21>=xbins_co21[j]))
			else:
				if j<len(xbins_co10)-2:
					cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co21>=xbins_co21[j]) & (best_lognorm_co21<xbins_co21[j+1]))
				else:
					cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co21>=xbins_co21[j]))
			#
			binned_co10_data = best_lognorm_co10[cut_all]
			num_co10_data = len(binned_co10_data)
			#
			binned_co21_data = best_lognorm_co21[cut_all]
			num_co21_data = len(binned_co21_data)
			# create noise
			binned_co10_data_and_noise = np.log10(10**binned_co10_data + np.random.normal(0.0, 10**log_co10_noise_k[i], num_co10_data))
			list_output_co10.extend(binned_co10_data_and_noise)
			#
			binned_co21_data_and_noise = np.log10(10**binned_co21_data + np.random.normal(0.0, 10**log_co21_noise_k[i], num_co21_data))
			list_output_co21.extend(binned_co21_data_and_noise)

	return np.array(list_output_co10), np.array(list_output_co21)

def create_best_models(
	log_co10_mom0_k,
	log_co21_mom0_k,
	log_co10_noise_k,
	log_co21_noise_k,
	xbins_co10,
	xbins_co21,
	best_co10_parameter,
	best_co21_parameter,
	):
	### co10 parameters
	co10_mean        = best_co10_parameter[0]
	co10_disp        = best_co10_parameter[1]
	co10_scatter     = best_co10_parameter[2]
	range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
	num_co10         = len(log_co10_mom0_k)
	#
	### co21 parameters
	co21_slope       = best_co21_parameter[0]
	co21_intercept   = best_co21_parameter[1]
	co21_scatter     = best_co21_parameter[2]
	range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
	num_co21         = len(log_co21_mom0_k)
	#
	### log_co_mom0_k_model
	log_co10_mom0_k_model = np.random.normal(co10_mean, co10_disp, num_co10)
	log_co10_mom0_k_model.sort()
	#
	log_co21_mom0_k_model = func_co10_vs_co21(log_co10_mom0_k_model, co21_slope, co21_intercept)
	#
	### log_co_mom0_k_model_scatter
	# add scatter
	log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, co10_scatter)
	log_co21_mom0_k_model_scatter = add_scatter(log_co21_mom0_k_model, co21_scatter)
	print("### co10_best_model_scatter mean = " + str(np.mean(log_co10_mom0_k_model_scatter)))
	print("### co21_best_model_scatter mean = " + str(np.mean(log_co21_mom0_k_model_scatter)))
	#
	# cut
	log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = 100
	log_co21_mom0_k_model_scatter[np.isnan(log_co21_mom0_k_model_scatter)] = 100
	cut = np.where((log_co10_mom0_k_model_scatter<100) & (log_co21_mom0_k_model_scatter<100))
	log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
	log_co21_mom0_k_model_scatter = log_co21_mom0_k_model_scatter[cut]
	#
	### log_co_mom0_k_model_scatter_noise
	log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model_scatter_noise = \
		add_noise(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10, log_co21_mom0_k_model_scatter, log_co21_noise_k, xbins_co21)
	#
	### cut
	#cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0])) # & (log_co21_mom0_k_model_scatter>range_co21_input[0]))
	#log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
	#log_co21_mom0_k_model_scatter = log_co21_mom0_k_model_scatter[cut]
	#
	#cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]) & (log_co21_mom0_k_model_scatter_noise>range_co21_input[0]) & (log_co21_mom0_k_model_scatter_noise<range_co21_input[1]))
	#log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]
	#log_co21_mom0_k_model_scatter_noise = log_co21_mom0_k_model_scatter_noise[cut]
	#
	### print
	print("### co10_best_model mean = " + str(np.mean(log_co10_mom0_k_model)))
	print("### co10_best_model_scatter mean = " + str(np.mean(log_co10_mom0_k_model_scatter)))
	print("### co10_best_model_scatter_noise mean = " + str(np.mean(log_co10_mom0_k_model_scatter_noise)))

	return log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise


#####################
### main
#####################
list_range_co10_input = []
list_range_co21_input = []
list_log_co10_mom0_k_model_scatter_cut = []
list_log_co21_mom0_k_model_scatter_cut = []
list_log_co10_mom0_k_model_scatter_noise = []
list_log_co21_mom0_k_model_scatter_noise = []
list_log_co10_mom0_k_model_scatter_noise_cut = []
list_log_co21_mom0_k_model_scatter_noise_cut = []
list_log_r21_mom_k = []
list_log_r21_mom0_k_model_scatter = []
list_log_r21_mom0_k_model_scatter_noise = []
for i in range(len(beams)):
	### get best fit values
	nbin = nbins[i]
	dataco10 = np.loadtxt(dir_proj + "eps/bootstrap_co10_models_"+galname+"_"+beams[i]+".txt")
	dataco21 = np.loadtxt(dir_proj + "eps/bootstrap_co21_models_"+galname+"_"+beams[i]+".txt")
	best_co10_parameter = np.median(dataco10, axis=0)
	best_co21_parameter = np.median(dataco21, axis=0)

	### print parameters
	print("### co10 norm mean     = " + str(np.round(np.percentile(dataco10, 16, axis=0)[0], 3)) + ", " + str(np.round(np.percentile(dataco10, 50, axis=0)[0], 3)) + ", " + str(np.round(np.percentile(dataco10, 84, axis=0)[0], 3)))
	print("### co10 norm std      = " + str(np.round(np.percentile(dataco10, 16, axis=0)[1], 3)) + ", " + str(np.round(np.percentile(dataco10, 50, axis=0)[1], 3)) + ", " + str(np.round(np.percentile(dataco10, 84, axis=0)[1], 3)))
	print("### co10 scatter       = " + str(np.round(np.percentile(dataco10, 16, axis=0)[2], 3)) + ", " + str(np.round(np.percentile(dataco10, 50, axis=0)[2], 3)) + ", " + str(np.round(np.percentile(dataco10, 84, axis=0)[2], 3)))
	print("### co21-co10 slope    = " + str(np.round(np.percentile(dataco21, 16, axis=0)[0], 3)) + ", " + str(np.round(np.percentile(dataco21, 50, axis=0)[0], 3)) + ", " + str(np.round(np.percentile(dataco21, 84, axis=0)[0], 3)))
	print("### co21-co10 intecept = " + str(np.round(np.percentile(dataco21, 16, axis=0)[1], 3)) + ", " + str(np.round(np.percentile(dataco21, 50, axis=0)[1], 3)) + ", " + str(np.round(np.percentile(dataco21, 84, axis=0)[1], 3)))
	print("### co21 scatter       = " + str(np.round(np.percentile(dataco21, 16, axis=0)[2], 3)) + ", " + str(np.round(np.percentile(dataco21, 50, axis=0)[2], 3)) + ", " + str(np.round(np.percentile(dataco21, 84, axis=0)[2], 3)))


	### get filenames
	this_beam = beams[i]
	co10_mom0  = dir_proj + galname + "_co10/co10_"+this_beam+".moment0"
	co10_noise = dir_proj + galname + "_co10/co10_"+this_beam+".moment0.noise"
	co21_mom0  = dir_proj + galname + "_co21/co21_"+this_beam+".moment0"
	co21_noise = dir_proj + galname + "_co21/co21_"+this_beam+".moment0.noise"


	### plot noise vs. mom-0
	log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21)
	p84_co10, p50_co10, p16_co10, p84_co21, p50_co21, p16_co21 = print_things(log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k)
	xbins_co10, xbins_co21 = plotter_noise(dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbin, percentile, galname)


	### create best models
	log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise = \
		create_best_models(log_co10_mom0_k, log_co21_mom0_k, log_co10_noise_k, log_co21_noise_k, xbins_co10, xbins_co21, best_co10_parameter, best_co21_parameter)

	### cut data
	range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
	range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
	log_co10_mom0_k_model_scatter_cut = log_co10_mom0_k_model_scatter[np.where((log_co10_mom0_k_model_scatter>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter<=range_co21_input[1]))]
	log_co21_mom0_k_model_scatter_cut = log_co21_mom0_k_model_scatter[np.where((log_co10_mom0_k_model_scatter>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter<=range_co21_input[1]))]
	log_co10_mom0_k_model_scatter_noise_cut = log_co10_mom0_k_model_scatter_noise[np.where((log_co10_mom0_k_model_scatter_noise>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter_noise>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter_noise<=range_co21_input[1]))]
	log_co21_mom0_k_model_scatter_noise_cut = log_co21_mom0_k_model_scatter_noise[np.where((log_co10_mom0_k_model_scatter_noise>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter_noise>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter_noise<=range_co21_input[1]))]
	log_r21_mom_k = np.log10(10**log_co21_mom0_k/10**log_co10_mom0_k)
	log_r21_mom0_k_model_scatter = np.log10(10**log_co21_mom0_k_model_scatter_cut/10**log_co10_mom0_k_model_scatter_cut)
	log_r21_mom0_k_model_scatter_noise = np.log10(10**log_co21_mom0_k_model_scatter_noise_cut/10**log_co10_mom0_k_model_scatter_noise_cut)
	#
	list_range_co10_input.append(range_co10_input)
	list_range_co21_input.append(range_co21_input)
	list_log_co10_mom0_k_model_scatter_cut.append(log_co10_mom0_k_model_scatter_cut.tolist())
	list_log_co21_mom0_k_model_scatter_cut.append(log_co21_mom0_k_model_scatter_cut.tolist())
	list_log_co10_mom0_k_model_scatter_noise_cut.append(log_co10_mom0_k_model_scatter_noise_cut.tolist())
	list_log_co21_mom0_k_model_scatter_noise_cut.append(log_co21_mom0_k_model_scatter_noise_cut.tolist())
	list_log_co10_mom0_k_model_scatter_noise.append(log_co10_mom0_k_model_scatter_noise.tolist())
	list_log_co21_mom0_k_model_scatter_noise.append(log_co21_mom0_k_model_scatter_noise.tolist())
	list_log_r21_mom_k.append(log_r21_mom_k.tolist())
	list_log_r21_mom0_k_model_scatter.append(log_r21_mom0_k_model_scatter.tolist())
	list_log_r21_mom0_k_model_scatter_noise.append(log_r21_mom0_k_model_scatter_noise.tolist())


list_log_r21_mom0_k_model_scatter_noise_nocut = []
for i in range(len(list_log_co21_mom0_k_model_scatter_noise)):
	log_r21_mom0_k_model_scatter_noise_nocut = np.log10(10**np.array(list_log_co21_mom0_k_model_scatter_noise[i])/10**np.array(list_log_co10_mom0_k_model_scatter_noise[i]))
	list_log_r21_mom0_k_model_scatter_noise_nocut.append(log_r21_mom0_k_model_scatter_noise_nocut)


#
list_median_nocut = [10**np.median(s) for s in list_log_r21_mom0_k_model_scatter_noise_nocut]
list_width_nocut = [10**np.percentile(s,84)-10**np.percentile(s,16) for s in list_log_r21_mom0_k_model_scatter_noise_nocut]
list_median_wco10_nocut = []
list_width_wco10_nocut = []
list_median_wco21_nocut = []
list_width_wco21_nocut = []
for i in range(len(list_log_r21_mom0_k_model_scatter_noise_nocut)):
	list_median_wco10_nocut.append(weighted_percentile(10**list_log_r21_mom0_k_model_scatter_noise_nocut[i], 0.50, 10**np.array(list_log_co10_mom0_k_model_scatter_noise[i])))
	list_p16_wco10_nocut.append(weighted_percentile(10**list_log_r21_mom0_k_model_scatter_noise_nocut[i], 0.16, 10**np.array(list_log_co10_mom0_k_model_scatter_noise[i])))
	list_p84_wco10_nocut.append(weighted_percentile(10**list_log_r21_mom0_k_model_scatter_noise_nocut[i], 0.84, 10**np.array(list_log_co10_mom0_k_model_scatter_noise[i])))
	list_median_wco21_nocut.append(weighted_percentile(10**list_log_r21_mom0_k_model_scatter_noise_nocut[i], 0.50, 10**np.array(list_log_co21_mom0_k_model_scatter_noise[i])))
	list_p16_wco21_nocut.append(weighted_percentile(10**list_log_r21_mom0_k_model_scatter_noise_nocut[i], 0.16, 10**np.array(list_log_co21_mom0_k_model_scatter_noise[i])))
	list_p84_wco21_nocut.append(weighted_percentile(10**list_log_r21_mom0_k_model_scatter_noise_nocut[i], 0.84, 10**np.array(list_log_co21_mom0_k_model_scatter_noise[i])))




#
os.system("rm -rf *.last")

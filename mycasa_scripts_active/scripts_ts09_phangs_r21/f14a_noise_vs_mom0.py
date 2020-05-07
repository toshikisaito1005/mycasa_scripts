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
nbins = 40
percentile = 84


#####################
### functions
#####################
def func1(x, a, b, c):
	"""
	"""
	return a * np.exp(-(x-b)**2 / (2*c**2))

def func2(x, a1, b1, c1, a2, b2, c2):
	"""
	"""
	return a1 * np.exp(-(x-b1)**2/(2*c1**2)) + a2 * np.exp(-(x-b2)**2/(2*c2**2))

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
	ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
	ax2.set_xlabel("CO(2-1) mom-0 (K.km/s)")
	ax1.set_ylabel("CO(1-0) mom-0 noise (K.km/s)")
	ax2.set_ylabel("CO(2-1) mom-0 noise (K.km/s)")
	plt.rcParams["font.size"] = 16
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
	plt.savefig(dir_proj + "eps/fig_noise_vs_mom0.png",dpi=200)

	return xbins_co10, xbins_co21

def fit_func1(func1, data_x, data_y, guess):
    """
    """
    popt, pcov = curve_fit(func1,
                           data_x, data_y,
                           p0=guess)
    best_func = func1(data_x,popt[0],popt[1],popt[2])
    residual = data_y - best_func
                           
    return popt, residual

def fit_func2(func1, data_x, data_y, guess):
    """
    """
    popt, pcov = curve_fit(func2,
                           data_x, data_y,
                           p0=guess)
    best_func = func2(data_x,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
    residual = data_y - best_func
                           
    return popt, residual

def fit_norm(
	data,
	histrange,
	nbins,
	weights=None,
	):
	"""
	"""
	histo = np.histogram(data, range=histrange, bins=nbins, weights=weights)
	x, y = np.delete(histo[1],-1), histo[0]
	y = y/float(sum(y))
	popt, residual = fit_func1(func1, x, y, [0.05,0.74,0.26])

	return popt

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

def add_noise_co10(
	best_lognorm_co10,
	log_co10_noise_k,
	xbins_co10,
	):
	"""
	"""
	list_output_co10 = []
	for i in range(len(xbins_co10)):
			# create binned data
			if i<=37:
				cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co10<xbins_co10[i+1]))
			else:
				cut_all = np.where((best_lognorm_co10>=xbins_co10[i]))
			#
			binned_co10_data = best_lognorm_co10[cut_all]
			num_co10_data = len(binned_co10_data)
			# create noise
			binned_co10_data_and_noise = np.log10(10**binned_co10_data + np.random.normal(0.0, 10**log_co10_noise_k[i], num_co10_data))
			list_output_co10.extend(binned_co10_data_and_noise)

	return np.array(list_output_co10)

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
			if i<=37:
				if j<=37:
					cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co10<xbins_co10[i+1]) & (best_lognorm_co21>=xbins_co21[j]) & (best_lognorm_co21<xbins_co21[j+1]))
				else:
					cut_all = np.where((best_lognorm_co10>=xbins_co10[i]) & (best_lognorm_co10<xbins_co10[i+1]) & (best_lognorm_co21>=xbins_co21[j]))
			else:
				if j<37:
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

def create_best_co10_model(
	log_co10_mom0_k,
	log_co10_noise_k,
	xbins_co10,
	nbins,
	best_parameters=None,
	):
	# prepare
	range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
	num_co10 = len(log_co10_mom0_k)
	popt = fit_norm(log_co10_mom0_k, range_co10_input, nbins)
	#
	range_popt1   = np.linspace(-0.2, 0.2, 21)
	range_popt2   = np.linspace(-0.2, 0.2, 21)
	range_scatter = np.linspace(-0.2, 0.2, 21)
	#
	list_popt1 = []
	list_popt2 = []
	list_scatter = []
	list_d = []
	list_p = []
	list_output = []
	numiter = 0
	numall = 21*21*21
	if best_parameters==None:
		for i, j, k in itertools.product(range_popt1, range_popt2, range_scatter):
			numiter += 1
			print("### create co10 model " + str(numiter).zfill(4) + "/" + str(numall))
			#
			log_co10_mom0_k_model = np.random.normal(popt[1]+i, popt[2]+j, num_co10)
			#
			log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, 1.0+k)
			log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = -9999
			cut = np.where((log_co10_mom0_k_model_scatter>-9000))
			log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
			#
			log_co10_mom0_k_model_scatter_noise = add_noise_co10(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10)
			#
			cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0]) & (log_co10_mom0_k_model_scatter<range_co10_input[1]))
			log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
			#
			cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]))
			log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]
			d, p = stats.ks_2samp(log_co10_mom0_k, log_co10_mom0_k_model_scatter)
			#
			list_popt1.append(i)
			list_popt2.append(j)
			list_scatter.append(k)
			list_d.append(d)
			list_p.append(p)
			#
		list_output = np.c_[list_popt1, list_popt2, list_scatter, list_d, list_p]
		best_parameter = list_output[np.argmin(list_output[:,3])]
		#
		return best_parameter
	else:
		#
		print("### create best co10 model")
		#
		best_mean = best_co10_parameter[0]
		best_disp = best_co10_parameter[1]
		best_scatter = best_co10_parameter[2]
		#
		log_co10_mom0_k_model = np.random.normal(popt[1]+best_mean, popt[2]+best_disp, num_co10)
		log_co10_mom0_k_model.sort()
		#
		log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, 1.0+best_scatter)
		log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = -9999
		cut = np.where((log_co10_mom0_k_model_scatter>-9000))
		log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
		#
		log_co10_mom0_k_model_scatter_noise = add_noise_co10(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10)
		#
		cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0]) & (log_co10_mom0_k_model_scatter<range_co10_input[1]))
		log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
		#
		cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]))
		log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]

		return log_co10_mom0_k_model, log_co10_mom0_k_model_scatter_noise

def create_best_co21_model(
	log_co21_mom0_k,
	log_co21_noise_k,
	xbins_co21,
	nbins,
	best_parameters=None,
	):
	# prepare
	range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
	num_co21 = len(log_co21_mom0_k)
	#
	range_slope   = np.linspace(-0.2, 0.2, 21)
	range_intercept   = np.linspace(-0.3, 0.3, 21)
	#
	list_popt1 = []
	list_popt2 = []
	list_scatter = []
	list_d = []
	list_p = []
	list_output = []
	numiter = 0
	numall = 21*21*21
	if best_parameters==None:
		for i, j, k in itertools.product(range_popt1, range_popt2, range_scatter):
			numiter += 1
			print("### create co10 model " + str(numiter).zfill(4) + "/" + str(numall))
			#
			log_co10_mom0_k_model = np.random.normal(popt[1]+i, popt[2]+j, num_co10)
			#
			log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, 1.0+k)
			log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = -9999
			cut = np.where((log_co10_mom0_k_model_scatter>-9000))
			log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
			#
			log_co10_mom0_k_model_scatter_noise = add_noise_co10(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10)
			#
			cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0]) & (log_co10_mom0_k_model_scatter<range_co10_input[1]))
			log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
			#
			cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]))
			log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]
			d, p = stats.ks_2samp(log_co10_mom0_k, log_co10_mom0_k_model_scatter)
			#
			list_popt1.append(i)
			list_popt2.append(j)
			list_scatter.append(k)
			list_d.append(d)
			list_p.append(p)
			#
		list_output = np.c_[list_popt1, list_popt2, list_scatter, list_d, list_p]
		best_parameter = list_output[np.argmin(list_output[:,3])]
		#
		return best_parameter
	else:
		#
		print("### create best co10 model")
		#
		best_mean = best_co10_parameter[0]
		best_disp = best_co10_parameter[1]
		best_scatter = best_co10_parameter[2]
		#
		log_co10_mom0_k_model = np.random.normal(popt[1]+best_mean, popt[2]+best_disp, num_co10)
		log_co10_mom0_k_model.sort()
		#
		log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, 1.0+best_scatter)
		log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = -9999
		cut = np.where((log_co10_mom0_k_model_scatter>-9000))
		log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
		#
		log_co10_mom0_k_model_scatter_noise = add_noise_co10(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10)
		#
		cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0]) & (log_co10_mom0_k_model_scatter<range_co10_input[1]))
		log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
		#
		cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]))
		log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]

		return log_co10_mom0_k_model, log_co10_mom0_k_model_scatter_noise


#####################
### plot noise
#####################
### get filenames
co10_mom0  = dir_proj + galname + "_co10/co10_04p0.moment0"
co10_noise = dir_proj + galname + "_co10/co10_04p0.moment0.noise"
co21_mom0  = dir_proj + galname + "_co21/co21_04p0.moment0"
co21_noise = dir_proj + galname + "_co21/co21_04p0.moment0.noise"
#
### plot noise vs. mom-0
log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21)
p84_co10, p50_co10, p16_co10, p84_co21, p50_co21, p16_co21 = print_things(log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k)
xbins_co10, xbins_co21 = plotter_noise( dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbins, percentile)


#####################
### modeling
#####################
### create best co10 distribution
best_co10_parameter = create_best_co10_model(log_co10_mom0_k, log_co10_noise_k, xbins_co10, nbins)
log_co10_mom0_k_model, log_co10_mom0_k_model_scatter_noise = create_best_co10_model(log_co10_mom0_k, log_co10_noise_k, xbins_co10, nbins, best_co10_parameter)
#
### create best co21 distribution
log_co21_mom0_k_model = func_co10_vs_co21(log_co10_mom0_k_model, 1.27, -0.5)


"""
### model co10 mom-0 distribution
## define plot range
range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
#
## create log co10 vs log co21 scaling relation with log-normal intensity distributions
# create co10 model lognormal distribution
num_co10 = len(log_co10_mom0_k)
popt = fit_norm(log_co10_mom0_k, range_co10_input, nbins)
log_co10_mom0_k_model = np.random.normal(popt[1], popt[2], num_co10)
#log_co10_mom0_k_model = log_co10_mom0_k * 1.0
log_co10_mom0_k_model.sort()
#
# create co10 model lognormal distribution
log_co21_mom0_k_model = func_co10_vs_co21(log_co10_mom0_k_model, 1.27, -0.5)#-0.7)
#
## adding scatter
# add
log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, 1.1)
log_co21_mom0_k_model_scatter = add_scatter(log_co21_mom0_k_model, 1.1)
# cut
log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = -9999
log_co21_mom0_k_model_scatter[np.isnan(log_co21_mom0_k_model_scatter)] = -9999
cut = np.where((log_co10_mom0_k_model_scatter>-9000) & (log_co21_mom0_k_model_scatter>-9000))
#
## adding noise
log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model_scatter_noise = \
	add_noise(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10, log_co21_mom0_k_model_scatter, log_co21_noise_k, xbins_co21)

## cut
#
cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0]) & (log_co21_mom0_k_model_scatter>range_co21_input[0]))
log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
log_co21_mom0_k_model_scatter = log_co21_mom0_k_model_scatter[cut]
#
cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co21_mom0_k_model_scatter_noise>range_co21_input[0]))
log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]
log_co21_mom0_k_model_scatter_noise = log_co21_mom0_k_model_scatter_noise[cut]
"""


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
ax1.hist(log_co10_mom0_k, normed=True, color="black", alpha=0.3, bins=nbins, lw=0, range=range_co10_input)
ax1.hist(log_co10_mom0_k_model_scatter_noise, normed=True, color="red", alpha=0.3, bins=nbins, lw=0, range=range_co10_input)
ax1.set_xlim([0,3.0])
#
#ax2
# ax1
ax2.hist(log_co21_mom0_k, normed=True, color="black", alpha=0.5, bins=nbins, lw=0, range=range_co21_input)
ax2.hist(log_co21_mom0_k_model, normed=True, color="blue", alpha=0.3, bins=nbins, lw=0, range=range_co21_input)
#ax2.hist(log_co21_mom0_k_model_scatter, normed=True, color="green", alpha=0.3, bins=nbins, lw=0, range=range_co21_input)
#ax2.hist(log_co21_mom0_k_model_scatter_noise, normed=True, color="red", alpha=0.3, bins=nbins, lw=0, range=range_co21_input)
ax2.set_xlim([-0.5,2.6])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_histo.png",dpi=200)



"""
### plot obs and model mom-0
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
plt.rcParams["font.size"] = 16

# ax1
ax1.plot(log_co10_mom0_k_model, log_co21_mom0_k_model, "o", color="black", alpha=1.0, markersize=3, markeredgewidth=0, zorder=1e22)
ax1.plot(log_co10_mom0_k_model_scatter, log_co21_mom0_k_model_scatter, "o", color="blue", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e20, label="scatter")
ax1.plot(log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model_scatter_noise, "o", color="red", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e18, label="scatter and noise")
ax1.plot(log_co10_mom0_k, log_co21_mom0_k, "o", color="grey", alpha=1.0, markersize=10, markeredgewidth=0)
ax1.plot([-0.5,3.0], [-0.5,3.0], "k--", lw=5)
ax1.set_xlim([-0.5,2.0])
ax1.set_ylim([-0.5,2.0])
#
ax1.legend()
plt.savefig(dir_proj + "eps/fig_obs_vs_model_mom0.png",dpi=200)
#

### plot obs and model mom-0
#
r21 = np.log10(10**log_co21_mom0_k/10**log_co10_mom0_k)
r21_model = np.log10(10**log_co21_mom0_k_model/10**log_co10_mom0_k_model)
r21_model_scatter = np.log10(10**log_co21_mom0_k_model_scatter/10**log_co10_mom0_k_model_scatter)
r21_model_scatter_noise = np.log10(10**log_co21_mom0_k_model_scatter_noise/10**log_co10_mom0_k_model_scatter_noise)
#
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
plt.rcParams["font.size"] = 16

# ax1
ax1.plot(log_co21_mom0_k_model, r21_model, "o", color="black", alpha=1.0, markersize=3, markeredgewidth=0, zorder=1e22)
ax1.plot(log_co21_mom0_k_model_scatter, r21_model_scatter, "o", color="blue", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e20, label="scatter")
ax1.plot(log_co21_mom0_k_model_scatter_noise, r21_model_scatter_noise, "o", color="red", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e18, label="scatter and noise")
ax1.plot(log_co21_mom0_k, r21, "o", color="grey", alpha=1.0, markersize=10, markeredgewidth=0)
ax1.set_xlim([-0.5,2.0])
ax1.set_ylim([-1.2,0.5])
#
ax1.legend()
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21.png",dpi=200)
#
"""

#
os.system("rm -rf *.last")

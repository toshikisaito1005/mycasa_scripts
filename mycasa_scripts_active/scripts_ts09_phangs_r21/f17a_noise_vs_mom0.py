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
i = 0
freqco10 = 115.27120
freqco21 = 230.53800
nbins = 40
percentile = 84
scales = [44/1.0, 52/1.3, 103/1.4]
cnt_ras = [24.174, 170.063, 185.729]
cnt_decs = [15.783, 12.9914, 15.8223]
pas = [180-21.1, 180-172.4, 180-157.8]
incs = [90-8.7, 90-56.2, 90-35.1]
def_nucleus = [50*44./1.0, 50*52./1.3*1.5, 30*103/1.4]
#
scale = scales[i]
cnt_ra = cnt_ras[i]
cnt_dec = cnt_decs[i]
pa = pas[i]
inc = incs[i]
def_nucleus = def_nucleus[i]


#####################
### functions
#####################
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
	pa,
	inc,
	cnt_ra,
	cnt_dec,
	scale,
	def_nucleus,
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
	data_ra  = r21.import_data(co10_mom0, mode="coords", index=0)
	data_dec = r21.import_data(co10_mom0, mode="coords", index=1)
	dist = distance(data_ra, data_dec, pa, inc, cnt_ra, cnt_dec, scale)
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

def get_best_co10_parameter(
	dir_proj,
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
	range_popt1   = popt[1] + np.linspace(-0.005, 0.010, 11)
	range_popt2   = popt[2] + np.linspace(-0.010, 0.010, 11)
	range_scatter = np.logspace(np.log10(0.01), np.log10(1), 11)
	#
	list_popt1 = []
	list_popt2 = []
	list_scatter = []
	list_d = []
	list_p = []
	list_output = []
	numiter = 0
	numall = 11**3
	if best_parameters==None:
		done = glob.glob(dir_proj+"eps/best_co10_model_parameter.txt")
		if not done:
			for i, j, k in itertools.product(range_popt1, range_popt2, range_scatter):
				numiter += 1
				if numiter % 500 == 0:
					print("### create co10 model " + str(numiter).zfill(4) + "/" + str(numall))
				#
				log_co10_mom0_k_model = np.random.normal(i, j, num_co10)
				#
				log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, k)
				log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = -9999
				cut = np.where((log_co10_mom0_k_model_scatter>-9000))
				log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
				#
				if np.mean(log_co10_mom0_k_model_scatter)-np.mean(log_co10_mom0_k_model)>0.2:
					print("### co10_model_scatter - co10_model = " + str(np.mean(log_co10_mom0_k_model_scatter) - np.mean(log_co10_mom0_k_model)))
				#
				log_co10_mom0_k_model_scatter_noise = add_noise_co10(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10)
				#
				cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0]) & (log_co10_mom0_k_model_scatter<range_co10_input[1]))
				log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
				#
				cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]))
				log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]
				d, p = stats.ks_2samp(log_co10_mom0_k, log_co10_mom0_k_model_scatter_noise)
				#
				list_popt1.append(i)
				list_popt2.append(j)
				list_scatter.append(k)
				n = len(log_co10_mom0_k)
				m = len(log_co10_mom0_k_model_scatter_noise)
				list_d.append(d*np.sqrt(n*m/(n+m)))
				list_p.append(p)
				#
			list_output = np.c_[list_popt1, list_popt2, list_scatter, list_d, list_p]
			best_parameter = list_output[np.argmin(list_output[:,3])]
			print(best_parameter)
			#
			np.savetxt(dir_proj+"eps/best_co10_model_all_parameters.txt", np.array(list_output))
			np.savetxt(dir_proj+"eps/best_co10_model_parameter.txt", np.array(best_parameter))
		else:
			print("### skip creating co10 model because of best_co10_model_parameter.txt")
			best_parameter = np.loadtxt(dir_proj+"eps/best_co10_model_parameter.txt")
		#
		return best_parameter

def get_best_co21_parameter(
	dir_proj,
	best_co10_parameter,
	log_co10_mom0_k,
	log_co21_mom0_k,
	log_co10_noise_k,
	log_co21_noise_k,
	xbins_co10,
	xbins_co21,
	nbins,
	):
	# prepare
	range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
	range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
	#num_co21 = len(log_co21_mom0_k)
	#
	range_slope = np.linspace(1.05, 1.15, 11)
	range_intercept = np.linspace(-0.45, -0.20, 11)
	range_scatter = np.logspace(np.log10(0.5), np.log10(1.3), 11)
	#
	best_mean = best_co10_parameter[0]
	best_disp = best_co10_parameter[1]
	best_scatter = best_co10_parameter[2]
	num_co10 = len(log_co10_mom0_k)
	#
	list_slope = []
	list_intercept = []
	list_scatter = []
	list_d = []
	list_p = []
	list_output = []
	numiter = 0
	numall = 11*11*11
	done = glob.glob(dir_proj+"eps/best_co21_model_parameter.txt")
	if not done:
		for i, j, k in itertools.product(range_slope, range_intercept, range_scatter):
			numiter += 1
			if numiter % 500 == 0:
				print("### create co21 model " + str(numiter).zfill(4) + "/" + str(numall))
			#
			log_co10_mom0_k_model = np.random.normal(best_mean, best_disp, num_co10)
			log_co10_mom0_k_model_scatter = add_scatter(log_co10_mom0_k_model, best_scatter)
			#
			this_slope = i
			this_intercept = j
			this_scatter = k
			#
			log_co10_mom0_k_model.sort()
			log_co21_mom0_k_model = func_co10_vs_co21(log_co10_mom0_k_model, this_slope, this_intercept)
			#
			log_co21_mom0_k_model_scatter = add_scatter(log_co21_mom0_k_model, this_scatter)
			log_co10_mom0_k_model_scatter[np.isnan(log_co10_mom0_k_model_scatter)] = 100
			log_co21_mom0_k_model_scatter[np.isnan(log_co21_mom0_k_model_scatter)] = 100
			#
			cut = np.where((log_co10_mom0_k_model_scatter<100) & (log_co21_mom0_k_model_scatter<100))
			log_co21_mom0_k_model_scatter = log_co21_mom0_k_model_scatter[cut]
			log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
			#
			log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model_scatter_noise = add_noise(log_co10_mom0_k_model_scatter, log_co10_noise_k, xbins_co10, log_co21_mom0_k_model_scatter, log_co21_noise_k, xbins_co21)
			#
			cut = np.where((log_co10_mom0_k_model_scatter_noise>range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<range_co10_input[1]) & (log_co21_mom0_k_model_scatter_noise>range_co21_input[0]) & (log_co21_mom0_k_model_scatter_noise<range_co21_input[1]))
			log_co10_mom0_k_model_scatter_noise = log_co10_mom0_k_model_scatter_noise[cut]
			log_co21_mom0_k_model_scatter_noise = log_co21_mom0_k_model_scatter_noise[cut]
			#
			log_r21_mom0_k = np.log10(10**log_co21_mom0_k/10**log_co10_mom0_k)
			log_r21_mom0_k_model_scatter_noise = np.log10(10**log_co21_mom0_k_model_scatter_noise/10**log_co10_mom0_k_model_scatter_noise)
			#
			cut = np.where((log_r21_mom0_k_model_scatter_noise>=log_r21_mom0_k.min()) & (log_r21_mom0_k_model_scatter_noise<=log_r21_mom0_k.max()))
			d, p = stats.ks_2samp(log_r21_mom0_k, log_r21_mom0_k_model_scatter_noise)
			#
			list_slope.append(this_slope)
			list_intercept.append(this_intercept)
			list_scatter.append(this_scatter)
			n = len(log_co21_mom0_k)
			m = len(log_co21_mom0_k_model_scatter_noise)
			list_d.append(d*np.sqrt(n*m/(n+m)))
			list_p.append(p)
			#
		list_output = np.c_[list_slope, list_intercept, list_scatter, list_d, list_p]
		best_parameter = list_output[np.argmin(list_output[:,3])]
		print(best_parameter)
		#
		np.savetxt(dir_proj+"eps/best_co21_model_all_parameters.txt", np.array(list_output))
		np.savetxt(dir_proj+"eps/best_co21_model_parameter.txt", np.array(best_parameter))
	else:
		print("### skip creating co21 model because of best_co21_model_parameter.txt")
		best_parameter = np.loadtxt(dir_proj+"eps/best_co21_model_parameter.txt")
	#
	return best_parameter

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
	cut = np.where((log_co10_mom0_k_model_scatter>range_co10_input[0])) # & (log_co21_mom0_k_model_scatter>range_co21_input[0]))
	log_co10_mom0_k_model_scatter = log_co10_mom0_k_model_scatter[cut]
	log_co21_mom0_k_model_scatter = log_co21_mom0_k_model_scatter[cut]
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

def print_boot(
	listdata,
	text,
	):
	list_median = str(np.percentile(listdata,50))
	list_max = str(np.max(listdata))
	list_min = str(np.min(listdata))
	print("# " + text)
	print("# median = " + list_median)
	print("# max    = " + list_max)
	print("# min    = " + list_min)


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
log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21, pa, inc, cnt_ra, cnt_dec, scale, def_nucleus)
p84_co10, p50_co10, p16_co10, p84_co21, p50_co21, p16_co21 = print_things(log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k)
xbins_co10, xbins_co21 = plotter_noise(dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbins, percentile)


#####################
### modeling
#####################
list_best_co10_parameter = []
list_best_co21_parameter = []
for i in range(1000):
	print("### bootstrap " + str(i+1).zfill(3) + "/100")
	os.system("rm -rf " + dir_proj + "eps/best_co10_model_parameter.txt")
	os.system("rm -rf " + dir_proj + "eps/best_co21_model_parameter.txt")
	### get best parameters for co10 model
	best_co10_parameter = get_best_co10_parameter(dir_proj, log_co10_mom0_k, log_co10_noise_k, xbins_co10, nbins)
	#log_co10_mom0_k_model_for_co21, log_co10_mom0_k_model_scatter_for_co21 = get_best_co10_parameter(dir_proj, log_co10_mom0_k, log_co10_noise_k, xbins_co10, nbins, best_co10_parameter)
	#
	### get best parameters for co21 model
	best_co21_parameter = get_best_co21_parameter(dir_proj, best_co10_parameter, log_co10_mom0_k, log_co21_mom0_k, log_co10_noise_k, log_co21_noise_k, xbins_co10, xbins_co21, nbins)
	#
	### output
	list_best_co10_parameter.append(best_co10_parameter.tolist())
	list_best_co21_parameter.append(best_co21_parameter.tolist())
	# print
	print_boot(np.array(list_best_co10_parameter)[:,0], "co10_norm_mean")
	print_boot(np.array(list_best_co10_parameter)[:,1], "co10_norm_disp")
	print_boot(np.array(list_best_co10_parameter)[:,2], "co10_scatter")
	print_boot(np.array(list_best_co21_parameter)[:,0], "slope")
	print_boot(np.array(list_best_co21_parameter)[:,1], "intercept")
	print_boot(np.array(list_best_co21_parameter)[:,2], "co21_scatter")
	#
	### create best models
	log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise = \
		create_best_models(log_co10_mom0_k, log_co21_mom0_k, log_co10_noise_k, log_co21_noise_k, xbins_co10, xbins_co21, best_co10_parameter, best_co21_parameter)
	#
	#
	#
	#####################
	### plot
	######################
	### plot obs and model mom-0
	histdata10 = np.array(list_best_co10_parameter)
	histdata21 = np.array(list_best_co21_parameter)
	#
	figure = plt.figure(figsize=(10,10))
	gs = gridspec.GridSpec(nrows=9, ncols=9)
	plt.subplots_adjust(bottom=0.05, left=0.05, right=0.95, top=0.95)
	ax1 = plt.subplot(gs[0:2,0:4])
	ax2 = plt.subplot(gs[3:5,0:4])
	ax3 = plt.subplot(gs[6:8,0:4])
	ax4 = plt.subplot(gs[0:2,5:9])
	ax5 = plt.subplot(gs[3:5,5:9])
	ax6 = plt.subplot(gs[6:8,5:9])
	ax1.hist(histdata10[:,0], range=[0.735, 0.745], bins=11)
	ax2.hist(histdata10[:,1], range=[-0.015+0.2848, 0.015+0.2848], bins=11)
	ax3.hist(np.log10(np.array(histdata10[:,2])), range=[-3.0, 0.0], bins=11)
	ax4.hist(histdata21[:,0], range=[1.05, 1.15],bins=11)
	ax5.hist(histdata21[:,1], range=[-0.45, -0.20], bins=11)
	ax6.hist(np.log10(np.array(histdata21[:,2])), range=[-0.30, 0.12], bins=11)
	ax1.set_title("co10 norm mean at niter = " + str(i+1))
	ax2.set_title("co10 norm disp")
	ax3.set_title("log co10 scatter")
	ax4.set_title("co10 vs co21 slope")
	ax5.set_title("co10 vs co21 intercept")
	ax6.set_title("log co21 scatter")
	plt.savefig(dir_proj + "eps/fig_model_param_"+galname+".png",dpi=200)
	#
	range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
	range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
	log_co10_mom0_k_model_scatter_cut = log_co10_mom0_k_model_scatter[np.where((log_co10_mom0_k_model_scatter>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter<=range_co21_input[1]))]
	log_co21_mom0_k_model_scatter_cut = log_co21_mom0_k_model_scatter[np.where((log_co10_mom0_k_model_scatter>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter<=range_co21_input[1]))]
	log_co10_mom0_k_model_scatter_noise_cut = log_co10_mom0_k_model_scatter_noise[np.where((log_co10_mom0_k_model_scatter_noise>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter_noise>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter_noise<=range_co21_input[1]))]
	log_co21_mom0_k_model_scatter_noise_cut = log_co21_mom0_k_model_scatter_noise[np.where((log_co10_mom0_k_model_scatter_noise>=range_co10_input[0]) & (log_co10_mom0_k_model_scatter_noise<=range_co10_input[1]) & (log_co21_mom0_k_model_scatter_noise>=range_co21_input[0]) & (log_co21_mom0_k_model_scatter_noise<=range_co21_input[1]))]
	#
	figure = plt.figure(figsize=(10,10))
	gs = gridspec.GridSpec(nrows=8, ncols=8)
	plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
	ax1 = plt.subplot(gs[0:2,0:8])
	ax2 = plt.subplot(gs[3:5,0:8])
	ax3 = plt.subplot(gs[6:8,0:8])
	ax1.grid(axis="x")
	ax2.grid(axis="x")
	ax3.grid(axis="x")
	ax1.set_xlabel("log CO(1-0) mom-0 (K.km/s)")
	ax2.set_xlabel("log CO(2-1) mom-0 (K.km/s)")
	ax3.set_xlabel("log $R_{21}$")
	plt.rcParams["font.size"] = 16
	#
	# ax1
	ax1.hist(log_co10_mom0_k, normed=True, color="black", alpha=0.5, bins=nbins, lw=0, range=range_co10_input, label="Observed Data")
	#ax1.hist(log_co10_mom0_k_model, normed=True, color="blue", alpha=0.3, bins=nbins, lw=0, range=range_co10_input)
	#ax1.hist(log_co10_mom0_k_model_scatter_cut, normed=True, color="green", alpha=0.3, bins=nbins, lw=0, range=range_co10_input)
	ax1.hist(log_co10_mom0_k_model_scatter_noise_cut, normed=True, color="red", alpha=0.3, bins=nbins, lw=0, range=range_co10_input, label="Model with Scatter+Noise")
	ax1.set_xlim([0,3.0])
	ax1.legend(loc = "upper right")
	#
	# ax2
	ax2.hist(log_co21_mom0_k, normed=True, color="black", alpha=0.5, bins=nbins, lw=0, range=range_co21_input)
	ax2.hist(log_co21_mom0_k_model_scatter_noise_cut, normed=True, color="red", alpha=0.3, bins=nbins, lw=0, range=range_co21_input)
	ax2.set_xlim([-0.5,2.6])
	#
	# ax3
	log_r21_mom_k = np.log10(10**log_co21_mom0_k/10**log_co10_mom0_k)
	log_r21_mom0_k_model_scatter = np.log10(10**log_co21_mom0_k_model_scatter_cut/10**log_co10_mom0_k_model_scatter_cut)
	log_r21_mom0_k_model_scatter_noise = np.log10(10**log_co21_mom0_k_model_scatter_noise_cut/10**log_co10_mom0_k_model_scatter_noise_cut)
	#
	ax3.hist(log_r21_mom_k, normed=True, color="black", alpha=0.5, bins=nbins, lw=0)
	ax3.hist(log_r21_mom0_k_model_scatter, normed=True, color="blue", alpha=0.3, bins=nbins, lw=0, range=[-1.0,0.5])
	ax3.hist(log_r21_mom0_k_model_scatter_noise, normed=True, color="red", alpha=0.3, bins=nbins, lw=0, range=[-1.0,0.5])
	ax3.set_xlim([-1.0,0.5])
	#
	plt.savefig(dir_proj + "eps/fig_obs_vs_model_histo_"+galname+".png",dpi=200)


	### plot co10 vs co21
	figure = plt.figure(figsize=(10,10))
	gs = gridspec.GridSpec(nrows=8, ncols=8)
	plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
	ax1 = plt.subplot(gs[0:8,0:8])
	ax1.grid(axis="both")
	ax1.set_xlabel("log CO(1-0) mom-0 (K.km/s)")
	ax1.set_ylabel("log CO(2-1) mom-0 (K.km/s)")
	plt.rcParams["font.size"] = 16
	#
	binx, mean, std = get_binned_dist(log_co10_mom0_k_model_scatter_noise_cut, log_co21_mom0_k_model_scatter_noise_cut, range_co10_input)
	ax1.errorbar(binx, mean, yerr = std, color = "dimgrey", ecolor = "dimgrey", lw=4)
	#
	# ax1
	ax1.plot(log_co10_mom0_k_model, log_co21_mom0_k_model, "o", color="black", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e18, label="Model")
	ax1.plot(log_co10_mom0_k_model_scatter_cut, log_co21_mom0_k_model_scatter_cut, "o", color="blue", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e20, label="Model with Scatter")
	ax1.plot(log_co10_mom0_k_model_scatter_noise_cut, log_co21_mom0_k_model_scatter_noise_cut, "o", color="red", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e22, label="Model with Scatter+Noise")
	ax1.plot(log_co10_mom0_k, log_co21_mom0_k, "o", color="grey", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e24, label="Observed Data")
	ax1.plot([-0.5,3.0], [-0.5,3.0], "k--", lw=5)
	ax1.set_xlim([-0.5,2.0])
	ax1.set_ylim([-0.5,2.0])
	#
	ax1.legend(loc = "upper left")
	plt.savefig(dir_proj + "eps/fig_obs_vs_model_mom0_"+galname+".png",dpi=200)


	### plot co21 vs r21
	r21 = np.log10(10**log_co21_mom0_k/10**log_co10_mom0_k)
	r21_model = np.log10(10**log_co21_mom0_k_model/10**log_co10_mom0_k_model)
	r21_model_scatter = np.log10(10**log_co21_mom0_k_model_scatter_cut/10**log_co10_mom0_k_model_scatter_cut)
	r21_model_scatter_noise = np.log10(10**log_co21_mom0_k_model_scatter_noise_cut/10**log_co10_mom0_k_model_scatter_noise_cut)
	#
	figure = plt.figure(figsize=(10,10))
	gs = gridspec.GridSpec(nrows=8, ncols=8)
	plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
	ax1 = plt.subplot(gs[0:8,0:8])
	ax1.grid(axis="both")
	ax1.set_xlabel("log CO(2-1) mom-0 (K.km/s)")
	ax1.set_ylabel("log $R_{21}$")
	plt.rcParams["font.size"] = 16
	#
	binx, mean, std = get_binned_dist(log_co21_mom0_k_model_scatter_noise_cut, r21_model_scatter_noise, range_co21_input)
	ax1.errorbar(binx, mean, yerr = std, color = "dimgrey", ecolor = "dimgrey", lw=4)
	#
	# ax1
	ax1.plot(log_co21_mom0_k_model, r21_model, "o", color="black", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e18)
	ax1.plot(log_co21_mom0_k_model_scatter_cut, r21_model_scatter, "o", color="blue", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e20)
	ax1.plot(log_co21_mom0_k_model_scatter_noise_cut, r21_model_scatter_noise, "o", color="red", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e22)
	ax1.plot(log_co21_mom0_k, r21, "o", color="grey", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e24)
	ax1.set_xlim([-0.5,2.0])
	ax1.set_ylim([-1.2,0.5])
	#
	plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_"+galname+".png",dpi=200)
	#
	os.system("rm -rf " + dir_proj+"eps/bootstrap_co*_models_"+galname+".txt")
	np.savetxt(dir_proj+"eps/bootstrap_co10_models_"+galname+".txt", np.array(list_best_co10_parameter))
	np.savetxt(dir_proj+"eps/bootstrap_co21_models_"+galname+".txt", np.array(list_best_co21_parameter))
	#


#
os.system("rm -rf *.last")

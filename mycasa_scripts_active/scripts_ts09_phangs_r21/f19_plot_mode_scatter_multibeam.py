import os, re, sys, glob
import itertools
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats

plt.ioff()

#
import scripts_phangs_r21 as r21tool


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galname = "ngc0628"
freqco10 = 115.27120
freqco21 = 230.53800
percentile = 84
scales = [44/1.0, 52/1.3, 103/1.4]
cnt_ras = [24.174, 170.063, 185.729]
cnt_decs = [15.783, 12.9914, 15.8223]
pas = [180-21.1, 180-172.4, 180-157.8]
incs = [90-8.7, 90-56.2, 90-35.1]
def_nucleuss = [50*44./1.0, 50*52./1.3*1.5, 30*103/1.4]

nbins_n0628 = [40, 30, 20, 10, 10]
nbins_n3627 = [30, 20, 20, 10, 10]
nbins_n4321 = [40, 30, 25, 20, 15]
beams_n0628 = ["04p0","08p0","12p0","16p0","20p0"]
beams_n3627 = ["08p0","12p0","16p0","20p0","24p0"]
beams_n4321 = ["04p0","08p0","12p0","16p0","20p0"]


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
	data_co10_mom0  = r21tool.import_data(co10_mom0, mode="data")
	data_co10_noise = r21tool.import_data(co10_noise, mode="data")
	data_co21_mom0  = r21tool.import_data(co21_mom0, mode="data")
	data_co21_noise = r21tool.import_data(co21_noise, mode="data")
	#
	data_ra  = r21tool.import_data(co10_mom0, mode="coords", index=0)
	data_dec = r21tool.import_data(co10_mom0, mode="coords", index=1)
	dist = r21tool.distance(data_ra, data_dec, pa, inc, cnt_ra, cnt_dec, scale)
	# select data
	cut_all = np.where((data_co10_mom0>0) & (data_co10_noise>0) & (data_co21_mom0>0) & (data_co21_noise>0) & (dist>def_nucleus))
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
	#plt.savefig(dir_proj + "eps/fig_noise_vs_mom0_"+galname+".png",dpi=200)

	return xbins_co10, xbins_co21

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
	co10_scatter = abs(co10_scatter)
	co21_scatter = abs(co21_scatter)
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
	print("###")

	return log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise

def func_co10_vs_co21(x, a, b):
	"""
	"""
	return a * x + b

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
list_median_84 = []
list_median_50 = []
list_median_16 = []
list_width_84 = []
list_width_50 = []
list_width_16 = []

##
i=0
scale = scales[i]
cnt_ra = cnt_ras[i]
cnt_dec = cnt_decs[i]
pa = pas[i]
inc = incs[i]
def_nucleus = def_nucleuss[i]
for i in range(len(nbins_n0628)):
	n0628_co10_best_params = get_best_params(txt_n0628_co10[i])
	n0628_co21_best_params = get_best_params(txt_n0628_co21[i])
	co10_mom0  = dir_proj + "ngc0628_co10/co10_"+beams_n0628[i]+".moment0"
	co10_noise = dir_proj + "ngc0628_co10/co10_"+beams_n0628[i]+".moment0.noise"
	co21_mom0  = dir_proj + "ngc0628_co21/co21_"+beams_n0628[i]+".moment0"
	co21_noise = dir_proj + "ngc0628_co21/co21_"+beams_n0628[i]+".moment0.noise"
	#
	log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21, pa, inc, cnt_ra, cnt_dec, scale, def_nucleus)
	xbins_co10, xbins_co21 = plotter_noise(dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbins_n0628[i], percentile, galname)
	#
	bootstrap_median = []
	bootstrap_width = []
	for j in range(100):
		print(j)
		log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise = \
			create_best_models(log_co10_mom0_k, log_co21_mom0_k, log_co10_noise_k, log_co21_noise_k, xbins_co10, xbins_co21, n0628_co10_best_params, n0628_co21_best_params)
		r21 = 10**log_co21_mom0_k_model_scatter/10**log_co10_mom0_k_model_scatter
		#
		median = np.log10(np.percentile(r21, 50))
		width = np.log10(np.percentile(r21, 84)) - np.log10(np.percentile(r21, 16))
		bootstrap_median.append(median)
		bootstrap_width.append(width)
	#
	list_median_84.append(np.percentile(bootstrap_median,84))
	list_median_50.append(np.percentile(bootstrap_median,50))
	list_median_16.append(np.percentile(bootstrap_median,16))
	list_width_84.append(np.percentile(bootstrap_width,84))
	list_width_50.append(np.percentile(bootstrap_width,50))
	list_width_16.append(np.percentile(bootstrap_width,16))

#
i=1
scale = scales[i]
cnt_ra = cnt_ras[i]
cnt_dec = cnt_decs[i]
pa = pas[i]
inc = incs[i]
def_nucleus = def_nucleuss[i]
for i in range(len(nbins_n3627)):
	n3627_co10_best_params = get_best_params(txt_n3627_co10[i])
	n3627_co21_best_params = get_best_params(txt_n3627_co21[i])
	co10_mom0  = dir_proj + "ngc3627_co10/co10_"+beams_n3627[i]+".moment0"
	co10_noise = dir_proj + "ngc3627_co10/co10_"+beams_n3627[i]+".moment0.noise"
	co21_mom0  = dir_proj + "ngc3627_co21/co21_"+beams_n3627[i]+".moment0"
	co21_noise = dir_proj + "ngc3627_co21/co21_"+beams_n3627[i]+".moment0.noise"
	#
	log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21, pa, inc, cnt_ra, cnt_dec, scale, def_nucleus)
	xbins_co10, xbins_co21 = plotter_noise(dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbins_n3627[i], percentile, galname)
	#
	bootstrap_median = []
	bootstrap_width = []
	for j in range(100):
		print(j)
		log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise = \
			create_best_models(log_co10_mom0_k, log_co21_mom0_k, log_co10_noise_k, log_co21_noise_k, xbins_co10, xbins_co21, n3627_co10_best_params, n3627_co21_best_params)
		r21 = 10**log_co21_mom0_k_model_scatter/10**log_co10_mom0_k_model_scatter
		#
		median = np.log10(np.percentile(r21, 50))
		width = np.log10(np.percentile(r21, 84)) - np.log10(np.percentile(r21, 16))
		bootstrap_median.append(median)
		bootstrap_width.append(width)
	#
	list_median_84.append(np.percentile(bootstrap_median,84))
	list_median_50.append(np.percentile(bootstrap_median,50))
	list_median_16.append(np.percentile(bootstrap_median,16))
	list_width_84.append(np.percentile(bootstrap_width,84))
	list_width_50.append(np.percentile(bootstrap_width,50))
	list_width_16.append(np.percentile(bootstrap_width,16))

#
i=2
scale = scales[i]
cnt_ra = cnt_ras[i]
cnt_dec = cnt_decs[i]
pa = pas[i]
inc = incs[i]
def_nucleus = def_nucleuss[i]
for i in range(len(nbins_n4321)):
	n4321_co10_best_params = get_best_params(txt_n4321_co10[i])
	n4321_co21_best_params = get_best_params(txt_n4321_co21[i])
	co10_mom0  = dir_proj + "ngc4321_co10/co10_"+beams_n4321[i]+".moment0"
	co10_noise = dir_proj + "ngc4321_co10/co10_"+beams_n4321[i]+".moment0.noise"
	co21_mom0  = dir_proj + "ngc4321_co21/co21_"+beams_n4321[i]+".moment0"
	co21_noise = dir_proj + "ngc4321_co21/co21_"+beams_n4321[i]+".moment0.noise"
	#
	log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21, pa, inc, cnt_ra, cnt_dec, scale, def_nucleus)
	xbins_co10, xbins_co21 = plotter_noise(dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbins_n4321[i], percentile, galname)
	#
	bootstrap_median = []
	bootstrap_width = []
	for j in range(100):
		print(j)
		log_co10_mom0_k_model, log_co10_mom0_k_model_scatter, log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model, log_co21_mom0_k_model_scatter, log_co21_mom0_k_model_scatter_noise = \
			create_best_models(log_co10_mom0_k, log_co21_mom0_k, log_co10_noise_k, log_co21_noise_k, xbins_co10, xbins_co21, n4321_co10_best_params, n4321_co21_best_params)
		r21 = 10**log_co21_mom0_k_model_scatter/10**log_co10_mom0_k_model_scatter
		#
		median = np.log10(np.percentile(r21, 50))
		width = np.log10(np.percentile(r21, 84)) - np.log10(np.percentile(r21, 16))
		bootstrap_median.append(median)
		bootstrap_width.append(width)
	#
	list_median_84.append(np.percentile(bootstrap_median,84))
	list_median_50.append(np.percentile(bootstrap_median,50))
	list_median_16.append(np.percentile(bootstrap_median,16))
	list_width_84.append(np.percentile(bootstrap_width,84))
	list_width_50.append(np.percentile(bootstrap_width,50))
	list_width_16.append(np.percentile(bootstrap_width,16))


###
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=1, ncols=15)
plt.subplots_adjust(bottom=0.15, left=0.07, right=0.98, top=0.90)
ax1 = plt.subplot(gs[0:5,0:5])
ax2 = plt.subplot(gs[0:5,5:10])
ax3 = plt.subplot(gs[0:5,10:15])
ax1.grid(axis="y")
ax2.grid(axis="y")
ax3.grid(axis="y")
ax1.set_ylabel("Normed Median")
ax1.set_xlabel("Beam Size (arcsec)")
ax2.set_xlabel("Beam Size (arcsec)")
ax3.set_xlabel("Beam Size (arcsec)")
ax2.tick_params(labelleft=False)
ax3.tick_params(labelleft=False)
ax1.set_title("NGC 0628")
ax2.set_title("NGC 3627")
ax3.set_title("NGC 4321")
plt.rcParams["font.size"] = 12

#
ax1.plot([float(s.replace("p",".")) for s in beams_n0628], list_median_50[0:5]/list_median_50[0], "o-", color=cm.brg(0/2.5), alpha=0.6, lw=2)
ax2.plot([float(s.replace("p",".")) for s in beams_n3627], list_median_50[5:10]/list_median_50[5], "o-", color=cm.brg(1/2.5), alpha=0.6, lw=2)
ax3.plot([float(s.replace("p",".")) for s in beams_n4321], list_median_50[10:15]/list_median_50[10], "o-", color=cm.brg(2/2.5), alpha=0.6, lw=2)

#
ax1.fill_between([float(s.replace("p",".")) for s in beams_n0628], list_median_84[0:5]/list_median_50[0], list_median_16[0:5]/list_median_50[0], facecolor=cm.brg(0/2.5), alpha=0.5)
ax2.fill_between([float(s.replace("p",".")) for s in beams_n3627], list_median_84[5:10]/list_median_50[5], list_median_16[5:10]/list_median_50[5], facecolor=cm.brg(1/2.5), alpha=0.5)
ax3.fill_between([float(s.replace("p",".")) for s in beams_n4321], list_median_84[10:15]/list_median_50[10], list_median_16[10:15]/list_median_50[10], facecolor=cm.brg(2/2.5), alpha=0.5)

#
ax1.set_ylim([0.9,1.4])
ax2.set_ylim([0.9,1.4])
ax3.set_ylim([0.9,1.4])
ax1.set_xlim([2.0,35.0])
ax2.set_xlim([6.0,35.0])
ax3.set_xlim([2.0,35.0])

plt.savefig(dir_proj+"eps/violin_median_simu.png",dpi=300)


###
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=1, ncols=15)
plt.subplots_adjust(bottom=0.15, left=0.07, right=0.98, top=0.90)
ax1 = plt.subplot(gs[0:5,0:5])
ax2 = plt.subplot(gs[0:5,5:10])
ax3 = plt.subplot(gs[0:5,10:15])
ax1.grid(axis="y")
ax2.grid(axis="y")
ax3.grid(axis="y")
ax1.set_ylabel("Normed Median")
ax1.set_xlabel("Beam Size (arcsec)")
ax2.set_xlabel("Beam Size (arcsec)")
ax3.set_xlabel("Beam Size (arcsec)")
ax2.tick_params(labelleft=False)
ax3.tick_params(labelleft=False)
ax1.set_title("NGC 0628")
ax2.set_title("NGC 3627")
ax3.set_title("NGC 4321")
plt.rcParams["font.size"] = 12

#
ax1.plot([float(s.replace("p",".")) for s in beams_n0628], list_width_50[0:5]/list_width_50[0], "o-", color=cm.brg(0/2.5), alpha=0.6, lw=2)
ax2.plot([float(s.replace("p",".")) for s in beams_n3627], list_width_50[5:10]/list_width_50[5], "o-", color=cm.brg(1/2.5), alpha=0.6, lw=2)
ax3.plot([float(s.replace("p",".")) for s in beams_n4321], list_width_50[10:15]/list_width_50[10], "o-", color=cm.brg(2/2.5), alpha=0.6, lw=2)

#
ax1.fill_between([float(s.replace("p",".")) for s in beams_n0628], list_width_84[0:5]/list_width_50[0], list_width_16[0:5]/list_width_50[0], facecolor=cm.brg(0/2.5), alpha=0.5)
ax2.fill_between([float(s.replace("p",".")) for s in beams_n3627], list_width_84[5:10]/list_width_50[5], list_width_16[5:10]/list_width_50[5], facecolor=cm.brg(1/2.5), alpha=0.5)
ax3.fill_between([float(s.replace("p",".")) for s in beams_n4321], list_width_84[10:15]/list_width_50[10], list_width_16[10:15]/list_width_50[10], facecolor=cm.brg(2/2.5), alpha=0.5)

#
ax1.set_ylim([0.3,1.4])
ax2.set_ylim([0.3,1.4])
ax3.set_ylim([0.3,1.4])
ax1.set_xlim([2.0,35.0])
ax2.set_xlim([6.0,35.0])
ax3.set_xlim([2.0,35.0])

plt.savefig(dir_proj+"eps/violin_width_simu.png",dpi=300)

os.system("rm -rf *.last")

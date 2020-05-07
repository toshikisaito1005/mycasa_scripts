import os, re, sys, glob
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats
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
percentile = 84


#####################
### functions
#####################
def func_co10_vs_co21(x, a, b):
	"""
	"""
	return a * x + b

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

def fit_lognorm(
	log_co10_mom0_k,
	num_input,
	nbins,
	):
	"""
	"""
	num_input = len(log_co10_mom0_k)
	minimum = log_co10_mom0_k.min()
	maximum = log_co10_mom0_k.max()
	list_x = []
	list_y = []
	list_d = []
	list_p = []
	list_mean = np.linspace(-2.00, 2.00, nbins)
	list_disp = np.linspace(0.1, 2, nbins)
	for i in list_mean:
		for j in list_disp:
			lognorm_model = np.random.normal(i, j, num_input)
			lognorm_model = lognorm_model[lognorm_model>minimum]
			lognorm_model = lognorm_model[lognorm_model<maximum]
			d, p = stats.ks_2samp(log_co10_mom0_k, lognorm_model)
			list_x.append(i)
			list_y.append(j)
			list_d.append(d)
			list_p.append(p)

	list_output = np.c_[list_x, list_y, list_d, list_p]
	list_output = np.nan_to_num(list_output)
	list_output2 = []
	for i in range(len(list_output)):
		if list_output[i][2]!=0 and list_output[i][3]!=0:
			list_output2.append(list_output[i])

	best_lognorm = list_output[np.argmin(np.array(list_output2)[:,2])]

	return best_lognorm[0], best_lognorm[1], list_output2

def add_scatter(
	best_lognorm_co10,
	scatter_sigma,
	):
	"""
	"""
	# create noise
	num_data = len(best_lognorm_co10)
	binned_data_and_noise = np.log10(10**best_lognorm_co10 + np.random.normal(0.0, scatter_sigma, num_data))

	return np.array(binned_data_and_noise)

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


#####################
### Main Procedure
#####################
### get filenames
co10_mom0  = dir_proj + "ngc4321_co10/co10_04p0.moment0"
co10_noise = dir_proj + "ngc4321_co10/co10_04p0.moment0.noise"
co21_mom0  = dir_proj + "ngc4321_co21/co21_04p0.moment0"
co21_noise = dir_proj + "ngc4321_co21/co21_04p0.moment0.noise"
#
### plot noise vs. mom-0
log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k = getdata(co10_mom0, co10_noise, co21_mom0, co21_noise, freqco10, freqco21)
p84_co10, p50_co10, p16_co10, p84_co21, p50_co21, p16_co21 = print_things(log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k)
xbins_co10, xbins_co21 = plotter_noise( dir_proj, log_co10_mom0_k, log_co10_noise_k, log_co21_mom0_k, log_co21_noise_k, nbins, percentile)





### model co10 mom-0 distribution
## define plot range
range_co10_input = [log_co10_mom0_k.min(), log_co10_mom0_k.max()]
range_co21_input = [log_co21_mom0_k.min(), log_co21_mom0_k.max()]
#
## create log co10 vs log co21 scaling relation with log-normal intensity distributions
# create co10 model lognormal distribution
num_input = len(log_co10_mom0_k)
best_mean, best_disp, _ = fit_lognorm(log_co10_mom0_k, num_input, nbins)
best_lognorm_co10 = np.random.lognormal(best_mean, best_disp, num_input)
best_lognorm_co10 = best_lognorm_co10[best_lognorm_co10<log_co10_mom0_k.max()]
best_lognorm_co10 = best_lognorm_co10[best_lognorm_co10>log_co10_mom0_k.min()]
best_lognorm_co10.sort()
# create co21 model
best_lognorm_co21 = func_co10_vs_co21(best_lognorm_co10, 1.27, -0.7)
best_lognorm_co21 = best_lognorm_co21[best_lognorm_co21<log_co21_mom0_k.max()]
best_lognorm_co21 = best_lognorm_co21[best_lognorm_co21>log_co21_mom0_k.min()]
best_lognorm_co10 = best_lognorm_co10[best_lognorm_co21<log_co21_mom0_k.max()]
best_lognorm_co10 = best_lognorm_co10[best_lognorm_co21>log_co21_mom0_k.min()]
#
## adding scatter
best_lognorm_co10_w_scatter = add_scatter(best_lognorm_co10, 1.1)
best_lognorm_co21_w_scatter = add_scatter(best_lognorm_co21, 1.1)

## adding noise
best_lognorm_co10_w_scatter_noise, best_lognorm_co21_w_scatter_noise = \
	add_noise(best_lognorm_co10_w_scatter, log_co10_noise_k, xbins_co10, best_lognorm_co21_w_scatter, log_co21_noise_k, xbins_co21)



### cut data
cut_all_scatter = np.where((best_lognorm_co10_w_scatter>=xbins_co10.min()) & (best_lognorm_co10_w_scatter<=xbins_co10.max()) & (best_lognorm_co21_w_scatter>=xbins_co21.min()) & (best_lognorm_co21_w_scatter<=xbins_co21.max()))
cut_all_scatter_noise = np.where((best_lognorm_co10_w_scatter_noise>=xbins_co10.min()) & (best_lognorm_co10_w_scatter_noise<=xbins_co10.max()) & (best_lognorm_co21_w_scatter_noise>=xbins_co21.min()) & (best_lognorm_co21_w_scatter_noise<=xbins_co21.max()))
#
best_lognorm_co10_w_scatter = best_lognorm_co10_w_scatter[cut_all_scatter]
best_lognorm_co21_w_scatter = best_lognorm_co21_w_scatter[cut_all_scatter]
best_lognorm_co10_w_scatter_noise = best_lognorm_co10_w_scatter_noise[cut_all_scatter_noise]
best_lognorm_co21_w_scatter_noise = best_lognorm_co21_w_scatter_noise[cut_all_scatter_noise]




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
ax1.hist(log_co10_mom0_k, normed=True, color="black", alpha=0.5, bins=nbins, range=range_co10_input, lw=0)
ax1.hist(best_lognorm_co10_w_scatter, normed=True, color="blue", alpha=0.5, bins=nbins, lw=0, range=range_co10_input)
ax1.hist(best_lognorm_co10_w_scatter_noise, normed=True, color="red", alpha=0.5, bins=nbins, lw=0, range=range_co10_input)
ax1.set_xlim([0,2.0])
#
#ax2
ax2.hist(log_co21_mom0_k, normed=True, color="black", alpha=0.5, bins=nbins, range=range_co21_input, lw=0)
ax2.hist(best_lognorm_co21_w_scatter_noise, normed=True, color="red", alpha=0.5, bins=nbins, lw=0, range=range_co21_input)
ax2.set_xlim([-0.5,1.6])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_histo.png",dpi=200)






### plot obs and model mom-0
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
plt.rcParams["font.size"] = 16

# ax1
ax1.plot(best_lognorm_co10, best_lognorm_co21, "o", color="black", alpha=1.0, markersize=3, markeredgewidth=0, zorder=1e22)
ax1.plot(best_lognorm_co10_w_scatter_noise, best_lognorm_co21_w_scatter_noise, "o", color="red", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e18, label="scatter and noise")
ax1.plot(best_lognorm_co10_w_scatter, best_lognorm_co21_w_scatter, "o", color="blue", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e20, label="scatter")
ax1.plot(log_co10_mom0_k, log_co21_mom0_k, "o", color="grey", alpha=0.2, markersize=10, markeredgewidth=0)
ax1.plot([-0.5,3.0], [-0.5,3.0], "k--", lw=5)
ax1.set_xlim([-0.5,3.0])
ax1.set_ylim([-0.5,3.0])
#
ax1.legend()
plt.savefig(dir_proj + "eps/fig_obs_vs_model_mom0.png",dpi=200)
#






### plot obs and model mom-0
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("CO(1-0) mom-0 (K.km/s)")
plt.rcParams["font.size"] = 16

# ax1
ax1.plot(best_lognorm_co21, np.log10(10**best_lognorm_co21/10**best_lognorm_co10), "o", color="black", alpha=1.0, markersize=3, markeredgewidth=0, zorder=1e22)
ax1.plot(best_lognorm_co21_w_scatter_noise, np.log10(10**best_lognorm_co21_w_scatter_noise/10**best_lognorm_co10_w_scatter_noise), "o", color="red", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e18, label="scatter and noise")
ax1.plot(best_lognorm_co21_w_scatter, np.log10(10**best_lognorm_co21_w_scatter/10**best_lognorm_co10_w_scatter), "o", color="blue", alpha=0.2, markersize=7, markeredgewidth=0, zorder=1e20, label="scatter")
ax1.plot(log_co21_mom0_k, np.log10(10**log_co21_mom0_k/10**log_co10_mom0_k), "o", color="grey", alpha=0.2, markersize=10, markeredgewidth=0)
ax1.set_xlim([-0.5,3.0])
ax1.set_ylim([-1.0,0.5])
#
ax1.legend()
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21.png",dpi=200)
#
os.system("rm -rf *.last")



### print
#
r21_obs = np.log10(10**log_co21_mom0_k / 10**log_co10_mom0_k)
r21_obs_above_one = r21_obs[r21_obs>np.log10(1)]
r21_obs_above_one_percent = np.round(len(r21_above_one)/float(len(r21_obs)) * 100, 1)
#
r21_scatter = np.log10(10**best_lognorm_co21_w_scatter/10**best_lognorm_co10_w_scatter)
r21_scatter_above_one = r21_scatter[r21_scatter>np.log10(1)]
r21_scatter_above_one_percent = np.round(len(r21_scatter_above_one)/float(len(r21_scatter)) * 100, 1)
#
r21_scatter_noise = np.log10(10**best_lognorm_co21_w_scatter_noise/10**best_lognorm_co10_w_scatter_noise)
r21_scatter_noise_above_one = r21_scatter_noise[r21_scatter_noise>np.log10(1)]
r21_scatter_noise_above_one_percent = np.round(len(r21_scatter_noise_above_one)/float(len(r21_scatter_noise)) * 100, 1)
#
print("### r21_obs                  > 1.0 = "+str(r21_obs_above_one_percent)+" %")
print("### r21_model(scatter)       > 1.0 = "+str(r21_scatter_above_one_percent)+" %")
print("### r21_model(scatter+noise) > 1.0 = "+str(r21_scatter_noise_above_one_percent)+" %")

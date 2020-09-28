import os, re, sys, glob
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats
plt.ioff()

#
import scripts_phangs_r21 as r21

# n0628: 04p0
# n3627: 08p0
# n4321: 04p0


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galname, i = "ngc4321", 2
freqco10 = 115.27120
freqco21 = 230.53800
nbins = 40 # 40/10, 30/10, 40/15
percentile = 84
beams = ["04p0"] # 04p0, 08p0, 04p0
xlim = [-0.5,1.8] # [-0.6,1.8], [-0.1,2.3], [-0.5,1.8]
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
beamstr = beams[0]


#####################
### main
#####################
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
ax1.set_xlabel("log CO(2-1) mom-0 (K km s$^{-1}$)")
ax1.set_ylabel("log $R_{21}$")
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
#
binx, mean, std = get_binned_dist(log_co21_mom0_k_model_scatter_noise_cut, r21_model_scatter_noise, range_co21_input)
ax1.errorbar(binx, mean, yerr = std, color = "dimgrey", ecolor = "dimgrey", lw=4)
#
# ax1
ax1.plot(log_co21_mom0_k_model, r21_model, "o", color="black", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e18)
ax1.plot(log_co21_mom0_k_model_scatter_cut, r21_model_scatter, "o", color="blue", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e20)
ax1.plot(log_co21_mom0_k_model_scatter_noise_cut, r21_model_scatter_noise, "o", color="red", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e22)
ax1.plot(log_co21_mom0_k, r21, "o", color="grey", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e24)
ax1.set_xlim(xlim)
ax1.set_ylim([-1.2,0.5])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_"+galname+"_"+beamstr+".png",dpi=200)
#

#
#np.savetxt(dir_proj + "eps/"+galname+"_model.txt", np.c_[log_co10_mom0_k_model, log_co21_mom0_k_model])
np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter.txt", np.c_[log_co10_mom0_k_model_scatter, log_co21_mom0_k_model_scatter])
np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter_noise.txt", np.c_[log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model_scatter_noise])
#
np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter_cut.txt", np.c_[log_co10_mom0_k_model_scatter_cut, log_co21_mom0_k_model_scatter_cut])
np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter_noise_cut.txt", np.c_[log_co10_mom0_k_model_scatter_noise_cut, log_co21_mom0_k_model_scatter_noise_cut])
#"""

#
os.system("rm -rf *.last")

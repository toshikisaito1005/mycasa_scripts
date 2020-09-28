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


#####################
### main
#####################
#np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter.txt", np.c_[log_co10_mom0_k_model_scatter, log_co21_mom0_k_model_scatter])
#np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter_noise.txt", np.c_[log_co10_mom0_k_model_scatter_noise, log_co21_mom0_k_model_scatter_noise])
np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter_cut.txt", np.c_[log_co10_mom0_k_model_scatter_cut, log_co21_mom0_k_model_scatter_cut])
#np.savetxt(dir_proj + "eps/"+galname+"_model_"+beamstr+"_scatter_noise_cut.txt", np.c_[log_co10_mom0_k_model_scatter_noise_cut, log_co21_mom0_k_model_scatter_noise_cut])

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
#ax1.plot(log_co21_mom0_k_model, r21_model, "o", color="black", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e18)
ax1.plot(log_co21_mom0_k_model_scatter_cut, r21_model_scatter, "o", color="blue", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e20)
#ax1.plot(log_co21_mom0_k_model_scatter_noise_cut, r21_model_scatter_noise, "o", color="red", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e22)
#ax1.plot(log_co21_mom0_k, r21, "o", color="grey", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e24)
ax1.set_xlim(xlim)
ax1.set_ylim([-1.2,0.5])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_"+galname+"_"+beamstr+".png",dpi=200)
#

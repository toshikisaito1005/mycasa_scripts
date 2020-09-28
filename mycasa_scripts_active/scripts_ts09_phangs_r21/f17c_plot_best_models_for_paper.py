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
###
data_high = np.loadtxt(dir_proj + "eps/ngc0628_model_04p0_scatter_cut.txt")
data_low = np.loadtxt(dir_proj + "eps/ngc0628_model_20p0_scatter_cut.txt")
xlim = [-0.5,1.8] # [-0.6,1.8], [-0.1,2.3], [-0.5,1.8]
r21_high = np.log10(10**data_high[:,0]/10**data_high[:,1])
r21_low = np.log10(10**data_low[:,0]/10**data_low[:,1])
#
### plot co21 vs r21
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
# ax1
#ax1.plot(log_co21_mom0_k_model, r21_model, "o", color="black", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e18)
ax1.plot(log_co21_mom0_k_model_scatter_cut, r21_model_scatter, "o", color="blue", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e20)
#ax1.plot(log_co21_mom0_k_model_scatter_noise_cut, r21_model_scatter_noise, "o", color="red", alpha=0.5, markersize=5, markeredgewidth=0, zorder=-1e22)
#ax1.plot(log_co21_mom0_k, r21, "o", color="grey", alpha=1.0, markersize=5, markeredgewidth=0, zorder=-1e24)
ax1.set_xlim(xlim)
ax1.set_ylim([-1.2,0.5])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_ngc0628.png",dpi=200)
#

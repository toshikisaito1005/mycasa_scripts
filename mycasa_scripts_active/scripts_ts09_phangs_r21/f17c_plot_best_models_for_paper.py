import os, re, sys, glob
import itertools
import matplotlib.cm as cm
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
xlim = [-0.6,1.8]
#
data_high = np.loadtxt(dir_proj + "eps/ngc0628_model_04p0_scatter_cut.txt")
data_low = np.loadtxt(dir_proj + "eps/ngc0628_model_20p0_scatter_cut.txt")
co10_high = data_high[:,0]
co21_high = data_high[:,1]
co10_low = data_low[:,0]
co21_low = data_low[:,1]
r21_high = np.log10(10**co21_high/10**co10_high)
r21_low = np.log10(10**co21_low/10**co10_low)
#
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax1.set_ylabel("log $R_{21}$")
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
#
ax1.plot(co21_high, r21_high, "o", color=cm.brg(0./2.5), alpha=0.5, markersize=10, markeredgewidth=0)
ax1.plot(co21_low, r21_low, "o", color="black", alpha=0.5, markersize=10, markeredgewidth=0)
ax1.set_xlim(xlim)
ax1.set_ylim([-1.2,0.5])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_ngc0628.png",dpi=200)
#

###
xlim = [-0.1,2.3]
#
data_high = np.loadtxt(dir_proj + "eps/ngc3627_model_08p0_scatter_cut.txt")
data_low = np.loadtxt(dir_proj + "eps/ngc3627_model_24p0_scatter_cut.txt")
co10_high = data_high[:,0]
co21_high = data_high[:,1]
co10_low = data_low[:,0]
co21_low = data_low[:,1]
r21_high = np.log10(10**co21_high/10**co10_high)
r21_low = np.log10(10**co21_low/10**co10_low)
#
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax1.set_ylabel("log $R_{21}$")
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
#
ax1.plot(co21_high, r21_high, "o", color=cm.brg(1./2.5), alpha=0.5, markersize=10, markeredgewidth=0)
ax1.plot(co21_low, r21_low, "o", color="black", alpha=0.5, markersize=10, markeredgewidth=0)
ax1.set_xlim(xlim)
ax1.set_ylim([-1.2,0.5])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_ngc3627.png",dpi=200)
#

###
xlim = [-0.5,1.8]
#
data_high = np.loadtxt(dir_proj + "eps/ngc4321_model_04p0_scatter_cut.txt")
data_low = np.loadtxt(dir_proj + "eps/ngc4321_model_20p0_scatter_cut.txt")
co10_high = data_high[:,0]
co21_high = data_high[:,1]
co10_low = data_low[:,0]
co21_low = data_low[:,1]
r21_high = np.log10(10**co21_high/10**co10_high)
r21_low = np.log10(10**co21_low/10**co10_low)
#
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=8, ncols=8)
plt.subplots_adjust(bottom=0.10, left=0.15, right=0.98, top=0.95)
ax1 = plt.subplot(gs[0:8,0:8])
ax1.grid(axis="both")
ax1.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax1.set_ylabel("log $R_{21}$")
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
#
ax1.plot(co21_high, r21_high, "o", color=cm.brg(2./2.5), alpha=0.5, markersize=10, markeredgewidth=0)
ax1.plot(co21_low, r21_low, "o", color="black", alpha=0.5, markersize=10, markeredgewidth=0)
ax1.set_xlim(xlim)
ax1.set_ylim([-1.2,0.5])
#
plt.savefig(dir_proj + "eps/fig_obs_vs_model_r21_ngc4321.png",dpi=200)
#
import os, re, sys, glob
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib.cm as cm
plt.ioff()


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
bins = 8


#####################
### main
#####################
###
data_scatter_ngc0628 = np.loadtxt(dir_proj + "eps/ngc0628_model_scatter.txt")
co10_scatter = data_scatter_ngc0628[:,0]
co21_scatter = data_scatter_ngc0628[:,1]
#
data_scatter_noise_ngc0628 = np.loadtxt(dir_proj + "eps/ngc0628_model_scatter_noise.txt")
co10_scatter_noise = data_scatter_noise_ngc0628[:,0]
co21_scatter_noise = data_scatter_noise_ngc0628[:,1]

###
xwdith = co10.max() - co10.min()
xlim = [co10.min(), co10.max()]

###
n_scatter, _ = np.histogram(co10_scatter, bins=bins, range=xlim)
sy_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter, range=xlim)
sy2_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter*co21_scatter, range=xlim)
#
n_scatter_noise, _ = np.histogram(co10_scatter_noise, bins=bins, range=xlim)
sy_scatter_noise, _ = np.histogram(co10_scatter_noise, bins=bins, weights=co21_scatter_noise, range=xlim)
sy2_scatter_noise, _ = np.histogram(co10_scatter_noise, bins=bins, weights=co21_scatter_noise*co21_scatter_noise, range=xlim)

###
mean_scatter = sy_scatter / n_scatter
std_scatter = np.sqrt(sy2_scatter/n_scatter - mean_scatter*mean_scatter)
#
mean_scatter_noise = sy_scatter_noise / n_scatter_noise
std_scatter_noise = np.sqrt(sy2_scatter_noise/n_scatter_noise - mean_scatter_noise*mean_scatter_noise)

#
plt.figure(figsize=(12,5))
plt.rcParams["font.size"] = 14
plt.rcParams["legend.fontsize"] = 11
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
gs = gridspec.GridSpec(nrows=5, ncols=15)
ax = plt.subplot(gs[0:5,0:15])
ax.grid(axis='both')
#
ax.plot((_[1:] + _[:-1])/2, std_scatter, "-", color=cm.brg(0/2.5), alpha=0.5, lw=3)
ax.plot((_[1:] + _[:-1])/2, std_scatter_noise, "--", color=cm.brg(0/2.5), alpha=0.5, lw=3)
ax.set_xlim([0.2,1.8])
ax.set_ylim([0,0.4])
#
plt.savefig(dir_proj + "eps/model_scatter.png",dpi=200)

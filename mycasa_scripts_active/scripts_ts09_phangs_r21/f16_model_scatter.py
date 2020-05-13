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
r21_scatter = np.log10(10**co21_scatter/10**co10_scatter)
#
data_scatter_cut_ngc0628 = np.loadtxt(dir_proj + "eps/ngc0628_model_scatter_cut.txt")
co10_scatter_cut = data_scatter_cut_ngc0628[:,0]
co21_scatter_cut = data_scatter_cut_ngc0628[:,1]
r21_scatter_cut = np.log10(10**co21_scatter_cut/10**co10_scatter_cut)

###
xwdith = co10.max() - co10.min()
xlim = [co10.min(), co10.max()]

###
n_scatter, _ = np.histogram(co10_scatter, bins=bins, range=xlim)
sy_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter, range=xlim)
sy2_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter*co21_scatter, range=xlim)
#
n_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, range=xlim)
sy_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, weights=co21_scatter_cut, range=xlim)
sy2_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, weights=co21_scatter_cut*co21_scatter_cut, range=xlim)

###
mean_scatter = sy_scatter / n_scatter
std_scatter = np.sqrt(sy2_scatter/n_scatter - mean_scatter*mean_scatter)
#
mean_scatter_cut = sy_scatter_cut / n_scatter_cut
std_scatter_cut = np.sqrt(sy2_scatter_cut/n_scatter_cut - mean_scatter_cut*mean_scatter_cut)

#
plt.figure(figsize=(12,7))
plt.rcParams["font.size"] = 14
plt.rcParams["legend.fontsize"] = 11
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
gs = gridspec.GridSpec(nrows=5, ncols=15)
ax = plt.subplot(gs[0:5,0:15])
ax.grid(axis='both')
#
ax.plot((_[1:] + _[:-1])/2, std_scatter, "-", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax.plot((_[1:] + _[:-1])/2, std_scatter_cut, "--", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax.set_xlim([0.2,1.8])
ax.set_ylim([0,0.4])
#
plt.savefig(dir_proj + "eps/model_scatter.png",dpi=200)

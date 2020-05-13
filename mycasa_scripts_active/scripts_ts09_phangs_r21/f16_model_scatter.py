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
xwdith_co10 = co10.max() - co10.min()
xlim_co10 = [co10.min(), co10.max()]
xwdith_co21 = co21.max() - co21.min()
xlim_co21 = [co21.min(), co21.max()]

###
n_scatter, _ = np.histogram(co10_scatter, bins=bins, range=xlim_co10)
sy_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter, range=xlim_co10)
sy2_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter*co21_scatter, range=xlim_co10)
#
n_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, range=xlim_co10)
sy_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, weights=co21_scatter_cut, range=xlim_co10)
sy2_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, weights=co21_scatter_cut*co21_scatter_cut, range=xlim_co10)
#
n_r21scatter, _ = np.histogram(co21_scatter, bins=bins, range=xlim_co21)
sy_r21scatter, _ = np.histogram(co21_scatter, bins=bins, weights=r21_scatter, range=xlim_co21)
sy2_r21scatter, _ = np.histogram(co21_scatter, bins=bins, weights=r21_scatter*r21_scatter, range=xlim_co21)
#
n_r21scatter_cut, _ = np.histogram(co21_scatter_cut, bins=bins, range=xlim_co21)
sy_r21scatter_cut, _ = np.histogram(co21_scatter_cut, bins=bins, weights=r21_scatter_cut, range=xlim_co21)
sy2_r21scatter_cut, _ = np.histogram(co21_scatter_cut, bins=bins, weights=r21_scatter_cut*r21_scatter_cut, range=xlim_co21)

###
mean_scatter = sy_scatter / n_scatter
std_scatter = np.sqrt(sy2_scatter/n_scatter - mean_scatter*mean_scatter)
#
mean_scatter_cut = sy_scatter_cut / n_scatter_cut
std_scatter_cut = np.sqrt(sy2_scatter_cut/n_scatter_cut - mean_scatter_cut*mean_scatter_cut)
#
mean_r21scatter = sy_r21scatter / n_r21scatter
std_r21scatter = np.sqrt(sy2_r21scatter/n_r21scatter - mean_r21scatter*mean_r21scatter)
#
mean_r21scatter_cut = sy_r21scatter_cut / n_r21scatter_cut
std_r21scatter_cut = np.sqrt(sy2_r21scatter_cut/n_r21scatter_cut - mean_r21scatter_cut*mean_r21scatter_cut)

#
plt.figure(figsize=(12,5))
plt.rcParams["font.size"] = 14
plt.rcParams["legend.fontsize"] = 11
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
gs = gridspec.GridSpec(nrows=5, ncols=16)
ax1 = plt.subplot(gs[0:5,0:8])
ax2 = plt.subplot(gs[0:5,8:16])
ax1.grid(axis='both')
ax2.grid(axis='both')
#
# ax1
ax1.plot((_[1:] + _[:-1])/2, std_scatter, "-", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax1.plot((_[1:] + _[:-1])/2, std_scatter_cut, "--", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax1.set_xlim([0.2,1.8])
ax1.set_ylim([0,0.4])
# ax2
ax2.plot((_[1:] + _[:-1])/2, std_r21scatter, "-", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax2.plot((_[1:] + _[:-1])/2, std_r21scatter_cut, "--", color=cm.brg(0/2.5), alpha=0.5, lw=4)
#ax2.set_xlim([0.2,1.8])
#ax2.set_ylim([0,0.4])
#
plt.savefig(dir_proj + "eps/model_scatter.png",dpi=200)

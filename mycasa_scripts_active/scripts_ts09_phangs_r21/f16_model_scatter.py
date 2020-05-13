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
data_ngc0628 = np.loadtxt(dir_proj + "eps/ngc0628_model_scatter.txt")
co10 = data_ngc0628[:,0]
co21 = data_ngc0628[:,1]

#
xwdith = co10.max() - co10.min()
xlim = [co10.min(), co10.max()]

#
n, _ = np.histogram(co10, bins=bins, range=xlim)
sy, _ = np.histogram(co10, bins=bins, weights=co21, range=xlim)
sy2, _ = np.histogram(co10, bins=bins, weights=co21*co21, range=xlim)

#
mean = sy / n
std = np.sqrt(sy2/n - mean*mean)

#
plt.figure(figsize=(12,5))
plt.rcParams["font.size"] = 14
plt.rcParams["legend.fontsize"] = 11
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
gs = gridspec.GridSpec(nrows=5, ncols=15)
ax = plt.subplot(gs[0:5,0:15])
ax.grid(axis='both')
#
ax.plot((_[1:] + _[:-1])/2, std, "-", color=cm.brg(0/2.5), alpha=0.5, lw=3)
ax.set_xlim([0.2,1.8])
ax.set_ylim([0,0.2])
#
plt.savefig(dir_proj + "eps/model_scatter.png",dpi=200)

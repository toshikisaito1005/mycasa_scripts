import os, re, sys, glob
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats
plt.ioff()


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"


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
ax.plot((_[1:] + _[:-1])/2, std, "-", color="")
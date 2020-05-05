import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]
nbins = 75
xlim = [0,2.5]


#####################
### functions
#####################
def weighted_median(
    data,
    weights,
    percent,
    ):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    if weights==None:
        w_median = np.median(data)
    else:
        data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
        s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
        midpoint = percent * sum(s_weights)
        if any(weights > midpoint):
            w_median = (data[weights == np.max(weights)])[0]
        else:
            cs_weights = np.cumsum(s_weights)
            idx = np.where(cs_weights <= midpoint)[0][-1]
            if cs_weights[idx] == midpoint:
                w_median = np.mean(s_data[idx:idx+2])
            else:
                w_median = s_data[idx+1]

    return w_median


#####################
### main
#####################
### get data
txtfile = glob.glob(dir_product + "ngc*_parameter_600pc.txt")
#
data_all = []
data_norm_all = []
for i in range(len(txtfile)):
    data = np.loadtxt(txtfile[i])[:,1]
    data = data[data>0]
    data_norm = data / np.median(data)
    data_all.extend(data)
    data_norm_all.extend(data_norm)
#
data_all = np.array(data_all)
data_norm_all = np.array(data_norm_all)


### histogram and stats
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
y_all = y_all / float(sum(y_all))
#
histo_norm = np.histogram(data_norm_all, bins=nbins, range=(xlim), weights=None)
x_norm, y_norm = np.delete(histo_norm[1],-1),histo_norm[0]
y_norm = y_norm / float(sum(y_norm))
#
p16_all = weighted_median(data_all, None, 0.16)
p50_all = weighted_median(data_all, None, 0.5)
p84_all = weighted_median(data_all, None, 0.84)
#
p16_norm = weighted_median(data_norm_all, None, 0.16)
p50_norm = weighted_median(data_norm_all, None, 0.50)
p84_norm = weighted_median(data_norm_all, None, 0.84)


### plot
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=8, ncols=18)
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,10:18])
ax1.grid(axis="both")
ax2.grid(axis="both")
plt.rcParams["font.size"] = 16

# ax1
ylim = [0.0001, y_all.max()*1.1]
ax1.step(x_all, y_all, "black", lw=1, alpha=1.0, where="mid")
ax1.bar(x_all, y_all, lw=0, color="black", alpha=0.2, width=x_all[1]-x_all[0], align="center")
ax1.plot([p50_all, p50_all], [ylim[1]/1.1*1.05, ylim[1]/1.1*1.05])
#
ax1.set_ylim(ylim)

# ax2
ylim = [0.0001, y_norm.max()*1.1]
ax2.step(x_norm, y_norm, "black", lw=1, alpha=1.0, where="mid")
ax2.bar(x_norm, y_norm, lw=0, color="black", alpha=0.2, width=x_norm[1]-x_norm[0], align="center")
#
ax2.set_ylim(ylim)

plt.savefig(dir_product+"histoall.png",dpi=200)

os.system("rm -rf *.last")

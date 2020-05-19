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
#dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]
def_nucleus = [50*44./1.0,50*52./1.3,30*103/1.4]
nbins = 75
xlim = [0,2.5]
r21err = 0.074504715864920745


#####################
### functions
#####################
def weighted_percentile(
    data,
    percentile,
    weights=None,
    ):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    if weights==None:
        w_median = np.percentile(data,percentile*100)
    else:
        data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
        s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
        midpoint = percentile * sum(s_weights)
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
data_nuc_all = []
data_nuc_norm_all = []
data_out_all = []
data_out_norm_all = []
for i in range(len(txtfile)):
    dist = np.loadtxt(txtfile[i])[:,0]
    data = np.loadtxt(txtfile[i])[:,1]
    #
    data = data[data>0]
    dist = dist[data>0]
    #
    data_norm = data / np.median(data)
    data_all.extend(data)
    data_norm_all.extend(data_norm)
    #
    data_nuc = data[dist<=def_nucleus[i]]
    data_nuc_norm = data_nuc / np.median(data_nuc)
    data_nuc_all.extend(data_nuc)
    data_nuc_norm_all.extend(data_nuc_norm)
    #
    data_out = data[dist>def_nucleus[i]]
    data_out_norm = data_out / np.median(data_out)
    data_out_all.extend(data_out)
    data_out_norm_all.extend(data_out_norm)
#
data_all = np.array(data_all)
data_norm_all = np.array(data_norm_all)
data_nuc_all = np.array(data_nuc_all)
data_nuc_norm_all = np.array(data_nuc_norm_all)
data_out_all = np.array(data_out_all)
data_out_norm_all = np.array(data_out_norm_all)


### histogram and stats
## all
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
y_all = y_all / float(sum(y_all))
#
histo_norm = np.histogram(data_norm_all, bins=nbins, range=(xlim), weights=None)
x_norm, y_norm = np.delete(histo_norm[1],-1),histo_norm[0]
y_norm = y_norm / float(sum(y_norm))
## out
#
histo_out_all = np.histogram(data_out_all, bins=nbins, range=(xlim), weights=None)
x_out_all, y_out_all = np.delete(histo_out_all[1],-1),histo_out_all[0]
y_out_all = y_out_all / float(sum(y_out_all))
#
histo_out_norm = np.histogram(data_out_norm_all, bins=nbins, range=(xlim), weights=None)
x_out_norm, y_out_norm = np.delete(histo_out_norm[1],-1),histo_out_norm[0]
y_out_norm = y_out_norm / float(sum(y_out_norm))
## nuc
#
histo_nuc_all = np.histogram(data_nuc_all, bins=nbins, range=(xlim), weights=None)
x_nuc_all, y_nuc_all = np.delete(histo_nuc_all[1],-1),histo_nuc_all[0]
y_nuc_all = y_nuc_all / float(sum(y_nuc_all))
#
histo_nuc_norm = np.histogram(data_nuc_norm_all, bins=nbins, range=(xlim), weights=None)
x_nuc_norm, y_nuc_norm = np.delete(histo_nuc_norm[1],-1),histo_nuc_norm[0]
y_nuc_norm = y_nuc_norm / float(sum(y_nuc_norm))


###
##
#
p16_all = weighted_percentile(data_all, 0.16)
p50_all = weighted_percentile(data_all, 0.5)
p84_all = weighted_percentile(data_all, 0.84)
#
p16_norm = weighted_percentile(data_norm_all, 0.16)
p50_norm = weighted_percentile(data_norm_all, 0.50)
p84_norm = weighted_percentile(data_norm_all, 0.84)
##
#
p16_out_all = weighted_percentile(data_out_all, 0.16)
p50_out_all = weighted_percentile(data_out_all, 0.5)
p84_out_all = weighted_percentile(data_out_all, 0.84)
#
p16_out_norm = weighted_percentile(data_out_norm_all, 0.16)
p50_out_norm = weighted_percentile(data_out_norm_all, 0.50)
p84_out_norm = weighted_percentile(data_out_norm_all, 0.84)


### plot
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=8, ncols=18)
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,10:18])
ax1.grid(axis="both")
ax2.grid(axis="both")
plt.rcParams["font.size"] = 16
#plt.rcParams["legend.fontsize"] = 11

# ax1
ylim = [0.0001, y_all.max()*1.2]
ax1.step(x_all, y_all, "black", lw=1, alpha=1.0, where="mid")
ax1.bar(x_all, y_all, lw=0, color="black", alpha=0.2, width=x_all[1]-x_all[0], align="center")
ax1.plot(p50_all, ylim[1]/1.2*1.05, "o", markeredgewidth=0, c="grey", markersize=7, zorder=1)
ax1.plot([p16_all, p84_all], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "-", c="grey", lw=2, zorder=0)
#
ax1.plot([2.25, 2.25+r21err], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "k-", lw=2)
#
ax1.text(p16_all, ylim[1]/1.2*1.1, str(np.round(p16_all,2)), fontsize=13, ha="right")
ax1.text(p50_all, ylim[1]/1.2*1.1, str(np.round(p50_all,2)), fontsize=13, ha="center")
ax1.text(p84_all, ylim[1]/1.2*1.1, str(np.round(p84_all,2))+"0", fontsize=13, ha="left")
#
ax1.set_xlabel("$R_{21}$")
ax1.set_ylim(ylim)

# ax2
ylim = [0.0001, y_norm.max()*1.2]
ax2.step(x_norm, y_norm, "black", lw=1, alpha=1.0, where="mid")
ax2.bar(x_norm, y_norm, lw=0, color="black", alpha=0.2, width=x_norm[1]-x_norm[0], align="center")
ax2.plot(p50_norm, ylim[1]/1.2*1.05, "o", markeredgewidth=0, c="grey", markersize=7, zorder=1)
ax2.plot([p16_norm, p84_norm], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "-", c="grey", lw=2, zorder=0)
#
ax2.text(p16_norm, ylim[1]/1.2*1.1, str(np.round(p16_norm,2)), fontsize=13, ha="right")
ax2.text(p50_norm, ylim[1]/1.2*1.1, str(np.round(p50_norm,2))+"0", fontsize=13, ha="center")
ax2.text(p84_norm, ylim[1]/1.2*1.1, str(np.round(p84_norm,2)), fontsize=13, ha="left")
#
ax2.set_xlabel("$R_{21}$/Median($R_{21}$)")
ax2.set_ylim(ylim)

plt.savefig(dir_product+"histoall.png",dpi=200)

os.system("rm -rf *.last")

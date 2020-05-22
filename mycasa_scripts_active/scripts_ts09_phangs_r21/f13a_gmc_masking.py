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
nbins = 40
def_nucleus = [50*44./1.0,50*52./1.3,30*103/1.4]
xlim = [0,1.45]


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
txtfile = glob.glob(dir_product + "ngc*_parameter_matched_res.txt")
#
data_all = []
data_inmask_all = []
data_inmask_norm_all = []
data_outmask_all = []
data_outmask_norm_all = []
for i in range(len(txtfile)):
    dist = np.loadtxt(txtfile[i])[:,0]
    data = np.loadtxt(txtfile[i])[:,9]
    gmcmask = np.loadtxt(txtfile[i])[:,16]
    #
    cut_all = np.where(data>0) # np.where((data>0) & (dist>def_nucleus[i]))
    dist = dist[cut_all]
    data = data[cut_all]
    gmcmask = gmcmask[cut_all]
    #
    data_inmask  = data[gmcmask==1]
    data_outmask = data[gmcmask==0]
    #
    data_inmask_norm = data_inmask / np.median(data_inmask)
    data_inmask_all.extend(data_inmask)
    data_inmask_norm_all.extend(data_inmask_norm)
    #
    data_outmask_norm = data_outmask / np.median(data_outmask)
    data_outmask_all.extend(data_outmask)
    data_outmask_norm_all.extend(data_outmask_norm)
    #
    data_all.extend(data)
#
data_inmask_all = np.array(data_inmask_all)
data_inmask_norm_all = np.array(data_inmask_norm_all)
#
data_outmask_all = np.array(data_outmask_all)
data_outmask_norm_all = np.array(data_outmask_norm_all)


### histogram and stats
## all
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
## in
#
histo_inmask_all = np.histogram(data_inmask_all, bins=nbins, range=(xlim), weights=None)
x_ino, y_ino = np.delete(histo_inmask_all[1],-1),histo_inmask_all[0]
x_in = x_ino
y_in = y_ino / float(sum(y_ino))
#
## out
#
histo_outmask_all = np.histogram(data_outmask_all, bins=nbins, range=(xlim), weights=None)
x_outo, y_outo = np.delete(histo_outmask_all[1],-1),histo_outmask_all[0]
x_out = x_outo
y_out = y_outo / float(sum(y_outo))


###
##
#
p16_in = weighted_percentile(data_inmask_all, 0.16)
p50_in = weighted_percentile(data_inmask_all, 0.5)
p84_in = weighted_percentile(data_inmask_all, 0.84)
#
p16_in_norm = weighted_percentile(data_inmask_norm_all, 0.16)
p50_in_norm = weighted_percentile(data_inmask_norm_all, 0.50)
p84_in_norm = weighted_percentile(data_inmask_norm_all, 0.84)
##
#
p16_out = weighted_percentile(data_outmask_all, 0.16)
p50_out = weighted_percentile(data_outmask_all, 0.5)
p84_out = weighted_percentile(data_outmask_all, 0.84)
#
p16_out_norm = weighted_percentile(data_outmask_norm_all, 0.16)
p50_out_norm = weighted_percentile(data_outmask_norm_all, 0.50)
p84_out_norm = weighted_percentile(data_outmask_norm_all, 0.84)



### plot
figure = plt.figure(figsize=(10,2))
gs = gridspec.GridSpec(nrows=8, ncols=17)
plt.subplots_adjust(bottom=0.22, left=0.05, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,9:17])
ax1.grid(axis="x")
ax2.grid(axis="both")
plt.rcParams["font.size"] = 11
plt.rcParams["legend.fontsize"] = 9

# ax1
ylim = [0.0001, np.r_[y_in, y_out].max()*1.4]
ax1.step(x_in, y_in, color=cm.bwr(1/1.), lw=1, alpha=1.0, where="mid")
ax1.bar(x_in, y_in, lw=0, color=cm.bwr(1/1.), alpha=0.2, width=x_in[1]-x_in[0], align="center", label="inside mask")
ax1.plot(p50_in, ylim[1]*0.95, "o", markeredgewidth=0, c=cm.bwr(1/1.), markersize=7, zorder=1)
ax1.plot([p16_in, p84_in], [ylim[1]*0.95, ylim[1]*0.95], "-", c=cm.bwr(1/1.), lw=2, zorder=0)
#
ax1.step(x_out, y_out, color=cm.bwr(0/1.), lw=1, alpha=1.0, where="mid")
ax1.bar(x_out, y_out, lw=0, color=cm.bwr(0/1.), alpha=0.2, width=x_out[1]-x_out[0], align="center", label="outside mask")
ax1.plot(p50_out, ylim[1]*0.88, "o", markeredgewidth=0, c=cm.bwr(0/1.), markersize=7, zorder=1)
ax1.plot([p16_out, p84_out], [ylim[1]*0.88, ylim[1]*0.88], "-", c=cm.bwr(0/1.), lw=2, zorder=0)
#
ax1.set_xlabel("$R_{21}$")
ax1.set_xlim([x_in.min(),x_in.max()])
ax1.set_ylim(ylim)
ax1.set_title("Histogram with Cloud Mask")

# ax2
fraction = y_ino.astype(float)/(y_ino+y_outo)
x_in = x_in[~np.isnan(fraction)]
fraction = fraction[~np.isnan(fraction)]

ax2.step(x_in, fraction, color="black", lw=1, where="mid")
ax2.bar(x_in, fraction, color=cm.bwr(1/1.), alpha=0.2, width=x_in[1]-x_in[0], align="center", lw=0, label="inside mask")
ax2.bar(x_in, -1*(1-fraction), color=cm.bwr(0/1.), alpha=0.2, width=x_in[1]-x_in[0], align="center", lw=0, bottom=1.0, label="outside mask")
#
ax2.set_xlabel("$R_{21}$")
ax2.set_xlim([x_in.min(),x_in.max()])
ax2.set_ylim([0.0001,1])
ax2.legend()
ax2.set_title("Fraction")

# save
plt.savefig(dir_product+"histo_mask_gmc.png",dpi=200)

os.system("rm -rf *.last")

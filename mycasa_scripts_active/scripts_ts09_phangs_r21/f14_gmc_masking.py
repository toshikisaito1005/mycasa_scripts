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
nbins = 75
xlim = [0,2.5]


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
data_inmask_all = []
data_inmask_norm_all = []
data_outmask_all = []
data_outmask_norm_all = []
for i in range(len(txtfile)):
    data = np.loadtxt(txtfile[i])[:,9]
    gmcmask = np.loadtxt(txtfile[i])[:,16]
    #
    data = data[data>0]
    gmcmask = gmcmask[data>0]
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
data_inmask_all = np.array(data_inmask_all)
data_inmask_norm_all = np.array(data_inmask_norm_all)
#
data_outmask_all = np.array(data_outmask_all)
data_outmask_norm_all = np.array(data_outmask_norm_all)


### histogram and stats
## in
#
histo_inmask_all = np.histogram(data_inmask_all, bins=nbins, range=(xlim), weights=None)
x_in, y_in = np.delete(histo_inmask_all[1],-1),histo_inmask_all[0]
y_in = y_in / float(sum(y_in))
#
histo_inmask_norm = np.histogram(data_inmask_norm_all, bins=nbins, range=(xlim), weights=None)
x_in_norm, y_in_norm = np.delete(histo_inmask_norm[1],-1),histo_inmask_norm[0]
y_in_norm = y_in_norm / float(sum(y_in_norm))
#
## out
#
histo_outmask_all = np.histogram(data_outmask_all, bins=nbins, range=(xlim), weights=None)
x_out, y_out = np.delete(histo_outmask_all[1],-1),histo_outmask_all[0]
y_out = y_out / float(sum(y_out))
#
histo_outmask_norm = np.histogram(data_outmask_norm_all, bins=nbins, range=(xlim), weights=None)
x_out_norm, y_out_norm = np.delete(histo_outmask_norm[1],-1),histo_outmask_norm[0]
y_out_norm = y_out_norm / float(sum(y_out_norm))


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
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=8, ncols=17)
plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:4,0:8])
ax2 = plt.subplot(gs[0:4,9:17])
ax3 = plt.subplot(gs[4:8,0:8])
ax4 = plt.subplot(gs[4:8,9:17])
ax1.grid(axis="both")
ax2.grid(axis="both")
ax3.grid(axis="both")
ax4.grid(axis="both")
plt.rcParams["font.size"] = 16
#plt.rcParams["legend.fontsize"] = 11

# ax1
ylim = [0.0001, y_in.max()*1.4]
ax1.step(x_in, y_in, "red", lw=1, alpha=1.0, where="mid")
ax1.bar(x_in, y_in, lw=0, color="red", alpha=0.2, width=x_in[1]-x_in[0], align="center")
ax1.plot(p50_in, ylim[1]/1.2*1.05, "o", markeredgewidth=0, c="red", markersize=7, zorder=1)
ax1.plot([p16_in, p84_in], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "-", c="red", lw=2, zorder=0)
#
ax1.text(p16_in, ylim[1]/1.2*1.1, str(np.round(p16_in,2)), fontsize=13, ha="right")
ax1.text(p50_in, ylim[1]/1.2*1.1, str(np.round(p50_in,2)), fontsize=13, ha="center")
ax1.text(p84_in, ylim[1]/1.2*1.1, str(np.round(p84_in,2)), fontsize=13, ha="left")
#
ax1.set_xlabel("$R_{21}$")
ax1.set_ylim(ylim)

# ax2
ylim = [0.0001, y_in_norm.max()*1.4]
ax2.step(x_in_norm, y_in_norm, "red", lw=1, alpha=1.0, where="mid")
ax2.bar(x_in_norm, y_in_norm, lw=0, color="red", alpha=0.2, width=x_in_norm[1]-x_in_norm[0], align="center")
ax2.plot(p50_in_norm, ylim[1]/1.2*1.05, "o", markeredgewidth=0, c="red", markersize=7, zorder=1)
ax2.plot([p16_in_norm, p84_in_norm], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "-", c="red", lw=2, zorder=0)
#
ax2.text(p16_in_norm, ylim[1]/1.2*1.1, str(np.round(p16_in_norm,2)), fontsize=13, ha="right")
ax2.text(p50_in_norm, ylim[1]/1.2*1.1, str(np.round(p50_in_norm,2))+"0", fontsize=13, ha="center")
ax2.text(p84_in_norm, ylim[1]/1.2*1.1, str(np.round(p84_in_norm,2)), fontsize=13, ha="left")
#
ax2.set_xlabel("$R_{21}$/Median($R_{21}$)")
ax2.set_ylim(ylim)

# ax3
ylim = [0.0001, y_out.max()*1.4]
ax3.step(x_out, y_out, "blue", lw=1, alpha=1.0, where="mid")
ax3.bar(x_out, y_out, lw=0, color="blue", alpha=0.2, width=x_out[1]-x_out[0], align="center")
ax3.plot(p50_out, ylim[1]/1.2*1.05, "o", markeredgewidth=0, c="blue", markersize=7, zorder=1)
ax3.plot([p16_out, p84_out], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "-", c="blue", lw=2, zorder=0)
#
ax3.text(p16_out, ylim[1]/1.2*1.1, str(np.round(p16_out,2)), fontsize=13, ha="right")
ax3.text(p50_out, ylim[1]/1.2*1.1, str(np.round(p50_out,2)), fontsize=13, ha="center")
ax3.text(p84_out, ylim[1]/1.2*1.1, str(np.round(p84_out,2)), fontsize=13, ha="left")
#
ax3.set_xlabel("$R_{21}$")
ax3.set_ylim(ylim)

# ax4
ylim = [0.0001, y_in_norm.max()*1.4]
ax4.step(x_out_norm, y_out_norm, "red", lw=1, alpha=1.0, where="mid")
ax4.bar(x_out_norm, y_out_norm, lw=0, color="red", alpha=0.2, width=x_out_norm[1]-x_out_norm[0], align="center")
ax4.plot(p50_out_norm, ylim[1]/1.2*1.05, "o", markeredgewidth=0, c="red", markersize=7, zorder=1)
ax4.plot([p16_out_norm, p84_out_norm], [ylim[1]/1.2*1.05, ylim[1]/1.2*1.05], "-", c="red", lw=2, zorder=0)
#
ax4.text(p16_out_norm, ylim[1]/1.2*1.1, str(np.round(p16_out_norm,2)), fontsize=13, ha="right")
ax4.text(p50_out_norm, ylim[1]/1.2*1.1, str(np.round(p50_out_norm,2))+"0", fontsize=13, ha="center")
ax4.text(p84_out_norm, ylim[1]/1.2*1.1, str(np.round(p84_out_norm,2)), fontsize=13, ha="left")
#
ax4.set_xlabel("$R_{21}$/Median($R_{21}$)")
ax4.set_ylim(ylim)


plt.savefig(dir_product+"histo_mask_gmc.png",dpi=200)

os.system("rm -rf *.last")

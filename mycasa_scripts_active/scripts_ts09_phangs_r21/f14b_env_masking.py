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
nbins = 50
def_nucleus = [50*44./1.0,50*52./1.3,30*103/1.4]


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
data_mask0_all = []
for i in range(len(txtfile)):
    dist = np.loadtxt(txtfile[i])[:,0]
    data = np.loadtxt(txtfile[i])[:,9]
    gmcmask = np.loadtxt(txtfile[i])[:,17]
    #
    cut_all = np.where(data>0) # np.where((data>0) & (dist>def_nucleus[i]))
    dist = dist[cut_all]
    data = data[cut_all]
    gmcmask = gmcmask[cut_all]
    #
    data_mask0 = data[gmcmask==0]
    data_mask1 = data[gmcmask==1]
    data_mask2 = data[gmcmask==2]
    data_mask3 = data[gmcmask==3]
    data_mask4 = data[gmcmask==4]
    #
    data_inmask_all.extend(data_inmask)
    #
    data_all.extend(data)
    data_mask0_all.extend(data_mask0)
    data_mask1_all.extend(data_mask1)
    data_mask2_all.extend(data_mask2)
    data_mask3_all.extend(data_mask3)
    data_mask4_all.extend(data_mask4)
#
data_all = np.array(data_all)
data_mask0_all = np.array(data_mask0_all)
data_mask1_all = np.array(data_mask1_all)
data_mask2_all = np.array(data_mask2_all)
data_mask3_all = np.array(data_mask3_all)
data_mask4_all = np.array(data_mask4_all)


### histogram and stats
## all
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
## 0
#
histo_mask0_all = np.histogram(data_mask0_all, bins=nbins, range=(xlim), weights=None)
x_0o, y_0o = np.delete(histo_mask0_all[1],-1),histo_mask0_all[0]
x_0 = x_0
y_0 = y_0 / float(sum(y_all))
#
## 1
#
histo_mask1_all = np.histogram(data_mask1_all, bins=nbins, range=(xlim), weights=None)
x_1o, y_1o = np.delete(histo_mask1_all[1],-1),histo_mask1_all[0]
x_1 = x_1
y_1 = y_1 / float(sum(y_all))
#
## 2
#
histo_mask2_all = np.histogram(data_mask2_all, bins=nbins, range=(xlim), weights=None)
x_2o, y_2o = np.delete(histo_mask2_all[1],-1),histo_mask2_all[0]
x_2 = x_2
y_2 = y_2 / float(sum(y_all))
#
## 3
#
histo_mask3_all = np.histogram(data_mask3_all, bins=nbins, range=(xlim), weights=None)
x_3o, y_3o = np.delete(histo_mask3_all[1],-1),histo_mask3_all[0]
x_3 = x_3
y_3 = y_3 / float(sum(y_all))
#
## 4
#
histo_mask4_all = np.histogram(data_mask4_all, bins=nbins, range=(xlim), weights=None)
x_4o, y_4o = np.delete(histo_mask4_all[1],-1),histo_mask4_all[0]
x_4 = x_4
y_4 = y_4 / float(sum(y_all))
#

###
##
#
p16_0 = weighted_percentile(data_mask0_all, 0.16)
p50_0 = weighted_percentile(data_mask0_all, 0.5)
p84_0 = weighted_percentile(data_mask0_all, 0.84)
#
p16_1 = weighted_percentile(data_mask1_all, 0.16)
p50_1 = weighted_percentile(data_mask1_all, 0.5)
p84_1 = weighted_percentile(data_mask1_all, 0.84)
#
p16_2 = weighted_percentile(data_mask2_all, 0.16)
p50_2 = weighted_percentile(data_mask2_all, 0.5)
p84_2 = weighted_percentile(data_mask2_all, 0.84)
#
p16_3 = weighted_percentile(data_mask3_all, 0.16)
p50_3 = weighted_percentile(data_mask3_all, 0.5)
p84_3 = weighted_percentile(data_mask3_all, 0.84)
#
p16_4 = weighted_percentile(data_mask4_all, 0.16)
p50_4 = weighted_percentile(data_mask4_all, 0.5)
p84_4 = weighted_percentile(data_mask4_all, 0.84)



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
ylim = [0.0001, np.r_[y_0, y_0].max()*1.4]
ax1.step(x_0, y_0, "red", lw=1, alpha=1.0, where="mid")
ax1.bar(x_0, y_0, lw=0, color="red", alpha=0.2, width=x_0[1]-x_0[0], align="center", label="inside mask")
ax1.plot(p50_0, ylim[1]*0.95, "o", markeredgewidth=0, c="red", markersize=7, zorder=1)
ax1.plot([p16_0, p84_0], [ylim[1]*0.95, ylim[1]*0.95], "-", c="red", lw=2, zorder=0)
#
ax1.step(x_1, y_1, "blue", lw=1, alpha=1.0, where="mid")
ax1.bar(x_1, y_1, lw=0, color="blue", alpha=0.2, width=x_1[1]-x_1[0], align="center", label="outside mask")
ax1.plot(p50_1, ylim[1]*0.88, "o", markeredgewidth=0, c="blue", markersize=7, zorder=1)
ax1.plot([p16_1, p84_1], [ylim[1]*0.88, ylim[1]*0.88], "-", c="blue", lw=2, zorder=0)
#
ax1.set_xlabel("$R_{21}$")
ax1.set_xlim([x_in.min(),x_in.max()])
ax1.set_ylim(ylim)
ax1.legend()
ax1.set_title("Histogram with Environmental Mask")

# ax2
fraction = y_ino.astype(float)/(y_ino+y_outo)
x_in = x_in[~np.isnan(fraction)]
fraction = fraction[~np.isnan(fraction)]

ax2.step(x_in, fraction, color="black", lw=1, where="mid")
ax2.bar(x_in, fraction, color="red", alpha=0.2, width=x_in[1]-x_in[0], align="center", lw=0)
ax2.bar(x_in, -1*(1-fraction), color="blue", alpha=0.2, width=x_in[1]-x_in[0], align="center", lw=0, bottom=1.0)
#
ax2.set_xlabel("$R_{21}$")
ax2.set_xlim([x_in.min(),x_in.max()])
ax2.set_ylim([0.0001,1])
ax2.legend()
ax2.set_title("Fraction")

# save
plt.savefig(dir_product+"histo_mask_env.png",dpi=200)

os.system("rm -rf *.last")

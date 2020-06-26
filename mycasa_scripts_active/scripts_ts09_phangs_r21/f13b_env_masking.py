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
beamsizes = [4.0,8.0,4.0]


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
data_mask1_all = []
data_mask2_all = []
data_mask3_all = []
#data_mask4_all = []
co10_mask0_all = []
co10_mask1_all = []
co10_mask2_all = []
co10_mask3_all = []
#co10_mask4_all = []
co21_mask0_all = []
co21_mask1_all = []
co21_mask2_all = []
co21_mask3_all = []
#co21_mask4_all = []
for i in range(len(txtfile)):
    dist = np.loadtxt(txtfile[i])[:,0]
    data = np.loadtxt(txtfile[i])[:,9]
    gmcmask = np.loadtxt(txtfile[i])[:,17]
    #
    cut_all = np.where(data>0) # np.where((data>0) & (dist>def_nucleus[i]))
    dist = dist[cut_all]
    data = data[cut_all]
    gmcmask = gmcmask[cut_all]
    co10 = np.loadtxt(txtfile[i])[:,1]
    co21 = np.loadtxt(txtfile[i])[:,3]
    #
    data_mask0 = data[gmcmask==0]
    data_mask1 = data[gmcmask==1]
    data_mask2 = data[gmcmask==2]
    data_mask3 = data[gmcmask>=3]
    #data_mask4 = data[gmcmask==4]
    co10_mask0 = co10[gmcmask==0]
    co10_mask1 = co10[gmcmask==1]
    co10_mask2 = co10[gmcmask==2]
    co10_mask3 = co10[gmcmask>=3]
    #co10_mask4 = data[gmcmask==4]
    co21_mask0 = co21[gmcmask==0]
    co21_mask1 = co21[gmcmask==1]
    co21_mask2 = co21[gmcmask==2]
    co21_mask3 = co21[gmcmask>=3]
    #co21_mask4 = data[gmcmask==4]
    #
    data_all.extend(data)
    data_mask0_all.extend(data_mask0)
    data_mask1_all.extend(data_mask1)
    data_mask2_all.extend(data_mask2)
    data_mask3_all.extend(data_mask3)
    #data_mask4_all.extend(data_mask4)
    #
    Jy2K_co10 = 1.222e6 / beamsizes[i]**2 / 115.27120**2
    Jy2K_co21 = 1.222e6 / beamsizes[i]**2 / 230.53800**2
    co10_mask0_all.append(co10_mask0 * Jy2K_co10)
    co10_mask1_all.append(co10_mask1 * Jy2K_co10)
    co10_mask2_all.append(co10_mask2 * Jy2K_co10)
    co10_mask3_all.append(co10_mask3 * Jy2K_co10)
    #co10_mask4_all.append(co10_mask4 * Jy2K_co10)
    co21_mask0_all.append(co21_mask0 * Jy2K_co21)
    co21_mask1_all.append(co21_mask1 * Jy2K_co21)
    co21_mask2_all.append(co21_mask2 * Jy2K_co21)
    co21_mask3_all.append(co21_mask3 * Jy2K_co21)
    #co21_mask4_all.append(co21_mask4 * Jy2K_co21)
#
data_all = np.array(data_all)
data_mask0_all = np.array(data_mask0_all)
data_mask1_all = np.array(data_mask1_all)
data_mask2_all = np.array(data_mask2_all)
data_mask3_all = np.array(data_mask3_all)
#data_mask4_all = np.array(data_mask4_all)


### histogram and stats
## all
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
## 0
#
histo_mask0_all = np.histogram(data_mask0_all, bins=nbins, range=(xlim), weights=None)
x_0o, y_0o = np.delete(histo_mask0_all[1],-1),histo_mask0_all[0]
x_0 = x_0o
y_0 = y_0o / float(sum(y_0o))
#
## 1
#
histo_mask1_all = np.histogram(data_mask1_all, bins=nbins, range=(xlim), weights=None)
x_1o, y_1o = np.delete(histo_mask1_all[1],-1),histo_mask1_all[0]
x_1 = x_1o
y_1 = y_1o / float(sum(y_1o))
#
## 2
#
histo_mask2_all = np.histogram(data_mask2_all, bins=nbins, range=(xlim), weights=None)
x_2o, y_2o = np.delete(histo_mask2_all[1],-1),histo_mask2_all[0]
x_2 = x_2o
y_2 = y_2o / float(sum(y_2o))
#
## 3
#
histo_mask3_all = np.histogram(data_mask3_all, bins=nbins, range=(xlim), weights=None)
x_3o, y_3o = np.delete(histo_mask3_all[1],-1),histo_mask3_all[0]
x_3 = x_3o
y_3 = y_3o / float(sum(y_3o))
#
"""
## 4
#
histo_mask4_all = np.histogram(data_mask4_all, bins=nbins, range=(xlim), weights=None)
x_4o, y_4o = np.delete(histo_mask4_all[1],-1),histo_mask4_all[0]
x_4 = x_4o
y_4 = y_4o / float(sum(y_4o))
#
"""

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
"""
#
p16_4 = weighted_percentile(data_mask4_all, 0.16)
p50_4 = weighted_percentile(data_mask4_all, 0.5)
p84_4 = weighted_percentile(data_mask4_all, 0.84)
#
p16_34 = weighted_percentile(np.r_[data_mask3_all, data_mask4_all], 0.16)
p50_34 = weighted_percentile(np.r_[data_mask3_all, data_mask4_all], 0.5)
p84_34 = weighted_percentile(np.r_[data_mask3_all, data_mask4_all], 0.84)
"""

###
print("# p16_0 = " + str(np.round(p16_0,2)))
print("# p50_0 = " + str(np.round(p50_0,2)))
print("# p84_0 = " + str(np.round(p84_0,2)))
print("# width_0 = " + str(np.round(p84_0,2) - np.round(p16_0,2)))
print("# p16_1 = " + str(np.round(p16_1,2)))
print("# p50_1 = " + str(np.round(p50_1,2)))
print("# p84_1 = " + str(np.round(p84_1,2)))
print("# width_1 = " + str(np.round(p84_1,2) - np.round(p16_1,2)))
print("# p16_2 = " + str(np.round(p16_2,2)))
print("# p50_2 = " + str(np.round(p50_2,2)))
print("# p84_2 = " + str(np.round(p84_2,2)))
print("# width_2 = " + str(np.round(p84_2,2) - np.round(p16_2,2)))
print("# p16_3 = " + str(np.round(p16_3,2)))
print("# p50_3 = " + str(np.round(p50_3,2)))
print("# p84_3 = " + str(np.round(p84_3,2)))
print("# width_3 = " + str(np.round(p84_3,2) - np.round(p16_3,2)))
"""
print("# p16_34 = " + str(np.round(p16_34,2)))
print("# p50_34 = " + str(np.round(p50_34,2)))
print("# p84_34 = " + str(np.round(p84_34,2)))
print("# width_34 = " + str(np.round(p84_34,2) - np.round(p16_34,2)))
"""

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
ylim = [0.0001, np.r_[y_0, y_1, y_2, y_3].max()*1.4]
ax1.step(x_0, y_0, color=cm.gnuplot(0/3.5), lw=1, alpha=1.0, where="mid")
ax1.bar(x_0, y_0, lw=0, color=cm.gnuplot(0/3.5), alpha=0.2, width=x_0[1]-x_0[0], align="center", label="inter-arm")
ax1.plot(p50_0, ylim[1]*0.95, "o", markeredgewidth=0, c=cm.gnuplot(0/3.5), markersize=7, zorder=1)
ax1.plot([p16_0, p84_0], [ylim[1]*0.95, ylim[1]*0.95], "-", c=cm.gnuplot(0/3.5), lw=2, zorder=0)
#
ax1.step(x_1, y_1, color=cm.gnuplot(1/3.5), lw=1, alpha=1.0, where="mid")
ax1.bar(x_1, y_1, lw=0, color=cm.gnuplot(1/3.5), alpha=0.2, width=x_1[1]-x_1[0], align="center", label="arm")
ax1.plot(p50_1, ylim[1]*0.88, "o", markeredgewidth=0, c=cm.gnuplot(1/3.5), markersize=7, zorder=1)
ax1.plot([p16_1, p84_1], [ylim[1]*0.88, ylim[1]*0.88], "-", c=cm.gnuplot(1/3.5), lw=2, zorder=0)
#
ax1.step(x_2, y_2, color=cm.gnuplot(2/3.5), lw=1, alpha=1.0, where="mid")
ax1.bar(x_2, y_2, lw=0, color=cm.gnuplot(2/3.5), alpha=0.2, width=x_2[1]-x_2[0], align="center", label="bulge")
ax1.plot(p50_2, ylim[1]*0.81, "o", markeredgewidth=0, c=cm.gnuplot(2/3.5), markersize=7, zorder=1)
ax1.plot([p16_2, p84_2], [ylim[1]*0.81, ylim[1]*0.81], "-", c=cm.gnuplot(2/3.5), lw=2, zorder=0)
#
ax1.step(x_3, y_3, color=cm.gnuplot(3/3.5), lw=1, alpha=1.0, where="mid")
ax1.bar(x_3, y_3, lw=0, color=cm.gnuplot(3/3.5), alpha=0.2, width=x_3[1]-x_3[0], align="center", label="bar + bar-end")
ax1.plot(p50_3, ylim[1]*0.74, "o", markeredgewidth=0, c=cm.gnuplot(3/3.5), markersize=7, zorder=1)
ax1.plot([p16_3, p84_3], [ylim[1]*0.74, ylim[1]*0.74], "-", c=cm.gnuplot(3/3.5), lw=2, zorder=0)
"""
#
ax1.step(x_4, y_4, color=cm.gnuplot(4/5.), lw=1, alpha=1.0, where="mid")
ax1.bar(x_4, y_4, lw=0, color=cm.gnuplot(4/5.), alpha=0.2, width=x_4[1]-x_4[0], align="center", label="bar-end")
ax1.plot(p50_4, ylim[1]*0.67, "o", markeredgewidth=0, c=cm.gnuplot(4/5.), markersize=7, zorder=1)
ax1.plot([p16_4, p84_4], [ylim[1]*0.67, ylim[1]*0.67], "-", c=cm.gnuplot(4/5.), lw=2, zorder=0)
"""
#
ax1.set_xlabel("$R_{21}$")
ax1.set_xlim([x_0.min(),x_0.max()])
ax1.set_ylim(ylim)
ax1.set_title("Histogram with Environmental Mask")

# ax2
fraction_0 = y_0.astype(float)/(y_0+y_1+y_2+y_3)
x_0 = x_0[~np.isnan(fraction_0)]
fraction_0 = fraction_0[~np.isnan(fraction_0)]
fraction_1 = y_1.astype(float)/(y_0+y_1+y_2+y_3)
fraction_1 = fraction_1[~np.isnan(fraction_1)]
fraction_2 = y_2.astype(float)/(y_0+y_1+y_2+y_3)
fraction_2 = fraction_2[~np.isnan(fraction_2)]
fraction_3 = y_3.astype(float)/(y_0+y_1+y_2+y_3)
fraction_3 = fraction_3[~np.isnan(fraction_3)]
#
ax2.step(x_0, fraction_0, color="black", lw=1, where="mid")
ax2.step(x_0, fraction_0+fraction_1, color="black", lw=1, where="mid")
ax2.step(x_0, fraction_0+fraction_1+fraction_2, color="black", lw=1, where="mid")
ax2.bar(x_0, fraction_0, color=cm.gnuplot(0/3.5), alpha=0.2, width=x_0[1]-x_0[0], align="center", lw=0, label="interarm")
ax2.bar(x_0, fraction_1, bottom=fraction_0, color=cm.gnuplot(1/3.5), alpha=0.2, width=x_1[1]-x_1[0], align="center", lw=0, label="arm")
ax2.bar(x_0, fraction_2, bottom=fraction_0+fraction_1, color=cm.gnuplot(2/3.5), alpha=0.2, width=x_2[1]-x_2[0], align="center", lw=0, label="bulge")
ax2.bar(x_0, fraction_3, bottom=fraction_0+fraction_1+fraction_2, color=cm.gnuplot(3/3.5), alpha=0.2, width=x_3[1]-x_3[0], align="center", lw=0, label="bar/bar-end")

#
ax2.set_xlabel("$R_{21}$")
ax2.set_xlim([x_0.min(),x_0.max()])
ax2.set_ylim([0.0001,1])
ax2.legend(ncol=2)
ax2.set_title("Fraction")

# save
plt.savefig(dir_product+"histo_mask_env.png",dpi=200)


# plot scatter
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=8, ncols=24)
plt.subplots_adjust(bottom=0.22, left=0.05, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:8,1:8])
ax2 = plt.subplot(gs[0:8,9:16])
ax3 = plt.subplot(gs[0:8,17:24])
ax1.grid(axis="both")
ax2.grid(axis="both")
ax3.grid(axis="both")
plt.rcParams["font.size"] = 11
plt.rcParams["legend.fontsize"] = 9
#
xlim = [-0.0,2.1]
ylim = [-1.2,0.5]
levels = [20,40,80]
ax1.scatter(np.log10(co21_mask0_all[0]),np.log10(co21_mask0_all[0]/co10_mask0_all[0]), c=cm.gnuplot(0/3.5), alpha=0.2, linewidths=0, s=5)
ax1.scatter(np.log10(co21_mask1_all[0]),np.log10(co21_mask1_all[0]/co10_mask1_all[0]), c=cm.gnuplot(1/3.5), alpha=0.2, linewidths=0, s=5)
ax1.scatter(np.log10(co21_mask2_all[0]),np.log10(co21_mask2_all[0]/co10_mask2_all[0]), c=cm.gnuplot(2/3.5), alpha=0.2, linewidths=0, s=5)
ax1.scatter(np.log10(co21_mask3_all[0]),np.log10(co21_mask3_all[0]/co10_mask3_all[0]), c=cm.gnuplot(3/3.5), alpha=0.2, linewidths=0, s=5)
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
#
H, xedges, yedges = np.histogram2d(np.log10(co21_inmask_all[1]/co10_inmask_all[1]),np.log10(co21_inmask_all[1]),bins=20,range=([-1.0,0.7],[-0.0,3.2]))
extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
ax2.contour(H/H.max()*100,levels=levels,extent=extent,colors=["red"],zorder=1,linewidths=1.5,alpha=1.0)

#
xlim = [-0.0,3.2]
ylim = [-1.0,0.7]
levels = [20,40,80]
ax2.scatter(np.log10(co21_mask0_all[1]),np.log10(co21_mask0_all[1]/co10_mask0_all[1]), c=cm.gnuplot(0/3.5), alpha=0.2, linewidths=0, s=5)
ax2.scatter(np.log10(co21_mask1_all[1]),np.log10(co21_mask1_all[1]/co10_mask1_all[1]), c=cm.gnuplot(1/3.5), alpha=0.2, linewidths=0, s=5)
ax2.scatter(np.log10(co21_mask2_all[1]),np.log10(co21_mask2_all[1]/co10_mask2_all[1]), c=cm.gnuplot(2/3.5), alpha=0.2, linewidths=0, s=5)
ax2.scatter(np.log10(co21_mask3_all[1]),np.log10(co21_mask3_all[1]/co10_mask3_all[1]), c=cm.gnuplot(3/3.5), alpha=0.2, linewidths=0, s=5)
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)

#
xlim = [-0.0,3.0]
ylim = [-1.2,0.7]
levels = [20,40,80]
ax3.scatter(np.log10(co21_mask0_all[2]),np.log10(co21_mask0_all[2]/co10_mask0_all[2]), c=cm.gnuplot(0/3.5), alpha=0.2, linewidths=0, s=5)
ax3.scatter(np.log10(co21_mask1_all[2]),np.log10(co21_mask1_all[2]/co10_mask1_all[2]), c=cm.gnuplot(1/3.5), alpha=0.2, linewidths=0, s=5)
ax3.scatter(np.log10(co21_mask2_all[2]),np.log10(co21_mask2_all[2]/co10_mask2_all[2]), c=cm.gnuplot(2/3.5), alpha=0.2, linewidths=0, s=5)
ax3.scatter(np.log10(co21_mask3_all[2]),np.log10(co21_mask3_all[2]/co10_mask3_all[2]), c=cm.gnuplot(3/3.5), alpha=0.2, linewidths=0, s=5)
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)
# save
plt.savefig(dir_product+"scatter_mask_env.png",dpi=200)

os.system("rm -rf *.last")

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
xlim = [0,2.2]
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
data_inmask_all = []
data_inmask_norm_all = []
data_outmask_all = []
data_outmask_norm_all = []
co10_inmask_all = []
co21_inmask_all = []
co10_outmask_all = []
co21_outmask_all = []
for i in range(len(txtfile)):
    dist = np.loadtxt(txtfile[i])[:,0]
    data = np.loadtxt(txtfile[i])[:,9]
    gmcmask = np.loadtxt(txtfile[i])[:,18]
    co10 = np.loadtxt(txtfile[i])[:,1]
    co21 = np.loadtxt(txtfile[i])[:,3]
    #
    cut_all = np.where(data>0) # np.where((data>0) & (dist>def_nucleus[i]))
    dist = dist[cut_all]
    data = data[cut_all]
    gmcmask = gmcmask[cut_all]
    co10 = co10[cut_all]
    co21 = co21[cut_all]
    #
    data_inmask = data[gmcmask==1]
    co10_inmask = co10[gmcmask==1]
    co21_inmask = co21[gmcmask==1]
    #
    data_outmask = data[gmcmask==0]
    co10_outmask = co10[gmcmask==0]
    co21_outmask = co21[gmcmask==0]
    #
    data_inmask_norm = data_inmask / np.median(data)
    data_inmask_all.extend(data_inmask)
    data_inmask_norm_all.extend(data_inmask_norm)
    #
    data_outmask_norm = data_outmask / np.median(data)
    data_outmask_all.extend(data_outmask)
    data_outmask_norm_all.extend(data_outmask_norm)
    #
    data_all.extend(data)
    #
    Jy2K_co10 = 1.222e6 / beamsizes[i]**2 / 115.27120**2
    Jy2K_co21 = 1.222e6 / beamsizes[i]**2 / 230.53800**2
    co10_inmask_all.append(co10_inmask * Jy2K_co10)
    co21_inmask_all.append(co21_inmask * Jy2K_co21)
    co10_outmask_all.append(co10_outmask * Jy2K_co10)
    co21_outmask_all.append(co21_outmask * Jy2K_co21)
#
data_inmask_all = np.array(data_inmask_all)
data_inmask_norm_all = np.array(data_inmask_norm_all)
#
data_outmask_all = np.array(data_outmask_all)
data_outmask_norm_all = np.array(data_outmask_norm_all)


### histogram and stats
xlim
## all
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
## in
#
histo_inmask_all = np.histogram(data_inmask_norm_all, bins=nbins, range=(xlim), weights=None)
x_ino, y_ino = np.delete(histo_inmask_all[1],-1),histo_inmask_all[0]
x_in = x_ino
y_in = y_ino / float(sum(y_ino))
#
## out
#
histo_outmask_all = np.histogram(data_outmask_norm_all, bins=nbins, range=(xlim), weights=None)
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


### print
print("# p16_in = " + str(np.round(p16_in,2)))
print("# p50_in = " + str(np.round(p50_in,2)))
print("# p84_in = " + str(np.round(p84_in,2)))
print("# width_in = " + str(np.round(p84_in,2) - np.round(p16_in,2)))
print("# p16_out = " + str(np.round(p16_out,2)))
print("# p50_out = " + str(np.round(p50_out,2)))
print("# p84_out = " + str(np.round(p84_out,2)))
print("# width_out = " + str(np.round(p84_out,2) - np.round(p16_out,2)))


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
ax1.step(x_in, y_in, color=cm.PiYG(1/1.), lw=1, alpha=1.0, where="mid")
ax1.bar(x_in, y_in, lw=0, color=cm.PiYG(1/1.), alpha=0.2, width=x_in[1]-x_in[0], align="center", label="inside mask")
ax1.plot(p50_in_norm, ylim[1]*0.95, "o", markeredgewidth=0, c=cm.PiYG(1/1.), markersize=7, zorder=1)
ax1.plot([p16_in_norm, p84_in_norm], [ylim[1]*0.95, ylim[1]*0.95], "-", c=cm.PiYG(1/1.), lw=2, zorder=0)
#
ax1.step(x_out, y_out, color=cm.PiYG(0/1.), lw=1, alpha=1.0, where="mid")
ax1.bar(x_out, y_out, lw=0, color=cm.PiYG(0/1.), alpha=0.2, width=x_out[1]-x_out[0], align="center", label="outside mask")
ax1.plot(p50_out_norm, ylim[1]*0.88, "o", markeredgewidth=0, c=cm.PiYG(0/1.), markersize=7, zorder=1)
ax1.plot([p16_out_norm, p84_out_norm], [ylim[1]*0.88, ylim[1]*0.88], "-", c=cm.PiYG(0/1.), lw=2, zorder=0)
#
ax1.set_xlabel("Normed $R_{21}$")
ax1.set_xlim([x_in.min(),x_in.max()])
ax1.set_ylim(ylim)
ax1.legend()
ax1.set_title("HII Region Masked Histogram")

# ax2
fraction = y_ino.astype(float)/(y_ino+y_outo)
x_in = x_in[~np.isnan(fraction)]
fraction = fraction[~np.isnan(fraction)]

ax2.step(x_in, fraction, color="black", lw=1, where="mid")
ax2.bar(x_in, fraction, color=cm.PiYG(1/1.), alpha=0.2, width=x_in[1]-x_in[0], align="center", lw=0, label="inside mask")
ax2.bar(x_in, -1*(1-fraction), color=cm.PiYG(0/1.), alpha=0.2, width=x_in[1]-x_in[0], align="center", lw=0, bottom=1.0, label="outside mask")
#
ax2.set_xlabel("Normed $R_{21}$")
ax2.set_xlim([x_in.min(),x_in.max()])
ax2.set_ylim([0.0001,1])
ax2.set_title("Fraction")

# save
plt.savefig(dir_product+"histo_mask_piechart.png",dpi=200)


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
ax1.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax2.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax3.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax1.set_ylabel("log $R_{21}$")
plt.rcParams["font.size"] = 11
plt.rcParams["legend.fontsize"] = 9
#
xlim = [-0.5,1.8]
ylim = [-1.2,0.5]
levels = [10,45,80]
bins_contour = 20
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1.legend(loc="upper left")
ax1.text(xlim[0]+(xlim[1]-xlim[0])*0.03, ylim[0]+(ylim[1]-ylim[0])*0.9, "NGC 0628 (HII Region Mask)")
co21_masks_all = [np.log10(co21_inmask_all[0]), np.log10(co21_outmask_all[0])]
r21_masks_all = [np.log10(co21_inmask_all[0]/co10_inmask_all[0]), np.log10(co21_outmask_all[0]/co10_outmask_all[0])]
for i in range(2):
    ax1.scatter(co21_masks_all[i], r21_masks_all[i], c="grey", alpha=0.2, linewidths=0, s=5, zorder=1)
    H, xedges, yedges = np.histogram2d(r21_masks_all[i],co21_masks_all[i],bins=bins_contour,range=(ylim,xlim))
    extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
    ax1.contour(H/H.max()*100,levels=levels,extent=extent,colors=[cm.PiYG(abs(i/1.-1))],zorder=1e9,linewidths=2,alpha=1.0)

#
xlim = [-0.3,2.7]
ylim = [-1.0,0.7]
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
ax2.legend(loc="upper left")
ax2.text(xlim[0]+(xlim[1]-xlim[0])*0.03, ylim[0]+(ylim[1]-ylim[0])*0.9, "NGC 3627 (HII Region Mask)")
co21_masks_all = [np.log10(co21_inmask_all[1]), np.log10(co21_outmask_all[1])]
r21_masks_all = [np.log10(co21_inmask_all[1]/co10_inmask_all[1]), np.log10(co21_outmask_all[1]/co10_outmask_all[1])]
for i in range(2):
    ax2.scatter(co21_masks_all[i], r21_masks_all[i], c="grey", alpha=0.2, linewidths=0, s=5, zorder=1)
    H, xedges, yedges = np.histogram2d(r21_masks_all[i],co21_masks_all[i],bins=bins_contour,range=(ylim,xlim))
    extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
    ax2.contour(H/H.max()*100,levels=levels,extent=extent,colors=[cm.PiYG(abs(i/1.-1))],zorder=1e9,linewidths=2,alpha=1.0)

#
xlim = [-0.3,2.7]
ylim = [-1.2,0.4]
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)
ax3.legend(loc="upper left")
ax3.text(xlim[0]+(xlim[1]-xlim[0])*0.03, ylim[0]+(ylim[1]-ylim[0])*0.9, "NGC 4321 (HII Region Mask)")
co21_masks_all = [np.log10(co21_inmask_all[2]), np.log10(co21_outmask_all[2])]
r21_masks_all = [np.log10(co21_inmask_all[2]/co10_inmask_all[2]), np.log10(co21_outmask_all[2]/co10_outmask_all[2])]
for i in range(2):
    ax3.scatter(co21_masks_all[i], r21_masks_all[i], c="grey", alpha=0.2, linewidths=0, s=5, zorder=1)
    H, xedges, yedges = np.histogram2d(r21_masks_all[i],co21_masks_all[i],bins=bins_contour,range=(ylim,xlim))
    extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
    ax3.contour(H/H.max()*100,levels=levels,extent=extent,colors=[cm.PiYG(abs(i/1.-1))],zorder=1e9,linewidths=2,alpha=1.0)
# save
plt.savefig(dir_product+"scatter_piechart.png",dpi=200)

os.system("rm -rf *.last")

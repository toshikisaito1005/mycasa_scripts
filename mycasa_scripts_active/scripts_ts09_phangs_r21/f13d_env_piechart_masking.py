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
data_mask0in_all = []
data_mask1in_all = []
data_mask2in_all = []
data_mask3in_all = []
data_mask0out_all = []
data_mask1out_all = []
data_mask2out_all = []
data_mask3out_all = []

co10_mask0in_all = []
co10_mask1in_all = []
co10_mask2in_all = []
co10_mask3in_all = []
co10_mask0out_all = []
co10_mask1out_all = []
co10_mask2out_all = []
co10_mask3out_all = []

co21_mask0in_all = []
co21_mask1in_all = []
co21_mask2in_all = []
co21_mask3in_all = []
co21_mask0out_all = []
co21_mask1out_all = []
co21_mask2out_all = []
co21_mask3out_all = []
for i in range(len(txtfile)):
    dist = np.loadtxt(txtfile[i])[:,0]
    data = np.loadtxt(txtfile[i])[:,9]
    gmcmask = np.loadtxt(txtfile[i])[:,17]
    piechartmask = np.loadtxt(txtfile[i])[:,18]
    #
    cut_all = np.where(data>0) # np.where((data>0) & (dist>def_nucleus[i]))
    dist = dist[cut_all]
    data = data[cut_all]
    gmcmask = gmcmask[cut_all]
    piechartmask = piechartmask[cut_all]
    co10 = np.loadtxt(txtfile[i])[:,1]
    co21 = np.loadtxt(txtfile[i])[:,3]
    #
    data_mask0in = data[np.where((gmcmask==0) & (piechartmask==1))]
    data_mask1in = data[np.where((gmcmask==1) & (piechartmask==1))]
    data_mask2in = data[np.where((gmcmask==2) & (piechartmask==1))]
    data_mask3in = data[np.where((gmcmask>=3) & (piechartmask==1))]
    data_mask0out = data[np.where((gmcmask==0) & (piechartmask==0))]
    data_mask1out = data[np.where((gmcmask==1) & (piechartmask==0))]
    data_mask2out = data[np.where((gmcmask==2) & (piechartmask==0))]
    data_mask3out = data[np.where((gmcmask>=3) & (piechartmask==0))]
    #
    co10_mask0in = co10[np.where((gmcmask==0) & (piechartmask==1))]
    co10_mask1in = co10[np.where((gmcmask==1) & (piechartmask==1))]
    co10_mask2in = co10[np.where((gmcmask==2) & (piechartmask==1))]
    co10_mask3in = co10[np.where((gmcmask>=3) & (piechartmask==1))]
    co10_mask0out = co10[np.where((gmcmask==0) & (piechartmask==0))]
    co10_mask1out = co10[np.where((gmcmask==1) & (piechartmask==0))]
    co10_mask2out = co10[np.where((gmcmask==2) & (piechartmask==0))]
    co10_mask3out = co10[np.where((gmcmask>=3) & (piechartmask==0))]
    #
    co21_mask0in = co21[np.where((gmcmask==0) & (piechartmask==1))]
    co21_mask1in = co21[np.where((gmcmask==1) & (piechartmask==1))]
    co21_mask2in = co21[np.where((gmcmask==2) & (piechartmask==1))]
    co21_mask3in = co21[np.where((gmcmask>=3) & (piechartmask==1))]
    co21_mask0out = co21[np.where((gmcmask==0) & (piechartmask==0))]
    co21_mask1out = co21[np.where((gmcmask==1) & (piechartmask==0))]
    co21_mask2out = co21[np.where((gmcmask==2) & (piechartmask==0))]
    co21_mask3out = co21[np.where((gmcmask>=3) & (piechartmask==0))]
    #
    data_all.extend(data)
    data_mask0in_all.extend(data_mask0in)
    data_mask1in_all.extend(data_mask1in)
    data_mask2in_all.extend(data_mask2in)
    data_mask3in_all.extend(data_mask3in)
    data_mask0out_all.extend(data_mask0out)
    data_mask1out_all.extend(data_mask1out)
    data_mask2out_all.extend(data_mask2out)
    data_mask3out_all.extend(data_mask3out)
    #
    Jy2K_co10 = 1.222e6 / beamsizes[i]**2 / 115.27120**2
    Jy2K_co21 = 1.222e6 / beamsizes[i]**2 / 230.53800**2
    co10_mask0in_all.append(co10_mask0in * Jy2K_co10)
    co10_mask1in_all.append(co10_mask1in * Jy2K_co10)
    co10_mask2in_all.append(co10_mask2in * Jy2K_co10)
    co10_mask3in_all.append(co10_mask3in * Jy2K_co10)
    co10_mask0out_all.append(co10_mask0out * Jy2K_co10)
    co10_mask1out_all.append(co10_mask1out * Jy2K_co10)
    co10_mask2out_all.append(co10_mask2out * Jy2K_co10)
    co10_mask3out_all.append(co10_mask3out * Jy2K_co10)
    #
    co21_mask0in_all.append(co21_mask0in * Jy2K_co21)
    co21_mask1in_all.append(co21_mask1in * Jy2K_co21)
    co21_mask2in_all.append(co21_mask2in * Jy2K_co21)
    co21_mask3in_all.append(co21_mask3in * Jy2K_co21)
    co21_mask0out_all.append(co21_mask0out * Jy2K_co21)
    co21_mask1out_all.append(co21_mask1out * Jy2K_co21)
    co21_mask2out_all.append(co21_mask2out * Jy2K_co21)
    co21_mask3out_all.append(co21_mask3out * Jy2K_co21)



# plot scatter
figure = plt.figure(figsize=(10,3))
gs = gridspec.GridSpec(nrows=8, ncols=32)
plt.subplots_adjust(bottom=0.22, left=0.05, right=0.98, top=0.88)
ax1 = plt.subplot(gs[0:8,1:8])
ax2 = plt.subplot(gs[0:8,9:16])
ax3 = plt.subplot(gs[0:8,17:24])
ax4 = plt.subplot(gs[0:8,25:32])
ax1.grid(axis="both")
ax2.grid(axis="both")
ax3.grid(axis="both")
ax4.grid(axis="both")
ax1.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax2.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax3.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax4.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax1.set_ylabel("log $R_{21}$")
plt.rcParams["font.size"] = 11
plt.rcParams["legend.fontsize"] = 9
#
axlist = [ax1,ax2,ax3,ax4,ax1,ax2,ax3,ax4]
xlim = [-0.5,1.8]
ylim = [-1.2,0.5]
levels = [10,45,80]
bins_contour = 20
colors = [cm.gnuplot(0/3.5),cm.gnuplot(1/3.5),cm.gnuplot(2/3.5),cm.gnuplot(3/3.5),cm.gnuplot(0/3.5),cm.gnuplot(1/3.5),cm.gnuplot(2/3.5),cm.gnuplot(3/3.5)]
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
co21_masks_all = [np.log10(co21_mask0in_all[0]), np.log10(co21_mask1in_all[0]), np.log10(co21_mask2in_all[0]), np.log10(co21_mask3in_all[0]),
                  np.log10(co21_mask0out_all[0]), np.log10(co21_mask1out_all[0]), np.log10(co21_mask2out_all[0]), np.log10(co21_mask3out_all[0])]
r21_masks_all = [np.log10(co21_mask0in_all[0]/co10_mask0in_all[0]), np.log10(co21_mask1in_all[0]/co10_mask1in_all[0]), np.log10(co21_mask2in_all[0]/co10_mask2in_all[0]), np.log10(co21_mask3in_all[0]/co10_mask3in_all[0]),
                 np.log10(co21_mask0out_all[0]/co10_mask0out_all[0]), np.log10(co21_mask1out_all[0]/co10_mask1out_all[0]), np.log10(co21_mask2out_all[0]/co10_mask2out_all[0]), np.log10(co21_mask3out_all[0]/co10_mask3out_all[0])]
for i in range(8):
    ax = axlist[i]
    ax.scatter(co21_masks_all[i], r21_masks_all[i], c="grey", alpha=0.2, linewidths=0, s=5, zorder=1)
    H, xedges, yedges = np.histogram2d(r21_masks_all[i],co21_masks_all[i],bins=bins_contour,range=(ylim,xlim))
    extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
    if i<=3:
        ax.contour(H/H.max()*100,levels=levels,extent=extent,colors=[colors[i]],zorder=1e9,linewidths=2,alpha=1.0)
    else:
        ax.contour(H/H.max()*100,levels=levels,extent=extent,colors=[colors[i]],zorder=1e9,linewidths=1,alpha=0.5)

# save
plt.savefig(dir_product+"scatter_mask_env_piechart_ngc0628.png",dpi=200)


#
xlim = [-0.3,2.7]
ylim = [-1.0,0.7]
ax2.set_xlim(xlim)
ax2.set_ylim(ylim)
co21_masks_all = [np.log10(co21_mask0in_all[1]), np.log10(co21_mask1in_all[1]), np.log10(co21_mask2in_all[1]), np.log10(co21_mask3in_all[1]),
                  np.log10(co21_mask0out_all[1]), np.log10(co21_mask1out_all[1]), np.log10(co21_mask2out_all[1]), np.log10(co21_mask3out_all[1])]
r21_masks_all = [np.log10(co21_mask0in_all[1]/co10_mask0in_all[1]), np.log10(co21_mask1in_all[1]/co10_mask1in_all[1]), np.log10(co21_mask2in_all[1]/co10_mask2in_all[1]), np.log10(co21_mask3in_all[1]/co10_mask3in_all[1]),
                 np.log10(co21_mask0out_all[1]/co10_mask0out_all[1]), np.log10(co21_mask1out_all[1]/co10_mask1out_all[1]), np.log10(co21_mask2out_all[1]/co10_mask2out_all[1]), np.log10(co21_mask3out_all[1]/co10_mask3out_all[1])]
for i in range(8):
    ax2.scatter(co21_masks_all[i], r21_masks_all[i], c="grey", alpha=0.2, linewidths=0, s=5, zorder=1)
    H, xedges, yedges = np.histogram2d(r21_masks_all[i],co21_masks_all[i],bins=bins_contour,range=(ylim,xlim))
    extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
    if i<=3:
        ax.contour(H/H.max()*100,levels=levels,extent=extent,colors=[colors[i]],zorder=1e9,linewidths=2,alpha=1.0)
    else:
        ax.contour(H/H.max()*100,levels=levels,extent=extent,colors=[colors[i]],zorder=1e9,linewidths=1,alpha=0.5)

# save
plt.savefig(dir_product+"scatter_mask_env_piechart_ngc3627.png",dpi=200)

"""
#
xlim = [-0.3,2.7]
ylim = [-1.2,0.4]
ax3.set_xlim(xlim)
ax3.set_ylim(ylim)
co21_masks_all = [np.log10(co21_mask0in_all[2]), np.log10(co21_mask1in_all[2]), np.log10(co21_mask2in_all[2]), np.log10(co21_mask3in_all[2]),
                  np.log10(co21_mask0out_all[2]), np.log10(co21_mask1out_all[2]), np.log10(co21_mask2out_all[2]), np.log10(co21_mask3out_all[2])]
r21_masks_all = [np.log10(co21_mask0in_all[2]/co10_mask0in_all[2]), np.log10(co21_mask1in_all[2]/co10_mask1in_all[2]), np.log10(co21_mask2in_all[2]/co10_mask2in_all[2]), np.log10(co21_mask3in_all[2]/co10_mask3in_all[2]),
                 np.log10(co21_mask0out_all[2]/co10_mask0out_all[2]), np.log10(co21_mask1out_all[2]/co10_mask1out_all[2]), np.log10(co21_mask2out_all[2]/co10_mask2out_all[2]), np.log10(co21_mask3out_all[2]/co10_mask3out_all[2])]
for i in range(8):
    ax3.scatter(co21_masks_all[i], r21_masks_all[i], c="grey", alpha=0.2, linewidths=0, s=5, zorder=1)
    H, xedges, yedges = np.histogram2d(r21_masks_all[i],co21_masks_all[i],bins=bins_contour,range=(ylim,xlim))
    extent = [yedges[0],yedges[-1],xedges[0],xedges[-1]]
    if i%2==0:
        ax3.contour(H/H.max()*100,levels=levels,extent=extent,colors=[colors[i]],zorder=1e9,linewidths=2,alpha=1.0)
    else:
        ax3.contour(H/H.max()*100,levels=levels,extent=extent,colors=[colors[i]],zorder=1e9,linewidths=1,alpha=1.0)
"""

os.system("rm -rf *.last")

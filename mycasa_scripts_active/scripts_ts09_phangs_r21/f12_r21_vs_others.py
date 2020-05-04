import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]


#####################
### functions
#####################
def get_data(txtdata,col):
    """
    """
    data = np.loadtxt(txtdata)
    #
    dist = data[:,0]
    #
    r21 = data[:,1]
    r21 = r21 / np.median(r21[r21>0])
    #
    r21err = data[:,2]
    co21 = data[:,3]
    co21snr = data[:,4]
    co10 = data[:,5]
    co10snr = data[:,6]
    tpeak = data[:,7]
    disp = data[:,8]
    w1 = data[:,9]
    w2 = data[:,10]
    w3 = data[:,11]
    mask = data[:,12]
    #
    data4use = data[:,col]
    data4use[np.isinf(data4use)] = 0
    data4use[np.isnan(data4use)] = 0
    #xlim = [0,data4use.max()*1.1]
    #
    cut_co21 = (co21 != 0)
    cut_4use = (data4use != 0)
    cut_low = (mask==-1)
    cut_mid = (mask==0)
    cut_high = (mask==1)
    cut_low = np.where((cut_co21) & (cut_low) & (cut_4use))
    cut_mid = np.where((cut_co21) & (cut_mid) & (cut_4use))
    cut_high = np.where((cut_co21) & (cut_high) & (cut_4use))
    cut_all = np.where((cut_co21) & (cut_4use))
    #
    r21_low  = r21[cut_low]
    r21_mid  = r21[cut_mid]
    r21_high = r21[cut_high]
    r21err_low  = r21err[cut_low]
    r21err_mid  = r21err[cut_mid]
    r21err_high = r21err[cut_high]
    data_low  = data4use[cut_low] / np.median(data4use[cut_all])
    data_mid  = data4use[cut_mid] / np.median(data4use[cut_all])
    data_high = data4use[cut_high] / np.median(data4use[cut_all])

    return r21_low, r21_mid, r21_high, data_low, data_mid, data_high, r21err_low, r21err_mid, r21err_high

def startup_plot(
    ):
    """
    """
    plt.figure(figsize=(12,4))
    plt.rcParams["font.size"] = 14
    gs = gridspec.GridSpec(nrows=5, ncols=15)
    ax1 = plt.subplot(gs[0:5,0:5])
    ax2 = plt.subplot(gs[0:5,5:10])
    ax3 = plt.subplot(gs[0:5,10:15])
    ax1.grid(axis='both')
    ax2.grid(axis='both')
    ax3.grid(axis='both')
    ax1.set_xscale("log")
    ax2.set_xscale("log")
    ax3.set_xscale("log")
    ax1.set_yscale("log")
    ax2.set_yscale("log")
    ax3.set_yscale("log")
    axlist = [ax1, ax2, ax3]

    return axlist

#####################
### Main Procedure
#####################
#
data_0628 = dir_data + "ngc0628_parameter_600pc.txt"
data_3627 = dir_data + "ngc3627_parameter_600pc.txt"
data_4321 = dir_data + "ngc4321_parameter_600pc.txt"
data_gals = [data_0628, data_3627, data_4321]

#
axlist = startup_plot()


r21_all = []
r21err_all = []
w1_all = []
for i in range(len(gals)):
    #
    ax = axlist[i]
    #
    r21_low,r21_mid,r21_high,w1_low,w1_mid,w1_high,r21err_low,r21err_mid,r21err_high = \
        get_data(data_gals[i], 9)
    r21_all.extend(r21_low)
    r21_all.extend(r21_mid)
    r21_all.extend(r21_high)
    r21err_all.extend(r21err_low)
    r21err_all.extend(r21err_mid)
    r21err_all.extend(r21err_high)
    w1_all.extend(w1_low)
    w1_all.extend(w1_mid)
    w1_all.extend(w1_high)
    #
    ax.scatter(w1_low, r21_low, alpha=1.0, lw=0,
        color=cm.brg(i/2.5))#"blue")
    ax.scatter(w1_mid, r21_mid, alpha=1.0, lw=0,
        color=cm.brg(i/2.5))#"green")
    ax.scatter(w1_high, r21_high, alpha=1.0, lw=0,
        color=cm.brg(i/2.5))#"red")

ax1.errorbar(w1_all, r21_all, yerr=r21err_all, color="grey", alpha=0.5, lw=2)
ax2.errorbar(w1_all, r21_all, yerr=r21err_all, color="grey", alpha=0.5, lw=2)
ax3.errorbar(w1_all, r21_all, yerr=r21err_all, color="grey", alpha=0.5, lw=2)


plt.savefig(dir_data + "fig_r21_vs_w1.png",dpi=200)

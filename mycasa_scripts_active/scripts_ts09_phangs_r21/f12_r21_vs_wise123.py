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
ylim = [0.1,10]
ylabel = "log $R_{21}$/Median($R_{21}$)"


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
    dist_low  = dist[cut_low]
    dist_mid  = dist[cut_mid]
    dist_high = dist[cut_high]
    data_low  = data4use[cut_low] / np.median(data4use[cut_all])
    data_mid  = data4use[cut_mid] / np.median(data4use[cut_all])
    data_high = data4use[cut_high] / np.median(data4use[cut_all])

    return r21_low, r21_mid, r21_high, data_low, data_mid, data_high, r21err_low, r21err_mid, r21err_high, dist_low, dist_mid, dist_high

def startup_plot(
    xlim,
    ylim,
    xlabel,
    ylabel,
    ):
    """
    """
    plt.figure(figsize=(12,5))
    plt.rcParams["font.size"] = 14
    plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.88)
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
    ax2.tick_params(labelleft=False)
    ax3.tick_params(labelleft=False)
    ax1.set_xticks([0.1,1,10,100])
    ax1.set_xticklabels(["-1","0","1","2"])
    ax2.set_xticks([0.1,1,10,100])
    ax2.set_xticklabels(["-1","0","1","2"])
    ax3.set_xticks([0.1,1,10,100])
    ax3.set_xticklabels(["-1","0","1","2"])
    ax1.set_yticks([0.1,1,10])
    ax1.set_yticklabels(["-1","0","1"])
    ax1.set_xlim(xlim)
    ax2.set_xlim(xlim)
    ax3.set_xlim(xlim)
    ax1.set_ylim(ylim)
    ax2.set_ylim(ylim)
    ax3.set_ylim(ylim)
    ax1.set_xlabel(xlabel)
    ax2.set_xlabel(xlabel)
    ax3.set_xlabel(xlabel)
    ax1.set_ylabel(ylabel)
    ax1.set_title("NGC 0628")
    ax2.set_title("NGC 3627")
    ax3.set_title("NGC 4321")
    axlist = [ax1, ax2, ax3]

    return axlist

def plotter_gal(
    axlist,
    gals,
    data_gals,
    col,
    ):
    """
    """
    r21_all = []
    r21err_all = []
    w1_all = []
    for i in range(len(gals)):
        #
        ax = axlist[i]
        #
        r21_low, r21_mid, r21_high, \
        w1_low, w1_mid, w1_high, \
        r21err_low, r21err_mid, r21err_high, \
        dist_low, dist_mid, dist_high = get_data(data_gals[i], col)
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
        r21_gal = np.r_[r21_high, r21_mid, r21_low]
        r21err_gal = np.r_[r21err_high, r21err_mid, r21err_low]
        w1_gal = np.r_[w1_high, w1_mid, w1_low]
        dist_gal = np.r_[dist_high, dist_mid, dist_low]
        #
        ax.scatter(w1_gal, r21_gal, alpha=1.0, lw=0, zorder=1e10, s=20,
            color=cm.gist_rainbow(dist_gal/dist_gal.max()))#i/2.5))
        """
        ax.scatter(w1_low, r21_low, alpha=1.0, lw=0, zorder=1e10, s=40,
            color=cm.gist_rainbow(dist_low/dist_high.max()))#i/2.5))
        ax.scatter(w1_mid, r21_mid, alpha=1.0, lw=0, zorder=1e10, s=40,
            color=cm.gist_rainbow(dist_mid/dist_high.max()))#i/2.5))
        ax.scatter(w1_high, r21_high, alpha=1.0, lw=0, zorder=1e10, s=40,
            color=cm.gist_rainbow(dist_high/dist_high.max()))#i/2.5))
        """

    return r21_all, r21err_all, w1_all

def plotter_alldata(
    axlist,
    r21_all,
    r21err_all,
    y_all,
    ):
    """
    """
    for i in range(len(gals)):
        ax = axlist[i]
        ax.errorbar(
            np.array(y_all),
            np.array(r21_all),
            yerr=np.array(r21err_all),
            fmt="o",
            color="darkgrey",
            markersize=3,
            markeredgewidth=0,
            alpha=1.0,
            lw=1,
            capsize=0,
            zorder=1)

def plotter(
    gals,
    data_gals,
    data_col,
    xlim,
    ylim,
    xlabel,
    ylabel,
    outputname,
    ):
    """
    """
    print("### start plottting " + outputname)
    axlist = startup_plot(xlim, ylim, xlabel, ylabel)
    r21_all, r21err_all, y_all = plotter_gal(axlist, gals, data_gals, data_col)
    plotter_alldata(axlist, r21_all, r21err_all, y_all)
    plt.savefig(dir_data + outputname, dpi=200)


#####################
### Main Procedure
#####################
# get data
data_0628 = dir_data + "ngc0628_parameter_600pc.txt"
data_3627 = dir_data + "ngc3627_parameter_600pc.txt"
data_4321 = dir_data + "ngc4321_parameter_600pc.txt"
data_gals = [data_0628, data_3627, data_4321]

# R21 vs WISE1
xlabel = u"log linewidth/Median(linewidth)"
outputname = "fig_r21_vs_disp.png"
data_col = 8
xlim = [0.3,10]
plotter(gals, data_gals, data_col, xlim, ylim, xlabel, ylabel, outputname)

# R21 vs WISE1
xlabel = "log W1/Median(W1)"
outputname = "fig_r21_vs_w1.png"
data_col = 9
xlim = [0.05,100]
plotter(gals, data_gals, data_col, xlim, ylim, xlabel, ylabel, outputname)

# R21 vs WISE2
xlabel = "log W2/Median(W2)"
outputname = "fig_r21_vs_w2.png"
data_col = 10
xlim = [0.05,100]
plotter(gals, data_gals, data_col, xlim, ylim, xlabel, ylabel, outputname)

# R21 vs WISE3
xlabel = "log W3/Median(W3)"
outputname = "fig_r21_vs_w3.png"
data_col = 11
xlim = [0.05,100]
plotter(gals, data_gals, data_col, xlim, ylim, xlabel, ylabel, outputname)
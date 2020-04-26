import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]
bins = 40
xlim1 = [0,3.01922848601*1.1]
xlim2 = [0,1.97644168938*1.1]
xlim3 = [-3.78251605579*1.1,-0.522595098867*0.9]
xlabel1 = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
xlabel2 = "log $\sigma_{CO(2-1)}$ (km s$^{-1}$)"
xlabel3 = "log W1"
title1 = "log $I_{CO(2-1)}$ Histograms"
title2 = "log $\sigma_{CO(2-1)}$ Histograms"
title3 = "log W1 test"


#####################
### functions
#####################
def get_data(txtdata,col,bins,xlim):
    """
    """
    data = np.loadtxt(txtdata)
    #
    dist = data[:,0]
    r21 = data[:,1]
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
    data4use = np.log10(data[:,col])
    #xlim = [0,data4use.max()*1.1]
    #
    cut_co21 = (co21 > 0)
    cut_4use = (data4use > 0)
    cut_all = np.where((cut_co21) & (cut_4use))
    #
    data_low  = data4use[mask[cut_all]==-1]
    data_mid  = data4use[mask[cut_all]==0]
    data_high = data4use[mask[cut_all]==1]
    co21_low  = co21[mask[cut_all]==-1]
    co21_mid  = co21[mask[cut_all]==0]
    co21_high = co21[mask[cut_all]==1]
    weights_low = np.log10(co21_low)
    weights_mid = np.log10(co21_mid)
    weights_high = np.log10(co21_high)
    hist_low  = np.histogram(data_low, bins=bins, range=xlim, weights=weights_low)
    hist_mid  = np.histogram(data_mid, bins=bins, range=xlim, weights=weights_mid)
    hist_high = np.histogram(data_high, bins=bins, range=xlim, weights=weights_high)
    histmax = np.max(data4use)
    #
    stats_low = [weighted_percentile(data_low,0.84,weights_low),   weighted_percentile(data_low,0.50,weights_low),  weighted_percentile(data_low,0.16,weights_low)]
    stats_mid = [weighted_percentile(data_mid,0.84,weights_mid),   weighted_percentile(data_mid,0.50,weights_mid),  weighted_percentile(data_mid,0.16,weights_mid)]
    stats_high = [weighted_percentile(data_high,0.84,weights_high),weighted_percentile(data_high,0.50,weights_high),weighted_percentile(data_high,0.16,weights_high)]

    return histmax, hist_low, hist_mid, hist_high, stats_low, stats_mid, stats_high

def startup_plot(
	xlim,
	xlabel,
    title,
	):
    """
    """
    plt.subplots(nrows=1,ncols=1,figsize=(7, 7),sharey=True)
    plt.rcParams["font.size"] = 14
    plt.rcParams["legend.fontsize"] = 9
    plt.subplots_adjust(bottom=0.08, left=0.08, right=0.97, top=0.95)
    gs = gridspec.GridSpec(nrows=18, ncols=25)
    ax1 = plt.subplot(gs[0:6,0:25])
    ax2 = plt.subplot(gs[6:12,0:25])
    ax3 = plt.subplot(gs[12:18,0:25])
    ax1.set_xlim(xlim)
    ax2.set_xlim(xlim)
    ax3.set_xlim(xlim)
    ax1.grid(axis="x")
    ax2.grid(axis="x")
    ax3.grid(axis="x")
    ax1.tick_params(axis="y", length=0)
    ax2.tick_params(axis="y", length=0)
    ax3.tick_params(axis="y", length=0)
    ax1.tick_params(labelbottom=False)
    ax2.tick_params(labelbottom=False)
    #ax3.tick_params(labelbottom=False)
    ax3.set_xlabel(xlabel)
    ax1.set_title(title)

    return ax1, ax2, ax3

def plotter(
    ax,
    hist_low,
    hist_mid,
    hist_high,
    stats_low,
    stats_mid,
    stats_high,
    ):
    """
    """
    x, y_low = np.delete(hist_low[1],-1), hist_low[0]
    y_low = y_low / float(sum(y_low))
    _, y_mid = np.delete(hist_mid[1],-1), hist_mid[0]
    y_mid = y_mid / float(sum(y_mid))
    _, y_high = np.delete(hist_high[1],-1), hist_high[0]
    y_high = y_high / float(sum(y_high))
    #
    ax.step(x, y_low, color="blue", lw=1.5, where="mid")
    ax.step(x, y_mid, color="green", lw=1.5, where="mid")
    ax.step(x, y_high, color="red", lw=1.5, where="mid")
    ax.bar(x, y_low, lw=0, color="blue", alpha=0.2, width=x[1]-x[0], align="center")
    ax.bar(x, y_mid, lw=0, color="green", alpha=0.2, width=x[1]-x[0], align="center")
    ax.bar(x, y_high, lw=0, color="red", alpha=0.2, width=x[1]-x[0], align="center")
    ylim_top = np.max([y_low,y_mid,y_high])*1.4
    ax.set_ylim(0.0005,np.max([y_low,y_mid,y_high])*1.4)
    # plot medians
    ylim_width = ylim_top - 0.0005
    ax.plot([stats_low[1],stats_low[1]], [ylim_top-ylim_width*0.15,ylim_top-ylim_width*0.15], "o", color="blue", markeredgewidth=0)
    ax.plot([stats_mid[1],stats_mid[1]], [ylim_top-ylim_width*0.10,ylim_top-ylim_width*0.10], "o", color="green", markeredgewidth=0)
    ax.plot([stats_high[1],stats_high[1]], [ylim_top-ylim_width*0.05,ylim_top-ylim_width*0.05], "o", color="red", markeredgewidth=0)
    ax.plot([stats_low[2],stats_low[0]], [ylim_top-ylim_width*0.15,ylim_top-ylim_width*0.15], "-", color="blue", lw=3, alpha=0.4)
    ax.plot([stats_mid[2],stats_mid[0]], [ylim_top-ylim_width*0.10,ylim_top-ylim_width*0.10], "-", color="green", lw=3, alpha=0.4)
    ax.plot([stats_high[2],stats_high[0]], [ylim_top-ylim_width*0.05,ylim_top-ylim_width*0.05], "-", color="red", lw=3, alpha=0.4)

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
# co21 mom-0
axlist = startup_plot(xlim1,xlabel1,title1)
#
histmaxs = []
for i in range(len(gals)):
    ax = axlist[i]
    galname = gals[i]
    galnamelabel = galname.replace("ngc","NGC ")
    # get data
    histmax, hist_low, hist_mid, hist_high, stats_low, stats_mid, stats_high = \
    	get_data(dir_product+galname+"_parameter_600pc.txt",3,bins,xlim1)
    #
    plotter(ax,hist_low,hist_mid,hist_high,stats_low,stats_mid,stats_high)
    #
    histmaxs.append(histmax)
    #
#print(np.max(histmaxs))
plt.savefig(dir_product+"maskhist_mom0.png",dpi=200)


# co21 disp
axlist = startup_plot(xlim2,xlabel2,title2)
#
histmaxs = []
for i in range(len(gals)):
    ax = axlist[i]
    galname = gals[i]
    galnamelabel = galname.replace("ngc","NGC ")
    # get data
    histmax, hist_low, hist_mid, hist_high, stats_low, stats_mid, stats_high = \
    	get_data(dir_product+galname+"_parameter_600pc.txt",8,bins,xlim2)
    #
    plotter(ax,hist_low,hist_mid,hist_high,stats_low,stats_mid,stats_high)
    #
    histmaxs.append(histmax)
    #
#print(np.max(histmaxs))
plt.savefig(dir_product+"maskhist_disp.png",dpi=200)


# co21 disp
axlist = startup_plot(xlim3,xlabel3,title3)
#
histmaxs = []
for i in range(len(gals)):
    ax = axlist[i]
    galname = gals[i]
    galnamelabel = galname.replace("ngc","NGC ")
    # get data
    histmax, hist_low, hist_mid, hist_high, stats_low, stats_mid, stats_high = \
        get_data(dir_product+galname+"_parameter_600pc.txt",9,bins,xlim3)
    #
    plotter(ax,hist_low,hist_mid,hist_high,stats_low,stats_mid,stats_high)
    #
    histmaxs.append(histmax)
    #
print(np.max(histmaxs))
plt.savefig(dir_product+"maskhist_w1.png",dpi=200)


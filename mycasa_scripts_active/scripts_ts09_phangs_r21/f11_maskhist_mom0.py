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
ylim = [0.0005,0.2]


#####################
### functions
#####################
def get_data(txtdata,col,bins):
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
    xlim = [0,data4use.max()*1.1]
    #
    co21_low  = co21[mask==-1][co21[mask==-1]>0]
    co21_mid  = co21[mask==0][co21[mask==0]>0]
    co21_high = co21[mask==1][co21[mask==1]>0]
    data_low  = data4use[mask==-1][data4use[mask==-1]>0]
    data_mid  = data4use[mask==0][data4use[mask==0]>0]
    data_high = data4use[mask==1][data4use[mask==1]>0]
    hist_low  = np.histogram(data_low, bins=bins, range=xlim, weights=np.log10(co21_low))
    hist_mid  = np.histogram(data_mid, bins=bins, range=xlim, weights=np.log10(co21_mid))
    hist_high = np.histogram(data_high, bins=bins, range=xlim, weights=np.log10(co21_high))

    return xlim, hist_low, hist_mid, hist_high


#####################
### main
#####################
for i in range(len(gals)):
    galname = gals[i]
    galnamelabel = galname.replace("ngc","NGC ")
    # get data
    xlim, hist_low, hist_mid, hist_high = \
    	get_data(dir_product+galname+"_parameter_600pc.txt",3,bins)
    # prepare for plot
    plt.subplots(nrows=1,ncols=1,figsize=(10, 7),sharey=True)
    plt.rcParams["font.size"] = 14
    plt.rcParams["legend.fontsize"] = 9
    plt.subplots_adjust(bottom=0.1, left=0.07, right=0.99, top=0.99)
    gs = gridspec.GridSpec(nrows=18, ncols=25)
    ax1 = plt.subplot(gs[0:6,0:25])
    ax2 = plt.subplot(gs[6:12,0:25])
    ax3 = plt.subplot(gs[12:18,0:25])
    ax1.set_ylim(ylim)
    ax2.set_ylim(ylim)
    ax3.set_ylim(ylim)
    ax1.grid(axis="y")
    ax2.grid(axis="y")
    ax3.grid(axis="y")
    ax1.set_xlim(xlim)
    ax2.set_xlim(xlim)
    ax3.set_xlim(xlim)
    #
    x, y_low = np.delete(hist_low[1],-1), hist_low[0]
    y_low = y_low / float(sum(y_low))
    _, y_mid = np.delete(hist_mid[1],-1), hist_mid[0]
    y_mid = y_mid / float(sum(y_mid))
    _, y_high = np.delete(hist_high[1],-1), hist_high[0]
    y_high = y_high / float(sum(y_high))
    #
    ax1.step(x, y_low, color="blue", lw=2, alpha=0.5)
    ax1.step(x, y_mid, color="green", lw=2, alpha=0.5)
    ax1.step(x, y_high, color="red", lw=2, alpha=0.5)
    #
plt.title(galnamelabel)
plt.savefig(dir_product+"maskhist_mom0.png",dpi=200)





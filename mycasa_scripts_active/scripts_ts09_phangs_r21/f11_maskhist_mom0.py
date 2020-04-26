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
bins = 20
ratiorange = [0.0,2.5]


#####################
### functions
#####################



#####################
### main
#####################
for i in range(len(gals)):
    galname = gals[i]
    galnamelabel = galname.replace("ngc","NGC ")
    data = np.loadtxt(dir_product + galname + "_parameter_600pc.txt")
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
    r21_low  = r21[mask==-1]
    r21_mid  = r21[mask==0]
    r21_high = r21[mask==1]
    #
    figure = plt.figure(figsize=(8,8))
    hist_low  = np.histogram(r21_low, bins=bins, range=ratiorange)
    x, y_low = np.delete(hist_low[1],-1), hist_low[0]
    y_low = y_low / float(sum(y_low))
    _, y_mid = np.delete(hist_mid[1],-1), hist_mid[0]
    y_mid = y_mid / float(sum(y_mid))
    _, y_high = np.delete(hist_high[1],-1), hist_high[0]
    y_high = y_high / float(sum(y_high))
    #
    plt.step(x, y_low, color="blue", lw=0, alpha=0.5)
    plt.step(x, y_mid, color="green", lw=0, alpha=0.5)
    plt.step(x, y_high, color="red", lw=0, alpha=0.5)
    #
    plt.savefig(dir_product+"maskhist_mom0.png",dpi=200)





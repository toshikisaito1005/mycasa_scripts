import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
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
    data4use[np.isinf(data4use)] = 0
    data4use[np.isnan(data4use)] = 0
    #xlim = [0,data4use.max()*1.1]
    #
    cut_co21 = (co21 != 0)
    cut_low = (mask==-1)
    cut_mid = (mask==0)
    cut_high = (mask==1)
    cut_low = np.where((cut_co21) & (cut_low))
    cut_mid = np.where((cut_co21) & (cut_mid))
    cut_high = np.where((cut_co21) & (cut_high))
    #
    data_low  = data4use[cut_low]
    data_mid  = data4use[cut_mid]
    data_high = data4use[cut_high]

    return data_low, data_mid, data_high


#####################
### Main Procedure
#####################
#
data_0628 = np.loadtxt(dir_data + "ngc0628_parameter_600pc.txt")
data_3627 = np.loadtxt(dir_data + "ngc3627_parameter_600pc.txt")
data_4321 = np.loadtxt(dir_data + "ngc4321_parameter_600pc.txt")
data_gals = [data_0628, data_3627, data_4321]
data_all = np.r_[data_0628, data_3627, data_4321]

for i in range(len(gals)):
	r21 = get_data(data_gal,1)


plt.figure(figsize=(10,0))
plt.rcParams["font.size"] = 14
gs = gridspec.GridSpec(nrows=5, ncols=15)
ax1 = plt.subplot(gs[0:5,0:5])
ax2 = plt.subplot(gs[0:5,5:10])
ax3 = plt.subplot(gs[0:5,10:15])


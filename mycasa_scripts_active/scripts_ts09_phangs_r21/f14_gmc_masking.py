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
nbins = 75
xlim = [0,2.5]


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
txtfile = glob.glob(dir_product + "ngc*_parameter_best.txt")
#
data_all = []
data_norm_all = []
data_nuc_all = []
data_nuc_norm_all = []
data_out_all = []
data_out_norm_all = []
for i in range(len(txtfile)):
    data = np.loadtxt(txtfile[i])[:,1]
    gmcmask = np.loadtxt(txtfile[i])[:,16]
    #
    data = data[data>0]
    gmcmask = gmcmask[data>0]
    #
    data_inmask  = data[gmcmask==1]
    data_outmask = data[gmcmask==0]
    #
    data_norm = data / np.median(data)
    data_all.extend(data)
    data_norm_all.extend(data_norm)
    #
#
data_all = np.array(data_all)
data_norm_all = np.array(data_norm_all)



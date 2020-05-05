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
dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]
nbins = 150
xlim = [0,2.5]


#####################
### functions
#####################



#####################
### main
#####################
### get data
txtfile = glob.glob(dir_product + "ngc*_parameter_600pc.txt")
#
data_all = []
data_norm_all = []
for i in range(len(txtfile)):
    data = np.loadtxt(txtfile[i])[:,1]
    data = data[data>0]
    data_norm = data / np.median(data)
    data_all.extend(data)
    data_norm_all.extend(data_norm)
#
data_all = np.array(data_all)
data_norm_all = np.array(data_norm_all)


### histogram
#
histo_all = np.histogram(data_all, bins=nbins, range=(xlim), weights=None)
x_all, y_all = np.delete(histo_all[1],-1),histo_all[0]
y_all = y_all / float(sum(y_all))
#
histo_norm = np.histogram(data_norm_all, bins=nbins, range=(xlim), weights=None)
x_norm, y_norm = np.delete(histo_norm[1],-1),histo_norm[0]


### plot
figure = plt.figure(figsize=(9,9))
gs = gridspec.GridSpec(nrows=8, ncols=16)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,8:16])
plt.rcParams["font.size"] = 16


plt.savefig(dir_product+"radial_r21.png",dpi=200)

os.system("rm -rf *.last")

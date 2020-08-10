import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
plt.ioff()


#####################
### Parameter
#####################
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"


#####################
### Main Procedure
#####################
data = np.loadtxt("fig04_data.txt")
logSFR = data[:,0]
logMstar = data[:,1]


#
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:9,0:9])
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
plt.subplots_adjust(bottom=0.15, left=0.20, right=0.90, top=0.85) 
#
plt
ax1.scatter(lirg_m0, lirg_ew, c="indianred", s=40, linewidths=0)
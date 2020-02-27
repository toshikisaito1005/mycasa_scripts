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
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
dist25 = []

#####################
### functions
#####################
def hist_percent(histo,percent):
    dat_sum = np.sum(histo)
    dat_sum_from_zero,i = 0,0
    while dat_sum_from_zero < dat_sum * percent:
        dat_sum_from_zero += histo[i]
        i += 1
    
    return i


#####################
### main
#####################
for i in range(len(gals)):
    galname = gals[i]
    data = np.loadtxt(dir_data + galname + "_parameter_600pc.txt")
    distance = data[;,0]
    r21 = data[;,1]




medians = [0.567146319177,
           0.694100944171,
           #0.620322003718,
           0.438006423556]


figure = plt.figure(figsize=(9,9))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:7,0:7])
ax2 = plt.subplot(gs[0:7,7:9])
ax2b = ax2.twinx()
plt.rcParams["font.size"] = 16
histdata = []
for i in range(len(gals)):
    data = np.loadtxt(glob.glob(dir_data + gals[i] + "_wise/radial_r21.txt")[0])
    dist = data[:,0]
    r21 = data[:,1] / medians[i]
    yerr = data[:,2] / medians[i]

    data = np.loadtxt(glob.glob(dir_data + gals[i] + "_wise/radial_r21_rawdata.txt")[0])

    ax1.plot(dist,r21,color=cm.brg(i/3.5),lw=7,alpha=0.5,
             label = gals[i].replace("ngc","NGC "))

    histdata.extend((data / medians[i]).tolist())

dathist = ax2.hist(histdata,orientation="horizontal",range=[0,2],
                   bins=100,lw=0,color="grey",alpha=0.6)
range_p = dathist[1][hist_percent(dathist[0],0.843)]
range_l = dathist[1][hist_percent(dathist[0],0.157)]

ax1.plot([0,14],[range_l,range_l],lw=5,linestyle="--",alpha=0.8,color="black")
ax1.plot([0,14],[range_p,range_p],lw=5,linestyle="--",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_l,range_l],
         lw=5,linestyle="--",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_p,range_p],
         lw=5,linestyle="--",alpha=0.8,color="black")

ax1.grid()
ax1.legend(ncol=2)
ax1.set_ylim([0,2])
ax1.set_xlabel("Deprojected Distance (kpc)")
ax1.set_ylabel("$R_{21}$/$Med(R_{21})$")

ax2.set_ylim([0,2])
ax2b.set_ylim([0,2])
ax2.grid(axis="both")
ax2.tick_params(labelbottom=False,labelleft=False,labeltop=False)
ax2b.tick_params(labelbottom=False,labelleft=False,labeltop=False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2b.set_ylabel("$R_{21}$/$Med(R_{21})$")

plt.savefig(dir_data+"eps/radial_norm_r21.png",dpi=200)

os.system("rm -rf *.last")

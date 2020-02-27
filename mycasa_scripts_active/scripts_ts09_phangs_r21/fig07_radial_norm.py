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
dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]

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
figure = plt.figure(figsize=(9,9))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:7,0:7])
ax2 = plt.subplot(gs[0:7,7:9])
ax2b = ax2.twinx()
plt.rcParams["font.size"] = 16

histodata = []
for i in range(len(gals)):
    galname = gals[i]
    data = np.loadtxt(dir_data + galname + "_parameter_600pc.txt")
    # galactocentric distance
    distance = data[:,0] # pc
    dist25_pc = dist25[i] * 60 * scales[i]
    galdist = distance / dist25_pc
    # median-subtracted r21
    r21 = data[:,1]
    med_r21 = np.median(r21[r21>0])
    norm_r21 = r21 - med_r21
    # cut data
    cut_r21 = (r21 > 0)
    galdist = galdist[cut_r21]
    norm_r21 = norm_r21[cut_r21]

    ax1.plot(
        galdist, norm_r21, color=cm.brg(i/2.5), lw=7, alpha=0.5,
             label = galname.replace("ngc","NGC "))

    histdata.extend(norm_r21.tolist())



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

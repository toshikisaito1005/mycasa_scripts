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
gals = ["ngc0628","ngc3627","ngc4321"]
dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]
nbins = 8
percents = [0.0,0.00,0.00]

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


histdata = []
for i in range(len(gals)):
#for i in [0]:
    galname = gals[i]
    data = np.loadtxt(dir_product + galname + "_parameter_600pc.txt")
    # galactocentric distance
    distance = data[:,0] # pc
    dist25_pc = dist25[i] * 60 * scales[i]
    galdist = distance / dist25_pc
    # values
    r21 = data[:,1][data[:,1]>0]
    galdist = galdist[data[:,1]>0]
    med_r21 = np.median(r21)
    norm_r21 = r21 / med_r21
    # binning
    n, _ = np.histogram(galdist, bins=nbins)
    sy, _ = np.histogram(galdist, bins=nbins, weights=r21)
    sy2, _ = np.histogram(galdist, bins=nbins, weights=r21*r21)
    mean = sy / n
    std = np.sqrt(sy2/n - mean*mean)
    # plot
    ax1.errorbar(
        (_[1:] + _[:-1])/2, mean, yerr=std,
        color=cm.brg(i/2.5), lw=4, #alpha=0.5,
        label = galname.replace("ngc","NGC ")
        )
    ax1.scatter(
        galdist, r21,
        color=cm.brg(i/2.5),
        lw=0, alpha=0.2, s=50,
        label = galname.replace("ngc","NGC "))

    histdata.extend(r21.tolist())

dathist = ax2.hist(
    histdata,orientation="horizontal",range=[0,3],
    bins=100,lw=0,color="grey",alpha=0.6)

range_p = dathist[1][hist_percent(dathist[0],0.843)]
range_l = dathist[1][hist_percent(dathist[0],0.157)]

ax1.plot([0,1],[range_l,range_l],lw=5,linestyle="--",alpha=0.8,color="black")
ax1.plot([0,1],[range_p,range_p],lw=5,linestyle="--",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_l,range_l],
         lw=5,linestyle="--",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_p,range_p],
         lw=5,linestyle="--",alpha=0.8,color="black")
ax2.text(0.6*dathist[0].max()*1.25,range_p-0.1,str(range_p))
ax2.text(0.6*dathist[0].max()*1.25,range_l-0.1,str(range_l))

ax1.grid()
ax1.legend(ncol=2, loc="upper right")
ax1.set_xlim([0,1])
ax1.set_ylim([0,3])
ax1.set_xlabel("r/r25")
ax1.set_ylabel("$R_{21}$")

ax2.set_ylim([0,3])
ax2b.set_ylim([0,3])
ax2.grid(axis="both")
ax2.tick_params(labelbottom=False,labelleft=False,labeltop=False)
ax2b.tick_params(labelbottom=False,labelleft=False,labeltop=False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2b.set_ylabel("$R_{21}$")

ax1.set_title("Radial $R_{21}$ Distribution")
plt.savefig(dir_product+"radial_r21.png",dpi=200)

os.system("rm -rf *.last")

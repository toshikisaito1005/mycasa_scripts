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
percents = [0.01,0.01,0.01]

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
    sy, _ = np.histogram(galdist, bins=nbins, weights=norm_r21)
    sy2, _ = np.histogram(galdist, bins=nbins, weights=norm_r21*norm_r21)
    mean = sy / n
    std = np.sqrt(sy2/n - mean*mean)
    ax1.errorbar(
        (_[1:] + _[:-1])/2, mean, yerr=std,
        color=cm.brg(i/2.5), lw=4, #alpha=0.5,
        label = galname.replace("ngc","NGC ")
        )
    """
    # contour
    H, xedges, yedges = np.histogram2d(norm_r21,galdist,bins=30,range=([0,2],[0,2]))
    extent = [xedges[0],xedges[-1],yedges[0],yedges[-1]]
    ax1.contour(H/H.max()*100,levels=[16,32,64,96],extent=extent,
        colors=[cm.brg(i/2.5)],zorder=2,linewidths=2.5,alpha=1.0,labels=galname.replace("ngc","NGC "))
        """
    # plot
    ax1.scatter(
        galdist, norm_r21,
        color="grey",#cm.brg(i/2.5),
        lw=0, alpha=0.3, s=30)

    histdata.extend(norm_r21.tolist())

dathist = ax2.hist(
    histdata,orientation="horizontal",range=[0,3],
    bins=100,lw=0,color="grey",alpha=0.6)

range_p = dathist[1][hist_percent(dathist[0],0.843)]
range_median = dathist[1][hist_percent(dathist[0],0.50)]
range_l = dathist[1][hist_percent(dathist[0],0.157)]

ax1.plot([0,1],[range_l,range_l],lw=3,linestyle="--",alpha=0.8,color="black")
ax1.plot([0,1],[range_median,range_median],lw=5,linestyle="-",alpha=0.8,color="black")
ax1.plot([0,1],[range_p,range_p],lw=3,linestyle="--",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_l,range_l],
         lw=3,linestyle="--",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_median,range_median],
         lw=5,linestyle="-",alpha=0.8,color="black")
ax2.plot([0,dathist[0].max()*1.25],[range_p,range_p],
         lw=3,linestyle="--",alpha=0.8,color="black")
ax1.text(0.98,range_p+0.05,"84%",horizontalalignment="right")
ax1.text(0.98,range_median+0.05,"Median",horizontalalignment="right")
ax1.text(0.98,range_l-0.1,"16%",horizontalalignment="right")
ax2.text(0.6*dathist[0].max()*1.25,range_p+0.05,str(range_p))
ax2.text(0.6*dathist[0].max()*1.25,range_median+0.05,str(range_median))
ax2.text(0.6*dathist[0].max()*1.25,range_l-0.1,str(range_l))

ax1.grid()
ax1.legend(ncol=2, loc="upper right")
ax1.set_xlim([0,1])
ax1.set_ylim([0,2.5])
ax1.set_xlabel("r/r25")
ax1.set_ylabel("Normed $R_{21}$")

ax2.set_ylim([0,2.5])
ax2b.set_ylim([0,2.5])
ax2.grid(axis="y")
ax2.tick_params(labelbottom=False,labelleft=False,labeltop=False)
ax2b.tick_params(labelbottom=False,labelleft=False,labeltop=False)
ax2.spines["top"].set_visible(False)
ax2.spines["left"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2b.set_ylabel("Normed $R_{21}$")

ax1.set_title("Radial $R_{21}$ Distribution")
plt.savefig(dir_product+"radial_r21_normed.png",dpi=200)

os.system("rm -rf *.last")

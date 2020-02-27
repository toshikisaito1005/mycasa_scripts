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
nbins = 4
percents = [0.15,0.025,0.010]

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
      # galactocentric distance
    distance = data[:,0] # pc
    dist25_pc = dist25[i] * 60 * scales[i]
    galdist = distance / dist25_pc
    # median-subtracted r21
    r21 = data[:,1]
    med_r21 = np.median(r21[r21>0])
    norm_r21 = r21 / med_r21
    # co21
    co21 = data[:,4]
    co21snr = data[:,5]
    # wise
    wise1 = data[:,8]
    wise2 = data[:,9]
    wise3 = data[:,10]
    # r21 mask
    r21mask = data[:,11]

    # cut data
    cut_r21 = (r21 > 0)
    cut_co21 = (co21 > co21.max() * percents[i])
    cut_all = np.where((cut_r21) & (cut_co21))

    galdist = galdist[cut_all]
    r21mask = r21mask[cut_all]
    norm_r21 = norm_r21[cut_all]
    co21 = co21[cut_all]
    wise1 = wise1[cut_all]
    wise2 = wise2[cut_all]
    wise3 = wise3[cut_all]

    # plot
    figure = plt.figure(figsize=(9,3))
    plt.rcParams["font.size"] = 16
    plt.grid(axis = "x")
    plt.hist(galdist[r21mask==-1])
    
    plt.savefig(dir_product+"fig10_"+galname+"_dist.png",dpi=200)

"""
ax1.grid(axis = "x")
ax1.legend(ncol=2, loc="upper right")
#ax1.set_xlim([0,1])
ax1.set_xscale("log")
ax1.set_ylim([0,2])
ax1.set_xlabel("WISE1 (currently Jy/b)")
ax1.set_ylabel("$R_{21}$/$Med(R_{21})$")

ax1.set_title("$R_{21}$/$Med(R_{21})$ vs. WISE1")
plt.savefig(dir_product+"radial_r21_vs_wise1.png",dpi=200)

os.system("rm -rf *.last")
"""

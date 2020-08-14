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
import astropy.io.fits as fits
plt.ioff()


#####################
### Parameter
#####################
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"


#####################
### Main Procedure
#####################
data = np.loadtxt("list_sfr_stellar.txt")
lirg_logSFR = data[:,0]
lirg_logMstar = data[:,1]
#
hdulist = fits.open(dir_eps + "../data_other/phangs_sample_table_v1p5.fits")


#
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:9,0:9])
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
plt.subplots_adjust(bottom=0.15, left=0.20, right=0.90, top=0.85) 
#
ax1.scatter(logMstar, logSFR, c="indianred", s=40, linewidths=0)
#
plt.xlim([9,12])
plt.ylim([-1,2])
plt.savefig(dir_eps+"plot_sfr_vs_mstar.png",dpi=200)
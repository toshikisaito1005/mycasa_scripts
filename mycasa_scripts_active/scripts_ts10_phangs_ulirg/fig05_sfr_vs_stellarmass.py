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
from astropy.io import fits
from astropy.table import Table
plt.ioff()


#####################
### Parameter
#####################
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"


#####################
### Main Procedure
#####################
data = np.loadtxt("list_sfr_stellar.txt")
lirg_logSFR = 10**data[:,0]
lirg_logMstar = 10**data[:,1]
#
hdu_list = fits.open(dir_eps + "../data_other/phangs_sample_table_v1p5.fits", memmap=True)
evt_data = Table(hdu_list[1].data)
phangs_logSFR = evt_data["props_sfr"] # np.log10(evt_data["props_sfr"])
phangs_logMstar = evt_data["props_mstar"] # np.log10(evt_data["props_mstar"])

print(hdu_list[1].columns)

#
figure = plt.figure(figsize=(5,3))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:9,0:9])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax1.scatter(lirg_logMstar, lirg_logSFR, c="indianred", s=20, marker="s", linewidths=0)
ax1.scatter(phangs_logMstar, phangs_logSFR, c="skyblue", s=10, marker="o", linewidths=0)
#
plt.xlim([10**9,10**11.5])
plt.ylim([10**-1.5,10**2.1])
plt.xscale("log")
plt.yscale("log")
plt.savefig(dir_eps+"plot_sfr_vs_mstar.png",dpi=200)

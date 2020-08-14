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
ax1.scatter(lirg_logMstar, lirg_logSFR, c="indianred", s=20, marker="s", lw=1, zorder=1e9, label="(U)LIRGs")
ax1.scatter(phangs_logMstar, phangs_logSFR, c="skyblue", s=10, marker="o", lw=1, zorder=1e9, label="PHANGS")
#
ax1.plot([10**9,10**11.7], [0.14125375446227556,9.6827785626124676], "--", lw=2, c="grey")
ax1.text(10**np.log10(10**11.2),10,"z=0 MS",rotation=14.5)
ax1.plot([10**9,10**11.7], [0.14125375446227556*10,9.6827785626124676*10], "--", lw=2, c="grey")
ax1.text(10**np.log10(10**9.2),8,"+1 dex from MS",rotation=14.5)
#
ax1.set_xlim([10**9,10**11.7])
ax1.set_ylim([10**-1.8,10**2.2])
plt.xscale("log")
plt.yscale("log")
plt.xticks([10**9,10**10,10**11],[9,10,11])
plt.yticks([10**-1,10**0,10**1,10**2],[-1,0,1,2])
plt.xlabel(r"log $M_{\star}$ ($M_{\odot}$)")
plt.ylabel(r"log SFR ($M_{\odot}$ yr$^{-1}$)")
plt.legend(loc="upper left")
plt.savefig(dir_eps+"plot_sfr_vs_mstar.png",dpi=200)


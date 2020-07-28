import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import matplotlib.patches as mpatches
plt.ioff()

#####################
### Parameter
#####################
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = ['eso267', 'eso297g011', 'eso297g012', 'eso319', 'eso507', 'eso557', 'ic4518e', 'ic4518w', 'ic5179', 'iras06592', 'irasf10409', 'irasf17138', 'mcg02', 'ngc1614', 'ngc2369', 'ngc3110', 'ngc3256', 'ngc5257', 'ngc6240']


#####################
### Main Procedure
#####################
### get data
this_m0 = []
this_ew = []
for i in range(len(galaxy)):
	this_galaxy = galaxy[i]
	this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
	this_m0.extend(this_data[:,0])
	this_ew.extend(this_data[:,1])

figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,8:9])
ax3 = plt.subplot(gs[8:9,0:8])
plt.rcParams["font.size"] = 18
plt.rcParams["legend.fontsize"] = 16
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95) 
# plot
ax1.scatter(this_m0*0.8, this_ew, c="pink", s=40, linewidths=0)
# ax1
ax1.set_xlim([10**0,10**4.5])
ax1.set_ylim([10**0,10**2.4])
ax1.grid()
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel(r"$\Sigma_{\mathsf{mol,150pc}}$ ($M_{\odot}$ pc$^{-2}$)")
ax1.set_ylabel(r"$\sigma_{\mathsf{mol,150pc}}$ (km s$^{-1}$)")
#
plt.legend(ncol=4, loc="upper left")
plt.savefig(dir_eps+"plot_scatter_all.png",dpi=200)

os.system("rm -rf *.last")

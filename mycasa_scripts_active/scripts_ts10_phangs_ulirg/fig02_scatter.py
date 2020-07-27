import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.cm as cm
import matplotlib.patches as mpatches


#####################
### Parameter
#####################
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = ['eso267', 'eso297g011', 'eso297g012', 'eso319', 'eso507', 'eso557', 'ic4518e', 'ic4518w', 'ic5179', 'iras06592', 'irasf10409', 'irasf17138', 'mcg02', 'ngc1614', 'ngc2369', 'ngc3110', 'ngc3256', 'ngc5257', 'ngc6240']


#####################
### Main Procedure
#####################
fig, ax = plt.subplots(1, 1)
plt.rcParams["font.size"] = 14
plt.rcParams["legend.fontsize"] = 10
ax.set_xlim([10**0,10**4.5])
ax.set_ylim([10**0,10**3.2])
for i in range(len(galaxy)):
	this_galaxy = galaxy[i]
	this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
	this_m0 = this_data[:,0]
	this_ew = this_data[:,1]
	c = cm.jet(i/float(len(galaxy)))
	ax.scatter(this_m0*0.8, this_ew, c=c, linewidths=0, alpha=0.4, label=this_galaxy)
	#
plt.legend(ncol=4, loc="upper left")
plt.grid()
plt.xscale("log")
plt.yscale("log")
plt.xlabel(r"$\Sigma_{\mathsf{mol,150pc}}$ ($M_{\odot}$ pc$^{-2}$)")
plt.ylabel(r"$\sigma_{\mathsf{mol,150pc}}$ (km s$^{-1}$)")
plt.savefig(dir_eps+"plot_scatter_all.png",dpi=200)

os.system("rm -rf *.last")

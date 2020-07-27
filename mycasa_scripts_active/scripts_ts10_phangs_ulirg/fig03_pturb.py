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
### functions
#####################
def weighted_percentile(
    data,
    percentile,
    weights=None,
    ):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    if weights==None:
        w_median = np.percentile(data,percentile*100)
    else:
        data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
        s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
        midpoint = percentile * sum(s_weights)
        if any(weights > midpoint):
            w_median = (data[weights == np.max(weights)])[0]
        else:
            cs_weights = np.cumsum(s_weights)
            idx = np.where(cs_weights <= midpoint)[0][-1]
            if cs_weights[idx] == midpoint:
                w_median = np.mean(s_data[idx:idx+2])
            else:
                w_median = s_data[idx+1]

    return w_median


#####################
### Main Procedure
#####################
list_wp16 = []
list_wp50 = []
list_wp84 = []
for i in range(len(galaxy)):
	this_galaxy = galaxy[i]
	this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
	this_m0 = this_data[:,0]
	this_ew = this_data[:,1]
	this_pturb = this_m0 * this_ew**2
	#
	wp50 = weighted_percentile(this_pturb,0.50,this_m0)
	wp16 = weighted_percentile(this_pturb,0.16,this_m0)
	wp84 = weighted_percentile(this_pturb,0.84,this_m0)
	#
	list_wp16.append(wp16)
	list_wp50.append(wp50)
	list_wp84.append(wp84)
	#
# figure
fig, ax = plt.subplots(1, 1)
plt.rcParams["font.size"] = 14
plt.rcParams["legend.fontsize"] = 10
#ax.set_xlim([0,4.5])
#ax.set_ylim([0,3.2])
ax.scatter(np.array(range(len(galaxy)))+1, list_wp50)
for i in range(len(galaxy)):
	ax.plot([i+1, i+1], [list_wp16[i], list_wp84[i]])
#
plt.legend(ncol=4, loc="upper left")
plt.grid()
plt.xscale("log")
plt.yscale("log")
plt.xticks(np.array(range(len(galaxy)))+1, galaxy)
plt.xticks(rotation=45)
#plt.xlabel(r"$\Sigma_{\mathsf{mol,150pc}}$ ($M_{\odot}$ pc$^{-2}$)")
#plt.ylabel(r"$\sigma_{\mathsf{mol,150pc}}$ (km s$^{-1}$)")
plt.savefig(dir_eps+"plot_pturb_all.png",dpi=200)

os.system("rm -rf *.last")

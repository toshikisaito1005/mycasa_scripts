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
galaxy = ['eso297g011', 'eso297g012', 'ic4518e', 'ic4518w', 'eso319',
          'ngc2369', 'mcg02', 'ic5179', 'iras06592',
          'eso267', 'eso557', 'irasf10409', 'ngc5257', 'ngc3110', 'irasf17138',
          'eso507', 'ngc3256', 'ngc1614', 'ngc6240']
galname1 = [s.replace("eso","ESO ").replace("ngc","NGC ").replace("mcg","MCG-") for s in galaxy]
galname2 = [s.replace("e","E").replace("w","W").replace("ic","IC") for s in galname1]
galname3 = [s.replace("iras","IRAS ").replace("f","F").replace("g","-G") for s in galname2]
galname4 = [s.replace("319","319-G022").replace("507","507-G070") for s in galname3]
galname5 = [s.replace("557","557-G002").replace("06592","06592-6313") for s in galname4]
galname6 = [s.replace("10409","10409-4556").replace("17138","17138-1017") for s in galname5]
galname = [s.replace("-02","-02-33-098").replace("267","267-G030") for s in galname6]



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
plt.subplots_adjust(bottom=0.35, left=0.10, right=0.95, top=0.95)
#
ax.set_xlim([0,len(galaxy)+1])
#ax.set_ylim([0,3.2])
ax.scatter(np.array(range(len(galaxy)))+1, list_wp50, s=100, c="black")
for i in range(len(galaxy)):
	ax.plot([i+1, i+1], [list_wp16[i], list_wp84[i]], lw=4, c="black")
#
ax.plot([0,len(galaxy)+1], [np.median(list_wp50), np.median(list_wp50)], "--", c="red")
#
plt.legend(ncol=4, loc="upper left")
plt.grid()
plt.yscale("log")
plt.xticks(np.array(range(len(galaxy)))+1, galname)
plt.xticks(rotation=90)
plt.ylabel(r"$P_{\mathsf{turb,150pc}}$ (K km s$^{-1}$)")
plt.savefig(dir_eps+"plot_pturb_all.png",dpi=200)

os.system("rm -rf *.last")
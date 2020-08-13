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
plt.ioff()


#####################
### Parameter
#####################
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = ['eso297g011', 'eso297g012', 'ic4518e', 'ic4518w', 'eso319',
          'ngc2369', 'mcg02', 'ic5179', 'iras06592',
          'eso267', 'eso557', 'irasf10409', 'ngc5257', 'ngc3110', 'irasf17138',
          'eso507', 'ngc3256', 'ngc1614', 'ngc6240']
phangs = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_eps + "../data_phangs/*mom0*")]
ylim = [0.1,100]

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

def calc_virial(
    density,
    ew,
    dbeam=150, # pc
    ):
    pturb = 3.1 * (density/100.)**-1 * (ew/10.)**2 * (dbeam/150.)**-1

    return pturb


#####################
### Main Procedure
#####################
list_wp16 = []
list_wp50 = []
list_wp84 = []
lirg_m0 = []
lirg_ew = []
list_wp16_center = []
list_wp50_center = []
list_wp84_center = []
lirg_m0_center = []
lirg_ew_center = []
for i in range(len(galaxy)):
    print(galaxy[i])
    ### all
    this_galaxy = galaxy[i]
    this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
    this_m0 = this_data[:,0] * 0.8
    this_ew = this_data[:,1]
    this_r = this_data[:,2]
    this_pturb = calc_virial(this_m0, this_ew)
    #
    cut_data = np.where((this_pturb>0) & (this_m0>0))
    this_m0 = this_m0[cut_data]
    this_ew = this_ew[cut_data]
    this_pturb = this_pturb[cut_data]
    #
    lirg_m0.extend(this_m0)
    lirg_ew.extend(this_ew)
    #
    wp50 = weighted_percentile(this_pturb,0.50,this_m0)
    wp16 = weighted_percentile(this_pturb,0.16,this_m0)
    wp84 = weighted_percentile(this_pturb,0.84,this_m0)
    #
    list_wp16.append(wp16)
    list_wp50.append(wp50)
    list_wp84.append(wp84)
    #
    ### center
    this_galaxy = galaxy[i]
    this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
    this_m0 = this_data[:,0] * 0.8
    this_ew = this_data[:,1]
    this_r = this_data[:,2]
    this_pturb = calc_virial(this_m0, this_ew)
    #
    cut_data = np.where((this_pturb>0) & (this_m0>0) & (this_r<=0.5))
    this_m0 = this_m0[cut_data]
    this_ew = this_ew[cut_data]
    this_pturb = this_pturb[cut_data]
    #
    lirg_m0_center.extend(this_m0)
    lirg_ew_center.extend(this_ew)
    #
    wp50 = weighted_percentile(this_pturb,0.50,this_m0)
    wp16 = weighted_percentile(this_pturb,0.16,this_m0)
    wp84 = weighted_percentile(this_pturb,0.84,this_m0)
    #
    list_wp16_center.append(wp16)
    list_wp50_center.append(wp50)
    list_wp84_center.append(wp84)
    #
lirg_pturb = calc_virial(np.array(lirg_m0), np.array(lirg_ew))
lirg_wp50 = weighted_percentile(lirg_pturb,0.50,lirg_m0)
lirg_wp16 = weighted_percentile(lirg_pturb,0.16,lirg_m0)
lirg_wp84 = weighted_percentile(lirg_pturb,0.84,lirg_m0)
#
lirg_pturb_center = calc_virial(np.array(lirg_m0_center), np.array(lirg_ew_center))
lirg_wp50_center = weighted_percentile(lirg_pturb_center,0.50,lirg_m0_center)
lirg_wp16_center = weighted_percentile(lirg_pturb_center,0.16,lirg_m0_center)
lirg_wp84_center = weighted_percentile(lirg_pturb_center,0.84,lirg_m0_center)
#
phangs_m0 = []
phangs_ew = []
for i in range(len(phangs)):
    this_galaxy = phangs[i]
    this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
    this_m0 = this_data[:,0] * 4.3
    this_ew = this_data[:,1]
    #
    cut_data = np.where((this_ew>0) & (this_m0>0))
    this_m0 = this_m0[cut_data]
    this_ew = this_ew[cut_data]
    #
    phangs_m0.extend(this_m0)
    phangs_ew.extend(this_ew)
    #
phangs_pturb = calc_virial(np.array(phangs_m0), np.array(phangs_ew))
phangs_wp50 = weighted_percentile(phangs_pturb,0.50,phangs_m0)
phangs_wp16 = weighted_percentile(phangs_pturb,0.16,phangs_m0)
phangs_wp84 = weighted_percentile(phangs_pturb,0.84,phangs_m0)

### figure
figure = plt.figure(figsize=(10,2))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:9])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.subplots_adjust(bottom=0.05, left=0.06, right=0.99, top=0.95)
# plot individual
ax.scatter(np.array(range(len(galaxy)))+1, list_wp50, s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9)
ax.scatter(np.array(range(len(galaxy)))+1, list_wp50_center, s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9)
for i in range(len(galaxy)):
    ax.plot([i+1, i+1], [list_wp16[i], list_wp84[i]], lw=1, c="indianred")
    ax.text(i+1-0.15, list_wp50[i], galname[i], rotation=90, horizontalalignment="right", fontsize=8, color="indianred")
    #
# plot total
ax.scatter(-0.2, phangs_wp50, s=30, c="skyblue", lw=1, edgecolors="skyblue", zorder=1e9)
ax.plot([-0.2, -0.2], [phangs_wp16, phangs_wp84], lw=2, c="skyblue")
ax.text(-0.2, 10**5.8, "PHANGS", rotation=90, horizontalalignment="center", verticalalignment="bottom", fontsize=8, color="skyblue", weight='bold')
ax.scatter(0.2, lirg_wp50, s=30, c="indianred", lw=1, edgecolors="indianred", zorder=1e9, marker="s")
ax.scatter(0.2, lirg_wp50_center, s=60, c="indianred", lw=1, edgecolors="indianred", zorder=1e9, marker="*")
ax.plot([0.2, 0.2], [lirg_wp16, lirg_wp84], lw=2, c="indianred")
ax.text(0.2, 10**5, "(U)LIRGs", rotation=90, horizontalalignment="center", verticalalignment="top", fontsize=8, color="indianred", weight='bold')
#
ax.plot([0.5,0.5], [0.1,100], "black")
# set
ax.set_xlim([-0.5,len(galaxy)+0.5])
ax.set_ylim(ylim)
plt.legend(ncol=4, loc="upper left")
plt.tick_params(labelbottom=False)
plt.grid(axis="y")
plt.yscale("log")
plt.xticks(np.r_[np.array([-0.2,0.2]), np.array(range(1,20,1))])
plt.yticks([10**-1,10**0,10**1,10**2],[-1,0,1,2])
plt.ylabel(r"log $\alpha_{\mathsf{vir,150pc}}$")
plt.savefig(dir_eps+"plot_vir_all.png",dpi=200)

# save txt
list_save = np.c_[galaxy,list_wp16,list_wp50,list_wp84,list_wp50_center]
header = "galname virial16 virial50 virial84 virial50(center)"
np.savetxt("list_virial.txt", list_save, fmt="%s", header=header)
#
list_save = np.c_[phangs,phangs_wp16,phangs_wp50,phangs_wp84]
header = "galname pturb16 pturb50 pturb84 pturb50(center)"
np.savetxt("list_pturb_phangs.txt", list_save, fmt="%s", header=header)

os.system("rm -rf *.last")

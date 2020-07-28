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
galaxy = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_proj + "*mom0*")]
phangs = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_proj + "../data_phangs/*mom0*")]


#####################
### def
#####################
def getdata(listgal):
	list_m0 = []
	list_ew = []
	for i in range(len(listgal)):
		print(str(i) + "/" + str(len(listgal)))
		this_galaxy = listgal[i]
		this_data = np.loadtxt(dir_eps+"scatter_"+this_galaxy+".txt")
		list_m0.extend(this_data[:,0])
		list_ew.extend(this_data[:,1])
	#
	list_m0 = np.array(list_m0)
	list_ew = np.array(list_ew)
	#
	cut_data = np.where((list_m0>0) & (list_ew>0))
	list_m0 = list_m0[cut_data]
	list_ew = list_ew[cut_data]

	return list_m0, list_ew

#####################
### Main Procedure
#####################
### get data
print("# get lirg data")
#lirg_m0, lirg_ew = getdata(galaxy)
print("# get phangs data")
#phangs_m0, phangs_ew = getdata(phangs)

### plot
print("# plot")
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:8,0:8])
ax2 = plt.subplot(gs[0:8,8:9])
ax3 = plt.subplot(gs[8:9,0:8])
plt.rcParams["font.size"] = 18
plt.rcParams["legend.fontsize"] = 16
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95) 
# plot
ax1.scatter(lirg_m0*0.8, lirg_ew, c="pink", s=40, alpha=0.4, linewidths=0)
ax1.scatter(phangs_m0*4.3, phangs_ew, c="skyblue", s=40, alpha=0.4, linewidths=0)
# ax1
ax1.set_xlim([10**-1,10**4.5])
ax1.set_ylim([10**-0.8,10**2.4])
ax1.grid()
ax1.set_xscale("log")
ax1.set_yscale("log")
ax1.set_xlabel(r"$\Sigma_{\mathsf{mol,150pc}}$ ($M_{\odot}$ pc$^{-2}$)")
ax1.set_ylabel(r"$\sigma_{\mathsf{mol,150pc}}$ (km s$^{-1}$)")
#
plt.legend(ncol=4, loc="upper left")
plt.savefig(dir_eps+"plot_scatter_all.png",dpi=200)

os.system("rm -rf *.last")

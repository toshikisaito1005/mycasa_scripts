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
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_proj + "*mom0*")]
phangs = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_proj + "../data_phangs/*mom0*")]
title_ulirg = str(len(galaxy)) + r" nearby (U)LIRGs " # ($\alpha_{\mathsf{CO}}$ = 0.8)"
title_phangs = str(len(phangs)) + r" nearby MS galaxies " # ($\alpha_{\mathsf{CO}}$ = 4.3)"
xlim = [-1,4.5]
ylim = [-0.1,2.7]
bins = 60

#####################
### def
#####################
def density_estimation(m1, m2,xlim,ylim):
    X, Y = np.mgrid[xlim[0]:xlim[1]:100j, ylim[0]:ylim[1]:100j]                                                     
    positions = np.vstack([X.ravel(), Y.ravel()])                                                       
    values = np.vstack([m1, m2])                                                                        
    kernel = scipy.stats.gaussian_kde(values)                                                                 
    Z = np.reshape(kernel(positions).T, X.shape)
    return X, Y, Z

def getdata(listgal, alphaco):
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
	list_m0 = np.log10(list_m0[cut_data] * alphaco)
	list_ew = np.log10(list_ew[cut_data])

	return list_m0, list_ew

#####################
### Main Procedure
#####################
### get data
print("# get lirg data")
lirg_m0, lirg_ew = getdata(galaxy, 0.8)
print("# get phangs data")
#phangs_m0, phangs_ew = getdata(phangs, 4.3)

### plot
print("# plot")
figure = plt.figure(figsize=(10,10))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax1 = plt.subplot(gs[0:7,0:7])
ax2 = plt.subplot(gs[0:7,7:9])
ax3 = plt.subplot(gs[7:9,0:7])
ax2b = ax2.twinx()
plt.rcParams["font.size"] = 20
plt.rcParams["legend.fontsize"] = 18
plt.subplots_adjust(bottom=0.15, left=0.20, right=0.90, top=0.85) 
# plot ax1 scatter
ax1.scatter(phangs_m0, phangs_ew, c="powderblue", s=40, linewidths=0)
ax1.scatter(lirg_m0, lirg_ew, c="indianred", s=40, linewidths=0)
ax1.text(xlim[0]+(xlim[1]-xlim[0])*0.04, ylim[0]+(ylim[1]-ylim[0])*0.93, title_phangs+"("+str("{:,}".format(len(phangs_m0)))+")", color="skyblue")
ax1.text(xlim[0]+(xlim[1]-xlim[0])*0.04, ylim[0]+(ylim[1]-ylim[0])*0.87, title_ulirg+"("+str("{:,}".format(len(lirg_m0)))+")", color="indianred")
# plot ax1 contour
#X, Y, Z = density_estimation(phangs_m0, phangs_ew, xlim, ylim)
ax1.contourf(X, Y, Z, [0.015,0.15,1.5,Z.max()], colors=[cm.Blues(1/4.),cm.Blues(2/4.),cm.Blues(3/4.),cm.Blues(4/4.)], linewidths=[1], alpha=0.5)
ax1.contour(X, Y, Z, [0.015,0.15,1.5,Z.max()], colors=["blue"], linewidths=[0.5], alpha=0.3)
A, B, C = density_estimation(lirg_m0, lirg_ew, xlim, ylim)
ax1.contourf(A, B, C, [0.05,0.2,1.0,C.max()], colors=[cm.Reds(3/4.),cm.Reds(3.3/4.),cm.Reds(3.6/4.),cm.Reds(3.9/4.)], linewidths=[1], alpha=0.5)
ax1.contour(A, B, C, [0.05,0.2,1.0,C.max()], colors=["red"], linewidths=[0.5], alpha=0.3)
# plot ax2 right
histo = np.histogram(phangs_ew, bins=bins, range=ylim)
x = np.delete(histo[1],-1)
y = histo[0]/(histo[0].max()*1.05)
height = (ylim[1]-ylim[0])/bins
ax2b.plot(y, x, drawstyle="steps", color="grey", lw=0.5)
ax2b.barh(x, y, height=height, lw=0, color="skyblue", alpha=0.5)
#
histo = np.histogram(lirg_ew, bins=bins, range=ylim)
x = np.delete(histo[1],-1)
y = histo[0]/(histo[0].max()*1.05)
height = (ylim[1]-ylim[0])/bins
ax2b.plot(y, x, drawstyle="steps", color="grey", lw=0.5)
ax2b.barh(x, y, height=height, lw=0, color="indianred", alpha=0.5)
# plot ax3 bottom
histo = np.histogram(phangs_m0, bins=bins, range=xlim)
y = np.delete(histo[1],-1)
x = histo[0]/(histo[0].max()*1.05)
width = (xlim[1]-xlim[0])/bins
ax3.plot(y ,x, drawstyle="steps-mid", color="grey", lw=0.5)
ax3.bar(y, x, width=width, lw=0, color="skyblue", alpha=0.5, align="center")
#
histo = np.histogram(lirg_m0, bins=bins, range=xlim)
y = np.delete(histo[1],-1)
x = histo[0]/(histo[0].max()*1.05)
width = (xlim[1]-xlim[0])/bins
ax3.plot(y ,x, drawstyle="steps-mid", color="grey", lw=0.5)
ax3.bar(y, x, width=width, lw=0, color="indianred", alpha=0.5, align="center")
# set ax1 scatter
ax1.set_xlim(xlim)
ax1.set_ylim(ylim)
ax1.grid()
ax1.tick_params(labelbottom=False)
ax1.set_ylabel(r"log $\sigma_{\mathsf{mol,150pc}}$ (km s$^{-1}$)")
# set ax2 right
ax2.tick_params(labelbottom=False,labelleft=False)
ax2.spines["top"].set_visible(False)
ax2.spines["bottom"].set_visible(False)
ax2.tick_params(top=False,bottom=False)
ax2b.set_ylim(ylim)
ax2b.grid(axis="y")
ax2b.tick_params(labelbottom=False)
ax2b.spines["top"].set_visible(False)
ax2b.spines["bottom"].set_visible(False)
ax2b.tick_params(top=False,bottom=False)
ax2b.set_ylabel(r"log $\sigma_{\mathsf{mol,150pc}}$ (km s$^{-1}$)")
# set ax3 bottom
ax3.set_xlim(xlim)
ax3.set_ylim(1,0)
ax3.grid(axis="x")
ax3.tick_params(labelleft=False)
ax3.spines["left"].set_visible(False)
ax3.spines["right"].set_visible(False)
ax3.tick_params(left=False,right=False)
ax3.set_xlabel(r"log $\Sigma_{\mathsf{mol,150pc}}$ ($M_{\odot}$ pc$^{-2}$)")
#
ax1.
#
plt.legend(ncol=4, loc="upper left")
plt.savefig(dir_eps+"plot_scatter_all.png",dpi=200)

os.system("rm -rf *.last")

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
dir_proj = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/data/"
dir_eps = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/eps/"
galaxy = ['eso267','eso297g011','eso297g012','eso319','eso507','eso557','ic4518e','ic4518w','ic5179','iras06592','irasf10409','irasf17138','mcg02','ngc1614','ngc2369','ngc3110','ngc3256','ngc5257','ngc6240']
phangs = [s.split("/")[-1].split("_12m")[0] for s in glob.glob(dir_eps + "../data_phangs/*mom0*")]
ylim = [0.1,100]

galname1 = [s.replace("eso","ESO ").replace("ngc","NGC ").replace("mcg","MCG-") for s in galaxy]
galname2 = [s.replace("e","E").replace("w","W").replace("ic","IC") for s in galname1]
galname3 = [s.replace("iras","IRAS ").replace("f","F").replace("g","-G") for s in galname2]
galname4 = [s.replace("319","319-G022").replace("507","507-G070") for s in galname3]
galname5 = [s.replace("557","557-G002").replace("06592","06592-6313") for s in galname4]
galname6 = [s.replace("10409","10409-4556").replace("17138","17138-1017") for s in galname5]
galname = [s.replace("mcg02","mcg-02-33-098").replace("267","267-G030") for s in galname6]


#####################
### Main Procedure
#####################
###
list_all = []
for i in range(len(galaxy)):
#for i in [0]:
	this_galaxy = galaxy[i]
	print("# working on " + this_galaxy)
	# get image
	this_mom0 = glob.glob(dir_proj + this_galaxy + "*_mom0.fits")[0]
	# get box
	this_header = imhead(this_mom0,mode="list")
	shape = this_header["shape"]
	box = "0,0," + str(shape[0]-1) + "," + str(shape[1]-1)
	# pixel size in parsec
	this_scale = 150/this_header["beammajor"]["value"]
	pixsize = abs(this_header["cdelt1"])*3600*180/np.pi * this_scale / 1000.
	pixarea  = pixsize**2
	# galarea in kpc^2
	this_data = imval(this_mom0, box=box)
	galarea = sum(this_data["mask"].flatten()) * pixarea
	radius = np.sqrt(galarea / np.pi)
	# get pturb
	data = np.loadtxt("list_pturb.txt", dtype="str")
	this_pturb = data[data[:,0]==this_galaxy][:,1:]
	# get virial
	data = np.loadtxt("list_virial.txt", dtype="str")
	this_virial = data[data[:,0]==this_galaxy][:,1:]
	# combine list
	this_list = np.c_[np.array(this_galaxy),radius,this_pturb,this_virial][0]
	list_all.append(this_list.tolist())
	#
list_all = np.array(list_all)
list_all = list_all[list_all[:,1].argsort()]
list_name = list_all[:,0]
list_r = list_all[:,1].astype("float64")
list_pturb = list_all[:,2:6].astype("float64")
list_virial = list_all[:,6:10].astype("float64")

###
phangs_all = []
for i in range(len(phangs)):
#for i in [0]:
	this_galaxy = phangs[i]
	print("# working on " + this_galaxy)
	# get image
	this_mom0 = glob.glob(dir_proj + "../data_phangs/" + this_galaxy + "*_mom0_150pc.fits")[0]
	# get box
	this_header = imhead(this_mom0,mode="list")
	shape = this_header["shape"]
	box = "0,0," + str(shape[0]-1) + "," + str(shape[1]-1)
	# pixel size in parsec
	this_scale = 150/this_header["beammajor"]["value"]
	pixsize = abs(this_header["cdelt1"])*3600*180/np.pi * this_scale / 1000.
	pixarea  = pixsize**2
	# galarea in kpc^2
	this_data = imval(this_mom0, box=box)
	galarea = sum(this_data["mask"].flatten()) * pixarea
	radius = np.sqrt(galarea / np.pi)
	# get pturb
	data = np.loadtxt("list_pturb_phangs.txt", dtype="str")
	this_pturb = data[data[:,0]==this_galaxy][:,1:]
	# get virial
	data = np.loadtxt("list_virial_phangs.txt", dtype="str")
	this_virial = data[data[:,0]==this_galaxy][:,1:]
	# combine list
	this_list = np.c_[np.array(this_galaxy),radius,this_pturb,this_virial][0]
	phangs_all.append(this_list.tolist())
	#
phangs_all = np.array(phangs_all)
phangs_all = phangs_all[phangs_all[:,1].argsort()]
phangs_name = phangs_all[:,0]
phangs_r = phangs_all[:,1].astype("float64")
phangs_pturb = phangs_all[:,2:5].astype("float64")
phangs_virial = phangs_all[:,5:8].astype("float64")


# plot
figure = plt.figure(figsize=(5,5))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:9])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax.plot(list_r, list_pturb[:,1], c="indianred")
ax.plot(list_r, list_pturb[:,3], "--", c="indianred")
ax.scatter(list_r, list_pturb[:,1], s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9)
ax.scatter(list_r, list_pturb[:,3], s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9)
#for i in range(len(galaxy)):
#    ax.plot([list_r[i], list_r[i]], [list_pturb[i,0], list_pturb[i,2]], lw=1, c="indianred")
#
ax.plot(phangs_r, phangs_pturb[:,1], c="skyblue")
ax.scatter(phangs_r, phangs_pturb[:,1], s=20, marker="s", c="white", lw=1, edgecolors="skyblue", zorder=1e9)
#
plt.xscale("log")
plt.yscale("log")
#plt.xlim([0.6,4.5])
plt.xlabel(r"log CO Radius (kpc)")
plt.ylabel(r"log $P_{\mathsf{turb,150pc}}$ (K cm$^{-3}$)")
plt.savefig(dir_eps+"plot_size_pturb.png",dpi=200)


# plot
figure = plt.figure(figsize=(5,5))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:9])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax.plot(list_r, list_virial[:,1], c="indianred")
ax.plot(list_r, list_virial[:,3], "--", c="indianred")
ax.scatter(list_r, list_virial[:,1], s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9)
ax.scatter(list_r, list_virial[:,3], s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9)
#for i in range(len(galaxy)):
#    ax.plot([list_r[i], list_r[i]], [list_pturb[i,0], list_pturb[i,2]], lw=1, c="indianred")
#
plt.xscale("log")
plt.yscale("log")
plt.xlim([0.6,4.5])
plt.ylim([3,40])
plt.xlabel(r"log CO Radius (kpc)")
plt.ylabel(r"log $\alpha_{\mathsf{vir,150pc}}$")
plt.savefig(dir_eps+"plot_size_virial.png",dpi=200)


#
os.system("rm -rf *last")

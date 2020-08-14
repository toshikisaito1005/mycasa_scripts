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
### def
#####################
def deltaMS(sfr,mass):
	log_sfr_ms = (-0.32*(np.log10(mass)-np.log10(10**10))-10.17) + np.log10(mass)
	#ms_offset = np.log10(sfr) - log_sfr_ms
	ms_offset = sfr / 10**log_sfr_ms

	return ms_offset


#####################
### Main Procedure
#####################
###
data = np.loadtxt("list_sfr_stellar.txt", dtype="str")
lirg_name = data[:,0]
lirg_logSFR = 10**data[:,1].astype("float64")
lirg_logMstar = 10**data[:,2].astype("float64")
#
hdu_list = fits.open(dir_eps + "../data_other/phangs_sample_table_v1p5.fits", memmap=True)
evt_data = Table(hdu_list[1].data)
phangs_name = evt_data["name"]
phangs_logSFR = evt_data["props_sfr"] # np.log10(evt_data["props_sfr"])
phangs_logMstar = evt_data["props_mstar"] # np.log10(evt_data["props_mstar"])


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
	#
	index = np.where(lirg_name==this_galaxy)[0]
	if index:
		index = index[0]
		stellarmass = lirg_logMstar[index]
		sfr = lirg_logSFR[index]
	else:
		stellarmass = 0
		sfr = 0
	# combine list
	this_list = np.c_[np.array(this_galaxy),radius,this_pturb,this_virial,stellarmass,sfr][0]
	list_all.append(this_list.tolist())
	#
list_all = np.array(list_all)
list_all = list_all[list_all[:,1].argsort()]
list_name = list_all[:,0]
list_r = list_all[:,1].astype("float64")
list_pturb = list_all[:,2:6].astype("float64")
list_virial = list_all[:,6:10].astype("float64")
list_mass = list_all[:,10].astype("float64")
list_sfr = list_all[:,11].astype("float64")
list_delta = deltaMS(list_sfr,list_mass)


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
	#
	index = np.where(phangs_name==this_galaxy)[0][0]
	stellarmass = phangs_logMstar[index]
	sfr = phangs_logSFR[index]
	# combine list
	this_list = np.c_[np.array(this_galaxy),radius,this_pturb,this_virial,stellarmass,sfr][0]
	phangs_all.append(this_list.tolist())
	#
phangs_all = np.array(phangs_all)
phangs_all = phangs_all[phangs_all[:,1].argsort()]
phangs_name = phangs_all[:,0]
phangs_r = phangs_all[:,1].astype("float64")
phangs_pturb = phangs_all[:,2:5].astype("float64")
phangs_virial = phangs_all[:,5:8].astype("float64")
phangs_mass = phangs_all[:,8].astype("float64")
phangs_sfr = phangs_all[:,9].astype("float64")
phangs_delta = deltaMS(phangs_sfr,phangs_mass)


# plot
figure = plt.figure(figsize=(5,3))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:7])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 8
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax.scatter(phangs_mass, phangs_pturb[:,1], s=10, marker="o", c="white", lw=1, edgecolors="skyblue", zorder=1e9, label="PHANGS")
#
ax.scatter(list_mass, list_pturb[:,1], s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9, label="(U)LIRGs")
ax.scatter(list_mass, list_pturb[:,3], s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9, label="(U)LIRG centers")
#for i in range(len(galaxy)):
#    ax.plot([list_r[i], list_r[i]], [list_pturb[i,0], list_pturb[i,2]], lw=1, c="indianred")
#
plt.xscale("log")
plt.yscale("log")
plt.xlim([10**8.9,10**12])
plt.ylim([10**2.1,10**9.2])
plt.xlabel(r"log $M_{\star}$ ($M_{\odot}$)")
plt.ylabel(r"log $P_{\mathsf{turb,150pc}}$ (K cm$^{-3}$)")
plt.xticks([10**9,10**10,10**11,10**12],[9,10,11,12])
plt.yticks([10**3,10**4,10**5,10**6,10**7,10**8,10**9],[3,4,5,6,7,8,9])
plt.savefig(dir_eps+"plot_mass_pturb.png",dpi=200)

# plot
cut_phangs = np.where((phangs_mass>10**10.3) & (phangs_mass<10**11.1))
cut_lirg = np.where((list_mass>10**10.3) & (list_mass<10**11.1))
#
figure = plt.figure(figsize=(5,3))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:7])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 8
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax.scatter(phangs_delta[cut_phangs], phangs_pturb[:,1][cut_phangs], s=10, marker="o", c="white", lw=1, edgecolors="skyblue", zorder=1e9, label="PHANGS")
#
ax.scatter(list_delta[cut_lirg], list_pturb[:,1][cut_lirg], s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9, label="(U)LIRGs")
ax.scatter(list_delta[cut_lirg], list_pturb[:,3][cut_lirg], s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9, label="(U)LIRG centers")
#for i in range(len(galaxy)):
#    ax.plot([list_r[i], list_r[i]], [list_pturb[i,0], list_pturb[i,2]], lw=1, c="indianred")
#
plt.xscale("log")
plt.yscale("log")
ax.set_xlim([10**-1.1,10**1.5])
plt.ylim([10**2.1,10**9.2])
plt.xlabel(r"log $\Delta_{\mathsf{MS}}$")
plt.ylabel(r"log $P_{\mathsf{turb,150pc}}$ (K cm$^{-3}$)")
plt.xticks([10**-1,10**0,10**1],[-1,0,1])
plt.yticks([10**3,10**4,10**5,10**6,10**7,10**8,10**9],[3,4,5,6,7,8,9])
plt.savefig(dir_eps+"plot_deltams_pturb.png",dpi=200)


# plot
figure = plt.figure(figsize=(5,3))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:7])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 10
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax.scatter(phangs_mass, phangs_virial[:,1], s=10, marker="o", c="white", lw=1, edgecolors="skyblue", zorder=1e9)
#
ax.scatter(list_mass, list_virial[:,1], s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9)
ax.scatter(list_mass, list_virial[:,3], s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9)
#for i in range(len(galaxy)):
#    ax.plot([list_r[i], list_r[i]], [list_pturb[i,0], list_pturb[i,2]], lw=1, c="indianred")
#
plt.xscale("log")
plt.yscale("log")
plt.xlim([10**8.9,10**12])
plt.ylim([1.5,40])
plt.xlabel(r"log $M_{\star}$ ($M_{\odot}$)")
plt.ylabel(r"log $\alpha_{\mathsf{vir,150pc}}$")
plt.xticks([10**9,10**10,10**11,10**12],[9,10,11,12])
plt.yticks([10**np.log10(3),10**1,10**np.log10(30)],[3,10,30])
plt.savefig(dir_eps+"plot_mass_virial.png",dpi=200)

# plot
figure = plt.figure(figsize=(5,3))
gs = gridspec.GridSpec(nrows=9, ncols=9)
ax = plt.subplot(gs[0:9,0:7])
plt.rcParams["font.size"] = 10
plt.rcParams["legend.fontsize"] = 8
plt.subplots_adjust(bottom=0.15, left=0.15, right=0.95, top=0.95)
#
ax.scatter(phangs_delta, phangs_virial[:,1], s=10, marker="o", c="white", lw=1, edgecolors="skyblue", zorder=1e9, label="PHANGS")
#
ax.scatter(list_delta, list_virial[:,1], s=20, marker="s", c="white", lw=1, edgecolors="indianred", zorder=1e9, label="(U)LIRGs")
ax.scatter(list_delta, list_virial[:,3], s=40, marker="*", c="white", lw=1, edgecolors="indianred", zorder=1e9, label="(U)LIRG centers")
#for i in range(len(galaxy)):
#    ax.plot([list_r[i], list_r[i]], [list_pturb[i,0], list_pturb[i,2]], lw=1, c="indianred")
#
plt.xscale("log")
plt.yscale("log")
ax.set_xlim([10**-1.1,10**1.5])
plt.ylim([1.5,40])
plt.xlabel(r"log $\Delta_{\mathsf{MS}}$")
plt.ylabel(r"log $\alpha_{\mathsf{vir,150pc}}$")
plt.xticks([10**-1,10**0,10**1],[-1,0,1])
plt.yticks([10**np.log10(3),10**1,10**np.log10(30)],[3,10,30])
plt.savefig(dir_eps+"plot_deltams_virial.png",dpi=200)


#
os.system("rm -rf *last")

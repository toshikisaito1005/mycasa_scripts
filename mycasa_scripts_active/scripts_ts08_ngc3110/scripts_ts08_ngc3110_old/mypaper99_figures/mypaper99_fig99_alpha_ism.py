import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim


dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_output = "../../../ngc3110/ana/eps/"
data_sfr = "ngc3110_sfr.txt"
data_alpha = "ngc3110_alpha_ism.txt"
data_fl = "ngc3110_flux_uvlim.txt"

# center
ra = "10h04m02.090s"
decl = "-6d28m29.604s"
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60


#####################
### Main Procedure
#####################
# SFR
data = np.loadtxt(dir_data + data_sfr,
                  usecols = (0,1,2))
d_sfr = data[:,2]
#  alpha
data = np.loadtxt(dir_data + data_alpha,
                  usecols = (0,1,2,3))
d_ra, d_decl = data[:,0], data[:,1]
d_imass = data[:,3]
d_co10 = data[:,2] * 795443.
d_alpha = d_imass / d_co10
for i in range(len(d_alpha)):
    if d_co10[i] == 0:
        d_alpha[i] = 0
# CO lines
data = np.loadtxt(dir_data + data_fl,
                  usecols = (0,1,2,3,4,5,6))
d_13co21, d_co21 = data[:,6], data[:,4]
d_13co10, d_co10 = data[:,5], data[:,3]

area1 = (3. * 0.325 / 2.) ** 2 * np.pi
area2 = (3. * 0.325 / 2.) ** 2 * np.pi * 1.e+6

ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

value = np.sqrt((d_ra - ra_cent_deg) ** 2 + (d_decl - decl_cent_deg) ** 2) * 3600.


### $^{12/13}R_{2-1}$ - SFE
ratio = d_co21/d_co10
for i in range(len(ratio)):
    if d_co10[i] == 0:
        ratio[i] = 0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("alpha")
plt.ylabel("$^{12}R_{2-1/1-0}$")
#plt.xlim([3e-10, 3e-8])
#plt.ylim([1e+0, 1e+2])
plt.title("alpha - $^{12}R_{2-1/1-0}$")
plt.scatter(d_alpha, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
plt.colorbar()
plt.clim([0, max(value) * 0.8])

os.system("rm -rf " + dir_output + "plot_alpha_R_co21_co10.png")
plt.savefig(dir_output + "plot_alpha_R_co21_co10.png", dpi=300)


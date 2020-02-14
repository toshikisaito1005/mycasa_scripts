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
data_h2 = "ngc3110_H2mass.txt"
data_fl = "ngc3110_flux_uvlim.txt"
data_radex = "ngc3110_radex_map.txt"

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
# CO lines
data = np.loadtxt(dir_data + data_fl,
                  usecols = (0,1,2,3,4,5,6))
d_13co21, d_co21 = data[:,6], data[:,4]
d_13co10, d_co10 = data[:,5], data[:,3]
# H2 mass
data = np.loadtxt(dir_data + data_h2,
                  usecols = (0,1,2))
d_ra, d_decl = data[:,0], data[:,1]
d_h2 = data[:,2]
d_sfe = d_sfr / d_h2
for i in range(len(d_sfe)):
    if d_h2[i] == 0:
        d_sfe[i] = 0

area1 = (3. * 0.325 / 2.) ** 2 * np.pi
area2 = (3. * 0.325 / 2.) ** 2 * np.pi * 1.e+6

# distance from the nucleus
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325


### $^{12/13}R_{2-1}$ - SFE
ratio = d_co21/d_13co21
for i in range(len(ratio)):
    if d_13co21[i] == 0:
        ratio[i] = 0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("SFE (yr$^{-1}$)")
plt.ylabel("$^{12/13}R_{2-1}$")
plt.xlim([3e-10, 3e-8])
plt.ylim([1e+0, 1e+2])
plt.title("SFE - $^{12/13}R_{2-1}$")
plt.scatter(d_sfe, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_sfe_R_co21_13co21.png")
plt.savefig(dir_output + "plot_sfe_R_co21_13co21.png", dpi=300)


### $^{12/13}R_{1-0}$ - SFE
ratio = d_co10/d_13co10
for i in range(len(ratio)):
    if d_13co10[i] == 0:
        ratio[i] = 0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("SFE (yr$^{-1}$)")
plt.ylabel("$^{12/13}R_{1-0}$")
plt.xlim([3e-10, 3e-8])
plt.ylim([1e+0, 1e+2])
plt.title("SFE - $^{12/13}R_{1-0}$")
plt.scatter(d_sfe, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_sfe_R_co10_13co10.png")
plt.savefig(dir_output + "plot_sfe_R_co10_13co10.png", dpi=300)


### $^{12}R_{2-1/1-0}$ - SFE
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
plt.xlabel("SFE (yr$^{-1}$)")
plt.ylabel("$^{12}R_{2-1/1-0}$")
plt.xlim([3e-10, 3e-8])
plt.ylim([7.e-2, 7.e+0])
plt.title("SFE - $^{12}R_{2-1/1-0}$")
plt.scatter(d_sfe, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_sfe_R_co21_co10.png")
plt.savefig(dir_output + "plot_sfe_R_co21_co10.png", dpi=300)


### $^{12}R_{2-1/1-0}$ - SFE
ratio = d_13co21/d_13co10
for i in range(len(ratio)):
    if d_13co10[i] == 0:
        ratio[i] = 0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("SFE (yr$^{-1}$)")
plt.ylabel("$^{13}R_{2-1/1-0}$")
plt.xlim([3e-10, 3e-8])
plt.ylim([7.e-2, 7.e+0])
plt.title("SFE - $^{13}R_{2-1/1-0}$")
plt.scatter(d_sfe, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_sfe_R_13co21_13co10.png")
plt.savefig(dir_output + "plot_sfe_R_13co21_13co10.png", dpi=300)



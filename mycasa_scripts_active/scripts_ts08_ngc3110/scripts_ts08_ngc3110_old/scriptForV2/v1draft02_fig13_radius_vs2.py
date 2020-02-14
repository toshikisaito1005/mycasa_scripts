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
data_ism = "ngc3110_ISMmass.txt"
data_ssc = "ngc3110_flux_ssc.txt"
data_radex1 = "ngc3110_radex_map_22.0.txt"
data_radex2 = "ngc3110_radex_map_22.2.txt"
data_radex3 = "ngc3110_radex_map_22.4.txt"

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
area1 = (3. * 0.325 / 2.) ** 2 * np.pi
area2 = (3. * 0.325 / 2.) ** 2 * np.pi * 1.e+6

# SFR
data = np.loadtxt(dir_data + data_sfr,
                  usecols = (0,1,2))
d_sfr = data[:,2] / area1
# CO lines
data = np.loadtxt(dir_data + data_fl,
                  usecols = (0,1,2,3,4,5,6))
d_13co21, d_co21 = data[:,6], data[:,4]
d_13co10, d_co10 = data[:,5], data[:,3]
# H2 mass
data = np.loadtxt(dir_data + data_h2,
                  usecols = (0,1,2))
d_ra, d_decl = data[:,0], data[:,1]
d_h2 = data[:,2] / area2
# ISM mass
data = np.loadtxt(dir_data + data_ism,
                  usecols = (0,1,2))
d_ism = data[:,2]
# SSC
data = np.loadtxt(dir_data + data_ssc,
                  usecols = (0,1,2))
d_ssc = data[:,2]


area1 = (3. * 0.325 / 2.) ** 2 * np.pi
area2 = (3. * 0.325 / 2.) ** 2 * np.pi * 1.e+6

# radex1 = 22.2
data = np.loadtxt(dir_data + data_radex1,
                  usecols = (0,1,2,3))
d_Tkin1 = data[:,2]
d_nH21 = data[:,3]

# radex2 = 22.5
data = np.loadtxt(dir_data + data_radex2,
                  usecols = (0,1,2,3))
d_Tkin2 = data[:,2]
d_nH22 = data[:,3]

# radex3 = 22.5
data = np.loadtxt(dir_data + data_radex3,
                  usecols = (0,1,2,3))
d_Tkin3 = data[:,2]
d_nH23 = data[:,3]

# distance from the nucleus
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325


### radius - $^{12/13}R_{2-1}$
ratio = d_co21/d_13co21
for i in range(len(ratio)):
    if d_13co21[i] == 0:
        ratio[i] = 0

value2 = value[value != 0]
value_mean = np.mean(value2)
value_median = np.median(value2)

plt.figure()
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['xtick.minor.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
plt.rcParams['ytick.minor.width'] = 1.5
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("$^{12/13}R_{2-1}$")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([1e+0, 1e+2])
plt.title("Radial $^{12/13}R_{2-1}$")
plt.plot([1.5e-1, 1.5e+1], [value_mean, value_mean],
         color = "black", lw = 2,
         label="mean = "+str(round(value_mean, 1)))
plt.plot([1.5e-1, 1.5e+1], [value_median, value_median], "--",
         color = "black", lw = 2,
         label="median = "+str(round(value_median, 1)))
plt.scatter(value, ratio, s=130, color = "skyblue", linewidths=0)
plt.legend()
#plt.scatter(value, ratio,
#            c = value,
#            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
#cbar = plt.colorbar()
#cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_R_co21_13co21.png")
plt.grid(which='major',color='grey',linestyle='-')
plt.grid(which='minor',color='grey',linestyle='--')
plt.savefig(dir_output + "plot_radius_R_co21_13co21.png", dpi=300)


### radius - $^{12}R_{2-1/1-0}$
ratio = d_co21/d_co10
for i in range(len(ratio)):
    if d_co10[i] == 0:
        ratio[i] = 0

value2 = ratio[ratio != 0]
value_mean = np.mean(value2)
value_median = np.median(value2)

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("$^{12}R_{2-1/1-0}$")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([7.e-2, 7.e+0])
plt.title("Radial $^{12}R_{2-1/1-0}$")
plt.plot([1.5e-1, 1.5e+1], [value_mean, value_mean],
         color = "black", lw = 2,
         label="mean = "+str(round(value_mean, 2)))
plt.plot([1.5e-1, 1.5e+1], [value_median, value_median], "--",
         color = "black", lw = 2,
         label="median = "+str(round(value_median, 2)))
plt.scatter(value, ratio, s=130, color="skyblue", linewidths=1)
plt.legend()
"""
    plt.scatter(value, ratio,
    c = value,
    s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
    """
#cbar = plt.colorbar()
#cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_R_co21_co10.png")
plt.grid(which='major',color='grey',linestyle='-')
plt.grid(which='minor',color='grey',linestyle='--')
plt.savefig(dir_output + "plot_radius_R_co21_co10.png", dpi=300)


### radius - Tkin1 = 22.0
value2 = d_Tkin1[np.where(value < 1.3)[0]]
value_mean = np.mean(value2)
value_median = np.median(value2)

value3 = d_Tkin2[np.where(value < 1.3)[0]]
value_mean2 = np.mean(value3)
value_median2 = np.median(value3)

value4 = d_Tkin3[np.where(value < 1.3)[0]]
value_mean3 = np.mean(value4)
value_median3 = np.median(value4)

d_Tkin_mean = (d_Tkin1 + d_Tkin2 + d_Tkin3) / 3.
value5 = d_Tkin_mean[d_Tkin_mean != 0]
value_mean4 = np.mean(value5)
value_median4 = np.median(value5)

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("Kinetic Temperature (K)")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([1.e-0, 1.e+2])
plt.title("Radial Kinetic Temperature")
plt.plot([1.5e-1, 1.5e+1], [value_mean, value_mean],
         color = "blue", lw = 2,
         )#label="$\mu$(T$_{kin}$) = "+str(int(value_mean))+" K")
plt.plot([1.5e-1, 1.5e+1], [value_mean2, value_mean2],
         color = "green", lw = 2,
         )#label="mean = "+str(int(value_mean2))+" K")
plt.plot([1.5e-1, 1.5e+1], [value_mean3, value_mean3],
         color = "red", lw = 2,
         )#label="mean = "+str(int(value_mean3))+" K")
#plt.plot([1.5e-1, 1.5e+1], [value_mean4, value_mean4],
#         color = "black", lw = 2,
#         label="mean = "+str(round(value_mean4, 2)))
plt.scatter(value, d_Tkin1, s=130, color="skyblue", linewidths=0, alpha = 0.4,
            label = "$N_{H_2}$ = 10$^{22.0}$ cm$^{-3}$")
plt.scatter(value, d_Tkin2, s=130, color="limegreen", linewidths=0, alpha = 0.4,
            label = "$N_{H_2}$ = 10$^{22.2}$ cm$^{-3}$")
plt.scatter(value, d_Tkin3, s=130, color="darksalmon", linewidths=0, alpha = 0.4,
            label = "$N_{H_2}$ = 10$^{22.4}$ cm$^{-3}$")
#plt.scatter(value, d_Tkin_mean, s=130, color="black", linewidths=0, alpha = 0.7)
plt.legend(loc = "lower left")
"""
plt.scatter(value, ratio,
c = value,
s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
"""
#cbar = plt.colorbar()
#cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_Tkin1.png")
plt.savefig(dir_output + "plot_radius_Tkin1.png", dpi=300)


"""
### radius - nH21 = 22.0
value2 = d_nH21[d_nH21 != 10]
value_mean = np.mean(value2)
value_median = np.median(value2)

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
#plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("Kinetic Temperature (K)")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([1.e+3, 1.e+7])
plt.title("Radial Kinetic Temperature")
plt.plot([1.5e-1, 1.5e+1], [value_mean, value_mean],
         color = "black", lw = 2,
         label="mean = "+str(round(value_mean, 2)))
plt.plot([1.5e-1, 1.5e+1], [value_median, value_median], "--",
         color = "black", lw = 2,
         label="median = "+str(round(value_median, 2)))
plt.scatter(value, d_nH21, s=130, color="skyblue", linewidths=1)
plt.legend()
#cbar = plt.colorbar()
#cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_R_co21_co10.png")
plt.savefig(dir_output + "plot_radius_nH21.png", dpi=300)
"""

"""
### radius - $^{12/13}R_{1-0}$
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
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("$^{12/13}R_{1-0}$")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([1e+0, 1e+2])
plt.title("Radial $^{12/13}R_{1-0}$")
plt.scatter(value, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_R_co10_13co10.png")
plt.savefig(dir_output + "plot_radius_R_co10_13co10.png", dpi=300)

### radius - $^{12}R_{2-1/1-0}$
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
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("$^{13}R_{2-1/1-0}$")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([7.e-2, 7.e+0])
plt.title("Radial $^{13}R_{2-1/1-0}$")
plt.scatter(value, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_R_13co21_13co10.png")
plt.savefig(dir_output + "plot_radius_R_13co21_13co10.png", dpi=300)


### radius - SFE
ratio = d_sfr/(d_h2 * 1000000.)
for i in range(len(ratio)):
    if d_h2[i] == 0:
        ratio[i] = 0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("SFE (yr$^{-1}$)")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([3.e-10, 3.e-8])
plt.title("Radial SFE")
plt.scatter(value, ratio,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_SFE.png")
plt.savefig(dir_output + "plot_radius_SFE.png", dpi=300)


### radius - SSC
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("sigma SSC")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([2e-1, 2e+1])
plt.title("Radial SSC")
plt.scatter(value, d_ssc,
            c = value,
            s = 90, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_radius_SSC.png")
plt.savefig(dir_output + "plot_radius_SSC.png", dpi=300)
"""


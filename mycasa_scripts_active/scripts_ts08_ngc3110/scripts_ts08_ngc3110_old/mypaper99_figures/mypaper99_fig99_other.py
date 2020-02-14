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
from numpy import linspace, meshgrid
from matplotlib.mlab import griddata



dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_output = "../../../ngc3110/ana/eps/"
data_sfr = "ngc3110_sfr.txt"
data_h2 = "ngc3110_H2mass.txt"
data_fl = "ngc3110_flux_uvlim.txt"
data_ssc = "ngc3110_flux_ssc.txt"
data_flux_normal = "ngc3110_flux_contin.txt"
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
area1 = (3. * 0.325 / 2.) ** 2 * np.pi
area2 = (3. * 0.325 / 2.) ** 2 * np.pi * 1.e+6

# SFR
data = np.loadtxt(dir_data + data_sfr,
                  usecols = (0,1,2))
d_sfr = data[:,2] / area1

# Tkin, nH2
data = np.loadtxt(dir_data + data_radex,
                  usecols = (0,1,2,3))
d_ra_radex, d_decl_radex = data[:,0], data[:,1]
d_Tkin, d_nH2 = data[:,2], data[:,3]

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
d_sfe = d_sfr / d_h2
for i in range(len(d_sfe)):
    if d_h2[i] == 0:
        d_sfe[i] = 0

# SSC
data = np.loadtxt(dir_data + data_ssc,
                  usecols = (0,1,2))
d_ra, d_decl = data[:,0], data[:,1]
d_ssc = data[:,2]

# spectral index
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3,4))
d_band3, d_band6 = data[:,3], data[:,4]

# distance from the nucleus
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325

### SSC - SFE
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.ylabel("SFE (yr$^{-1}$)")
plt.xlabel("$\Sigma_{SSC}$ (kpc$^{-2}$)")
plt.ylim([3e-10, 3e-8])
plt.xlim([2.e-1, 2.e+1])
plt.title("$\Sigma_{SSC}$ - SFE")
plt.scatter(d_ssc, d_sfe/1e6,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_sfe_ssc.png")
plt.savefig(dir_output + "plot_sfe_ssc.png", dpi=300)


### SSC - spectral index
ratio = np.log10(d_band6/d_band3)/np.log10(234.6075/104.024625)
for i in range(len(ratio)):
    if d_band3[i] == 0.0:
        ratio[i] = 0.0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.ylabel("Spectral Index")
plt.xlabel("$\Sigma_{SSC}$ (kpc$^{-2}$)")
plt.ylim([4e-2, 4e+0])
plt.xlim([2.e-1, 2.e+1])
plt.title("Spectral Index - $\Sigma_{SSC}$")
plt.scatter(d_ssc, ratio,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_index_ssc.png")
plt.savefig(dir_output + "plot_index_ssc.png", dpi=300)


### SFR - spectral index
ratio = np.log10(d_band6/d_band3)/np.log10(234.6075/104.024625)
for i in range(len(ratio)):
    if d_band3[i] == 0.0:
        ratio[i] = 0.0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.ylabel("Spectral Index")
plt.xlabel("$\Sigma_{SFR}$ ($M_{\odot}$ kpc$^{-2}$ yr$^{-1}$)")
plt.ylim([4e-2, 4e+0])
plt.xlim([2e-2, 2e-0])
plt.title("$\Sigma_{SFR}$ - Spectral Index")
plt.scatter(d_sfr, ratio,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

os.system("rm -rf " + dir_output + "plot_index_sfr.png")
plt.savefig(dir_output + "plot_index_sfr.png", dpi=300)


### SFE - spectral index
ratio = np.log10(d_band6/d_band3)/np.log10(234.6075/104.024625)
for i in range(len(ratio)):
    if d_band3[i] == 0.0:
        ratio[i] = 0.0

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Spectral Index")
plt.ylabel("SFE (yr$^{-1}$)")
plt.xlim([4e-2, 4e+0])
plt.ylim([3e-10, 3e-8])
plt.title("Spectral Index - SFE")
plt.scatter(ratio, d_sfe/1e6,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
#plt.plot([2, 2], [3e-10, 3e-8], 'k--', lw=2,
#         label = "thermal dust")
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

plt.legend()
os.system("rm -rf " + dir_output + "plot_index_sfe.png")
plt.savefig(dir_output + "plot_index_sfe.png", dpi=300)


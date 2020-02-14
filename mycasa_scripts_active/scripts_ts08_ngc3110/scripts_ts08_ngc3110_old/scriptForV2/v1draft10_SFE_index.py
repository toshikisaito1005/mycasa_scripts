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
data_alpha = "ngc3110_alpha_ism_Trot.txt"

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
d_h2 = data[:,2] / area2 * 1.1/1.4
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

# alpha_co
data = np.loadtxt(dir_data + data_alpha)
#alpha = (data[:,3] + data[:,4] + data[:,5] + data[:,6]) / 4.
alpha = data[:,3]

# distance from the nucleus
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325


### SFE - spectral index (1)
ratio = np.log10(d_band6/d_band3)/np.log10(234.6075/104.024625)
for i in range(len(ratio)):
    if d_band3[i] == 0.0:
        ratio[i] = -1
    elif d_band6[i] == 0.0:
        ratio[i] = -1

plt.figure()
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['xtick.minor.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
plt.rcParams['ytick.minor.width'] = 1.5
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams["font.size"] = 16
#plt.subplots_adjust(bottom = 0.15)
#plt.gca().set_aspect('equal', adjustable='box')
#plt.xscale('log')
#plt.yscale('log')
plt.xlabel("log Spectral Index")
plt.ylabel("log SFE (yr$^{-1}$)")
#plt.xlim([-0.5, 3.5])
plt.xlim([-1.5, 0.8])
plt.ylim([-9.5, -7.5])
plt.title(u"Spectral Index - SFE with $\u03b1_{CO}$ = 1.1")

log_sfe = []
log_ratio = []
for i in range(len(d_sfe)):
    if d_sfe[i] == 0:
        log_sfe.append(-10)
        log_ratio.append(-10)
    else:
        log_sfe.append(np.log10(d_sfe[i]/1e6))
        log_ratio.append(np.log10(ratio[i]))

np_log_ratio = np.array(log_ratio)
np_log_sfe = np.array(log_sfe)

###
plt.scatter(np_log_ratio,
            np_log_sfe,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 1.0, linewidths=0)
#plt.plot([2, 2], [-9.7, -7.2], 'k--', lw=2,
#     label = "thermal dust")
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

plt.legend()
os.system("rm -rf " + dir_output + "plot_index_sfe.png")
plt.grid()
plt.savefig(dir_output + "plot_index_sfe.png", dpi=300)


### SFE - spectral index (2)
d_h2_b = []
for i in range(len(d_h2)):
    if d_h2[i] > 0:
        if alpha[i] > 0:
            d_h2_b.append(d_h2[i] * alpha[i] / 1.4)
        else:
            d_h2_b.append(0)
    else:
        d_h2_b.append(0)

d_h2_c = np.array(d_h2_b)

ratio = np.log10(d_band6/d_band3)/np.log10(234.6075/104.024625)
for i in range(len(ratio)):
    if d_band3[i] == 0.0:
        ratio[i] = -1
    elif d_band6[i] == 0.0:
        ratio[i] = -1

plt.figure()
plt.rcParams['xtick.major.width'] = 1.5
plt.rcParams['xtick.minor.width'] = 1.5
plt.rcParams['ytick.major.width'] = 1.5
plt.rcParams['ytick.minor.width'] = 1.5
plt.rcParams['axes.linewidth'] = 1.5
plt.rcParams["font.size"] = 16
#plt.subplots_adjust(bottom = 0.15)
#plt.gca().set_aspect('equal', adjustable='box')
#plt.xscale('log')
#plt.yscale('log')
plt.xlabel("log Spectral Index")
plt.ylabel("log SFE (yr$^{-1}$)")
#plt.xlim([-0.5, 3.5])
plt.xlim([-1.5, 0.8])
plt.ylim([-9.5, -7.5])
plt.title(u"Spectral Index - SFE with $\u03b1_{ISM}(T_{rot})$")

log_sfe = []
log_ratio = []
for i in range(len(d_sfe)):
    if d_sfe[i] == 0:
        log_sfe.append(-10)
        log_ratio.append(-10)
    else:
        log_sfe.append(np.log10(d_sfe[i]/1e6 * d_h2_c[i]/d_h2[i]))
        log_ratio.append(np.log10(ratio[i]))

np_log_ratio = np.array(log_ratio)
np_log_sfe = np.array(log_sfe)

###
plt.scatter(np_log_ratio,
            np_log_sfe,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 1.0, linewidths=0)
#plt.plot([2, 2], [-9.7, -7.2], 'k--', lw=2,
#     label = "thermal dust")
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])

plt.legend()
os.system("rm -rf " + dir_output + "plot_index_sfe_a.png")
plt.grid()
plt.savefig(dir_output + "plot_index_sfe_a.png", dpi=300)

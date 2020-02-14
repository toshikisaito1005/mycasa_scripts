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
data_ssc = "ngc3110_flux_ssc.txt"
data_flux_normal = "ngc3110_flux_contin.txt"
data_alpha = "ngc3110_alpha_ism_Trot.txt"
#data_alpha = "ngc3110_alpha_master.txt"

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
# H2 mass
data = np.loadtxt(dir_data + data_h2,
                  usecols = (0,1,2))
d_ra, d_decl = data[:,0], data[:,1]
d_h2 = data[:,2]

# SSC
data = np.loadtxt(dir_data + data_ssc,
                  usecols = (0,1,2))
d_ra, d_decl = data[:,0], data[:,1]
d_ssc = data[:,2]

# spectral index
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3,4))
d_band3, d_band6 = data[:,3], data[:,4]

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

# alpha_co
data = np.loadtxt(dir_data + data_alpha)
#alpha = (data[:,3] + data[:,4] + data[:,5] + data[:,6]) / 4.
alpha = data[:,3]

# KS plot (1)
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
plt.xlabel("log $\Sigma_{H_2}$ ($M_{\odot}$ pc$^{-2}$)")
plt.ylabel("log $\Sigma_{SFR}$ ($M_{\odot}$ kpc$^{-2}$ yr$^{-1}$)")
plt.xlim([3.e+6/area2, 3.e+9/area2])
plt.ylim([3.e-3/area1, 3.e+0/area1])
plt.title(u"KS Relation with $\u03b1_{CO}$ = 1.1")
plt.scatter(d_h2/area2 * 1.1/1.4, d_sfr/area1,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])
plt.plot([3.e+6/area2, 3.e+9/area2],
         [3.e-3/area1, 3.e+0/area1], 'k-', lw=2)
plt.plot([3.e+6/area2, 3.e+9/area2],
         [3.e-2/area1, 3.e+1/area1], 'k-', lw=2)
plt.text(1.5e+7/area2, 1.9e+0/area1,
         "SFE = 10$^{-8}$ yr$^{-1}$", rotation=45)
plt.text(1.5e+8/area2, 3.e-1/area1,
         "SFE = 10$^{-9}$ yr$^{-1}$", rotation=45)

os.system("rm -rf " + dir_output + "plot_ks.png")
plt.grid()
plt.savefig(dir_output + "plot_ks.png", dpi=300)


# KS plot (2)
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
plt.xlabel("log $\Sigma_{H_2}$ ($M_{\odot}$ pc$^{-2}$)")
plt.ylabel("log $\Sigma_{SFR}$ ($M_{\odot}$ kpc$^{-2}$ yr$^{-1}$)")
plt.xlim([3.e+6/area2, 3.e+9/area2])
plt.ylim([3.e-3/area1, 3.e+0/area1])
plt.title(u"KS Relation with $\u03b1_{ISM}(T_{rot})$")
plt.scatter(d_h2_c/area2, d_sfr/area1,
            c = value,
            s = 130, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
cbar.set_label("Deprojected Radius (kpc)")
plt.clim([0, max(value) * 0.65])
plt.plot([3.e+6/area2, 3.e+9/area2],
         [3.e-3/area1, 3.e+0/area1], 'k-', lw=2)
plt.plot([3.e+6/area2, 3.e+9/area2],
         [3.e-2/area1, 3.e+1/area1], 'k-', lw=2)
plt.text(1.5e+7/area2, 1.9e+0/area1,
         "SFE = 10$^{-8}$ yr$^{-1}$", rotation=45)
plt.text(1.5e+8/area2, 3.e-1/area1,
         "SFE = 10$^{-9}$ yr$^{-1}$", rotation=45)

os.system("rm -rf " + dir_output + "plot_ks_a.png")
plt.grid()
plt.savefig(dir_output + "plot_ks_a.png", dpi=300)


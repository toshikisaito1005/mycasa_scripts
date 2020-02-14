import os
import re
import sys
import glob
import scipy
import numpy as np
import scipy.optimize
import matplotlib.pyplot as plt
import matplotlib.patches as patches
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
from scipy.optimize import curve_fit


dir_data = "../../phangs/co_ratio/photmetry/"
dir_output = "../../phangs/co_ratio/eps/"
data_flux_normal = "m74_flux_2.txt"

# center
ra = "01h36m41.736s"
decl = "15d46m57.715s"
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60


#####################
### Main Procedure
#####################
# CO lines
data = np.loadtxt(dir_data + data_flux_normal,
                  usecols = (0,1,2,3))
d_ra, d_decl = data[:,0], data[:,1]
d_co10, d_co21 = data[:,2], data[:,3]

beta = 1.226 * 10 ** 6. / 3.2 / 3.2 / 115.27120 ** 2
Jb_co10 = d_co10 / beta * 80. / 46.4
rms_co10 = 0.01 * 6 * sqrt(17) * beta
beta = 1.226 * 10 ** 6. / 3.2 / 3.2 / 230.53800 ** 2
Jb_co21 = d_co21 / beta * 80. / 46.4
rms_co21 = 0.03 * 6 * sqrt(17) * beta

l_co10 = 3.25e+7 * Jb_co10 / (115.27120/1.002192)**2 * 9.0**2 / 1.002192**3
l_co21 = 3.25e+7 * Jb_co21 / (230.53800/1.002192)**2 * 9.0**2 / 1.002192**3

# distance from the nucleus
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh + decl_mm + decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

#x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
#y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)
x2 = x1
y2 = y1

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.044


### radius - ratio
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Projected Radius (kpc)")
plt.ylabel("Line Ratio")
plt.title("NGC 0628")
plt.scatter(value, d_co21/d_co10,
            c = value,
            s = 40, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
plt.xlim([1e-1,1e+1])
cbar.set_label("Projected Radius (kpc)")
plt.clim([0, max(value) * 0.65])
plt.plot([1e-1,1e+1], [0.66+0.13,0.66+0.13], "red", linewidth=1, linestyle='dashed')
plt.plot([1e-1,1e+1], [0.66,0.66], "red", linewidth=2)
plt.plot([1e-1,1e+1], [0.66-0.13,0.66-0.13], "red", linewidth=1, linestyle='dashed')

os.system("rm -rf " + dir_output + "fig_radius_ratio_m74_2.png")
plt.savefig(dir_output + "fig_radius_ratio_m74_2.png", dpi=300)


### co10 - ratio
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("CO(1-0) Luminosity (K kms s$^{-1}$ pc$^2$)")
plt.ylabel("Line Ratio")
plt.title("NGC 0628")
plt.scatter(l_co10, d_co21/d_co10,
            c = value,
            s = 40, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
plt.xlim([1e+5,4e+6])
plt.ylim([1e-1,4e+0])
cbar.set_label("Projected Radius (kpc)")
plt.clim([0, max(value) * 0.65])
plt.plot([2.5e+5,2.5e+5], [1e-1,4e+0], "black")
#plt.plot([1e+5,1.8e+6], [1.8e+0,1e-1], "black", linestyle='dashed')
plt.plot([1e+5,4e+6], [0.66+0.13,0.66+0.13], "red", linewidth=1, linestyle='dashed')
plt.plot([1e+5,4e+6], [0.66,0.66], "red", linewidth=2)
plt.plot([1e+5,4e+6], [0.66-0.13,0.66-0.13], "red", linewidth=1, linestyle='dashed')

os.system("rm -rf " + dir_output + "fig_co10_ratio_m74_2.png")
plt.savefig(dir_output + "fig_co10_ratio_m74_2.png", dpi=300)


### co21 - ratio
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("CO(2-1) Luminosity (K kms s$^{-1}$ pc$^2$)")
plt.ylabel("Line Ratio")
plt.title("NGC 0628")
plt.scatter(l_co21, d_co21/d_co10,
            c = value,
            s = 40, cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
cbar = plt.colorbar()
plt.xlim([1e+5,4e+6])
plt.ylim([1e-1,4e+0])
cbar.set_label("Projected Radius (kpc)")
plt.clim([0, max(value) * 0.65])
plt.plot([1.9e+5,1.9e+5], [1e-1,4e+0], "black")
#plt.plot([1e+5,1.15e+6], [4.5e-1,4e+0], "black", linestyle='dashed')
plt.plot([1e+5,4e+6], [0.66+0.13,0.66+0.13], "red", linewidth=1, linestyle='dashed')
plt.plot([1e+5,4e+6], [0.66,0.66], "red", linewidth=2)
plt.plot([1e+5,4e+6], [0.66-0.13,0.66-0.13], "red", linewidth=1, linestyle='dashed')

os.system("rm -rf " + dir_output + "fig_co21_ratio_m74_2.png")
plt.savefig(dir_output + "fig_co21_ratio_m74_2.png", dpi=300)


### image
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("X-offset (arcmin)")
plt.ylabel("Y-offset (arcmin)")
plt.title("NGC 0628")
for i in range(len(d_co10)):
    if d_co10[i] == 0.0:
        x2[i], y2[i] = 0, 0
# circle size = rms
colscale = d_co21/d_co10
for i in range(len(colscale)):
    if d_co10[i] < rms_co10 * 3:
        colscale[i] = 0
    elif d_co21[i] < rms_co21 * 3:
        colscale[i] = 0
    else:
        colscale[i] = 15

plt.scatter(x2 * 60., y2 * 60.,
            c = d_co21/d_co10,
            s = colscale,
            cmap = 'gist_rainbow', alpha = 0.6, linewidths=0)
"""
    # circle size = line ratio
    colscale = d_co21/d_co10
    for i in range(len(colscale)):
    if colscale[i] > 0.66+0.13:
    colscale[i] = 3
    elif colscale[i] < 0.66-0.13:
    colscale[i] = 3
    else:
    colscale[i] = 30
    plt.scatter(x2 * 60., y2 * 60.,
    c = value,
    s = colscale,
    cmap = 'gist_rainbow', alpha = 1, linewidths=0)
    """
cbar = plt.colorbar()
plt.xlim([0.04 * 60.,-0.04 * 60.])
plt.ylim([-0.04 * 60.,0.04 * 60.])
cbar.set_label("Projected Radius (kpc)")
#plt.clim([0, max(value) * 0.65])
plt.clim([0.66-0.13*3,0.66+0.13*3])
plt.plot(0, 0, marker='D', color = "black", markersize = 5)

os.system("rm -rf " + dir_output + "fig_radius_image_m74_2.png")
plt.savefig(dir_output + "fig_radius_image_m74_2.png", dpi=300)


### histogram
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

l1 = d_co21/d_co10
l2 = l1[l1 > 0.]
l3 = l2[l2 < 100.]
plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
#plt.gca().set_aspect('equal', adjustable='box')
plt.xlabel("Line Ratio")
plt.ylabel("Count")
sum2 = plt.hist(l3, bins = 64, color = "grey", linewidth=0, alpha = 0.6)
a = sum2[0].shape[0]
index = np.where(sum2[0] == max(sum2[0]))
edge = 300
dat = np.c_[list(sum2[1])[0:a], list(sum2[0])]
popt, pcov = curve_fit(gauss_function, dat[:,0], dat[:,1], p0 = [58, 75., 20.1], maxfev = 1000000)
plt.plot(dat[:,0], gauss_function(dat[:,0], *popt),
         color = "magenta", lw=4)
plt.text((max(plt.hist(l3, bins=64, color = "white", alpha=0.)[1])-min(plt.hist(l3, bins=64, color = "white", alpha=0.)[1])) * 1.5 * 0.02 + min(plt.hist(l3, bins=64, color = "white", alpha=0.)[1]) * 4.5,
         max(plt.hist(l3, bins=64, color = "white", alpha=0.)[0]) * 0.95,
         r"$\mu$ = " + str(round(popt[1], 2)) + ", $\sigma$ = " + str(round(popt[2], 2)))
sum2 = plt.hist(l3, bins = 64, color = "grey", linewidth=0, alpha = 0.6)

os.system("rm -rf " + dir_output + "fig_hist_m74_2.png")
plt.savefig(dir_output + "fig_hist_m74_2.png", dpi=300)


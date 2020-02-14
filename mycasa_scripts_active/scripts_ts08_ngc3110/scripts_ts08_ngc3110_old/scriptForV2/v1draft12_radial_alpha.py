import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy.optimize
from scipy.optimize import curve_fit
sys.path.append(os.getcwd() + "/../../")
#import mycasaimaging_tools as myim
plt.ioff()


def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))


dir_data = "../../../ngc3110/ana/other/photmetry/"
dir_output = "../../../ngc3110/ana/eps/"


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
data_ism_kin = np.loadtxt(dir_data + "ngc3110_alpha_ism_Tkin.txt")
data_ism_rot = np.loadtxt(dir_data + "ngc3110_alpha_ism_Trot.txt")
data_lte_kin = np.loadtxt(dir_data + "ngc3110_alpha_lte_Tkin.txt")
data_lte_rot = np.loadtxt(dir_data + "ngc3110_alpha_lte_Trot.txt")

radius_ism_kin1 = data_ism_kin[:,2]
alpha_ism_kin1 = data_ism_kin[:,3]

radius_ism_rot1 = data_ism_rot[:,2]
alpha_ism_rot1 = data_ism_rot[:,3]

radius_lte_kin1 = data_lte_kin[:,2]
alpha_lte_kin1 = data_lte_kin[:,3] * 0.75

radius_lte_rot1 = data_lte_rot[:,2]
alpha_lte_rot1 = data_lte_rot[:,3] * 0.75

#
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 20
plt.subplots_adjust(bottom=0.15, wspace=0.15)

plt.scatter(radius_ism_kin1,
            np.log10(alpha_ism_kin1),
            lw=0,c="red",alpha=0.4,s=100,
            label = u"$\u03b1_{ISM}(T_{kin})$; median = 1.0")

plt.scatter(radius_ism_rot1,
            np.log10(alpha_ism_rot1),
            lw=0,c="green",alpha=0.4,s=100,
            label = u"$\u03b1_{ISM}(T_{rot})$; median = 1.1")

plt.scatter(radius_lte_kin1,
            np.log10(alpha_lte_kin1),
            lw=0,c="blue",alpha=0.4,s=100,
            label = u"$\u03b1_{LTE}(T_{kin})$; median = 2.0")

plt.scatter(radius_lte_rot1,
            np.log10(alpha_lte_rot1),
            lw=0,c="black",alpha=0.4,s=100,
            label = u"$\u03b1_{LTE}(T_{rot})$; median = 1.8")

med_ism_kin = np.log10(np.median(alpha_ism_kin1[alpha_ism_kin1>0]))
med_ism_rot = np.log10(np.median(alpha_ism_rot1[alpha_ism_rot1>0]))
med_lte_kin = np.log10(np.median(alpha_lte_kin1[alpha_lte_kin1>0]))
med_lte_rot = np.log10(np.median(alpha_lte_rot1[alpha_lte_rot1>0]))

plt.plot([0,10.5],[med_ism_kin,med_ism_kin],c="red",lw=3)
plt.plot([0,10.5],[med_ism_rot,med_ism_rot],c="green",lw=3)
plt.plot([0,10.5],[med_lte_kin,med_lte_kin],c="blue",lw=3)
plt.plot([0,10.5],[med_lte_rot,med_lte_rot],c="black",lw=3)
plt.plot([0,10.5],[0.6812,0.6812],"k--",lw=2)

plt.xlim([0,10.5])
plt.ylim([-1.0,2.0])
plt.xlabel("Deprojected Distance (kpc)")
plt.ylabel(u"log $\u03b1_{CO}$")
plt.legend(loc = "upper left")
plt.savefig(dir_output+"alpha_radius.png",dpi=100)

# histogram
plt.figure(figsize=(10,10))
plt.rcParams["font.size"] = 20
plt.subplots_adjust(bottom=0.15, wspace=0.15)

dat = plt.hist(alpha_ism_rot1[alpha_ism_rot1>0], bins=30, range=[0,4],
               color="skyblue", histtype="stepfilled")

popt, pcov = curve_fit(gauss_function, dat[1][2:], dat[0][1:],
                       p0 = [25, 1.2, 0.05],
                       maxfev = 10000)

x = np.linspace(0, dat[1][-1], 50)
plt.plot(x,
         gauss_function(x, *popt),
         '-', c="black", lw=4,
         label = "$\mu$ = " + str(round(popt[1], 1)) + \
         ", $\sigma$ = " + str(round(popt[2], 1)))

plt.plot([popt[1],popt[1]], [0,23], '--', c="black", lw=3)
plt.ylabel("Count")
plt.xlabel(u"$\u03b1_{ISM}(T_{rot})$")
plt.ylim([0.1,23])
plt.legend(loc = "upper left")
plt.savefig(dir_output+"alpha_histo.png",dpi=100)

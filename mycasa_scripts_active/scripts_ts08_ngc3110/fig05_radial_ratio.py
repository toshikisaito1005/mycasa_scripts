import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as patches
plt.ioff()


#####################
### Main Procedure
#####################
# center
ra = "10h04m02.090s"
decl = "-6d28m29.604s"
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60
ra_cent_deg = (ra_hh + ra_mm + ra_ss)
decl_cent_deg = (decl_hh - decl_mm - decl_ss)

dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/image_nyquist/"
data_txt = "ngc3110_uvlim_sum.txt"

# distance
data = np.loadtxt(dir_data + data_txt)
x1 = data[:,0] - ra_cent_deg
y1 = data[:,1] - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

radius = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325

# radial r21
data_r21 = data[:,3]/data[:,2]/4.
for i in range(len(data_r21)):
    if data[:,2][i] == 0:
        data_r21[i] = 0

final_r21 = data_r21[data_r21>0]
final_radius = radius[data_r21>0]

value_mean = np.mean(final_r21)
value_median = np.median(final_r21)

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("$^{12}R_{2-1/1-0}$")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([1e-1, 1e+1])
plt.title("Radial $^{12}R_{2-1/1-0}$")
plt.plot([1.5e-1, 1.5e+1], [value_mean, value_mean],
         color = "black", lw = 2,
         label="mean = "+str(round(value_mean, 2)))
plt.plot([1.5e-1, 1.5e+1], [value_median, value_median], "--",
         color = "black", lw = 2,
         label="median = "+str(round(value_median, 2)))
plt.scatter(final_radius, final_r21, s=130, color = "skyblue", linewidths=0)
plt.legend()
plt.grid(which="major")
plt.grid(which="minor")
os.system("rm -rf " + dir_data + "../eps/fig5a_r21.eps")
plt.savefig(dir_data + "../eps/fig5a_r21.eps", dpi=300)

# radial r13
data_r21 = data[:,3]/data[:,5]/(230.53800000**2/220.39868420**2)
for i in range(len(data_r21)):
    if data[:,2][i] == 0:
        data_r21[i] = 0

final_r21 = data_r21[data_r21>0]
final_radius = radius[data_r21>0]
final_r21[np.where(np.isinf(final_r21))] = 0
final_radius[np.where(np.isinf(final_r21))] = 0
final2_r21 = final_r21[final_r21>0]
final2_radius = final_radius[final_r21>0]

value_mean = np.mean(final2_r21)
value_median = np.median(final2_r21)

plt.figure()
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom = 0.15)
plt.gca().set_aspect('equal', adjustable='box')
plt.xscale('log')
plt.yscale('log')
plt.xlabel("Deprojected Radius (kpc)")
plt.ylabel("$^{12/13}R_{2-1}$")
plt.xlim([1.5e-1, 1.5e+1])
plt.ylim([3e-0, 3e+2])
plt.title("Radial $^{12/13}R_{2-1}$")
plt.plot([1.5e-1, 1.5e+1], [value_mean, value_mean],
         color = "black", lw = 2,
         label="mean = "+str(int(value_mean)))
plt.plot([1.5e-1, 1.5e+1], [value_median, value_median], "--",
         color = "black", lw = 2,
         label="median = "+str(int(value_median)))
plt.scatter(final2_radius, final2_r21, s=130, color = "skyblue", linewidths=0)
plt.legend()
plt.grid(which="major")
plt.grid(which="minor")
os.system("rm -rf " + dir_data + "../eps/fig5b_r13.eps")
plt.savefig(dir_data + "../eps/fig5b_r13.eps", dpi=300)

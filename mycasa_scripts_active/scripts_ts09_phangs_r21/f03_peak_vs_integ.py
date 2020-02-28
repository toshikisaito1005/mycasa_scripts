import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
percents = [0.15,0.025,0.010]
co10rmss = [0.013,0.048,0.015]
co21rmss = [0.017,0.024,0.017]


#####################
### Main Procedure
#####################
figure = plt.figure(figsize=(8,8))
histo = []
for i in range(len(gals)):
	galname = gals[i]
	data = np.loadtxt(dir_data + galname + "_parameter_matched_res.txt")

	r21 = data[:,1]
	r21[np.isnan(r21)] = 0
	p21 = data[:,9]
	p21[np.isnan(p21)] = 0
	co21 = data[:,4]
	co10snr = data[:,5]
	co21snr = data[:,3]
	pco10snr = data[:,10]
	pco21snr = data[:,11]
	#
	cut_r21 = (r21 > 0)
	cut_p21 = (p21 > 0)
	cut_co21 = (co21 > co21.max() * percents[i])
	cut_all = np.where((cut_r21) & (cut_p21) & (cut_co21))
	#
	r21 = r21[cut_all]
	p21 = p21[cut_all]
	co10snr = co10snr[cut_all]
	co21snr = co21snr[cut_all]
	pco10snr = pco10snr[cut_all]
	pco21snr = pco21snr[cut_all]
	r21err = r21 * np.sqrt((1./co10snr)**2 + (1./co21snr)**2)
	p21err = p21 * np.sqrt((1./pco10snr)**2 + (1./pco21snr)**2)
	#
	plt.rcParams["font.size"] = 16
	plt.grid()
	plt.xscale("log")
	plt.yscale("log")
	plt.xlim([10**-2.0,10**1.0])
	plt.ylim([10**-2.0,10**1.0])
	plt.errorbar(
		x = r21,
		xerr = r21err,
		y = p21,
		yerr = p21err,
		marker = ".",
		markersize = 0,
		c="gray",
		alpha=1.0,
		linewidth=0,
		elinewidth=1,
		capsize=0,
		)
	#plt.plot([-1.2,0.7],[-1.2,0.7],"k-",lw=1)
	#plt.plot([-1.2,0.7],[-1.1,0.8],"k--",lw=1)
	#plt.plot([-1.2,0.7],[-1.3,0.6],"k--",lw=1)
	plt.xlabel("log Integrated Intensity Ratio")
	plt.ylabel("log Peak Temperature Ratio")
	plt.legend(loc = "upper left")

	histo.extend(p21/r21)

a = plt.axes([.55, .15, .3, .2])
plt.ylim([0,2500])
plt.yticks([])
plt.hist(histo,range=[0.4,1.4],bins=40,color="gray",lw=0,alpha=1.0)

plt.savefig(dir_product+"figure_r21_vs_p21.png",dpi=200)

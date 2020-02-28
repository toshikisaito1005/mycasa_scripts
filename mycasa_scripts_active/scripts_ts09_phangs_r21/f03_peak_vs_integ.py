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
### functions
#####################
def hist_percent(histo,percent):
    dat_sum = np.sum(histo)
    dat_sum_from_zero,i = 0,0
    while dat_sum_from_zero < dat_sum * percent:
        dat_sum_from_zero += histo[i]
        i += 1
    
    return i


#####################
### Main Procedure
#####################
figure = plt.figure(figsize=(8,8))
histo = []
r21_all = []
p21_all = []
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
	plt.xlim([10**-1.6,10**1.0])
	plt.ylim([10**-1.6,10**1.0])
	plt.errorbar(
		x = r21,
		xerr = r21err,
		y = p21,
		yerr = p21err,
		marker = ".",
		markersize = 0,
		c="gray",
		alpha=0.5,
		linewidth=0,
		elinewidth=1,
		capsize=0,
		)
	plt.plot([10**-1.6,10**1.0],[10**-1.6,10**1.0],"k-",lw=1.5)
	plt.plot([10**-1.6,10**1.0],[10**-1.6*0.775,10**1.0*0.775],"--",c="blue",alpha=0.5,lw=1)
	plt.plot([10**-1.6,10**1.0],[10**-1.6*0.925,10**1.0*0.925],"--",c="green",alpha=0.5,lw=1)
	plt.plot([10**-1.6,10**1.0],[10**-1.6*1.075,10**1.0*1.075],"--",c="red",alpha=0.5,lw=1)
	plt.xlabel("Integrated Intensity Ratio")
	plt.ylabel("Peak Temperature Ratio")
	plt.legend(loc = "upper left")

	histo.extend(p21/r21)
	r21_all.extend(r21)
	p21_all.extend(p21)

correlation = np.corrcoef(r21_all,p21_all)[0,1]
plt.text(4,0.03,'$\\rho$ = ' + str(np.round(correlation, 2)),fontsize=14)

a = plt.axes([.16, .68, .3, .2])
plt.ylim([0,2500])
plt.xlabel("y-axis / x-axis")
plt.yticks([])
histodata = plt.hist(histo,range=[0.4,1.4],bins=40,color="gray",lw=0,alpha=1.0)
line_84 = histodata[1][hist_percent(histodata[0],0.843)]
line_50 = histodata[1][hist_percent(histodata[0],0.5)]
line_16 = histodata[1][hist_percent(histodata[0],0.157)]
plt.plot([1.0,1.0],[0,2500],"k-",alpha=0.5,lw=1.5)
plt.plot([line_84,line_84],[0,2500],"--",color="red",alpha=0.5,lw=1)
plt.plot([line_50,line_50],[0,2500],"--",color="green",alpha=0.5,lw=1)
plt.plot([line_16,line_16],[0,2500],"--",color="blue",alpha=0.5,lw=1)
plt.text(line_84+0.02,2200,"84th",color="red",alpha=0.5,rotation=90)
plt.text(line_50-0.09,2200,str(np.round(line_50,2)),color="green",alpha=0.5,rotation=90)
plt.text(line_16-0.09,2200,str(np.round(line_16,2)),color="blue",alpha=0.5,rotation=90)

plt.text(1.45,700,
	"mode = " + str(scipy.stats.mode(np.round(histo,2))[0][0]) + "\n" \
	+ "mean = " + str(np.round(np.mean(histo), 2)) + "\n" \
	+ "84th = " + str(np.round(line_84,2)) + " (red)" + "\n" \
	+ "median = " + str(np.round(np.median(histo), 2)) + " (green)\n" \
	+ "16th = " + str(np.round(line_16,2))+ " (blue)\n",
	fontsize=14
	)


plt.savefig(dir_product+"figure_r21_vs_p21.png",dpi=200)

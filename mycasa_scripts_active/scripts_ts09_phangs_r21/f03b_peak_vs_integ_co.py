import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
percents = [0.00,0.00,0.00]


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
r21err_all = []
p21err_all = []
for i in range(len(gals)):
	galname = gals[i]
	data = np.loadtxt(dir_product + galname + "_parameter_matched_res.txt")

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
	plt.xlim([10**-1.2,10**0.7])
	plt.ylim([10**-1.2,10**0.7])
	markers, caps, bars = plt.errorbar(
		x = r21,
		xerr = r21err,
		y = p21,
		yerr = p21err,
		marker = ".",
		markersize = 0,
		c=cm.brg(i/2.5), # "gray",
		alpha=0.5,
		linewidth=0,
		elinewidth=1,
		capsize=0,
		)
	[bar.set_alpha(0.5) for bar in bars]
	plt.plot([10**-1.6,10**1.0],[10**-1.6,10**1.0],"k-",lw=1.5)
	plt.plot([10**-1.6,10**1.0],[10**-1.6*0.775,10**1.0*0.775],"--",c="blue",alpha=0.5,lw=1)
	plt.plot([10**-1.6,10**1.0],[10**-1.6*0.925,10**1.0*0.925],"--",c="green",alpha=0.5,lw=1)
	plt.plot([10**-1.6,10**1.0],[10**-1.6*1.075,10**1.0*1.075],"--",c="red",alpha=0.5,lw=1)
	plt.xlabel("log Integrated Intensity Ratio")
	plt.ylabel("log Peak Temperature Ratio")
	plt.xticks([0.1,1],[-1,0])
	plt.yticks([0.1,1],[-1,0])
	plt.legend(loc = "upper left")

	histo.extend(p21/r21)
	r21_all.extend(r21)
	p21_all.extend(p21)
	r21err_all.extend(r21err)
	p21err_all.extend(p21err)

p2r = np.array(p21_all)/np.array(r21_all)
r21err_all = np.array(r21err_all)
p21err_all = np.array(p21err_all)
p2rerr = p2r * np.sqrt((r21err_all/r21_all)**2 + (p21err_all/p21_all)**2)

correlation = np.corrcoef(r21_all,p21_all)[0,1]
plt.text(2.5,0.07,'$\\rho$ = ' + str(np.round(correlation, 2)),fontsize=14)

a = plt.axes([.16, .68, .3, .2])
plt.plot([0.45,0.45+np.median(p2rerr)],[2200,2200],"k-",lw=2)
plt.ylim([0,2500])
plt.xlabel("y-axis / x-axis" ,fontsize=14)
plt.xticks(fontsize=14)
plt.yticks([])
histodata = plt.hist(histo,range=[0.4,1.4],bins=50,color="gray",lw=0,alpha=0.5)
line_84 = histodata[1][hist_percent(histodata[0],0.843)]
line_50 = histodata[1][hist_percent(histodata[0],0.5)]
line_16 = histodata[1][hist_percent(histodata[0],0.157)]
plt.plot([1.0,1.0],[0,2500],"k-",alpha=0.5,lw=1.5)
plt.plot([line_84,line_84],[0,2500],"--",color="red",alpha=0.5,lw=1)
plt.plot([line_50,line_50],[0,2500],"--",color="green",alpha=0.5,lw=1)
plt.plot([line_16,line_16],[0,2500],"--",color="blue",alpha=0.5,lw=1)
plt.text(line_84+0.02,2100,"84th",color="red",alpha=0.5,rotation=90,fontsize=14)
plt.text(line_50-0.09,2100,"median",color="green",alpha=0.5,rotation=90,fontsize=14)
plt.text(line_16-0.09,2100,"16th",color="blue",alpha=0.5,rotation=90,fontsize=14)

plt.text(1.44,1400,
	"84th = " + str(np.round(line_84,2)) + " (red)" + "\n" \
	+ "median = " + str(np.round(np.median(histo), 2)) + " (green)\n" \
	+ "16th = " + str(np.round(line_16,2))+ " (blue)\n",
	fontsize=14
	)


plt.savefig(dir_product+"figure_peak_vs_integ_co.png",dpi=200)

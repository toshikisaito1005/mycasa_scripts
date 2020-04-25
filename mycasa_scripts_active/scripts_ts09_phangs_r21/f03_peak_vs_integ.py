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

	# get data
	dist = data[:,0]
	#
	co10 = data[:,1]
	co10err = data[:,2]
	co21 = data[:,3]
	co21err = data[:,4]
	#
	pco10 = data[:,5]
	pco10err = data[:,6]
	pco21 = data[:,7]
	pco21err = data[:,8]
	#
	r21 = data[:,9]
	r21err = data[:,10]
	#
	p21 = data[:,11]
	p21err = data[:,12]
	#
	r21mask = data[:,13]
	#
	co10disp = co10 / (np.sqrt(2*np.pi) * pco10)
	co21disp = co21 / (np.sqrt(2*np.pi) * pco21)

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
		markersize = 10,#0,
		c="gray", #cm.brg(i/2.5),
		alpha=0.5,
		linewidth=0,
		elinewidth=0,#1,
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


plt.savefig(dir_product+"figure_r21_vs_p21.png",dpi=200)

import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
from scipy.stats import gaussian_kde
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
percents = [0.15,0.025,0.010]
def_nucleus = [50*44./1.0,50*52./1.3,50*103/1.4]
xlim = [0.15,1.2]

#####################
### functions
#####################
def weighted_median(data, weights):
    """
    Args:
        data (list or numpy.array): data
        weights (list or numpy.array): weights
    """
    data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
    s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
    midpoint = 0.5 * sum(s_weights)
    if any(weights > midpoint):
        w_median = (data[weights == np.max(weights)])[0]
    else:
        cs_weights = np.cumsum(s_weights)
        idx = np.where(cs_weights <= midpoint)[0][-1]
        if cs_weights[idx] == midpoint:
            w_median = np.mean(s_data[idx:idx+2])
        else:
            w_median = s_data[idx+1]

    return w_median


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	galname = gals[i]
	data = np.loadtxt(dir_data + galname + "_parameter_matched_res.txt")

	dist = data[:,0]
	r21 = data[:,1]
	r21[np.isnan(r21)] = 0
	co21 = data[:,2]
	co21snr = data[:,3]
	co10 = data[:,4]
	co10snr = data[:,5]
	#
	cut_r21 = (r21 > 0)
	cut_co21 = (co21 > co21.max() * percents[i])
	cut_all = np.where((cut_r21) & (cut_co21))
	#
	dist = dist[cut_all]
	r21 = r21[cut_all]
	co10 = co10[cut_all]
	co21 = co21[cut_all]
	co10snr = co10snr[cut_all]
	co21snr = co21snr[cut_all]
	r21err = r21 * np.sqrt((1./co10snr)**2 + (1./co21snr)**2)

	### plot data
	plt.figure(figsize=(18,3))
	plt.rcParams["font.size"] = 14
	gs = gridspec.GridSpec(nrows=9, ncols=16)
	plt1 = plt.subplot(gs[1:7,0:4])
	plt2 = plt.subplot(gs[1:7,4:8])
	plt3 = plt.subplot(gs[1:7,8:12])
	#plt4 = plt.subplot(gs[1:7,12:16])
	plt1.grid(axis="x")
	plt2.grid(axis="x")
	plt3.grid(axis="x")
	#plt4.grid(axis="x")

	## hist 1
	histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=None)
	histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
	histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),weights=None)
	histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
	histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),weights=None)
	histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

	# kernel density estimation
	y11 = histo1y/float(sum(histo1y))
	y12 = histo2y/float(sum(histo1y))
	y13 = histo3y/float(sum(histo1y))
	med1 = np.median(r21)
	med2 = np.median(r21[dist<def_nucleus[i]])
	med3 = np.median(r21[dist>def_nucleus[i]])
	print(gals[i]+", median = "+str(med1))

	# plt1
	plt1.plot(histo1x,y11,"black",lw=5,alpha=0.5)
	plt1.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
	plt1.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
	plt1.plot(med1, 0.15, ".", markersize=14,c="black")
	plt1.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
	plt1.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
	plt1.plot([histo1x[hist_percent(histo1y,0.157)],
	           histo1x[hist_percent(histo1y,0.843)]],
	          [0.15,0.15],c="black",lw=3,alpha=0.5)
	plt1.plot([histo2x[hist_percent(histo2y,0.157)],
	           histo2x[hist_percent(histo2y,0.843)]],
	          [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
	plt1.plot([histo3x[hist_percent(histo3y,0.157)],
	           histo3x[hist_percent(histo3y,0.843)]],
	      [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)

	#plt1.set_yscale("log")
	plt1.set_xlim(xlim)
	plt1.set_ylim(ylim)

	## hist 2
	histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=co10)
	histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
	histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),
	                      weights=co10[dist<def_nucleus[i]])
	histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
	histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),
	                      weights=co10[dist>def_nucleus[i]])
	histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

	# kernel density estimation
	y11 = histo1y/float(sum(histo1y))
	y12 = histo2y/float(sum(histo1y))
	y13 = histo3y/float(sum(histo1y))
	med1 = weighted_median(r21,co10)
	med2 = weighted_median(r21[dist<def_nucleus[i]],co10[dist<def_nucleus[i]])
	med3 = weighted_median(r21[dist>def_nucleus[i]],co10[dist>def_nucleus[i]])

	# plt2
	plt2.plot(histo1x,y11,"black",lw=5,alpha=0.5)
	plt2.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
	plt2.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
	plt2.plot(med1, 0.15, ".", markersize=14,c="black")
	plt2.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
	plt2.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
	plt2.plot([histo1x[hist_percent(histo1y,0.157)],
	           histo1x[hist_percent(histo1y,0.843)]],
	          [0.15,0.15],c="black",lw=3,alpha=0.5)
	plt2.plot([histo2x[hist_percent(histo2y,0.157)],
	           histo2x[hist_percent(histo2y,0.843)]],
	          [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
	plt2.plot([histo3x[hist_percent(histo3y,0.157)],
	           histo3x[hist_percent(histo3y,0.843)]],
	          [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)

	#plt2.set_yscale("log")
	plt2.set_xlim(xlim)
	plt2.set_ylim(ylim)

	## hist 3
	histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=co21)
	histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
	histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),
	                      weights=co21[dist<def_nucleus[i]])
	histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
	histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),
	                      weights=co21[dist>def_nucleus[i]])
	histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

	# kernel density estimation
	y11 = histo1y/float(sum(histo1y))
	y12 = histo2y/float(sum(histo1y))
	y13 = histo3y/float(sum(histo1y))
	med1 = weighted_median(r21,co21)
	med2 = weighted_median(r21[dist<def_nucleus[i]],co21[dist<def_nucleus[i]])
	med3 = weighted_median(r21[dist>def_nucleus[i]],co21[dist>def_nucleus[i]])

	# plt3
	plt3.plot(histo1x,y11,"black",lw=5,alpha=0.5)
	plt3.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
	plt3.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
	plt3.plot(med1, 0.15, ".", markersize=14,c="black")
	plt3.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
	plt3.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
	plt3.plot([histo1x[hist_percent(histo1y,0.157)],
	           histo1x[hist_percent(histo1y,0.843)]],
	          [0.15,0.15],c="black",lw=3,alpha=0.5)
	plt3.plot([histo2x[hist_percent(histo2y,0.157)],
	           histo2x[hist_percent(histo2y,0.843)]],
	          [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
	plt3.plot([histo3x[hist_percent(histo3y,0.157)],
	           histo3x[hist_percent(histo3y,0.843)]],
	          [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)

	#plt3.set_yscale("log")
	plt3.set_xlim(xlim)
	plt3.set_ylim(ylim)

	## hist 4
	"""
	histo1 = np.histogram(r21,bins=bins,range=(xlim),weights=w3)
	histo1x,histo1y = np.delete(histo1[1],-1),histo1[0]
	histo2 = np.histogram(r21[dist<def_nucleus[i]],bins=bins,range=(xlim),
	                      weights=w3[dist<def_nucleus[i]])
	histo2x,histo2y = np.delete(histo2[1],-1),histo2[0]
	histo3 = np.histogram(r21[dist>def_nucleus[i]],bins=bins,range=(xlim),
	                      weights=w3[dist>def_nucleus[i]])
	histo3x,histo3y = np.delete(histo3[1],-1),histo3[0]

	# kernel density estimation
	y11 = histo1y/float(sum(histo1y))
	y12 = histo2y/float(sum(histo1y))
	y13 = histo3y/float(sum(histo1y))
	med1 = weighted_median(r21,co21)
	med2 = weighted_median(r21[dist<def_nucleus[i]],co21[dist<def_nucleus[i]])
	med3 = weighted_median(r21[dist>def_nucleus[i]],co21[dist>def_nucleus[i]])

	# plt4
	plt4.plot(histo1x,y11,"black",lw=5,alpha=0.5)
	plt4.plot(histo1x,y12,c=cm.brg(i/2.5),ls="dotted",lw=2,alpha=1.0)
	plt4.plot(histo1x,y13,c=cm.brg(i/2.5),ls="-",lw=5,alpha=0.5)
	plt4.plot(med1, 0.15, ".", markersize=14,c="black")
	plt4.plot(med2, 0.14, ".", markersize=14,c=cm.brg(i/2.5))
	plt4.plot(med3, 0.13, ".", markersize=14,c=cm.brg(i/2.5))
	plt4.plot([histo1x[hist_percent(histo1y,0.157)],
	           histo1x[hist_percent(histo1y,0.843)]],
	          [0.15,0.15],c="black",lw=3,alpha=0.5)
	plt4.plot([histo2x[hist_percent(histo2y,0.157)],
	           histo2x[hist_percent(histo2y,0.843)]],
	          [0.14,0.14],c=cm.brg(i/2.5),lw=3,alpha=1.0,linestyle="dotted")
	plt4.plot([histo3x[hist_percent(histo3y,0.157)],
	           histo3x[hist_percent(histo3y,0.843)]],
	          [0.13,0.13],c=cm.brg(i/2.5),lw=3,alpha=0.5)

	#plt4.set_yscale("log")
	plt4.set_xlim(xlim)
	plt4.set_ylim(ylim)
	"""

	plt1.tick_params(labelbottom=False)
	plt2.tick_params(labelleft=False,labelbottom=False)
	plt3.tick_params(labelleft=False,labelbottom=False)
	#plt4.tick_params(labelleft=False,labelbottom=False)
	#plt1.set_yticks(np.arange(0.9, ylim[1]+0.01, 0.9))
	#plt2.set_yticks(np.arange(0.9, ylim[1]+0.01, 0.9))
	#plt3.set_yticks(np.arange(0.9, ylim[1]+0.01, 0.9))

	txt_x = xlim[0]+(xlim[1]-xlim[0])*0.67
	bm = float(beam[i].replace("p","."))
	bm_arc = str(round(bm,1)).replace(".","\".")
	bm_kpc = str(int(round(bm*scales[i],-1)))+" pc"
	plt1.text(txt_x,ylim[1]*0.55,name_title+"\n"+bm_arc+"\n"+bm_kpc)

	if gals[i]=="ngc0628":
	    plt1.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"# of Sightlines")
	    plt2.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"CO(1-0) Flux")
	    plt3.text(xlim[0]+(xlim[1]-xlim[0])*0.0,ylim[1]*1.04,"CO(2-1) Flux")

	if gals[i]=="ngc4321":
	    plt1.set_xlabel("$R_{21}$")
	    plt2.set_xlabel("$R_{21}$")
	    plt3.set_xlabel("$R_{21}$")
	    plt1.tick_params(labelbottom=True)
	    plt2.tick_params(labelleft=False,labelbottom=True)
	    plt3.tick_params(labelleft=False,labelbottom=True)

	plt1.legend()
	plt2.legend()
	plt3.legend()

	plt1.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
	plt2.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))
	plt3.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))

	plt.savefig(dir_product+"figure_hists_"+gals[i]+".png",dpi=100)

os.system("rm -rf *.last")

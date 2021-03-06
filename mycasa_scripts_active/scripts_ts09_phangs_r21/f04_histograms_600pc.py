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

import scripts_phangs_r21_plot as plot_r21
reload(plot_r21)


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
percents = [0.15,0.025,0.010]
def_nucleus = [50*44./1.0,50*52./1.3,30*103/1.4]
scales = [44/1.0,52/1.3,103/1.4]
beam = ["13p6","15p0","08p5"]
xlim = [0.15,1.2]
ylim = [0,0.16]
bins=50


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	galname = gals[i]
	galnamelabel = galname.replace("ngc","NGC ")
	data = np.loadtxt(dir_product + galname + "_parameter_600pc.txt")
	#
	dist = data[:,0]
	r21 = data[:,1]
	r21[np.isnan(r21)] = 0
	r21[np.isinf(r21)] = 0
	co21 = data[:,3]
	co21snr = data[:,4]
	co10 = data[:,5]
	co10snr = data[:,6]
	#
	cut_dist = (dist > 0)
	cut_r21 = (r21 > 0)
	cut_co21 = (co21 > co21.max() * percents[i])
	cut_all = np.where((cut_dist) & (cut_r21) & (cut_co21))
	#
	dist = dist[cut_all]
	r21 = r21[cut_all]
	co10 = co10[cut_all]
	co21 = co21[cut_all]
	co10snr = co10snr[cut_all]
	co21snr = co21snr[cut_all]
	r21err = r21 * np.sqrt((1./co10snr)**2 + (1./co21snr)**2)
	#
	# plot data
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
	#
	# plot no-weight histogram
	plot_r21.plot_hists_for_nuclear_outer_whole(
		plt1,
		r21, dist, bins, xlim, ylim, cm.brg(i/2.5),
		weights = None, size_nuclear = def_nucleus[i])
	#
	# plot co10-weighted histogram
	plot_r21.plot_hists_for_nuclear_outer_whole(
		plt2,
		r21, dist, bins, xlim, ylim, cm.brg(i/2.5),
		weights = co10, size_nuclear = def_nucleus[i])
	#
	# plot co21-weighted histogram
	plot_r21.plot_hists_for_nuclear_outer_whole(
		plt3,
		r21, dist, bins, xlim, ylim, cm.brg(i/2.5),
		weights = co21, size_nuclear = def_nucleus[i])
	#
	# 
	plt1.tick_params(labelbottom=False)
	plt2.tick_params(labelleft=False,labelbottom=False)
	plt3.tick_params(labelleft=False,labelbottom=False)
	plt1.tick_params(axis="y", length=0)
	plt2.tick_params(axis="y", length=0)
	plt3.tick_params(axis="y", length=0)
	#
	txt_x = xlim[0]+(xlim[1]-xlim[0])*0.67
	bm = float(beam[i].replace("p","."))
	bm_arc = str(round(bm,1)).replace(".","\".")
	bm_kpc = str(int(round(bm*scales[i],-1)))+" pc"
	plt1.text(txt_x,ylim[1]*0.38,galnamelabel+"\n"+bm_arc+"\n"+bm_kpc)

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

	plt.savefig(dir_product+"figure_hists_"+gals[i]+".png",dpi=100)

	### statistics
	print("### galname = " + galname)
	r21_histo = np.histogram(r21,range=xlim,bins=bins)
	r21_histo_wco10 = np.histogram(r21,range=xlim,bins=bins,weights=co10)
	r21_histo_wco21 = np.histogram(r21,range=xlim,bins=bins,weights=co21)
	# unweighted
	p84 = np.round(r21_histo[1][plot_r21.hist_percent(r21_histo[0],0.843)],3)
	mean = np.round(np.average(r21),3)
	median = np.round(np.median(r21),3)
	mode =  np.round(r21_histo[1][np.argmax(r21_histo[0])],3)
	p16 = np.round(r21_histo[1][plot_r21.hist_percent(r21_histo[0],0.157)],3)
	list_stats = [p84,mean,median,mode,p16]

	# co10-weighted
	p84 = np.round(plot_r21.weighted_p84(r21,co10),3)
	mean = np.round(np.average(r21,weights=co10),3)
	median = np.round(plot_r21.weighted_median(r21,co10),3)
	mode =  np.round(r21_histo_wco10[1][np.argmax(r21_histo_wco10[0])],3)
	p16 = np.round(plot_r21.weighted_p16(r21,co10),3)
	list_stats_2 = [p84,mean,median,mode,p16]
	list_stats.extend(list_stats_2)

	# co21-weighted
	p84 = np.round(plot_r21.weighted_p84(r21,co21),3)
	mean = np.round(np.average(r21,weights=co21),3)
	median = np.round(plot_r21.weighted_median(r21,co21),3)
	mode =  np.round(r21_histo_wco21[1][np.argmax(r21_histo_wco21[0])],3)
	p16 = np.round(plot_r21.weighted_p16(r21,co21),3)
	list_stats_3 = [p84,mean,median,mode,p16]
	list_stats.extend(list_stats_3)

	os.system("rm -rf " + dir_product + galname + "_stats_600pc.txt",)
	np.savetxt(dir_product + galname + "_stats_600pc.txt",
		       np.c_[np.array(range(5)*3)+1+5*i, list_stats],
		       fmt = "%.2f")

os.system("rm -rf *.last")

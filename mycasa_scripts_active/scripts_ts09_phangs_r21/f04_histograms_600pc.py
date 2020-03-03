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
scales = [44/1.0,52/1.3,103/1.4]
beam = ["13p6","15p0","08p2"]
xlim = [0.15,1.2]
ylim = [0,0.16]
bins=50


#####################
### functions
#####################
def weighted_median(
	data,
	weights,
	):
	"""
	Args:
	    data (list or numpy.array): data
	    weights (list or numpy.array): weights
	"""
	if weights==None:
		w_median = np.median(data)
	else:
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


def hist_percent(
	histo,
	percent,
	):
	"""
	"""
	dat_sum = np.sum(histo)
	dat_sum_from_zero,i = 0,0
	while dat_sum_from_zero < dat_sum * percent:
		dat_sum_from_zero += histo[i]
		i += 1

	return i


def plot_hists_for_nuclear_outer_whole(
	ax,
	data,
	distance,
	bins,
	xlim,
	ylim,
	color,
	weights = None,
	size_nuclear = None,
	):
	"""
	"""
	#
	data_all = data
	data_in = data[distance<size_nuclear]
	data_out = data[distance>size_nuclear]
	if weights==None:
		weights_all = None
		weights_in = None
		weights_out = None
	else:
		weights_all = weights
		weights_in = weights[distance<size_nuclear]
		weights_out = weights[distance>size_nuclear]
	#
	# construct histograms
	histo_all = np.histogram(data_all,bins=bins,range=(xlim),weights=weights_all)
	histo_allx, histo_ally = np.delete(histo_all[1],-1),histo_all[0]

	histo_in = np.histogram(data_in,bins=bins,range=(xlim),weights=weights_in)
	_, histo_iny = np.delete(histo_in[1],-1),histo_in[0]

	histo_out = np.histogram(data_out,bins=bins,range=(xlim),weights=weights_out)
	_, histo_outy = np.delete(histo_out[1],-1),histo_out[0]
	#
	# normalize histograms
	histo_all_norm = histo_ally / float(sum(histo_ally))
	histo_in_norm = histo_iny / float(sum(histo_ally))
	histo_out_norm = histo_outy / float(sum(histo_ally))
	#
	# calculate median values
	print()
	median_all = weighted_median(data=data_all,weights=weights_all)
	median_in = weighted_median(data=data_in,weights=weights_in)
	median_out = weighted_median(data=data_out,weights=weights_out)
	#
	# plot histograms
	ax.plot(histo_allx,histo_all_norm,"black",lw=5,alpha=0.5)
	ax.plot(histo_allx,histo_in_norm,c=color,ls="dotted",lw=2,alpha=1.0)
	ax.plot(histo_allx,histo_out_norm,c=color,ls="-",lw=5,alpha=0.5)
	# plot median points
	ax.plot(median_all, 0.15,".",markersize=14,c="black")
	ax.plot(median_in, 0.14,".",markersize=14,c=color)
	ax.plot(median_out, 0.13,".",markersize=14,c=color)
	# plot sigma ranges
	ax.plot([histo_allx[hist_percent(histo_ally,0.157)],
			 histo_allx[hist_percent(histo_ally,0.843)]],
			[0.15,0.15],
			c="black",lw=3,alpha=0.5)
	ax.plot([histo_allx[hist_percent(histo_iny,0.157)],
			 histo_allx[hist_percent(histo_iny,0.843)]],
			[0.14,0.14],
			c=color,lw=3,alpha=1.0,linestyle="dotted")
	ax.plot([histo_allx[hist_percent(histo_outy,0.157)],
			 histo_allx[hist_percent(histo_outy,0.843)]],
			[0.13,0.13],
			c=color,lw=3,alpha=0.5)

	ax.set_xlim(xlim)
	ax.set_ylim(ylim)
	ax.legend()
	ax.set_yticks(np.arange(0, 0.15 + 0.01, 0.03))


#####################
### Main Procedure
#####################
for i in range(len(gals)):
	galname = gals[i]
	galnamelabel = galname.replace("ngc","NGC ")
	data = np.loadtxt(dir_data + galname + "_parameter_matched_res.txt")
	#
	dist = data[:,0]
	r21 = data[:,1]
	r21[np.isnan(r21)] = 0
	r21[np.isinf(r21)] = 0
	co21 = data[:,2]
	co21snr = data[:,3]
	co10 = data[:,4]
	co10snr = data[:,5]
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
	plot_hists_for_nuclear_outer_whole(
		plt1,
		r21, dist, bins, xlim, ylim, cm.brg(i/2.5),
		weights = None, size_nuclear = def_nucleus[i])
	#
	# plot co10-weighted histogram
	plot_hists_for_nuclear_outer_whole(
		plt2,
		r21, dist, bins, xlim, ylim, cm.brg(i/2.5),
		weights = co10, size_nuclear = def_nucleus[i])
	#
	# plot co21-weighted histogram
	plot_hists_for_nuclear_outer_whole(
		plt3,
		r21, dist, bins, xlim, ylim, cm.brg(i/2.5),
		weights = co21, size_nuclear = def_nucleus[i])
	#
	# 
	plt1.tick_params(labelbottom=False)
	plt2.tick_params(labelleft=False,labelbottom=False)
	plt3.tick_params(labelleft=False,labelbottom=False)
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

os.system("rm -rf *.last")

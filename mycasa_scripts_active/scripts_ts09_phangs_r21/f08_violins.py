import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
bins = 50
r21range = [0.05,1.45]
fontsize_general = 15
fontsize_legend = 13
xlabel = "Beam Size (arcsec)"
ylabel = "$R_{21}$"
gals = ["ngc0628",
		"ngc3627",
		"ngc4321"]
beam = [[4.0,8.0,12.0,16.0,20.0],
        [8.0,12.0,16.0,20.0,24.0],
        [4.0,8.0,12.0,16.0,20.0]]


#####################
### functions
#####################
def get_co_intensities(image_co10,image_co21,beamfloat):
	"""
	"""
	# get image shape
	imshape = imhead(image_co10,mode="list")["shape"]
	box = "0,0," + str(imshape[0]-1) + "," + str(imshape[1]-1)
	# imval
	data_co10_tmp = imval(image_co10,box=box)["data"].flatten()
	data_co21_tmp = imval(image_co21,box=box)["data"].flatten()
	# cut pixel = 0
	cut_data = np.where((data_co10_tmp>0) & (data_co21_tmp>0))
	data_co10 = data_co10_tmp[cut_data]
	data_co21 = data_co21_tmp[cut_data]
	# Jy-to-K
	co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
	co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
	data_co10_Kelvin = data_co10 * co10_jy2k
	data_co21_Kelvin = data_co21 * co21_jy2k

	return data_co10_Kelvin, data_co21_Kelvin

def weighted_percentile(
	data,
	percentile,
	weights,
	):
	"""
	Args:
	    data (list or numpy.array): data
	    weights (list or numpy.array): weights
	"""
	if weights==None:
		w_median = np.percentile(data,percentile*100)
	else:
		data, weights = np.array(data).squeeze(), np.array(weights).squeeze()
		s_data, s_weights = map(np.array, zip(*sorted(zip(data, weights))))
		midpoint = percentile * sum(s_weights)
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

def get_stats(
	data,
	weights,
	historange,
	):
	"""
	"""
	# percentiles
	p84 = weighted_percentile(data, 0.84, weights)
	p50 = weighted_percentile(data, 0.50, weights)
	p16 = weighted_percentile(data, 0.16, weights)
	# mode
	n, bins = np.histogram(data, weights=weights, range=historange)
	idx = np.argmax(n)
	mode = np.mean([bins[idx], bins[idx + 1]])
	# mean
	mean = np.average(data, weights=weights)

	return [p84, mean, p50, mode, p16]

def plot_one_violin(
	ax,
	x,
	x_absoffset,
	xhisto,
	yhisto,
	step,
	color,
	alpha,
	):
	"""
	"""
	ax.plot(yhisto+x+x_absoffset, xhisto, drawstyle="steps", color=color, lw=0.5)
	ax.plot(yhisto*-1+x+x_absoffset, xhisto, drawstyle="steps", color=color, lw=0.5)
	ax.barh(xhisto, yhisto, height=step, lw=0, color=color, alpha=alpha, left=x+x_absoffset)
	ax.barh(xhisto, yhisto*-1, height=step, lw=0, color=color, alpha=alpha, left=x+x_absoffset)

def plot_multi_violins(
	ax,
	list_violin,
	bins,
	ratiorange,
	weights,
	list_beam,
	color,
	alpha,
	x_absoffset,
	):
	"""
	"""
	for i in range(len(list_beam)):
		# make histogram
		if weights==None:
			histo = np.histogram(list_violin[i], bins, range=ratiorange, weights=None, density=True)
		else:
			histo = np.histogram(list_violin[i], bins, range=ratiorange, weights=weights[i], density=True)
			#
		# data for plot_one_violin
		xaxis = float(list_beam[i].replace("p","."))
		xaxis_histo = np.delete(histo[1],-1)
		yaxis_histo = histo[0]/(histo[0].max()*1.05)*2
		step_histo = (ratiorange[1]-ratiorange[0]) / bins
		#
		# plot each violin
		plot_one_violin(ax, xaxis, x_absoffset, xaxis_histo, yaxis_histo, step_histo, color, alpha)
		#
	# prerare for stats
	list_xaxis = np.array([float(s.replace("p",".")) for s in list_beam])
	if weights==None:
		list_median = [np.median(s) for s in list_violin]
	else:
		list_median = []
		for j in range(len(list_violin)):
			list_median.append(weighted_percentile(list_violin[j],0.5,weights[j]))
	# plot stats
	ax.plot(
		np.array(list_xaxis)+x_absoffset,list_median,
		"o-",color='black',markersize=4,markeredgewidth=0,alpha=0.5)

def plot_all_violins(
	ax,
	list_r21,
	bins,
	r21range,
	list_beam,
	color,
	weights1,
	weights2,
	):
	"""
	"""
	#
	weights = None
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.60,0.0)
	#
	weights = weights1
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.35,23.0)
	#
	weights = weights2
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.10,46.0)

def plot_one_stats(
	ax,
	statslist_r21,
	fmt,
	color,
	lw,
	alpha,
	):
	"""
	"""
	# get stats
	for i in range(len(statslist_r21)):
		xvalue = np.arange(i*6 + 1,i*6 + 6)
		yvalue = [s[i] for s in statslist_r21]
		ax.plot(xvalue, yvalue, fmt, lw=lw, color=color, alpha = alpha)

def plot_all_stats(
	ax,
	statslist_r21,
	statslist_r21_wco10,
	statslist_r21_wco21,
	color,
	):
	"""
	"""
	ymax = np.max([statslist_r21, statslist_r21_wco10, statslist_r21_wco21])
	ymin = np.min([statslist_r21, statslist_r21_wco10, statslist_r21_wco21])
	ax.set_ylim([ymin-0.05, ymax+0.05])
	plot_one_stats(ax, statslist_r21, "-", color, lw = 2, alpha = 0.60)
	plot_one_stats(ax, statslist_r21_wco10, "-", color, lw = 2, alpha = 0.35)
	plot_one_stats(ax, statslist_r21_wco21, "-", color, lw = 2, alpha = 0.10)

def startup_plot(
	fontsize_general,
	fontsize_legend,
	xlabel,
	ylabel,
	r21range,
	):
	plt.subplots(nrows=1,ncols=1,figsize=(10, 5),sharey=True)
	plt.rcParams["font.size"] = fontsize_general
	plt.rcParams["legend.fontsize"] = fontsize_legend
	plt.subplots_adjust(bottom=0.15, left=0.10, right=0.98, top=0.97)
	gs = gridspec.GridSpec(nrows=18, ncols=25)
	ax1 = plt.subplot(gs[0:6,0:14])
	ax2 = plt.subplot(gs[6:12,0:14])
	ax3 = plt.subplot(gs[12:18,0:14])
	ax4 = plt.subplot(gs[0:6,15:25])
	ax5 = plt.subplot(gs[6:12,15:25])
	ax6 = plt.subplot(gs[12:18,15:25])
	ax1.set_ylim(r21range)
	ax2.set_ylim(r21range)
	ax3.set_ylim(r21range)
	ax4.set_ylim(r21range)
	ax5.set_ylim(r21range)
	ax6.set_ylim(r21range)
	ax1.grid(axis="y")
	ax2.grid(axis="y")
	ax3.grid(axis="y")
	ax4.grid(axis="y")
	ax5.grid(axis="y")
	ax6.grid(axis="y")
	ax1.set_xlim([0,70])
	ax2.set_xlim([4,74])
	ax3.set_xlim([0,70])
	ax1.tick_params(axis="x", length=0)
	ax2.tick_params(axis="x", length=0)
	ax3.tick_params(axis="x", length=0)
	ax4.tick_params(axis="x", length=0)
	ax5.tick_params(axis="x", length=0)
	ax6.tick_params(axis="x", length=0)
	ax1.tick_params(labelbottom=False)
	ax2.tick_params(labelbottom=False)
	ax3.tick_params(labelbottom=False)
	ax4.tick_params(labelbottom=False)
	ax5.tick_params(labelbottom=False)
	ax6.tick_params(labelbottom=False)
	ax1.set_yticks([0.3,0.6,0.9,1.2])
	ax2.set_yticks([0.3,0.6,0.9,1.2])
	ax3.set_yticks([0.3,0.6,0.9,1.2])
	ax4.set_yticks([0.3,0.5,0.7,0.9,1.1,1.3])
	ax5.set_yticks([0.3,0.5,0.7,0.9,1.1,1.3])
	ax6.set_yticks([0.3,0.5,0.7,0.9,1.1,1.3])
	ax2.set_ylabel(ylabel)
	ax3.text(12, -0.2, "# of Sightlines", horizontalalignment="center")
	ax3.text(12+23.0, -0.2, "CO(1-0) Flux", horizontalalignment="center")
	ax3.text(12+46.0, -0.2, "CO(2-1) Flux", horizontalalignment="center")
	ax6.text(3, 0.2, "84%", horizontalalignment="center", rotation=45)
	ax6.text(9, 0.2, "Mean", horizontalalignment="center", rotation=45)
	ax6.text(15, 0.2, "Median", horizontalalignment="center", rotation=45)
	ax6.text(21, 0.2, "Mode", horizontalalignment="center", rotation=45)
	ax6.text(27, 0.2, "16%", horizontalalignment="center", rotation=45)
	ax1.text(12+46.0, 1.2, "MGC 0628", backgroundcolor="white")

	return ax1, ax2, ax3, ax4, ax5, ax6


#####################
### Main Procedure
#####################
### plot
ax1, ax2, ax3, ax4, ax5, ax6 \
	= startup_plot(fontsize_general,fontsize_legend,xlabel,ylabel,r21range)
#
ax_violin = [ax1, ax2, ax3]
ax_stats = [ax4, ax5, ax6]
for i in range(len(gals)):
#for i in [0]:
	list_co10 = []
	list_co21 = []
	list_r21 = []
	list_beam = []
	statslist_r21 = []
	statslist_r21_wco10 = []
	statslist_r21_wco21 = []
	#
	galname = gals[i]
	galname2 = gals[i].replace("ngc","for NGC ")
	dir_gal = dir_proj + galname
	for j in range(len(beam[i])):
		beamname = str(beam[i][j]).replace(".","p").zfill(4)
		print("# " + galname + " " + beamname)
		beamfloat = float(beam[i][j])
		#
		# co intensities (K.km/s)
		image_co10 = dir_gal + "_co10/co10_" + beamname + ".moment0"
		image_co21 = dir_gal + "_co21/co21_" + beamname + ".moment0"
		#
		# get values
		co10, co21 = get_co_intensities(image_co10,image_co21,beamfloat)
		r21 = co21/co10
		#
		# stats
		stats_r21 = get_stats(r21, None, r21range)
		stats_r21_wco10 = get_stats(r21, co10, r21range)
		stats_r21_wco21 = get_stats(r21, co21, r21range)
		#
		# save to list
		list_co10.append(co10)
		list_co21.append(co21)
		list_r21.append(r21)
		list_beam.append(beamname)
		statslist_r21.append(stats_r21) # [p84, mean, p50, mode, p16]
		statslist_r21_wco10.append(stats_r21_wco10)
		statslist_r21_wco21.append(stats_r21_wco21)
		#
	# plot
	color = cm.brg(i/2.5)
	plot_all_violins(ax_violin[i], list_r21, bins, r21range, list_beam, color, list_co10, list_co21)
	plot_all_stats(ax_stats[i], statslist_r21, statslist_r21_wco10, statslist_r21_wco21, color)
	#
plt.savefig(dir_proj+"eps/violin_co21.png",dpi=300)

os.system("rm -rf *.last")

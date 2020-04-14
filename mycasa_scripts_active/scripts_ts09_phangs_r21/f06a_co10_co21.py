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
xlabel = "log $I_{CO(1-0)}$ (K km s$^{-1}$)"
ylabel = "log $I_{CO(2-1)}$ (K km s$^{-1}$)"
text = "log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$"

gals = ["ngc0628",
		"ngc3627",
		"ngc4321"]
xlim = [[-1.2,1.8],
		[-0.7,2.7],
		[-0.2,2.7]]
ylim = [[-1.2,1.8],
		[-0.7,2.7],
		[-0.2,2.7]]
beam = [[4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0],
        [8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
        [4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0]]


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

def get_percentiles(data):
	"""
	"""
	median = np.median(data)
	p16 = np.percentile(data,16)
	p84 = np.percentile(data,84)

	return [p84, median, p16]

def get_binned_dist(x,y,binrange):
	"""
	"""
	n, _ = np.histogram(x, bins=10, range=binrange)
	sy, _ = np.histogram(x, bins=10, range=binrange, weights=y)
	sy2, _ = np.histogram(x, bins=10, range=binrange, weights=y*y)
	mean = sy / n
	std = np.sqrt(sy2/n - mean*mean)
	binx = (_[1:] + _[:-1])/2

	return binx, mean, std

def plot_scatter(
	ax,
	axb,
	list_co10,
	list_co21,
	list_beamname,
	xlim,
	ylim,
	xlabel,
	ylabel,
	text,
	galname,
	):
	"""
	"""
	### setup ax
	ax.tick_params(labelbottom=False)
	ax.set_xlim(xlim)
	ax.set_ylim(ylim)
	ax.grid(axis="both")
	#
	ax.set_ylabel(ylabel)
	axb.tick_params(labelbottom=False,labelleft=False)
	axb.set_xlim(xlim)
	axb.set_ylim(ylim)
	axb.set_xlabel(xlabel)
	#
	### plot data
	for i in range(len(list_co10)):
		# preparation
		x = np.log10(list_co10[i])
		y = np.log10(list_co21[i])
		beam = list_beamname[i].replace("p0","\"")
		color = cm.gnuplot(i/8.)
		binrange = [x.min(),x.max()]
		#
		# plot
		ax.scatter(x, y, color=color, alpha=0.1, s=20, lw=0, label = beam)
		if i==0:
			binx, mean, std = get_binned_dist(x,y,binrange)
			ax.errorbar(binx, mean, yerr = std, color = color, ecolor = color)
	#
	# plot annotation
	ax.plot(xlim, ylim, "--", color="black", lw=3, alpha=0.7)
	#
	x_line2 = [np.log10(1/0.7*10**xlim[0]), xlim[1]]
	y_line2 = [ylim[0], np.log10(0.7*10**ylim[1])]
	ax.plot(x_line2, y_line2, "--", color="grey", lw=1, alpha=0.9)
	#
	x_line3 = [np.log10(1/0.4*10**xlim[0]), xlim[1]]
	y_line3 = [ylim[0], np.log10(0.4*10**ylim[1])]
	ax.plot(x_line3, y_line3 ,"--", color="grey", lw=1, alpha=0.9)
	#
	# plot text
	ax.text(xlim[0]+(xlim[1]-xlim[0])*0.1, ylim[1]-(ylim[1]-ylim[0])*0.08, text)
	ax.text(xlim[0]+(xlim[1]-xlim[0])*0.1, ylim[1]-(ylim[1]-ylim[0])*0.16, galname)
	ax.text(xlim[0]+(xlim[1]-xlim[0])*0.02, ylim[1]-(ylim[1]-ylim[0])*0.90,
		"1:1", rotation=45, fontsize=12)
	ax.text(xlim[0]+(xlim[1]-xlim[0])*0.12, ylim[1]-(ylim[1]-ylim[0])*0.90,
		"1:0.7", rotation=45, fontsize=12)
	ax.text(xlim[0]+(xlim[1]-xlim[0])*0.21, ylim[1]-(ylim[1]-ylim[0])*0.90,
		"1:0.4", rotation=45, fontsize=12)
	#
	# set legend
	ax.legend(size=12)

#####################
### Main Procedure
#####################
#for i in range(len(gals)):
for i in [0]:
	### get data points ready for plot
	# initialize
	list_co10 = []
	list_co21 = []
	list_r21 = []
	list_beamname = []
	statslist_co10 = []
	statslist_co21 = []
	statslist_r21 = []
	galname = gals[i]
	galname2 = gals[i].replace("ngc","for NGC ")
	dir_gal = dir_proj + galname
	for j in range(len(beam[i])):
		beamname = str(beam[i][j]).replace(".","p").zfill(4)
		print("# " + galname + " " + beamname)
		beamfloat = float(beam[i][j])
		image_co10 = dir_gal + "_co10/co10_" + beamname + ".moment0"
		image_co21 = dir_gal + "_co21/co21_" + beamname + ".moment0"
		# get values
		co10, co21 = get_co_intensities(image_co10,image_co21,beamfloat)
		r21 = co21/co10
		# stats
		stats_co10 = get_percentiles(co10)
		stats_co21 = get_percentiles(co21)
		stats_r21 = get_percentiles(r21)
		# save to list
		list_co10.append(co10)
		list_co21.append(co21)
		list_r21.append(r21)
		statslist_co10.append(stats_co10)
		statslist_co21.append(stats_co21)
		statslist_r21.append(stats_r21)
		list_beamname.append(beamname)

	### plot
	# preparation
	plt.figure(figsize=(9,9))
	plt.rcParams["font.size"] = 14
	gs = gridspec.GridSpec(nrows=18, ncols=18)
	ax1 = plt.subplot(gs[0:9,0:9])
	ax2 = plt.subplot(gs[0:9,9:18])
	ax3 = plt.subplot(gs[9:18,0:9])
	ax1b = ax1.twiny()
	ax2b = ax2.twinx()
	# ax1 and ax1b
	plot_scatter(
		ax1,ax1b,list_co10,list_co21,list_beamname,xlim[i],ylim[i],xlabel,ylabel,text,galname2
		)

	plt.savefig(dir_proj+"eps/" + galname + "_co10_vs_co21.png",dpi=200)


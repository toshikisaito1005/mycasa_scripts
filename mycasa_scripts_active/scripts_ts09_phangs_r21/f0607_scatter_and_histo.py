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
ylabel_r21 = "log $R_{21}$"
text = "log $I_{CO(1-0)}$ vs log $I_{CO(2-1)}$"
text_r21 = "log $I_{CO(2-1)}$ vs log $R_{21}$"
fontsize_general = 15
fontsize_legend = 13

gals = ["ngc0628",
		"ngc3627",
		"ngc4321"]
xlim = [[-1.2,1.8],
		[-0.7,2.7],
		[-0.7,2.7]]
ylim = [[-1.2,1.8],
		[-0.7,2.7],
		[-0.7,2.7]]
ylim_r21 = [[-1.2,0.9],
			[-0.8,1.0],
			[-1.0,0.8]]
beam = [[4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0],
        [8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
        [4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0]]


#####################
### functions
#####################
def get_co_intensities(image_co10,image_co21,noise_co10,noise_co21,beamfloat):
	"""
	"""
	# get image shape
	imshape = imhead(image_co10,mode="list")["shape"]
	box = "0,0," + str(imshape[0]-1) + "," + str(imshape[1]-1)
	# imval
	data_co10_tmp = imval(image_co10,box=box)["data"].flatten()
	data_co21_tmp = imval(image_co21,box=box)["data"].flatten()
	data_noise_co10_tmp = imval(noise_co10,box=box)["data"].flatten()
	data_noise_co21_tmp = imval(noise_co21,box=box)["data"].flatten()
	# cut pixel = 0
	cut_data = np.where((data_co10_tmp>0) & (data_co21_tmp>0) & (data_noise_co10_tmp>0) & (data_noise_co21_tmp>0))
	data_co10 = data_co10_tmp[cut_data]
	data_co21 = data_co21_tmp[cut_data]
	noise_co10 = data_noise_co10_tmp[cut_data]
	noise_co21 = data_noise_co21_tmp[cut_data]
	# Jy-to-K
	co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
	co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
	data_co10_Kelvin = data_co10 * co10_jy2k
	data_co21_Kelvin = data_co21 * co21_jy2k
	data_noise_co10_Kelvin = noise_co10 * co10_jy2k
	data_noise__Kelvin = noise_co21 * co21_jy2k

	return data_co10_Kelvin, data_co21_Kelvin, data_noise_co10_Kelvin, data_noise__Kelvin

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
	list_x,
	list_y,
	snr_x,
	snr_y,
	list_beamname,
	xlim,
	ylim,
	xlabel,
	ylabel,
	text,
	galname,
	ncol=1,
	annotation="flux",
	):
	"""
	"""
	### setup ax
	ax.tick_params(labelbottom=False)
	ax.set_xlim(xlim)
	ax.set_ylim(ylim)
	ax.grid(axis="both")
	ax.set_ylabel(ylabel)
	#
	axb.tick_params(labelbottom=False,labelleft=False)
	axb.set_xlim(xlim)
	axb.set_ylim(ylim)
	axb.set_xlabel(xlabel)
	#
	### plot data
	for i in range(len(list_x)):
		# preparation
		x = np.log10(list_x[i])
		y = np.log10(list_y[i])
		beam = str(int(float(list_beamname[i].replace("p","."))))+"\""
		color = cm.gnuplot(i/9.)
		binrange = [x.min(),x.max()]
		#
		# plot
		ax.scatter(x, y, color=color, alpha=0.4, s=20, lw=0, label = beam)
		if i==0:
			binx, mean, std = get_binned_dist(x,y,binrange)
			ax.errorbar(binx, mean, yerr = std, color = "dimgrey", ecolor = "dimgrey", lw=4)
		# plot error bar
		mean_snr_x = np.mean(snr_x[i])
		mean_snr_y = np.mean(snr_y[i])
		posx = xlim[0]+(xlim[1]-xlim[0])*0.6 + i*0.13
		posy = ylim[1]-(ylim[1]-ylim[0])*0.9
		#
		bar_right  = np.log10(10**posx + 10**posx/mean_snr_x)
		bar_left   = np.log10(10**posx - 10**posx/mean_snr_x)
		bar_top    = np.log10(10**posy + 10**posy/mean_snr_y)
		bar_bottom = np.log10(10**posy - 10**posy/mean_snr_y)
		ax.plot([bar_left,bar_right], [posy,posy], color=color, lw=2)
		ax.plot([posx,posx], [bar_top,bar_bottom], color=color, lw=2)
		#
	# plot annotation
	if annotation=="flux":
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
		#
		# plot text
		ax.text(xlim[0]+(xlim[1]-xlim[0])*0.1, ylim[1]-(ylim[1]-ylim[0])*0.08, text, backgroundcolor="white")
		ax.text(xlim[0]+(xlim[1]-xlim[0])*0.1, ylim[1]-(ylim[1]-ylim[0])*0.14, galname, backgroundcolor="white")
		if "628" in galname:
			ax.text(xlim[0]+(xlim[1]-xlim[0])*0.04, ylim[1]-(ylim[1]-ylim[0])*0.89,
				"1:1", rotation=45, fontsize=12)
			ax.text(xlim[0]+(xlim[1]-xlim[0])*0.14, ylim[1]-(ylim[1]-ylim[0])*0.89,
				"1:0.7", rotation=45, fontsize=12)
			ax.text(xlim[0]+(xlim[1]-xlim[0])*0.23, ylim[1]-(ylim[1]-ylim[0])*0.89,
				"1:0.4", rotation=45, fontsize=12)
	elif annotation=="ratio":
		ax.plot(xlim, [0,0], "--", color="black", lw=3, alpha=0.7)
		#
		x_line2 = [xlim[0], xlim[1]]
		y_line2 = [np.log10(0.7), np.log10(0.7)]
		ax.plot(x_line2, y_line2, "--", color="grey", lw=1, alpha=0.9)
		#
		x_line3 = [xlim[0], xlim[1]]
		y_line3 = [np.log10(0.4), np.log10(0.4)]
		ax.plot(x_line3, y_line3 ,"--", color="grey", lw=1, alpha=0.9)
		#
		# plot text
		ax.text(xlim[0]+(xlim[1]-xlim[0])*0.1, ylim[1]-(ylim[1]-ylim[0])*0.08, text, backgroundcolor="white")
		ax.text(xlim[0]+(xlim[1]-xlim[0])*0.1, ylim[1]-(ylim[1]-ylim[0])*0.14, galname, backgroundcolor="white")
		if "628" in galname:
			ax.text(xlim[0]+(xlim[1]-xlim[0])*0.06, ylim[1]-(ylim[1]-ylim[0])*0.42,
				"1.0", fontsize=12)
			ax.text(xlim[0]+(xlim[1]-xlim[0])*0.06, ylim[1]-(ylim[1]-ylim[0])*0.49,
				"0.7", fontsize=12)
			ax.text(xlim[0]+(xlim[1]-xlim[0])*0.06, ylim[1]-(ylim[1]-ylim[0])*0.61,
				"0.4", fontsize=12)
		#
	# set legend
	ax.legend(bbox_to_anchor=(1.05, -0.05), loc="upper left", ncol=ncol)

def plot_hist_right(
	ax,
	axb,
	list_y,
	statslist_y,
	list_beamname,
	ylim,
	ylabel,
	bins = 60,
	):
	"""
	"""
	### setup ax
	ax.tick_params(labelbottom=False,labelleft=False)
	ax.spines["top"].set_visible(False)
	ax.spines["left"].set_visible(False)
	ax.spines["bottom"].set_visible(False)
	ax.tick_params(top=False,left=False,bottom=False)
	ax.set_ylim(ylim)
	ax.grid(axis="y")
	#
	axb.tick_params(labelbottom=False)
	axb.spines["top"].set_visible(False)
	axb.spines["left"].set_visible(False)
	axb.spines["bottom"].set_visible(False)
	axb.tick_params(top=False,left=False,bottom=False)
	axb.set_ylim(ylim)
	axb.set_ylabel(ylabel)
	#
	### plot data
	stats_step = []
	for i in range(len(list_y)):
		# preparation
		y = np.log10(list_y[i])
		beam = list_beamname[i].replace("p0","\"")
		color = cm.gnuplot(i/9.)
		#
		# histogram
		histo = np.histogram(y, bins=bins, range=ylim)
		x = np.delete(histo[1],-1)
		y = histo[0]/(histo[0].max()*1.05)
		height = (ylim[1]-ylim[0])/bins
		#
		# plot
		ax.plot(y+i, x, drawstyle="steps", color="grey", lw=0.5)
		ax.barh(x, y, height=height, lw=0, color=color, alpha=0.4, left=i)
		#
		stats_step.append(i+0.5)
		#
	### plot stats
	stats_step = np.array(stats_step)
	p84 = np.log10(np.array(statslist_y)[:,0])
	p50 = np.log10(np.array(statslist_y)[:,1])
	p16 = np.log10(np.array(statslist_y)[:,2])
	#
	# plot
	ax.plot(stats_step,p84,"--",color="black",markeredgewidth=0,markersize=3,lw=2,
		label="84% and 16%")
	ax.plot(stats_step,p50,"o-",color="black",markeredgewidth=2,markersize=7,lw=2,
		label="Median")
	ax.plot(stats_step,p16,"--",color="black",markeredgewidth=0,markersize=3,lw=2)
	#
	ax.legend()

def plot_hist_bottom(
	ax,
	list_x,
	statslist_x,
	list_beamname,
	xlim,
	xlabel,
	bins = 60,
	):
	"""
	"""
	# setup ax
	ax.tick_params(labelleft=False)
	ax.spines["top"].set_visible(False)
	ax.spines["left"].set_visible(False)
	ax.spines["right"].set_visible(False)
	ax.tick_params(top=False,left=False,right=False)
	ax.set_xlim(xlim)
	ax.set_ylim([9,0])
	ax.grid(axis="x")
	ax.set_xlabel(xlabel)
	#
	# plot data
	stats_step = []
	for i in range(len(list_x)):
		# preparation
		x = np.log10(list_x[i])
		beam = list_beamname[i].replace("p0","\"")
		color = cm.gnuplot(i/9.)
		#
		# histogram
		histo = np.histogram(x, bins=bins, range=xlim)
		y = np.delete(histo[1],-1)
		x = histo[0]/(histo[0].max()*1.05)
		width = (xlim[1]-xlim[0])/bins
		#
		# plot
		ax.plot(y ,x+i, drawstyle="steps-mid", color="grey", lw=0.5)
		ax.bar(y, x, width=width,
			lw=0, color=color, alpha=0.4, bottom=i, align="center")
		#
		stats_step.append(i+0.5)
		#
	### plot stats
	stats_step = np.array(stats_step)
	p84 = np.log10(np.array(statslist_x)[:,0])
	p50 = np.log10(np.array(statslist_x)[:,1])
	p16 = np.log10(np.array(statslist_x)[:,2])
	#
	# plot
	ax.plot(p84,stats_step,"--",color="black",markeredgewidth=0,markersize=3,lw=2)
	ax.plot(p50,stats_step,"o-",color="black",markeredgewidth=2,markersize=7,lw=2)
	ax.plot(p16,stats_step,"--",color="black",markeredgewidth=0,markersize=3,lw=2)

def plot_threshold(
	ax,
	list_noise_x,
	list_noise_y,
	xlim,
	ylim,
	list_x,
	mode="flux",
	):
	"""
	"""
	# plot
	for i in range(len(list_x)):
		noise_x = min(list_noise_x[i]) # np.median(list_noise_x[i])
		noise_y = min(list_noise_y[i]) # np.median(list_noise_y[i])
		color = cm.gnuplot(i/9.)
		ax.plot([np.log10(noise_x * 3.0), np.log10(noise_x * 3.0)],
			ylim, "-", color = color, alpha=0.5)
		if mode=="flux":
			ax.plot(xlim,
				[np.log10(noise_y * 3.0), np.log10(noise_y * 3.0)],
				"-", color = color, alpha=0.5)


#####################
### Main Procedure
#####################
for i in range(len(gals)):
#for i in [0]:
	### get data points ready for plot
	# initialize
	list_co10 = []
	list_co21 = []
	list_r21 = []
	list_errco10 = []
	list_errco21 = []
	list_errr21 = []
	list_snrco10 = []
	list_snrco21 = []
	list_snrr21 = []
	list_beamname = []
	statslist_co10 = []
	statslist_co21 = []
	statslist_r21 = []
	#
	galname = gals[i]
	galname2 = gals[i].replace("ngc","for NGC ")
	dir_gal = dir_proj + galname
	#
	for j in range(len(beam[i])):
		beamname = str(beam[i][j]).replace(".","p").zfill(4)
		print("# " + galname + " " + beamname)
		beamfloat = float(beam[i][j])
		# co intensities (K.km/s)
		image_co10 = dir_gal + "_co10/co10_" + beamname + ".moment0"
		image_co21 = dir_gal + "_co21/co21_" + beamname + ".moment0"
		# co noise (K.km/s)
		noise_co10 = dir_gal + "_co10/co10_" + beamname + ".moment0.noise"
		noise_co21 = dir_gal + "_co21/co21_" + beamname + ".moment0.noise"
		# get values
		co10, co21, err_co10, err_co21 \
			= get_co_intensities(image_co10,image_co21,noise_co10,noise_co21,beamfloat)
		r21 = co21/co10
		err_r21 = r21 * np.sqrt((err_co10/co10)**2 + (err_co21/co21)**2)
		snr_co10 = co10 / err_co10
		snr_co21 = co21 / err_co21
		snr_r21 = r21 / err_r21
		# stats
		stats_co10 = get_percentiles(co10)
		stats_co21 = get_percentiles(co21)
		stats_r21 = get_percentiles(r21)
		# save to list
		list_co10.append(co10)
		list_co21.append(co21)
		list_r21.append(r21)
		list_errco10.append(err_co10)
		list_errco21.append(err_co21)
		list_errr21.append(err_r21)
		list_snrco10.append(snr_co10)
		list_snrco21.append(snr_co21)
		list_snrr21.append(snr_r21)
		statslist_co10.append(stats_co10)
		statslist_co21.append(stats_co21)
		statslist_r21.append(stats_r21)
		list_beamname.append(beamname)


	### plot: co10 vs co21
	# preparation
	print("# plot co10 vs co21")
	plt.figure(figsize=(9,9))
	plt.rcParams["font.size"] = fontsize_general
	plt.rcParams["legend.fontsize"] = fontsize_legend
	gs = gridspec.GridSpec(nrows=18, ncols=18)
	ax1 = plt.subplot(gs[0:11,0:11])
	ax2 = plt.subplot(gs[0:11,11:18])
	ax3 = plt.subplot(gs[11:18,0:11])
	ax1b = ax1.twiny()
	ax2b = ax2.twinx()
	# plot
	plot_scatter(ax1, ax1b, list_co10, list_co21, list_snrco10, list_snrco21, list_beamname,xlim[i], ylim[i], xlabel, ylabel, text, galname2)
	plot_threshold(ax1, list_errco10, list_errco21, xlim[i], ylim[i], list_co10)
	plot_hist_right(ax2, ax2b, list_co21, statslist_co21, list_beamname, ylim[i], ylabel)
	plot_hist_bottom(ax3, list_co10, statslist_co10, list_beamname, xlim[i], xlabel)
	#
	plt.savefig(dir_proj+"eps/" + galname + "_co10_vs_co21.png",dpi=200)


	### plot: co21 vs r21
	# preparation
	print("# plot co21 vs r21")
	plt.figure(figsize=(9,9))
	plt.rcParams["font.size"] = fontsize_general
	plt.rcParams["legend.fontsize"] = fontsize_legend
	gs = gridspec.GridSpec(nrows=18, ncols=18)
	ax1 = plt.subplot(gs[0:11,0:11])
	ax2 = plt.subplot(gs[0:11,11:18])
	ax3 = plt.subplot(gs[11:18,0:11])
	ax1b = ax1.twiny()
	ax2b = ax2.twinx()
	# plot
	plot_scatter(ax1,ax1b, list_co21, list_r21, list_snrco21, list_snrr21, list_beamname, ylim[i], ylim_r21[i], ylabel, ylabel_r21, text_r21, galname2, annotation="ratio")
	plot_threshold(ax1, list_errco21, list_errr21, ylim[i], ylim_r21[i], list_co21, mode="ratio")
	plot_hist_right(ax2, ax2b, list_r21, statslist_r21, list_beamname, ylim_r21[i], ylabel_r21)
	plot_hist_bottom(ax3, list_co21, statslist_co21, list_beamname, ylim[i], ylabel)
	#
	plt.savefig(dir_proj+"eps/" + galname + "_co21_vs_r21.png",dpi=200)


os.system("rm -rf *.last")

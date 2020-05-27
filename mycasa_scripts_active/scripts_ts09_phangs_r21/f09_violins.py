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
bins = 70
r21range = [0.05,1.45]
ylabel = "$R_{21}$"
gals = ["ngc0628",
		"ngc3627",
		"ngc4321"]
beam = [[4.0,8.0,12.0,16.0,20.0],
        [8.0,12.0,16.0,20.0,24.0],
        [4.0,8.0,12.0,16.0,20.0]]
scales = [44/1.0, 52/1.3, 103/1.4]
cnt_ras = [24.174, 170.063, 185.729]
cnt_decs = [15.783, 12.9914, 15.8223]
pas = [180-21.1, 180-172.4, 180-157.8]
incs = [90-8.7, 90-56.2, 90-35.1]
def_nucleus = [50*44./1.0, 50*52./1.3*1.5, 30*103/1.4]


#####################
### functions
#####################
def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    """
    myim10
    """
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale # arcsec * pc/arcsec
    
    return r

def get_co_intensities(
	image_co10,
	image_co21,
	beamfloat,
	pa,
	inc,
	cnt_ra,
	cnt_dec,
	scale,
	def_nucleus,
	):
	"""
	"""
	# get image shape
	imshape = imhead(image_co10,mode="list")["shape"]
	box = "0,0," + str(imshape[0]-1) + "," + str(imshape[1]-1)
	# imval
	data_co10_tmp = imval(image_co10,box=box)["data"].flatten()
	data_co21_tmp = imval(image_co21,box=box)["data"].flatten()
	# distance
	data_ra = imval(image_co10,box=box)["coords"][:,:,0].flatten() * 180 / np.pi
	data_dec = imval(image_co10,box=box)["coords"][:,:,1].flatten() * 180 / np.pi
	data_dist = distance(data_ra, data_dec, pa, inc, cnt_ra, cnt_dec, scale)
	#print("# " + str(np.min(data_dist)))
	#print("# " + str(np.median(data_dist)))
	# cut pixel = 0
	cut_data = np.where((data_co10_tmp>0) & (data_co21_tmp>0) & (data_dist>def_nucleus/2.))
	data_co10 = data_co10_tmp[cut_data]
	data_co21 = data_co21_tmp[cut_data]
	data_dist = data_dist[cut_data]
	# Jy-to-K
	co10_jy2k = 1.222e6 / beamfloat**2 / 115.27120**2
	co21_jy2k = 1.222e6 / beamfloat**2 / 230.53800**2
	data_co10_Kelvin = data_co10 * co10_jy2k
	data_co21_Kelvin = data_co21 * co21_jy2k

	return data_co10_Kelvin, data_co21_Kelvin, data_dist

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
		list_p84 = [weighted_percentile(s,0.84,None) for s in list_violin]
		list_p16 = [weighted_percentile(s,0.16,None) for s in list_violin]
	else:
		list_median = []
		list_p84 = []
		list_p16 = []
		for j in range(len(list_violin)):
			list_median.append(weighted_percentile(list_violin[j],0.5,weights[j]))
			list_p84.append(weighted_percentile(list_violin[j],0.84,weights[j]))
			list_p16.append(weighted_percentile(list_violin[j],0.16,weights[j]))
	# plot medians
	ax.plot(np.array(list_xaxis)+x_absoffset,list_median,"-",color='black',alpha=1.0,lw=2)
	ax.plot(np.array(list_xaxis)+x_absoffset,list_median,"o",color='black',markersize=8,markeredgewidth=0,lw=2)
	# plot percentiles
	ax.plot(np.array(list_xaxis)+x_absoffset,list_p84,"--",color='black',alpha=1.0,lw=1)
	ax.plot(np.array(list_xaxis)+x_absoffset,list_p16,"--",color='black',alpha=1.0,lw=1)

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
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.40,23.0)
	#
	weights = weights2
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.20,46.0)

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
	plot_one_stats(ax, statslist_r21, "-", color, lw=3, alpha=0.60)
	plot_one_stats(ax, statslist_r21_wco10, "-", color, lw=3, alpha=0.40)
	plot_one_stats(ax, statslist_r21_wco21, "-", color, lw=3, alpha=0.20)

def startup_plot(
	ylabel,
	r21range,
	):
	plt.subplots(nrows=1,ncols=1,figsize=(10, 7),sharey=True)
	plt.rcParams["font.size"] = 14
	plt.rcParams["legend.fontsize"] = 9
	plt.subplots_adjust(bottom=0.1, left=0.07, right=0.99, top=0.99)
	gs = gridspec.GridSpec(nrows=18, ncols=25)
	ax1 = plt.subplot(gs[0:6,0:25])
	ax2 = plt.subplot(gs[6:12,0:25])
	ax3 = plt.subplot(gs[12:18,0:25])
	ax1.set_ylim(r21range)
	ax2.set_ylim(r21range)
	ax3.set_ylim(r21range)
	ax1.grid(axis="y")
	ax2.grid(axis="y")
	ax3.grid(axis="y")
	ax1.set_xlim([0,70])
	ax2.set_xlim([4,74])
	ax3.set_xlim([0,70])
	ax1.tick_params(axis="x", length=0)
	ax2.tick_params(axis="x", length=0)
	ax3.tick_params(axis="x", length=0)
	ax1.tick_params(labelbottom=False)
	ax2.tick_params(labelbottom=False)
	ax3.tick_params(labelbottom=False)
	ax1.set_yticks([0.3,0.6,0.9,1.2])
	ax2.set_yticks([0.3,0.6,0.9,1.2])
	ax3.set_yticks([0.3,0.6,0.9,1.2])
	ax2.set_ylabel(ylabel)
	# text
	boxdic = {
    "facecolor" : "white",
    "edgecolor" : "black",
    "boxstyle" : "square",
    "linewidth" : 1,
    }
	ax3.text(12,      -0.11, "# of Sightlines", horizontalalignment="center")
	ax3.text(12+23.0, -0.11, "CO(1-0) Flux", horizontalalignment="center")
	ax3.text(12+46.0, -0.11, "CO(2-1) Flux", horizontalalignment="center")
	ax1.text(8+7+46.0,  1.25,  "NGC 0628", bbox=boxdic)
	ax2.text(12+7+46.0, 1.25,  "NGC 3627", bbox=boxdic)
	ax3.text(8+7+46.0,  1.25,  "NGC 4321", bbox=boxdic) # , backgroundcolor="white")
	ax1.text(4.4,  0.08,  "4\"", fontsize=10)
	ax1.text(8.4,  0.08,  "8\"", fontsize=10)
	ax1.text(12.4, 0.08, "12\"", fontsize=10)
	ax1.text(16.4, 0.08, "16\"", fontsize=10)
	ax1.text(20.4, 0.08, "20\"", fontsize=10)
	ax2.text(8.4,  0.08,  "8\"", fontsize=10)
	ax2.text(12.4, 0.08, "12\"", fontsize=10)
	ax2.text(16.4, 0.08, "16\"", fontsize=10)
	ax2.text(20.4, 0.08, "20\"", fontsize=10)
	ax2.text(24.4, 0.08, "24\"", fontsize=10)
	ax3.text(4.4,  0.08,  "4\"", fontsize=10)
	ax3.text(8.4,  0.08,  "8\"", fontsize=10)
	ax3.text(12.4, 0.08, "12\"", fontsize=10)
	ax3.text(16.4, 0.08, "16\"", fontsize=10)
	ax3.text(20.4, 0.08, "20\"", fontsize=10)

	return ax1, ax2, ax3


#####################
### Main Procedure
#####################
### plot
ax1, ax2, ax3 = startup_plot(ylabel,r21range)
#
ax_violin = [ax1, ax2, ax3]
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
		co10, co21, dist = get_co_intensities(image_co10,image_co21,beamfloat,pas[i],incs[i],cnt_ras[i],cnt_decs[i],scales[i],def_nucleus[i])
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
		"""
		figure = plt.figure(figsize=(10,5))
		gs = gridspec.GridSpec(nrows=8, ncols=16)
		ax1 = plt.subplot(gs[0:7,0:7])
		ax2 = plt.subplot(gs[0:7,7:16])
		ax1.scatter(np.log10(co21), np.log10(r21))
		ax2.scatter(dist, np.log10(r21))
		plt.savefig(dir_proj+"test_"+str(i)+"_"+str(j)+".png",dpi=200)
		"""
		#
	# plot
	color = cm.brg(i/2.5)
	plot_all_violins(ax_violin[i], list_r21, bins, r21range, list_beam, color, list_co10, list_co21)
	#plot_all_stats(ax_stats[i], statslist_r21, statslist_r21_wco10, statslist_r21_wco21, color)
	#
plt.savefig(dir_proj+"eps/violin_co21.png",dpi=300)

os.system("rm -rf *.last")

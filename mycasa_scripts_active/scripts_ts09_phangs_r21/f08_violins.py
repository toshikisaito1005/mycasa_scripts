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

"""
def get_percentiles(data,wehgits):
	median = np.median(data)
	p16 = np.percentile(data,16)
	p84 = np.percentile(data,84)

	return [p84, median, p16]
"""

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
		# plot stats

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
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.7,0.0)
	#
	weights = weights1
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.4,23.0)
	#
	weights = weights2
	plot_multi_violins(ax,list_r21,bins,r21range,weights,list_beam,color,0.1,46.0)


#####################
### Main Procedure
#####################
### plot
plt.subplots(nrows=1,ncols=1,figsize=(10, 5),sharey=True)
plt.rcParams["font.size"] = fontsize_general
plt.rcParams["legend.fontsize"] = fontsize_legend
plt.subplots_adjust(bottom=0.10, left=0.10, right=0.98, top=0.92)
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
ax1.grid(axis="y")
ax2.grid(axis="y")
ax3.grid(axis="y")
ax4.grid(axis="y")
ax5.grid(axis="y")
ax6.grid(axis="y")
ax1.set_xlim([0,70])
ax2.set_xlim([4,74])
ax3.set_xlim([0,70])
ax4.set_xlim([2,22])
ax5.set_xlim([6,26])
ax6.set_xlim([2,22])
ax1.tick_params(labelbottom=False)
ax2.tick_params(labelbottom=False)
ax4.tick_params(labelbottom=False)
ax5.tick_params(labelbottom=False)
ax1.set_yticks([0.2,0.5,0.8,1.1,1.4])
ax2.set_yticks([0.2,0.5,0.8,1.1,1.4])
ax3.set_yticks([0.2,0.5,0.8,1.1,1.4])
ax4.set_yticks([0.2,0.5,0.8,1.1,1.4])
ax5.set_yticks([0.2,0.5,0.8,1.1,1.4])
ax6.set_yticks([0.2,0.5,0.8,1.1,1.4])
ax3.set_xticks(
	[4,8,12,16,20,
	 4+23,8+23,12+23,16+23,20+23,
	 4+46,8+46,12+46,16+46,20+46],
	[1,2,3,4,5,
	 1,2,3,4,5,
	 1,2,3,4,5])
#
ax_master = [ax1, ax2, ax3]
for i in range(len(gals)):
#for i in [0]:
	list_co10 = []
	list_co21 = []
	list_r21 = []
	list_beam = []
	statslist_co10 = []
	statslist_co21 = []
	statslist_r21 = []
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
		co10, co21 \
			= get_co_intensities(image_co10,image_co21,beamfloat)
		r21 = co21/co10
		#
		# save to list
		list_co10.append(co10)
		list_co21.append(co21)
		list_r21.append(r21)
		list_beam.append(beamname)
		#
	# plot
	color = cm.brg(i/2.5)
	plot_all_violins(
		ax_master[i],list_r21,bins,r21range,list_beam,color,list_co10,list_co21,
		)
	#
plt.savefig(dir_proj+"eps/violin_co21.png")

os.system("rm -rf *.last")

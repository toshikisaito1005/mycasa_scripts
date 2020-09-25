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
beam = [[4.0,8.0,12.0,16.0,20.0,33.0],
        [8.0,12.0,16.0,20.0,24.0,33.0],
        [4.0,8.0,12.0,16.0,20.0,33.0]]
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


#####################
### Main Procedure
#####################
### plot
figure = plt.figure(figsize=(10,4))
gs = gridspec.GridSpec(nrows=1, ncols=15)
plt.subplots_adjust(bottom=0.15, left=0.07, right=0.98, top=0.90)
ax1 = plt.subplot(gs[0:5,0:5])
ax2 = plt.subplot(gs[0:5,5:10])
ax3 = plt.subplot(gs[0:5,10:15])
ax1.grid(axis="y")
ax2.grid(axis="y")
ax3.grid(axis="y")
ax1.set_ylabel("Normed Median")
ax1.set_xlabel("Beam Size (arcsec)")
ax2.set_xlabel("Beam Size (arcsec)")
ax3.set_xlabel("Beam Size (arcsec)")
ax2.tick_params(labelleft=False)
ax3.tick_params(labelleft=False)
ax1.set_title("NGC 0628")
ax2.set_title("NGC 3627")
ax3.set_title("NGC 4321")
plt.rcParams["font.size"] = 12
#
axlist = [ax1, ax2, ax3]
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
		list_beam.append(beamfloat)
		statslist_r21.append(stats_r21) # [p84, mean, p50, mode, p16]
		statslist_r21_wco10.append(stats_r21_wco10)
		statslist_r21_wco21.append(stats_r21_wco21)
		#
	# plot
	color = cm.brg(i/2.5)
	ax = axlist[i]
	#
	if i==0:
		label1 = "Unweighted"
		label2 = "CO(1-0)-weighted"
		label3 = "CO(2-1)-weighted"
	else:
		label1=None
		label2=None
		label3=None
	#
	norm_median = np.log10(np.array(statslist_r21)[:,2] / np.array(statslist_r21)[:,2][0])
	bars = ax.plot(list_beam, norm_median, "o-", color=color, alpha=0.6, lw=2, label=label1)
	[bar.set_alpha(0.6) for bar in bars]
	#
	norm_median = np.log10(np.array(statslist_r21_wco10)[:,2] / np.array(statslist_r21_wco10)[:,2][0])
	bars = ax.plot(list_beam, norm_median, "o-", color=color, alpha=0.6, lw=2, label=label2)
	[bar.set_alpha(0.4) for bar in bars]
	#
	norm_median = np.log10(np.array(statslist_r21_wco21)[:,2] / np.array(statslist_r21_wco21)[:,2][0])
	bars = ax.plot(list_beam, norm_median, "o-", color=color, alpha=0.6, lw=2, label=label3)
	[bar.set_alpha(0.2) for bar in bars]

	ax.set_ylim([-0.1,0.2])
	if i==1:
		ax.set_xlim([6.0,35.0])
	else:
		ax.set_xlim([2.0,35.0])
	ax.legend()

plt.savefig(dir_proj+"eps/violin_median.png",dpi=300)

os.system("rm -rf *.last")

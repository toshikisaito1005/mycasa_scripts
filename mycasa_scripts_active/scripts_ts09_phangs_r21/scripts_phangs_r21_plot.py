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

def weighted_p16(
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
		midpoint = 0.157 * sum(s_weights)
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

def weighted_p84(
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
		midpoint = 0.843 * sum(s_weights)
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
	median_all = weighted_median(data=data_all,weights=weights_all)
	median_in = weighted_median(data=data_in,weights=weights_in)
	median_out = weighted_median(data=data_out,weights=weights_out)
	#
	# plot histograms
	ax.step(histo_allx,histo_all_norm,"black",lw=3,alpha=0.5)
	ax.step(histo_allx,histo_in_norm,c=color,ls="dotted",lw=2,alpha=1.0)
	ax.step(histo_allx,histo_out_norm,c=color,ls="-",lw=2,alpha=0.5)
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

import os, re, sys, glob
import itertools
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy.optimize import curve_fit
from scipy import stats
import matplotlib.cm as cm
plt.ioff()


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
bins = 25


#####################
### def
#####################
def extract_scatter(model_scatter, model_scatter_cut):
	###
	data_scatter_ngc0628 = np.loadtxt(model_scatter)
	co10_scatter = data_scatter_ngc0628[:,0]
	co21_scatter = data_scatter_ngc0628[:,1]
	r21_scatter = np.log10(10**co21_scatter/10**co10_scatter)
	#
	data_scatter_cut_ngc0628 = np.loadtxt(model_scatter_cut)
	co10_scatter_cut = data_scatter_cut_ngc0628[:,0]
	co21_scatter_cut = data_scatter_cut_ngc0628[:,1]
	r21_scatter_cut = np.log10(10**co21_scatter_cut/10**co10_scatter_cut)

	###
	xwdith_co10 = co10_scatter.max() - co10_scatter_cut.min()
	xlim_co10 = [co10_scatter_cut.min(), co10_scatter_cut.max()]
	xwdith_co21 = co21_scatter.max() - co21_scatter_cut.min()
	xlim_co21 = [co21_scatter_cut.min(), co21_scatter_cut.max()]

	###
	n_scatter, _ = np.histogram(co10_scatter, bins=bins, range=xlim_co10)
	sy_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter, range=xlim_co10)
	sy2_scatter, _ = np.histogram(co10_scatter, bins=bins, weights=co21_scatter*co21_scatter, range=xlim_co10)
	#
	n_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, range=xlim_co10)
	sy_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, weights=co21_scatter_cut, range=xlim_co10)
	sy2_scatter_cut, _ = np.histogram(co10_scatter_cut, bins=bins, weights=co21_scatter_cut*co21_scatter_cut, range=xlim_co10)
	xaxis_co10 = (_[1:] + _[:-1])/2
	#
	n_r21scatter, _ = np.histogram(co21_scatter, bins=bins, range=xlim_co21)
	sy_r21scatter, _ = np.histogram(co21_scatter, bins=bins, weights=r21_scatter, range=xlim_co21)
	sy2_r21scatter, _ = np.histogram(co21_scatter, bins=bins, weights=r21_scatter*r21_scatter, range=xlim_co21)
	#
	n_r21scatter_cut, _ = np.histogram(co21_scatter_cut, bins=bins, range=xlim_co21)
	sy_r21scatter_cut, _ = np.histogram(co21_scatter_cut, bins=bins, weights=r21_scatter_cut, range=xlim_co21)
	sy2_r21scatter_cut, _ = np.histogram(co21_scatter_cut, bins=bins, weights=r21_scatter_cut*r21_scatter_cut, range=xlim_co21)
	xaxis_co21 = (_[1:] + _[:-1])/2

	###
	mean_scatter = sy_scatter / n_scatter
	std_scatter = np.sqrt(sy2_scatter/n_scatter - mean_scatter*mean_scatter)
	#
	mean_scatter_cut = sy_scatter_cut / n_scatter_cut
	std_scatter_cut = np.sqrt(sy2_scatter_cut/n_scatter_cut - mean_scatter_cut*mean_scatter_cut)
	#
	mean_r21scatter = sy_r21scatter / n_r21scatter
	std_r21scatter = np.sqrt(sy2_r21scatter/n_r21scatter - mean_r21scatter*mean_r21scatter)
	#
	mean_r21scatter_cut = sy_r21scatter_cut / n_r21scatter_cut
	std_r21scatter_cut = np.sqrt(sy2_r21scatter_cut/n_r21scatter_cut - mean_r21scatter_cut*mean_r21scatter_cut)

	return xaxis_co10, xaxis_co21, std_scatter, std_scatter_cut, std_r21scatter, std_r21scatter_cut


#####################
### main
#####################
###
n0628_xaxis_co10, n0628_xaxis_co21, n0628_std_scatter, n0628_std_scatter_cut, n0628_std_r21scatter, n0628_std_r21scatter_cut = \
	extract_scatter(dir_proj + "eps/ngc0628_model_scatter.txt", dir_proj + "eps/ngc0628_model_scatter_cut.txt")

n3627_xaxis_co10, n3627_xaxis_co21, n3627_std_scatter, n3627_std_scatter_cut, n3627_std_r21scatter, n3627_std_r21scatter_cut = \
	extract_scatter(dir_proj + "eps/ngc3627_model_scatter.txt", dir_proj + "eps/ngc3627_model_scatter_cut.txt")

n4321_xaxis_co10, n4321_xaxis_co21, n4321_std_scatter, n4321_std_scatter_cut, n4321_std_r21scatter, n4321_std_r21scatter_cut = \
	extract_scatter(dir_proj + "eps/ngc4321_model_scatter.txt", dir_proj + "eps/ngc4321_model_scatter_cut.txt")

#
plt.figure(figsize=(10,8))
plt.rcParams["font.size"] = 16
plt.rcParams["legend.fontsize"] = 14
plt.subplots_adjust(bottom=0.05, left=0.10, right=0.98, top=0.95)
gs = gridspec.GridSpec(nrows=20, ncols=20)
ax1 = plt.subplot(gs[0:8,0:20])
ax2 = plt.subplot(gs[10:18,0:20])
ax1.grid(axis='both')
ax2.grid(axis='both')
ax1.set_xlabel("log $I_{CO(1-0)}$ (K km s$^{-1}$)")
ax2.set_xlabel("log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax1.set_ylabel("S.D. of log $I_{CO(2-1)}$ (K km s$^{-1}$)")
ax2.set_ylabel("S.D. of log $R_{21}$")
#
# ax1
ax1.plot(n0628_xaxis_co10, n0628_std_scatter, "-", color=cm.brg(0/2.5), alpha=0.5, lw=4, label="NGC 0628 Model with Scatter")
ax1.plot(n0628_xaxis_co10, n0628_std_scatter_cut, "--", color=cm.brg(0/2.5), alpha=0.5, lw=4, label="NGC 0628 Model with Scatter (sensitivity-limited)")
#
ax1.plot(n3627_xaxis_co10, n3627_std_scatter, "-", color=cm.brg(1/2.5), alpha=0.5, lw=4, label="NGC 3627 Model with Scatter")
ax1.plot(n3627_xaxis_co10, n3627_std_scatter_cut, "--", color=cm.brg(1/2.5), alpha=0.5, lw=4, label="NGC 3627 Model with Scatter (sensitivity-limited)")
#
ax1.plot(n4321_xaxis_co10, n4321_std_scatter, "-", color=cm.brg(2/2.5), alpha=0.5, lw=4, label="NGC 4321 Model with Scatter")
ax1.plot(n4321_xaxis_co10, n4321_std_scatter_cut, "--", color=cm.brg(2/2.5), alpha=0.5, lw=4, label="NGC 4321 Model with Scatter (sensitivity-limited)")
ax1.set_xlim(xlim_co10)
ax1.set_ylim([0,0.6])
ax1.legend()
# ax2
#ax2.plot(co21_scatter,r21_scatter,"o")
#ax2.plot(co21_scatter_cut,r21_scatter_cut,"o")
ax2.plot(n0628_xaxis_co21, n0628_std_r21scatter, "-", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax2.plot(n0628_xaxis_co21, n0628_std_r21scatter_cut, "--", color=cm.brg(0/2.5), alpha=0.5, lw=4)
ax2.set_xlim(xlim_co21)
ax2.set_ylim([0,0.25])
#
plt.savefig(dir_proj + "eps/model_scatter.png",dpi=200)


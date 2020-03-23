import os, re, sys
import glob
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
box = "103,115,180,192"
beamarea = 22.382

zspec = 0.01818
DL = 78.2 # Mpc
x_sncut = 0.00075 # rms in Jy/beam
y_sncut = 4.37 # log luminsity

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")


#####################
### def
#####################
def func1(x, a, b, c):
    return a*np.exp(-(x-b)**2/(2*c**2))

def func2(x, a1, b1, c1, a2, b2, c2):
    return a1*np.exp(-(x-b1)**2/(2*c1**2)) + a2*np.exp(-(x-b2)**2/(2*c2**2))

def fit_func1(func1, data_x, data_y, guess):
    """
    fit data with func1
    """
    popt, pcov = curve_fit(func1,
                           data_x, data_y,
                           p0=guess)
    best_func = func1(data_x,popt[0],popt[1],popt[2])
    residual = data_y - best_func
                           
    return popt, residual

def fit_func2(func1, data_x, data_y, guess):
    """
    fit data with func1
    """
    popt, pcov = curve_fit(func2,
                           data_x, data_y,
                           p0=guess)
    best_func = func2(data_x,popt[0],popt[1],popt[2],popt[3],popt[4],popt[5])
    residual = data_y - best_func
                           
    return popt, residual

def histplotter(
	ax,
	data,
	savefig,
	title,
	xlabel,
	color,
	weights = None,
	twogaussfit = False,
	ylim = [0.0,0.25],
	histrange = [0.01,0.39],
	bins = 25,
	):
    """
    """
    # histogram
    histo = np.histogram(data,range=histrange,bins=bins,weights=weights)
    histox,histoy = np.delete(histo[1],-1),histo[0]
    histoy = histoy/float(sum(histoy))

    # fit
    if twogaussfit==False:
        popt, residual = fit_func1(func1,histox,histoy,[0.20,0.15,0.02])
        label = str(np.round(popt[1],2)) + " $\pm$ " + str(np.round(popt[2],2))
        plt.plot(histox,func1(histox,*popt),c=color,lw=6,alpha=0.5,
        	label = label)

    elif twogaussfit==True:
        popt, residual = fit_func2(func2,histox,histoy,[0.20,0.15,0.02,0.05,0.15,0.20])
        plt.plot(histox,func2(histox,*popt),c=color,lw=6,alpha=0.5)
        plt.plot(histox,func1(histox,popt[0],popt[1],popt[2]),"--",c=color,lw=2,alpha=0.5)
        plt.plot(histox,func1(histox,popt[3],popt[4],popt[5]),"--",c=color,lw=2,alpha=0.5)

    # plot
    #ax.hist(data,range=histrange,bins=bins,weights=weights,color="black")
    ax.step(histox,histoy,"black",lw=4,alpha=0.5)

    # setup plot
    ax.set_xlim(histrange)
    ax.set_ylim(ylim)
    ax.set_xlabel(xlabel)
    ax.set_ylabel("Count")
    ax.set_title(title)
    ax.grid()
    plt.legend()
    plt.savefig(savefig,dpi=300)


#####################
### Main Procedure
#####################
# CI(1-0) observed frequency
obsfreq_x = 492.16065100 / (1 + 0.01818) # dust continuum
obsfreq_y1 = 492.16065100 / (1 + 0.01818) # CI
obsfreq_y2 = 115.27120 / (1 + 0.01818) # CO

# flux (Jy.km/s) to luminosity (K.km/spc^2)
eqn_fl2lum_x = 1.197e27 * DL**2 / (1 + zspec)**3
eqn_fl2lum_y1 = 3.25e+7 / obsfreq_y1**2 * DL**2 / (1 + zspec)**3
eqn_fl2lum_y2 = 3.25e+7 / obsfreq_y2**2 * DL**2 / (1 + zspec)**3

# moment-0 maps in Jy/beam.km/s
data_x_org = imval(dir_data + "image_b8contin/b8contin.flux",box=box)["data"]
data_y1_org = imval(dir_data + "image_ci10/ci10.moment0",box=box)["data"]
data_y2_org = imval(dir_data + "image_co10/co10.moment0",box=box)["data"]
data_x = data_x_org.flatten()
data_y1 = data_y1_org.flatten()
data_y2 = data_y2_org.flatten()
data1_x = data_x[data_x>0]
data1_y1 = data_y1[data_x>0]
data1_y2 = data_y2[data_x>0]
data2b_x = data1_x[data1_y1>0] / beamarea
data2b_y1 = data1_y1[data1_y1>0] / beamarea
data2b_y2 = data1_y2[data1_y1>0] / beamarea
data2_x = data2b_x[data2b_y2>0]
data2_y1 = data2b_y1[data2b_y2>0]
data2_y2 = data2b_y2[data2b_y2>0]

# noise maps in Jy.km/s
data_noise_y1_org = imval(dir_data + "image_ci10/ci10.moment0.noise_Jykms",box=box)["data"]
data_noise_y1 = data_noise_y1_org.flatten()
data1_noise_y1 = data_noise_y1[data_x>0]
data2b_noise_y1 = data1_noise_y1[data1_y1>0]
data2_noise_y1 = data2b_noise_y1[data2b_y2>0]

#
x = (data2_x * eqn_fl2lum_x)[data2_x > x_sncut/beamarea*2.5]
y1 = (data2_y1 * eqn_fl2lum_y1)[data2_x > x_sncut/beamarea*2.5]
y2 = (data2_y2 * eqn_fl2lum_y2)[data2_x > x_sncut/beamarea*2.5]

ratio_ci_co = y1 / y2
ratio_ci_dust = y1 / x # (x / 10**20.8)

#
plt.figure(figsize=(8,5))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.15, top=0.90)
ax = plt.subplot(1,1,1)
histplotter(
	ax,
	ratio_ci_co,
	dir_data+"eps/histo_ci_co.png",
	"(a) [CI]/CO Ratio Histogram",
	"[CI]/CO Luminosity Ratio",
	color = "red")

#
plt.figure(figsize=(8,5))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.15, top=0.90)
ax = plt.subplot(1,1,1)
histplotter(
	ax,
	ratio_ci_co,
	dir_data+"eps/histo_ci_co_weight.png",
	"(c) Weighted [CI]/CO Ratio Histogram",
	"[CI]/CO Luminosity Ratio",
	color = "red",
	weights = y1)

#
plt.figure(figsize=(8,5))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.15, top=0.90)
ax = plt.subplot(1,1,1)
histplotter(
	ax, 
	ratio_ci_dust*10**20.8,
	dir_data+"eps/histo_ci_dust.png",
	"(b) [CI]/Dust Ratio Histogram",
	"[CI]/Dust Luminosity Ratio (Scaled)",
	color = "blue")

#
plt.figure(figsize=(8,5))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.15, top=0.90)
ax = plt.subplot(1,1,1)
histplotter(
	ax, 
	ratio_ci_dust*10**20.8,
	dir_data+"eps/histo_ci_dust_weight.png",
	"(d) Weighted [CI]/Dust Ratio Histogram",
	"[CI]/Dust Luminosity Ratio (Scaled)",
	color = "blue",
	weights = y1)


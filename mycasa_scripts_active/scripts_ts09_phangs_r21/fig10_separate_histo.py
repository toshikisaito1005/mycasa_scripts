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
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
gals = ["ngc0628","ngc3627","ngc4321"]
dist25 = [4.9, 5.1, 3.0] # arcmin, Leroy et al. 2019
scales = [44/1.0, 52/1.3, 103/1.4]
bins = 30
percents = [0.15,0.025,0.010]

#####################
### functions
#####################
def hist_percent(histo,percent):
    dat_sum = np.sum(histo)
    dat_sum_from_zero,i = 0,0
    while dat_sum_from_zero < dat_sum * percent:
        dat_sum_from_zero += histo[i]
        i += 1
    
    return i

def plotter(dir_product,galname,parameter,output,xlim,ylim,xlabel):
    histo = np.histogram(parameter,bins=bins,range=(xlim),weights=None)
    histox,histoy = np.delete(histo[1],-1),histo[0]
    y = histoy/float(sum(histoy))
    # high
    histo_h = np.histogram(parameter[r21mask==1],bins=bins,range=(xlim),weights=None)
    histo_hx,histo_hy = np.delete(histo_h[1],-1),histo_h[0]
    yh = histo_hy/float(sum(histoy))
    # low
    histo_l = np.histogram(parameter[r21mask==-1],bins=bins,range=(xlim),weights=None)
    histo_lx,histo_ly = np.delete(histo_l[1],-1),histo_l[0]
    yl = histo_ly/float(sum(histoy))
    #
    figure = plt.figure(figsize=(10,3))
    plt.subplots_adjust(left=0.10, right=0.95, bottom=0.20, top=0.95)
    plt.rcParams["font.size"] = 16
    plt.grid(axis = "x")
    plt.plot(histo_hx,yh,"red",lw=4,alpha=0.5)
    plt.plot(histo_lx,yl,"blue",lw=4,alpha=0.5)
    plt.plot(histox,y,"black",lw=7,alpha=0.5)
    #
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(xlabel)
    plt.savefig(dir_product+"fig10_"+galname+"_"+output+".png",dpi=200)


#####################
### main
#####################

for i in range(len(gals)):
    galname = gals[i]
    data = np.loadtxt(dir_data + galname + "_parameter_600pc.txt")
      # galactocentric distance
    distance = data[:,0] # pc
    dist25_pc = dist25[i] * 60 * scales[i]
    galdist = distance / dist25_pc
    # median-subtracted r21
    r21 = data[:,1]
    med_r21 = np.median(r21[r21>0])
    norm_r21 = r21 / med_r21
    # co21
    co21 = data[:,4]
    co21snr = data[:,5]
    tpeak = data[:,6]
    disp = data[:,7]
    # wise
    wise1 = data[:,8]
    wise2 = data[:,9]
    wise3 = data[:,10]
    # r21 mask
    r21mask = data[:,11]

    # cut data
    cut_r21 = (r21 > 0)
    cut_co21 = (co21 > co21.max() * percents[i])
    cut_all = np.where((cut_r21) & (cut_co21))

    galdist = galdist[cut_all]
    r21mask = r21mask[cut_all]
    norm_r21 = norm_r21[cut_all]
    co21 = co21[cut_all]
    tpeak = tpeak[cut_all]
    disp = disp[cut_all]
    wise1 = wise1[cut_all]
    wise2 = wise2[cut_all]
    wise3 = wise3[cut_all]

    # plot; r/r25
    parameter = galdist
    output = "dist"
    xlim = [0,1]
    ylim = [0,0.15]
    xlabel = "r/r25"
    plotter(dir_product,galname,parameter,output,xlim,ylim,xlabel)

    # plot; co21 mom0
    parameter = np.log10(co21)
    output = "co21_mom0"
    xlim = [0.1,2.7]
    ylim = [0,0.17]
    xlabel = "log $I_{CO(2-1)}$ (currently Jy/b)"
    plotter(dir_product,galname,parameter,output,xlim,ylim,xlabel)

    # plot; co21 tpeak
    parameter = np.log10(tpeak)
    output = "co21_tpeak"
    xlim = [-1.0,1.2]
    ylim = [0,0.20]
    xlabel = "log $T_{CO(2-1)}$ (currently Jy/b)"
    plotter(dir_product,galname,parameter,output,xlim,ylim,xlabel)

    # plot; co21 disp
    parameter = np.log10(disp)
    output = "co21_disp"
    xlim = [0.0,2.0]
    ylim = [0,0.35]
    xlabel = "log $\sigma_{CO(2-1)}$ (km s$^{-1}$)"
    plotter(dir_product,galname,parameter,output,xlim,ylim,xlabel)

    # plot; wise3
    parameter = np.log10(wise3)
    output = "wise3"
    xlim = [-3.5,0.0]
    ylim = [0,0.28]
    xlabel = "log WISE3 (Jy/b)"
    plotter(dir_product,galname,parameter,output,xlim,ylim,xlabel)


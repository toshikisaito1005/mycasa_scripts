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
dir_data = "/Users/saito/data/phangs_ulirg/"
gals = ["ngc1614", # z = 0.01594
        "ngc3110", # z = 0.01686
        "ngc6240", # z = 0.02448
        "ngc3256", # z = 0.00935
        "irasf13373a", # ngc 5258, z = 0.02254
        "irasf13373b", # ngc 5257, z = 0.02268
        "iras13120"] # z = 0.03076
beams = [round(120/305.,2), # 120 pc resolution
         round(120/326.,2), # 120 pc resolution
         round(120/483.,2), # 120 pc resolution
         round(120/184.,2), # 120 pc resolution
         round(120/444.,2), # 120 pc resolution
         round(120/444.,2), # 120 pc resolution
         round(120/600.,2)] # 120 pc resolution
scales = [305., 326., 483., 184., 444., 444., 600.]
chanss = ["10~62", "5~58", "15~168", "85~165", "5~60", "10~65", "15~89"]
DLs = [65.0, 69.4, 104.7, 38.8, 95.9, 95.9, 131.5]
zs = [0.01594, 0.01686, 0.02448, 0.00935, 0.02254, 0.02268, 0.03076]
snr_mom = 3.
aco = 0.8

bins=60
step=0.03
xlim = [0,3]
ylim = [0,1.5]


#####################
### functions
#####################
def func1(x, a, b, c):
    return a*np.exp(-(x-b)**2/(2*c**2))

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

def hist_percent(histo,percent):
    dat_sum = np.sum(histo)
    dat_sum_from_zero,i = 0,0
    while dat_sum_from_zero < dat_sum * percent:
        dat_sum_from_zero += histo[i]
        i += 1
    
    return i

def ch_noise(image_cube,chans):
    ch_line_start = int(chans.split("~")[0])
    ch_line_end = int(chans.split("~")[1])
    size_cube = imhead(image_cube)["shape"][3]
    
    if int(ch_line_start)-1 > 0:
        ch_noise_1 = "0~"+str(ch_line_start-1)
    else:
        ch_noise_1 = ""
    
    if ch_line_end+1 < size_cube-1:
        ch_noise_2 = str(ch_line_end+1)+"~"+str(size_cube-1)
    else:
        ch_noise_2 = ""

    ch_noise = ",".join([ch_noise_1, ch_noise_2]).rstrip(",")

    return ch_noise

def beam_area(imagename):
    """
    for moment map creation
    """
    major = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beammajor")["value"]
    minor = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beamminor")["value"]
    pix = abs(imhead(imagename = imagename,
                     mode = "list")["cdelt1"])
                   
    pixelsize = pix * 3600 * 180 / np.pi
    beamarea_arcsec = major * minor * np.pi/(4 * np.log(2))
    beamarea_pix = beamarea_arcsec / (pixelsize ** 2)

    return beamarea_pix, pixelsize

#####################
### Main Procedure
#####################
for i in [0,1,2,3,4,5,6]:
    beam = str(beams[i]).replace(".","p")
    name_title = gals[i].replace("ngc","NGC ")
    image_co21 = dir_data+gals[i]+"/"+gals[i]+"_co21_"+beam+".moment2"
    image_r = imhead(image_co21,mode="list")["shape"][0] - 1
    image_t = imhead(image_co21,mode="list")["shape"][1] - 1

    value = imval(image_co21,box="0,0,"+str(image_r)+","+str(image_t))
    value_co21 = value["data"] * value["mask"]
    value_co21_1d = value_co21.flatten()

    disp = value_co21_1d[value_co21_1d>10.]

    # plot
    plt.figure(figsize=(15,11))
    plt.rcParams["font.size"] = 20
    plt.subplots_adjust(bottom=0.15, wspace=0.05)
    
    hist=plt.hist(np.log10(disp),
                  normed=True,
                  bins=bins,
                  range=xlim,
                  lw=0,
                  color="pink")

    plt.xlim(xlim)
    plt.ylim([0,hist[0].max()*1.3])
    plt.savefig(dir_data+"eps/hist_disp_"+gals[i]+".png",dpi=100)


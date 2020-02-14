import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
import scipy.stats as stats
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
dir_eps="/Users/saito/data/phangs/co_ratio/eps/"
dir_data = "/Users/saito/data/phangs/co_ratio/ngc4321_co/"
gal = "ngc4321"
scale = 103/1.4/1000. #kpc/arcsec 4321
ra_cnt = 185.729
dec_cnt = 15.8223
pa = 180-157.8
inc = 90-35.1
size = 0.03
apr = [100.,385.,870.,1550.,2400.,870.]
vmin=0.0
vmax=0.8
txtfiles = [dir_data+gal+"_flux_4p0_4p0_no.txt",
            dir_data+gal+"_flux_8p0_8p0_no.txt",
            dir_data+gal+"_flux_12p0_12p0_no.txt",
            dir_data+gal+"_flux_16p0_16p0_no.txt",
            dir_data+gal+"_flux_20p0_20p0_no.txt",
            dir_data+gal+"_flux_24p0_24p0_no.txt"]

#####################
### functions
#####################
def hex_map(size,scale,ra_cnt,dec_cnt,apr,txtfile,dir_eps):
    data = np.loadtxt(txtfile)
    y = data[:,3] / data[:,2] / 4.
    for i in range(len(y)):
        if data[:,2][i]==0:
            y[i] = 0

    ### plot
    # setup
    plt.figure(figsize=(8,8))
    plt.rcParams["font.size"] = 18
    plt.xlim([1*size*scale*3600, -1*size*scale*3600])
    plt.ylim([-1*size*scale*3600, 1*size*scale*3600])
    x_ra = data[:,0]-ra_cnt
    y_dec = data[:,1]-dec_cnt
    c_val = y
    plt.scatter(x_ra*scale*3600,
                y_dec*scale*3600,
                s = apr,
                c = c_val,
                lw = 0,
                vmin = vmin,
                vmax=  vmax,
                cmap = "rainbow",
                marker = "h",
                alpha=1.0)

    plt.xlabel("x-offset (kpc)")
    plt.ylabel("y-offset (kpc)")
    plt.savefig(dir_eps+txtfile.split("/")[-1].replace(".txt",".png"),
                dpi=200)


#####################
### Main Procedure
#####################
for i in range(len(txtfiles)):
    hex_map(size,scale,ra_cnt,dec_cnt,apr[i],txtfiles[i],dir_eps)


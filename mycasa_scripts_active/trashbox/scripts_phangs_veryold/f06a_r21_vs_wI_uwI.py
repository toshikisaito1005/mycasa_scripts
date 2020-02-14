import glob
import numpy as np
import math
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.gridspec as gridspec
import scipy.optimize
from scipy.optimize import curve_fit
plt.ioff()


#####################
### Define Functions
#####################
def load_data(txt_data):
    ap_size = int(txt_data.split("4p0_")[1].split(".txt")[0])
    bm_size = float(txt_data.split("p")[-2].split("_")[-1])
    beta10 = 1.222 * 10**6 / bm_size**2 / 115.27120**2
    beta21 = 1.222 * 10**6 / bm_size**2 / 230.53800**2
    
    data = np.loadtxt(txt_data, usecols=(2,3,6,7))
    x = np.log10(data[:,0] * beta10) # co10_m0
    y = np.log10(data[:,1] * beta21) # co21_m0
    
    data_w = np.loadtxt(txt_data, usecols=(8,9,12,13))
    x_w = np.log10(data_w[:,0] * beta10) # co10_m0 w
    y_w = np.log10(data_w[:,1] * beta21) # co21_m0 w
    
    data_w = np.loadtxt(txt_data, usecols=(14,15,18,19))
    x_iw = np.log10(data_w[:,0] * beta10) # co10_m0
    y_iw = np.log10(data_w[:,1] * beta21) # co21_m0
    
    for i in range(len(x)):
        if x[j] == 0:
            x[j], y[j] == 0, 0
            x_w[j], y_w[j] == 0, 0
            x_iw[j], y_iw[j] == 0, 0

    return x, y, x_w, y_w, x_iw, y_iw


#####################
### Main Procedure
#####################
### ngc4321
scale = 103/1.4/1000. #kpc/arcsec
dir_data = "/Users/saito/data/phangs/co_ratio/ngc4321/"
txt_files = glob.glob(dir_data + "ngc4321*4p0_04.txt")

x, y, x_w, y_w, x_iw, y_iw = load_data(txt_files[0])

# plot
plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 18

plt.scatter(10**y_w,
            10**y/10**x,
            s=50,
            linewidth=0,
            c=10**y,
            cmap="rainbow",
            marker="o",
            alpha=0.7)

#plt.xlim([1,2])
#plt.ylim([0.1,1.0])
#plt.clim([0.4,0.65])
#plt.xscale("log")
#plt.yscale("log")
plt.xlabel("log $I_{CO(1-0),w}$/$I_{CO(1-0),1/w}$")
plt.ylabel("$R_{21}$")
#plt.text(1*scale + (35*scale-1*scale)*0.05,
#         35*scale - (35*scale-1*scale)*0.08,
#         "(b) median $M_{21}$, $Me$($M_{21}$)")
#cbar=plt.colorbar()
#cbar.set_label("$Me$($M_{21}$)", size=18)
plt.savefig("/Users/saito/data/phangs/co_ratio/eps/f06a_r21_vs_wI_uwI_n4321.png",
            dpi=100)



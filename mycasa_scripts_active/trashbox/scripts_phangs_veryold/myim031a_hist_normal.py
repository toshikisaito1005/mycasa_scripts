import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
sys.path.append(os.getcwd() + "/../")
#import mycasaimaging_tools as myim
import scipy.optimize
from scipy.optimize import curve_fit
plt.ioff()

#####################
### Define Functions
#####################
def gauss_function(x, a, x0, sigma):
    return a*np.exp(-(x-x0)**2/(2*sigma**2))

def txt2ratio(txtfile,coeff):
    data = np.loadtxt(txtfile, usecols=(0,1,6,7))
    ratio_tmp = data[:,3] / data[:,2] / coeff
    ratio = []
    for j in range(len(ratio_tmp)):
        if data[:,2][j] > 0:
            if data[:,3][j] > 0:
                if ratio_tmp[j] < 2.5:
                    ratio.append(ratio_tmp[j])
    return ratio

def hist2eps(ratio,txtfile,txtsplit,histobin):
    plt.figure(figsize=(8,8))
    plt.rcParams["font.size"] = 16
    plt.subplots_adjust(bottom = 0.15)
    plt.xlabel("$R_{2-1/1-0}$")
    plt.ylabel("Count")
    plt.xlim([0,1])
    bins_tmp = txtfile.split(txtsplit)[1]
    bins_tmp2 = int(bins_tmp.replace(".txt", ""))
    bins = round(histobin / bins_tmp2, -1)
    histo = plt.hist(ratio,
                     bins=bins,
                     histtype="stepfilled",
                     alpha = 0.4,
                     color = "cornflowerblue")
    popt, pcov = curve_fit(gauss_function,
                           histo[1][2:],
                           histo[0][1:],
                           p0 = [150, 0.5, 0.1],
                           maxfev = 100000)
    x = np.linspace(histo[1][1], histo[1][-1], 50)
    plt.plot(x, gauss_function(x, *popt),
             "-", c="lightcoral", lw=4,
             label="$\mu$ = "+str(round(popt[1], 2))\
             +", $\sigma$ = "+str(round(popt[2], 2)))
    ratio_value = round(popt[1], 2)
    ratio_disp = round(popt[2], 2)
    plt.legend()
    plt.savefig(txtfile.replace("txt", "eps"), dpi = 30)
    return ratio_value, ratio_disp

def easy_zip(a1, a2):
    y1_in = [x+y for (x,y) in zip(a1, np.abs(a2))]
    y2_in = [x-y for (x,y) in zip(a1, np.abs(a2))]
    return y1_in, y2_in

#####################
### Main Procedure
#####################
### ngc0628
histobin = 300
scale = 0.047
dir_data = "../../phangs/co_ratio/ngc0628/"
txtfiles = glob.glob(dir_data + "*_flux_4p0_*.txt")
ratio_value_n0628 = []
ratio_disp_n0628 = []
ratio_disp_n0628 = []
aperture_size_kpc_n0628 = []

for i in range(len(txtfiles)):
    # data
    ratio = txt2ratio(txtfile=txtfiles[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles[i],
                   txtsplit="ngc0628_flux_4p0_",
                   histobin=histobin)
    ratio_value_n0628.append(ratio_value)
    ratio_disp_n0628.append(ratio_disp)
               
    # aperture size in kpc
    aperture_txt = txtfiles[i].split("flux_4p0_")[1].split(".txt")[0]
    aperture_size_kpc_n0628.append(int(aperture_txt)*scale)

y1_n0628, y2_n0628 = easy_zip(ratio_value_n0628,
                              ratio_disp_n0628)


### ngc4321
histobin = 300
scale = 0.103
dir_data = "../../phangs/co_ratio/ngc4321/"
txtfiles = glob.glob(dir_data + "*_flux_4p0_*.txt")
ratio_value_n4321 = []
ratio_disp_n4321 = []
ratio_disp_n4321 = []
aperture_size_kpc_n4321 = []

for i in range(len(txtfiles)):
    # data
    ratio = txt2ratio(txtfile=txtfiles[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles[i],
                   txtsplit="ngc4321_flux_4p0_",
                   histobin=histobin)
    ratio_value_n4321.append(ratio_value)
    ratio_disp_n4321.append(ratio_disp)

    # aperture size in kpc
    aperture_txt = txtfiles[i].split("flux_4p0_")[1].split(".txt")[0]
    aperture_size_kpc_n4321.append(int(aperture_txt)*scale)

y1_n4321, y2_n4321 = easy_zip(ratio_value_n4321,
                              ratio_disp_n4321)


### ngc3627
histobin = 200
scale = 0.040
dir_data = "../../phangs/co_ratio/ngc3627/"
txtfiles = glob.glob(dir_data + "*_flux_8p0_*.txt")
ratio_value_n3627 = []
ratio_disp_n3627 = []
ratio_disp_n3627 = []
aperture_size_kpc_n3627 = []

for i in range(len(txtfiles)):
    # data
    ratio = txt2ratio(txtfile=txtfiles[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles[i],
                   txtsplit="ngc3627_flux_8p0_",
                   histobin=histobin)
    ratio_value_n3627.append(ratio_value)
    ratio_disp_n3627.append(ratio_disp)

    # aperture size in kpc
    aperture_txt = txtfiles[i].split("flux_8p0_")[1].split(".txt")[0]
    aperture_size_kpc_n3627.append(int(aperture_txt)*scale)

y1_n3627, y2_n3627 = easy_zip(ratio_value_n3627,
                              ratio_disp_n3627)


### ngc4254
histobin = 500
scale = 0.081
dir_data = "../../phangs/co_ratio/ngc4254/"
txtfiles = glob.glob(dir_data + "*_flux_8p0_*.txt")
ratio_value_n4254 = []
ratio_disp_n4254 = []
ratio_disp_n4254 = []
aperture_size_kpc_n4254 = []

for i in range(len(txtfiles)):
    # data
    ratio = txt2ratio(txtfile=txtfiles[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles[i],
                   txtsplit="ngc4254_flux_8p0_",
                   histobin=histobin)
    ratio_value_n4254.append(ratio_value)
    ratio_disp_n4254.append(ratio_disp)

    # aperture size in kpc
    aperture_txt = txtfiles[i].split("flux_8p0_")[1].split(".txt")[0]
    aperture_size_kpc_n4254.append(int(aperture_txt)*scale)

y1_n4254, y2_n4254 = easy_zip(ratio_value_n4254,
                              ratio_disp_n4254)



### ngc3110
histobin = 200
scale = 0.325
dir_data = "../../phangs/co_ratio/ngc3110/"
txtfiles = glob.glob(dir_data + "*_flux_2p0_*.txt")
ratio_value_n3110 = []
ratio_disp_n3110 = []
ratio_disp_n3110 = []
aperture_size_kpc_n3110 = []

for i in range(len(txtfiles)):
    # data
    ratio = txt2ratio(txtfile=txtfiles[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles[i],
                   txtsplit="ngc3110_flux_2p0_",
                   histobin=histobin)
    ratio_value_n3110.append(ratio_value)
    ratio_disp_n3110.append(ratio_disp)

    # aperture size in kpc
    aperture_txt = txtfiles[i].split("flux_2p0_")[1].split(".txt")[0]
    aperture_size_kpc_n3110.append(int(aperture_txt)*scale)

y1_n3110, y2_n3110 = easy_zip(ratio_value_n3110,
                              ratio_disp_n3110)



#
xlim = [0.0,2.0]
ylim = [0.1,1.4]
plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 14
plt.ylabel("$R_{2-1/1-0}$")
plt.xlabel("Aperture Size (kpc)")
plt.xlim(xlim)
plt.ylim(ylim)
#
label_1 = str(np.round(np.mean(ratio_value_n0628), 2))
label_2 = np.round(np.mean(y1_n0628) \
                   - np.mean(ratio_value_n0628), 2)
label_3 = np.round(np.mean(ratio_value_n0628) \
                   - np.mean(y2_n0628), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
          + " (NGC 0628)"
label_n0628 = label_1 + "$\pm$" + label_4
#
label_1 = str(np.round(np.mean(ratio_value_n4321), 2))
label_2 = np.round(np.mean(y1_n4321) \
                   - np.mean(ratio_value_n4321), 2)
label_3 = np.round(np.mean(ratio_value_n4321) \
                   - np.mean(y2_n4321), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
          + " (NGC 4321)"
label_n4321 = label_1 + "$\pm$" + label_4
#
label_1 = str(np.round(np.mean(ratio_value_n3627), 2))
label_2 = np.round(np.mean(y1_n3627) \
                   - np.mean(ratio_value_n3627), 2)
label_3 = np.round(np.mean(ratio_value_n3627) \
                   - np.mean(y2_n3627), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
          + " (NGC 3627)"
label_n3627 = label_1 + "$\pm$" + label_4
#
label_1 = str(np.round(np.mean(ratio_value_n4254), 2))
label_2 = np.round(np.mean(y1_n4254) \
                   - np.mean(ratio_value_n4254), 2)
label_3 = np.round(np.mean(ratio_value_n4254) \
                   - np.mean(y2_n4254), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 4254)"
label_n4254 = label_1 + "$\pm$" + label_4
#
label_1 = str(np.round(np.mean(ratio_value_n3110), 2))
label_2 = np.round(np.mean(y1_n3110) \
                   - np.mean(ratio_value_n3110), 2)
label_3 = np.round(np.mean(ratio_value_n3110) \
                   - np.mean(y2_n3110), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 3110)"
label_n3110 = label_1 + "$\pm$" + label_4
#
plt.plot(aperture_size_kpc_n3110,
         ratio_value_n3110,
         c="purple",
         lw=4,
         label = label_n3110)
plt.fill_between(aperture_size_kpc_n3110,
                 y2_n3110,
                 y1_n3110,
                 facecolor="purple",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n3110), 2),
          np.round(np.mean(ratio_value_n3110), 2)],
         linestyle="dashed",
         lw=2,
         c="purple")
#
plt.plot(aperture_size_kpc_n3627,
         ratio_value_n3627,
         c="seagreen",
         lw=4,
         label = label_n3627)
plt.fill_between(aperture_size_kpc_n3627,
                 y2_n3627,
                 y1_n3627,
                 facecolor="seagreen",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n3627), 2),
          np.round(np.mean(ratio_value_n3627), 2)],
         linestyle="dashed",
         lw=2,
         c="seagreen")
#
plt.plot(aperture_size_kpc_n4254,
         ratio_value_n4254,
         c="black",
         lw=4,
         label = label_n4254)
plt.fill_between(aperture_size_kpc_n4254,
                 y2_n4254,
                 y1_n4254,
                 facecolor="black",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n4254), 2),
          np.round(np.mean(ratio_value_n4254), 2)],
         linestyle="dashed",
         lw=2,
         c="black")
#
plt.plot(aperture_size_kpc_n0628,
         ratio_value_n0628,
         c="cornflowerblue",
         lw=4,
         label = label_n0628)
plt.fill_between(aperture_size_kpc_n0628,
                 y2_n0628,
                 y1_n0628,
                 facecolor="cornflowerblue",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n0628), 2),
          np.round(np.mean(ratio_value_n0628), 2)],
         linestyle="dashed",
         lw=2,
         c="blue")
#
plt.plot(aperture_size_kpc_n4321,
         ratio_value_n4321,
         c="salmon",
         lw=4,
         label = label_n4321)
plt.fill_between(aperture_size_kpc_n4321,
                 y2_n4321,
                 y1_n4321,
                 facecolor="salmon",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n4321), 2),
          np.round(np.mean(ratio_value_n4321), 2)],
         linestyle="dashed",
         lw=2,
         c="red")
#
plt.legend(loc="upper left")
plt.savefig("../../phangs/co_ratio/eps/ratio_aperture.png", dpi = 300)



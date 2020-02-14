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
    data = np.loadtxt(txtfile, usecols=(0,1,2,3))
    ratio_tmp = data[:,3] / data[:,2] / coeff
    ratio = []
    for j in range(len(ratio_tmp)):
        if data[:,2][j] > 0:
            if data[:,3][j] > 0:
                if ratio_tmp[j] < 2.5:
                    ratio.append(ratio_tmp[j])
    return ratio

def hist2eps(ratio,txtfile,txtsplit,histobin):
    plt.figure()
    plt.rcParams["font.size"] = 16
    plt.subplots_adjust(bottom = 0.15)
    plt.xlabel("$R_{2-1/1-0}$")
    plt.ylabel("Count")
    plt.xlim([0,2])
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

def easy_zip(a1, a2, b1, b2):
    y1_in = [x+y for (x,y) in zip(a1, np.abs(a2))]
    y2_in = [x-y for (x,y) in zip(a1, np.abs(a2))]
    y1_out = [x+y for (x,y) in zip(b1, np.abs(b2))]
    y2_out = [x-y for (x,y) in zip(b1, np.abs(b2))]
    return y1_in, y2_in, y1_out, y2_out

#####################
### main procedure
#####################
### ngc4321
histobin = 500
scale = 0.103
dir_data = "../../phangs/co_ratio/ngc4321/"
txtfiles_in = glob.glob(dir_data + "*_fluxin_*.txt")
txtfiles_out = glob.glob(dir_data + "*_fluxout_*.txt")
ratio_value_n4321_in = []
ratio_value_n4321_out = []
ratio_disp_n4321_in = []
ratio_disp_n4321_out = []
aperture_size_kpc_n4321 = []

for i in range(len(txtfiles_in)):
    # data inside mask
    ratio = txt2ratio(txtfile=txtfiles_in[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles_in[i],
                   txtsplit="ngc4321_fluxin_Halpha_",
                   histobin=histobin)
    ratio_value_n4321_in.append(ratio_value)
    ratio_disp_n4321_in.append(ratio_disp)

    # data outside mask
    ratio = txt2ratio(txtfile=txtfiles_out[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles_out[i],
                   txtsplit="ngc4321_fluxout_Halpha_",
                   histobin=histobin)
    ratio_value_n4321_out.append(ratio_value)
    ratio_disp_n4321_out.append(ratio_disp)
    # aperture size in kpc
    aperture_txt = txtfiles_in[i].split("fluxin_Halpha_")[1].split(".txt")[0]
    aperture_size_kpc_n4321.append(int(aperture_txt)*scale)

y1_n4321_in, y2_n4321_in, y1_n4321_out, y2_n4321_out \
    = easy_zip(ratio_value_n4321_in,
               ratio_disp_n4321_in,
               ratio_value_n4321_out,
               ratio_disp_n4321_out)

### ngc0628
histobin = 500
scale = 0.047
dir_data = "../../phangs/co_ratio/ngc0628/"
txtfiles_in = glob.glob(dir_data + "*_fluxin_*.txt")
txtfiles_out = glob.glob(dir_data + "*_fluxout_*.txt")
ratio_value_n0628_in = []
ratio_value_n0628_out = []
ratio_disp_n0628_in = []
ratio_disp_n0628_out = []
aperture_size_kpc_n0628 = []

for i in range(len(txtfiles_in)):
    # data inside mask
    ratio = txt2ratio(txtfile=txtfiles_in[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles_in[i],
                   txtsplit="ngc0628_fluxin_Halpha_",
                   histobin=histobin)
    ratio_value_n0628_in.append(ratio_value)
    ratio_disp_n0628_in.append(ratio_disp)

    # data outside mask
    ratio = txt2ratio(txtfile=txtfiles_out[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles_out[i],
                   txtsplit="ngc0628_fluxout_Halpha_",
                   histobin=histobin)
    ratio_value_n0628_out.append(ratio_value)
    ratio_disp_n0628_out.append(ratio_disp)
    # aperture size in kpc
    aperture_txt = txtfiles_in[i].split("fluxin_Halpha_")[1].split(".txt")[0]
    aperture_size_kpc_n0628.append(int(aperture_txt)*scale)

    y1_n0628_in, y2_n0628_in, y1_n0628_out, y2_n0628_out \
        = easy_zip(ratio_value_n0628_in,
                   ratio_disp_n0628_in,
                   ratio_value_n0628_out,
                   ratio_disp_n0628_out)


### ngc3627
histobin = 300
scale = 0.040
dir_data = "../../phangs/co_ratio/ngc3627/"
txtfiles_in = glob.glob(dir_data + "*_fluxin_*.txt")
txtfiles_out = glob.glob(dir_data + "*_fluxout_*.txt")
ratio_value_n3627_in = []
ratio_value_n3627_out = []
ratio_disp_n3627_in = []
ratio_disp_n3627_out = []
aperture_size_kpc_n3627 = []

for i in range(len(txtfiles_in)):
    # data inside mask
    ratio = txt2ratio(txtfile=txtfiles_in[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles_in[i],
                   txtsplit="ngc3627_fluxin_Halpha_",
                   histobin=histobin)
    ratio_value_n3627_in.append(ratio_value)
    ratio_disp_n3627_in.append(ratio_disp)

    # data outside mask
    ratio = txt2ratio(txtfile=txtfiles_out[i],coeff=4.)
    ratio_value, ratio_disp \
        = hist2eps(ratio=ratio,
                   txtfile=txtfiles_out[i],
                   txtsplit="ngc3627_fluxout_Halpha_",
                   histobin=histobin)
    ratio_value_n3627_out.append(ratio_value)
    ratio_disp_n3627_out.append(ratio_disp)
    # aperture size in kpc
    aperture_txt = txtfiles_in[i].split("fluxin_Halpha_")[1].split(".txt")[0]
    aperture_size_kpc_n3627.append(int(aperture_txt)*scale)
               
    y1_n3627_in, y2_n3627_in, y1_n3627_out, y2_n3627_out \
        = easy_zip(ratio_value_n3627_in,
                   ratio_disp_n3627_in,
                   ratio_value_n3627_out,
                   ratio_disp_n3627_out)



#####################
### data to eps
#####################

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
label_1 = "$\mu$ = " \
    + str(np.round(np.mean(ratio_value_n4321_in), 2))
label_2 = np.round(np.mean(y1_n4321_in) \
                   - np.mean(ratio_value_n4321_in), 2)
label_3 = np.round(np.mean(ratio_value_n4321_in) \
                   - np.mean(y2_n4321_in), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 4321)"
label_n4321 = label_1 + ", $\sigma$ = " + label_4
#
plt.plot(aperture_size_kpc_n4321,
         ratio_value_n4321_in,
         c="salmon",
         lw=4,
         label = label_n4321)
plt.fill_between(aperture_size_kpc_n4321,
                 y1_n4321_in,
                 y2_n4321_in,
                 facecolor="salmon",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n4321_in), 2),
          np.round(np.mean(ratio_value_n4321_in), 2)],
         linestyle="dashed",
         lw=2,
         c="red")
#
label_1 = "$\mu$ = " \
    + str(np.round(np.mean(ratio_value_n0628_in), 2))
label_2 = np.round(np.mean(y1_n0628_in) \
                   - np.mean(ratio_value_n0628_in), 2)
label_3 = np.round(np.mean(ratio_value_n0628_in) \
                   - np.mean(y2_n0628_in), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 0628)"
label_n0628 = label_1 + ", $\sigma$ = " + label_4
#
plt.plot(aperture_size_kpc_n0628,
         ratio_value_n0628_in,
         c="cornflowerblue",
         lw=4,
         label = label_n0628)
plt.fill_between(aperture_size_kpc_n0628,
                 y1_n0628_in,
                 y2_n0628_in,
                 facecolor="cornflowerblue",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n0628_in), 2),
          np.round(np.mean(ratio_value_n0628_in), 2)],
         linestyle="dashed",
         lw=2,
         c="blue")
#
label_1 = "$\mu$ = " \
    + str(np.round(np.mean(ratio_value_n3627_in), 2))
label_2 = np.round(np.mean(y1_n3627_in) \
                   - np.mean(ratio_value_n3627_in), 2)
label_3 = np.round(np.mean(ratio_value_n3627_in) \
                   - np.mean(y2_n3627_in), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 3627)"
label_n3627 = label_1 + ", $\sigma$ = " + label_4
#
plt.plot(aperture_size_kpc_n3627,
         ratio_value_n3627_in,
         c="seagreen",
         lw=4,
         label = label_n3627)
plt.fill_between(aperture_size_kpc_n3627,
                 y1_n3627_in,
                 y2_n3627_in,
                 facecolor="seagreen",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n3627_in), 2),
          np.round(np.mean(ratio_value_n3627_in), 2)],
         linestyle="dashed",
         lw=2,
         c="seagreen")
#
plt.legend(loc="upper left")
plt.savefig(dir_data + "../eps/ratio_aperture_galmask_in.png",
            dpi = 300)




#
plt.figure(figsize=(8,8))
plt.rcParams["font.size"] = 14
plt.ylabel("$R_{2-1/1-0}$")
plt.xlabel("Aperture Size (kpc)")
plt.xlim(xlim)
plt.ylim(ylim)
#
label_1 = "$\mu$ = " \
    + str(np.round(np.mean(ratio_value_n4321_out), 2))
label_2 = np.round(np.mean(y1_n4321_out) \
                   - np.mean(ratio_value_n4321_out), 2)
label_3 = np.round(np.mean(ratio_value_n4321_out) \
                   - np.mean(y2_n4321_out), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 4321)"
label_n4321 = label_1 + ", $\sigma$ = " + label_4
#
plt.plot(aperture_size_kpc_n4321,
         ratio_value_n4321_out,
         c="salmon",
         lw=4,
         label = label_n4321)
plt.fill_between(aperture_size_kpc_n4321,
                 y1_n4321_out,
                 y2_n4321_out,
                 facecolor="salmon",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n4321_out), 2),
          np.round(np.mean(ratio_value_n4321_out), 2)],
         linestyle="dashed",
         lw=2,
         c="red")
#
label_1 = "$\mu$ = " \
    + str(np.round(np.mean(ratio_value_n0628_out), 2))
label_2 = np.round(np.mean(y1_n0628_out) \
                   - np.mean(ratio_value_n0628_out), 2)
label_3 = np.round(np.mean(ratio_value_n0628_out) \
                   - np.mean(y2_n0628_out), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 0628)"
label_n0628 = label_1 + ", $\sigma$ = " + label_4
#
plt.plot(aperture_size_kpc_n0628,
         ratio_value_n0628_out,
         c="cornflowerblue",
         lw=4,
         label = label_n0628)
plt.fill_between(aperture_size_kpc_n0628,
                 y1_n0628_out,
                 y2_n0628_out,
                 facecolor="cornflowerblue",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n0628_out), 2),
          np.round(np.mean(ratio_value_n0628_out), 2)],
         linestyle="dashed",
         lw=2,
         c="blue")
#
label_1 = "$\mu$ = " \
    + str(np.round(np.mean(ratio_value_n3627_out), 2))
label_2 = np.round(np.mean(y1_n3627_out) \
                   - np.mean(ratio_value_n3627_out), 2)
label_3 = np.round(np.mean(ratio_value_n3627_out) \
                   - np.mean(y2_n3627_out), 2)
label_4 = str(round(label_2/2. + label_3/2., 2)) \
    + " (NGC 3627)"
label_n3627 = label_1 + ", $\sigma$ = " + label_4
#
plt.plot(aperture_size_kpc_n3627,
         ratio_value_n3627_out,
         c="seagreen",
         lw=4,
         label = label_n3627)
plt.fill_between(aperture_size_kpc_n3627,
                 y1_n3627_out,
                 y2_n3627_out,
                 facecolor="seagreen",
                 alpha=0.4,
                 lw=0)
plt.plot(xlim,
         [np.round(np.mean(ratio_value_n3627_out), 2),
          np.round(np.mean(ratio_value_n3627_out), 2)],
         linestyle="dashed",
         lw=2,
         c="seagreen")
#
plt.legend(loc="upper left")
plt.savefig("../../phangs/co_ratio/eps/ratio_aperture_galmask_out.png",
            dpi = 300)



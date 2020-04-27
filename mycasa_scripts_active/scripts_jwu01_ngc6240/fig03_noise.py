import os
import glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.ioff()

imageco10 = "co10_cube.image"
imageco21 = "co21_cube.image"

### set signal-to-noise ratio you want to use
snr_mom = 3.0

##################################################
### define some functions
##################################################
def func1(x, a, c):
    return a * np.exp(-(x)**2/(2*c**2))

def noisehist(
    imagename,
    noises_byeye,
    output,
    snr,
    title,
    bins=200,
    thres=0.00001,
    logscale=True,
    plotter=True,
    ):
    """
    """
    ### get pixel values from a datacube
    shape = imhead(imagename, mode="list")["shape"]
    box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
    data = imval(imagename, box=box)
    pixvalues = data["data"].flatten()
    pixvalues = pixvalues[abs(pixvalues)>thres]
    ### plot
    # get plot range
    histrange = [pixvalues.min()/1.5 - 0.02, -pixvalues.min()/1.5 + 0.02]
    # prepare for plot
    plt.figure(figsize=(10,10))
    plt.rcParams["font.size"] = 22
    plt.subplots_adjust(bottom=0.08, left=0.10, right=0.99, top=0.95)
    # plot
    histdata = \
        plt.hist(pixvalues,
                 bins=bins,
                 range=histrange,
                 lw=0,
                 log=logscale,
                 color="blue",
                 alpha=0.3,
                 label="positive pixels")
    plt.hist(pixvalues * -1,
             bins=bins,
             range=histrange,
             lw=0,
             log=logscale,
             color="red",
             alpha=0.3,
             label="negative pixels (reversed)")
    # fit the histogram using a Gaussian
    popt, pcov = \
        curve_fit(
            func1,
            histdata[1][2:][histdata[1][2:]<noises_byeye],
            histdata[0][1:][histdata[1][2:]<noises_byeye],
            p0 = [np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]),
                  noises_byeye],
            maxfev = 10000)
    #
    x = np.linspace(histdata[1][1], histdata[1][-1], 200)
    plt.plot(x, func1(x, popt[0], popt[1]), '-', c="black", lw=5)
    plt.plot([0, 0],
             [2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2],
             "-",
             color="black",
             lw=2)
    plt.plot([popt[1], popt[1]],
             [2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2],
             "--",
             color="black",
             lw=2,
             label="1.0 sigma = " + str(np.round(popt[1]*1000.,2)) + " mJy beam$^{-1}$")
    plt.plot([popt[1]*snr,popt[1]*snr],
             [2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2],
             "--",
             color="black",
             lw=5,
             label=str(snr) + " sigma = " + str(np.round(popt[1]*snr*1000.,2)) + " mJy beam$^{-1}$")
    plt.plot([-popt[1], -popt[1]],
             [2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2],
             "--",
             color="black",
             lw=2)
    #
    plt.xlim(0, histrange[1])
    plt.ylim([2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2])
    plt.xlabel("Pixel value (Jy beam$^{-1}$)")
    plt.ylabel("Number of pixels")
    plt.title(title)
    plt.legend(loc = "upper right")
    if plotter==True:
      plt.savefig(output,dpi=100)

    return popt[1]

##################################################
### main part
##################################################
### plot CO(1-0) noise histogram
output = imageco10.replace(".image","_noisehistogram.png")
title = "CO(1-0) Datacube Noise Histogram"
co10snr_value = noisehist(imageco10, 0.001, output, snr_mom, title)

### plot CO(2-1) noise histogram
output = imageco21.replace(".image","_noisehistogram.png")
title = "CO(2-1) Datacube Noise Histogram"
co21snr_value = noisehist(imageco21, 0.001, output, snr_mom, title)

### print results
print("### CO(1-0) datacube "+str(snr_mom)+" sigma level = " + str(np.round(co10snr_value*1000., 2)) + " mJy/beam")
print("### CO(2-1) datacube "+str(snr_mom)+" sigma level = " + str(np.round(co21snr_value*1000., 2)) + " mJy/beam")

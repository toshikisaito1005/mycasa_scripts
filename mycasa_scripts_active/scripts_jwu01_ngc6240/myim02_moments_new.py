import os
import glob
import scipy
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
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
def tscreatemask(
    imagename,
    thres,
    outmask):
    """
    myim03
    """
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)
    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")

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

def eazy_immoments(
    imagename,
    nchan,
    outputname,
    snr_mom,
    snr_mask=2.5,
    ):
    """
    """
    ### create mask
    # get name
    smcube1 = imagename + ".smooth1"
    smcube2 = imagename + ".smooth2"
    smcube3 = imagename + ".smooth3"
    # cleanup
    os.system("rm -rf " + smcube1)
    os.system("rm -rf " + smcube2)
    os.system("rm -rf " + smcube3)
    # smooth1
    smbeam = str(imhead(smcube1, mode="list")["beammajor"]["value"] * 2.0) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube1)
    smnoise1 = noisehist(smcube1, 0.02, "", snr_mom, plotter=False)
    tscreatemask(smcube1, smnoise1 * snr_mask, smcube1+".mask")
    #
    # smooth2
    smbeam = str(imhead(smcube2, mode="list")["beammajor"]["value"] * 4.0) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube2)
    smnoise2 = noisehist(smcube2, 0.02, "", snr_mom, plotter=False)
    tscreatemask(smcube2, smnoise2 * snr_mask, smcube2+".mask")
    #
    # smooth3
    smbeam = str(imhead(smcube3, mode="list")["beammajor"]["value"] * 6.0) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube3)
    smnoise3 = noisehist(smcube3, 0.02, "", snr_mom, plotter=False)
    tscreatemask(smcube3, smnoise3 * snr_mask, smcube3+".mask")
    #
    # combine mask
    immath(imagename = [smcube1 + ".mask",
                        smcube2 + ".mask",
                        smcube3 + ".mask"],
               expr = "iif(IM0+IM1+IM2>=2.0, 1.0, 0.0)",
               outfile = imagename + ".mask")
    # cleanup
    os.system("rm -rf " + smcube1 + "*")
    os.system("rm -rf " + smcube2 + "*")
    os.system("rm -rf " + smcube3 + "*")

    ### masking cube





    immath(imagename = [cubeimage,mask_use_here],
           expr = "iif( IM0>=" + str(noise*snr_mom) + ", IM0*IM1, 0.0)",
           outfile = cubeimage+".masked")




    vch = abs(imhead(cubeimage,mode="list")["cdelt4"]) / 115.27120e9 * 299792.458
    
    immath(imagename = cubeimage+".masked",
           expr = "iif( IM0>0, 1.0/" + str(vch) + ", 0.0)",
           outfile = cubeimage+".maskedTF")

    immoments(imagename = cubeimage+".maskedTF",
              moments = [0],
              outfile = dir_image+name_line+".moment0.noise_tmp") # Nch

    beamarea_pix = tsbeam_area(dir_image+name_line+".moment0.noise_tmp")
    immath(dir_image+name_line+".moment0.noise_tmp",
           expr = str(vch)+"*sqrt(IM0)*"+str(noise),#+"/"+str(np.sqrt(beamarea_pix)),
           outfile = dir_image+name_line+"_"+beamp+".moment0.noise")

    immoments(imagename = cubeimage+".masked",
              moments = [0],
              #includepix = [noises[i]*3.0,10000.],
              outfile = dir_image+name_line+".moment0_tmp")

    immoments(imagename = cubeimage+".masked",
              moments = [1],
              #includepix = [noises[i]*3.0,10000.],
              outfile = dir_image+name_line+".moment1_tmp")

    immoments(imagename = cubeimage+".masked",
              moments = [8],
              #includepix = [noises[i]*3.0,10000.],
              outfile = dir_image+name_line+".moment8_tmp")

    # masking
    peak = imstat(dir_image+name_line+".moment0_tmp")["max"][0]
    
    #
    immath(imagename = [dir_image+name_line+".moment0_tmp",
                        dir_image+name_line+".moment0_tmp"],
           expr = "iif( IM0>=" + str(peak*percent) + ", IM1, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment0_tmp2")
    
    immath(imagename = [dir_image+name_line+"_"+beamp+".moment0_tmp2",
                        dir_image+name_line+".moment0.noise_tmp"],
           expr = "iif( IM1>="+str(nchan)+", IM0, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment0")

    #
    immath(imagename = [dir_image+name_line+".moment0_tmp",
                        dir_image+name_line+".moment1_tmp"],
           expr = "iif( IM0>=" + str(peak*percent) + ", IM1, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment1_tmp2")
    
    immath(imagename = [dir_image+name_line+"_"+beamp+".moment1_tmp2",
                        dir_image+name_line+".moment0.noise_tmp"],
           expr = "iif( IM1>="+str(nchan)+", IM0, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment1")

    #      
    immath(imagename = [dir_image+name_line+".moment0_tmp",
                        dir_image+name_line+".moment8_tmp"],
           expr = "iif( IM0>=" + str(peak*percent) + ", IM1, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment8_tmp2")
    
    immath(imagename = [dir_image+name_line+"_"+beamp+".moment8_tmp2",
                        dir_image+name_line+".moment0.noise_tmp"],
           expr = "iif( IM1>="+str(nchan)+", IM0, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment8")

    #
    immath(imagename = [dir_image+name_line+"_"+beamp+".moment0",
                         dir_image+name_line+"_"+beamp+".moment0.noise"],
           expr = "IM0/IM1",
           outfile = dir_image+name_line+"_"+beamp+".moment0.snratio_tmp")
    
    immath(imagename = [dir_image+name_line+"_"+beamp+".moment0.snratio_tmp",
                        dir_image+name_line+".moment0.noise_tmp"],
           expr = "iif( IM1>="+str(nchan)+", IM0, 0.0)",
           outfile = dir_image+name_line+"_"+beamp+".moment0.snratio")

    os.system("rm -rf " + cubeimage+".maskedTF")
    os.system("rm -rf " + dir_image+name_line+".moment0.noise_tmp")
    os.system("rm -rf " + dir_image+name_line+"_"+beamp+".moment0.snratio_tmp")
    os.system("rm -rf " + dir_image+name_line+".moment0_tmp")
    os.system("rm -rf " + dir_image+name_line+".moment1_tmp")
    os.system("rm -rf " + dir_image+name_line+".moment8_tmp")
    os.system("rm -rf " + dir_image+name_line+"_"+beamp+".moment0_tmp2")
    os.system("rm -rf " + dir_image+name_line+"_"+beamp+".moment1_tmp2")
    os.system("rm -rf " + dir_image+name_line+"_"+beamp+".moment8_tmp2")

    return mask_use_here

##################################################
### main part
##################################################

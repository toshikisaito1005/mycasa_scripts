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
    snr_mom,
    nchan,
    ):
    """
    """
    ### create mask
    # get name
    smcube1 = imagename + ".smooth1"
    smcube2 = imagename + ".smooth2"
    smcube3 = imagename + ".smooth3"
    # cleanup
    os.system("rm -rf " + smoothcube1)
    os.system("rm -rf " + smoothcube2)
    os.system("rm -rf " + smoothcube3)
    # smooth1
    smbeam = str(imhead(smoothcube1, mode="list")["beammajor"]["value"] * 2.0) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smoothcube1)




        # noise
        noisesmooth1 = noisehist(cubesmooth1,0.02,"test",3.0,bins=200,thres=0.0001,plotter=False)
        noisesmooth2 = noisehist(cubesmooth2,0.02,"test",3.0,bins=200,thres=0.0001,plotter=False)
        noisesmooth3 = noisehist(cubesmooth3,0.02,"test",3.0,bins=200,thres=0.0001,plotter=False)
        # create mask
        #tscreatemask(cubeimage,noise*1.*2.,dir_image+name_line+"_mask0.image")
        tscreatemask(cubesmooth1,noisesmooth1*0.0,dir_image+name_line+"_mask1.image")
        tscreatemask(cubesmooth2,noisesmooth2*0.0,dir_image+name_line+"_mask2.image")
        tscreatemask(cubesmooth3,noisesmooth3*0.0,dir_image+name_line+"_mask3.image")

        immath(imagename = [dir_image+name_line+"_mask1.image", dir_image+name_line+"_mask2.image", dir_image+name_line+"_mask3.image"],
               expr = "iif(IM0+IM1 >= 2.0, 1.0, 0.0)",
               outfile = dir_image+name_line+"_"+beamp+"_mask.image")

        os.system("rm -rf "+cubesmooth1)
        os.system("rm -rf "+cubesmooth2)
        os.system("rm -rf "+cubesmooth3)
        os.system("rm -rf "+dir_image+name_line+"_mask0.image")
        os.system("rm -rf "+dir_image+name_line+"_mask1.image")
        os.system("rm -rf "+dir_image+name_line+"_mask2.image")

        mask_use_here = dir_image+name_line+"_"+beamp+"_mask.image"

    else:
        mask_use_here = dir_image+name_line+"_"+beamp+"_mask.image"
        os.system("cp -r " + maskname + " " + mask_use_here)

    immath(imagename = [cubeimage,mask_use_here],
           expr = "iif( IM0>=" + str(noise*snr_mom) + ", IM0*IM1, 0.0)",
           outfile = cubeimage+".masked")
    #os.system("rm -rf " + mask_use_here)

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

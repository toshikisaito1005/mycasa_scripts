import os, glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.ioff()


#####################
### Define Parameters
#####################
# co10 images
imageco10    = "co10_cube.image"
pbco10       = "co10_cube.pb"
#
# co21 images
imageco21    = "co21_cube.image"
pbco21       = "co21_cube.pb"
#
# parameters for moment map creations
snr_mom      = 2.5                    # clip sn ratio level for immoments
redshift     = 0.02448                # source redshift
clipbox      = "108,108,263,263"      # clip image size of the output
rms_co10     = 0.00115                # Jy/beam unit (float), 1 sigma value or None
rms_co21     = 0.00605                # Jy/beam unit (float), 1 sigma value or None
obsfreq_co10 = 115.27120/(1+redshift) # GHz unit, co10 observed frequency
obsfreq_co21 = 230.53800/(1+redshift) # GHz unit, co21 observed frequency


#####################
### define functions
#####################
def createmask(
    imagename,
    thres,
    outmask,
    ):
    """
    """
    print("# create " + outmask)
    os.system("rm -rf " + outmask)
    expr = "iif(IM0>=" + str(thres) + ",1.0,0.0)"
    immath(imagename=imagename, mode="evalexpr", expr=expr, outfile=outmask)
    imhead(imagename=outmask, mode="del", hdkey="beammajor")
    makemask(mode="copy", inpimage=outmask, inpmask=outmask, output=outmask+":mask0", overwrite=True)

def func1(x, a, c):
    return a * np.exp(-(x)**2/(2*c**2))

def noisehist(
    imagename,
    noises_byeye,
    output,
    snr,
    title="Not Assigned",
    bins=200,
    thres=0.000001,
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
    histrange = [-1*abs(pixvalues.min()), abs(pixvalues.min())]
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
    xaxis = histdata[1][2:][histdata[1][2:]<noises_byeye]
    yaxis = histdata[0][1:][histdata[1][2:]<noises_byeye]
    guess0 = np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])
    popt, pcov = \
        curve_fit(func1, xaxis, yaxis, p0=[guess0,noises_byeye], maxfev=10000)
    #
    x = np.linspace(histdata[1][1], histdata[1][-1], 200)
    plt.plot(x, func1(x, popt[0], popt[1]), '-', c="black", lw=5)
    ylim = [2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2]
    #
    plt.plot([0,0], ylim, "-", color="black", lw=2)
    plt.plot([popt[1],popt[1]], ylim, "--", color="black", lw=2,
             label="1.0 sigma = " + str(np.round(popt[1]*1000.,2)) + " mJy beam$^{-1}$")
    plt.plot([popt[1]*snr,popt[1]*snr], ylim, "--", color="black", lw=5,
             label=str(snr) + " sigma = " + str(np.round(popt[1]*snr*1000.,2)) + " mJy beam$^{-1}$")
    plt.plot([-popt[1],-popt[1]], ylim, "--", color="black", lw=2)
    #
    plt.xlim(0, histrange[1])
    plt.ylim([2e1, np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]) * 1.2])
    plt.xlabel("Pixel value (Jy beam$^{-1}$)")
    plt.ylabel("Number of pixels")
    plt.title(title)
    plt.legend(loc = "upper right")
    if plotter==True:
      plt.savefig(output,dpi=100)

    return abs(popt[1])

def Jy2Kelvin(
    imagename,
    obsfreq_GHz,
    hdvalue="K.km/s",
    ):
    """
    """
    #
    print("# Jy-to-Kelvin conversion of " + imagename)
    bmaj = imhead(imagename, mode="list")["beammajor"]["value"]
    bmin = imhead(imagename, mode="list")["beamminor"]["value"]
    J2K = 1.222e6 / bmaj / bmin / obsfreq_GHz**2
    #
    outfile = imagename.replace(".image","") + "_Kelvin.image"
    os.system("rm -rf " + outfile)
    immath(imagename=imagename, expr="IM0*"+str(J2K), outfile=outfile)
    imhead(outfile, mode="put", hdkey="bunit", hdvalue=hdvalue)

def mask_cube(
    imagename,
    bmaj,
    snr_mom,
    snr_mask,
    sm1=2.0,
    sm2=4.0,
    sm3=6.0,
    ):
    # get name
    smcube1 = imagename + ".smooth1"
    smcube2 = imagename + ".smooth2"
    smcube3 = imagename + ".smooth3"
    #
    # cleanup
    os.system("rm -rf " + smcube1 + " " + smcube2 + " " + smcube3)
    #
    # smooth1 cube mask
    smbeam = str(bmaj * sm1) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube1)
    smnoise1 = noisehist(smcube1, 0.02, "", snr_mom, plotter=False)
    createmask(smcube1, smnoise1 * snr_mask, smcube1+".mask")
    #
    # smooth2 cube mask
    smbeam = str(bmaj * sm2) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube2)
    smnoise2 = noisehist(smcube2, 0.02, "", snr_mom, plotter=False)
    createmask(smcube2, smnoise2 * snr_mask, smcube2+".mask")
    #
    # smooth3 cube mask
    smbeam = str(bmaj * sm3) + "arcsec"
    imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube3)
    smnoise3 = noisehist(smcube3, 0.02, "", snr_mom, plotter=False)
    createmask(smcube3, smnoise3 * snr_mask, smcube3+".mask")
    #
    # combined cube mask
    os.system("rm -rf " + imagename+".mask")
    maskimages = [smcube1+".mask", smcube2+".mask", smcube3+".mask"]
    immath(imagename=maskimages, expr="iif(IM0+IM1+IM2>=2.0,1.0,0.0)", outfile=imagename+".mask")
    # cleanup
    os.system("rm -rf " + smcube1 + "*")
    os.system("rm -rf " + smcube2 + "*")
    os.system("rm -rf " + smcube3 + "*")
    maskcube = imagename+".mask"

    return maskcube

def run_immoments(
    cube_for_moment,
    outputname,
    moment,
    bmaj,
    clipbox=None,
    ):
    """
    """
    print("# create moment " + str(moment))
    outfile_mom = outputname+"_mom" + str(moment) + ".image"
    immoments(imagename=cube_for_moment, moments=[moment], includepix=[0.,1e11], outfile=outfile_mom, box=clipbox)
    imhead(outfile_mom, mode="put", hdkey="beammajor", hdvalue=str(bmaj)+"arcsec")
    imhead(outfile_mom, mode="put", hdkey="beamminor", hdvalue=str(bmaj)+"arcsec")

    return outfile_mom

def eazy_immoments(
    imagename,      # input iamge cube
    pbimage,        # imput pb cube
    outputname,     # prefix of the output
    snr_mom,        # threshold for moment map creation
    obsfreq_GHz,    # observed frequency required for Jy-to-Kelvin conversion
    rms=None,       # 1 sigma level
    pblimit=0.5,    # primary beam limit for imaging
    maskimage=None, # additional mask for moment map creation
    nchan=3,        # threshold number of channel for moment map creation
    snr_mask=4.5,   # threshold for cube mask cretion
    clipbox="",     # clip image size of the output
    ):
    """
    """
    print("### moment map creation for " + imagename)
    ### step 0: get beam size
    bmaj = imhead(imagename, mode="list")["beammajor"]["value"]
    #
    #
    ### step 1: measure noise
    if rms==None:
        print("# step 1: estimate rms")
        noise = noisehist(imagename, 0.02, "", snr_mom, plotter=False)
    else:
        noise = rms
    print("# rms noise level = " + str(np.round(noise,5)) + " Jy/beam")
    #
    #
    ### step 2: create maskcube
    maskcube = glob.glob(imagename+".mask")
    if not maskcube:
        print("# step 2: running mask_cube")
        maskcube = mask_cube(imagename, bmaj, snr_mom, snr_mask)
    else:
        print("# step 2: skip mask_cube")
    #
    #
    ### step 3: create nchanmask
    print("# step 3: create nchan mask")
    # masking cube
    os.system("rm -rf " + imagename+".masked")
    immath(imagename=[imagename,maskcube], expr="iif(IM1>=1.0,IM0,0.0)", outfile=imagename+".masked")
    #
    # create nchan mask
    nchanmask = imagename + ".nchanmask"
    os.system("rm -rf " + nchanmask + "*")
    expr = "iif(IM0>=" + str(noise * snr_mom) + ",1.0/10.,0.0)"
    immath(imagename=imagename+".masked", expr=expr, outfile=nchanmask+"_tmp") # 10. is the channel width in km/s.
    immoments(imagename=nchanmask+"_tmp", moments=[0], outfile=nchanmask+"_tmp2")
    createmask(nchanmask+"_tmp2", nchan, nchanmask)
    #
    #
    ### step 4: combime maskimage if specified
    print("# step 4: combine masks")
    maskcube_pre = maskcube
    maskcube = imagename+".mask2"
    if maskimage!=None:
        immath(imagename=[maskcube_pre,maskimage,nchanmask], expr="IM0*IM1*IM2", outfile=maskcube)
    else:
        immath(imagename=[maskcube_pre,nchanmask], expr="IM0*IM1", outfile=maskcube)    
    #
    #
    ### step 5: pbcorr
    print("# step 5: pbcorr")
    os.system("rm -rf "+imagename+".pbcor")
    impbcor(imagename=imagename, pbimage=pbimage, outfile=imagename+".pbcor", cutoff=pblimit)
    #
    #
    ### step 6: maksing datacube
    print("# step 6: masking datacube")
    immath(imagename=[imagename+".pbcor",maskcube],expr="IM0*IM1",outfile=imagename+".masked2")
    #
    #
    ### step 7: moments
    print("# step 7: run_immoments")
    cube_for_moment = imagename+".masked2"
    outfile_mom0 = run_immoments(cube_for_moment, outputname, 0, bmaj, clipbox=clipbox)
    outfile_mom1 = run_immoments(cube_for_moment, outputname, 1, bmaj, clipbox=clipbox)
    outfile_mom2 = run_immoments(cube_for_moment, outputname, 2, bmaj, clipbox=clipbox)
    outfile_mom8 = run_immoments(cube_for_moment, outputname, 8, bmaj, clipbox=clipbox)
    #
    #
    ### step 8: other stuffs
    print("# step 8: other stuffs")
    # add header to mom0
    Jy2Kelvin(outfile_mom0, obsfreq_GHz, "K.km/s")
    Jy2Kelvin(outfile_mom8, obsfreq_GHz, "K")
    #
    # noise
    noise_mJy = str(np.round(noise*1000., 2))
    #
    # create mom-0 mask
    outfile_mom0_for_mask = run_immoments(cube_for_moment, outputname+"_for_mask", 0, bmaj)
    createmask(outfile_mom0_for_mask, 0.0000001, outfile_mom0+".mask")
    # cleanup
    os.system("rm -rf " + outfile_mom0_for_mask)
    os.system("rm -rf " + imagename + ".pbcor") 
    os.system("rm -rf " + imagename + ".mask2")
    os.system("rm -rf " + imagename + ".masked")
    os.system("rm -rf " + imagename + ".masked_tmp")
    os.system("rm -rf " + nchanmask + "*")

    return outfile_mom0+".mask", noise_mJy


#####################
### Main Procedure
#####################
### momemnt map creation
co10mask, noise_co10_mJy = \
    eazy_immoments(imagename   = imageco10,
                   pbimage     = pbco10,
                   outputname  = "n6240_co10",
                   snr_mom     = snr_mom,
                   rms         = rms_co10,
                   obsfreq_GHz = obsfreq_co10,
                   clipbox     = clipbox,
                   )

_, noise_co21_mJy = \
    eazy_immoments(imagename   = imageco21,
                   pbimage     = pbco21,
                   outputname  = "n6240_co21",
                   snr_mom     = snr_mom,
                   rms         = rms_co21,
                   obsfreq_GHz = obsfreq_co21,
                   pblimit     = 0.3,
                   clipbox     = clipbox,
                   maskimage   = co10mask,   # In this case, co10 mom-0 detection pixels are used as the additional mask
                   )

### print noise rms levels
print("###\n###\n###")
if rms_co10==None:
    print("### 1sigma of the input co10 datacube = " + noise_co10_mJy + " mJy/beam")
#
if rms_co21==None:
    print("### 1sigma of the input co21 datacube = " + noise_co21_mJy + " mJy/beam")
#

### cleanup
os.system("rm -rf *.last")
os.system("rm -rf " + co10mask+ " " + _)
#

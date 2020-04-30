import os, glob
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit
plt.ioff()


#####################
### Define Parameters
#####################
dir_data = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/data/"
#
dir_co10 = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/image_co10/"
imageco10 = dir_data + "ngc6240_co10_12m7m_na.smooth.regrid"
pbco10 = dir_data + "ngc6240_co10_12m7m_na.pb.regrid"
#
dir_co21 = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/image_co21/"
imageco21 = dir_data + "ngc6240_co21_12m7m_natpr.smooth.regrid"
pbco21 = dir_data + "ngc6240_co21_12m7m_natpr.pb.regrid"
#
dir_cs21 = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/image_cs21/"
imagecs21 = dir_data + "ngc6240_cs32_12m_l30_na.pb.regrid"
pbcs21 = dir_data + "ngc6240_cs21_12m_l30_na.pb.regrid"
#
dir_hcn10 = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/image_hcn10/"
imagehcn10 = dir_data + "ngc6240_hcn10_12m_l50_na.pb.regrid"
pbhcn10 = dir_data + "ngc6240_hcn10_12m_l50_na.smooth.regrid"
#
dir_hcop10 = "/Users/saito/data/myproj_active/proj_jwu01_ngc6240/image_hcop10/"
imagehcop10 = dir_data + "ngc6240_hcop10_12m_l50_na.pb.regrid"
pbhcop10 = dir_data + "ngc6240_hcop10_12m_l50_na.smooth.regrid"
#
snr_mom = 2.5   # clip signal-to-noise ratio level for immoments
redshift = 0.02448
clipbox = "93,93,278,278"


#####################
### define some functions
#####################
def tscreatemask(
    imagename,
    thres,
    outmask,
    ):
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
    title="Not Assigned",
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
    range_l = pixvalues.min()/1.5 - 0.02
    range_r = -pixvalues.min()/1.5 + 0.02
    if range_r>range_l:
        histrange = [range_l, range_r]
    else:
        histrange = [range_r, range_l]
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

def Jy2Kelvin(
    imagename,
    obsfreq_GHz,
    hdvalue="K.km/s",
    ):
    """
    """
    bmaj = imhead(imagename, mode="list")["beammajor"]["value"]
    bmin = imhead(imagename, mode="list")["beamminor"]["value"]
    J2K = 1.222e6 / bmaj / bmin / obsfreq_GHz**2
    #
    outfile = imagename.replace(".image","") + "_Kelvin.image"
    os.system("rm -rf " + outfile)
    immath(imagename=imagename, expr="IM0*"+str(J2K), outfile=outfile)
    imhead(outfile, mode="put", hdkey="bunit", hdvalue=hdvalue)

def eazy_immoments(
    imagename,
    pbimage,
    outputname,
    snr_mom,
    obsfreq_GHz,
    pblimit=0.5,
    maskimage=None,
    maskcube=None,
    nchan=3.0,
    snr_mask=6.0,
    clipbox="",
    ):
    """
    step 1: create a "cube" mask for the input cube
    step 2: create a "nchan" mask for moment maps using nchan
    step 3: mask the cube using the "cube" mask
    step 4: create moment maps with snr_mom cut
    step 5: mask the moment maps using the "nchan" mask
    """
    print("### moment map creation for " + imagename)
    bmaj = imhead(imagename, mode="list")["beammajor"]["value"]
    ### create signal-to-noise mask
    if maskcube==None:
        # get name
        smcube1 = imagename + ".smooth1"
        smcube2 = imagename + ".smooth2"
        smcube3 = imagename + ".smooth3"
        #
        # cleanup
        os.system("rm -rf " + smcube1)
        os.system("rm -rf " + smcube2)
        os.system("rm -rf " + smcube3)
        #
        # smooth1 cube mask
        smbeam = str(bmaj * 2.0) + "arcsec"
        imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube1)
        smnoise1 = noisehist(smcube1, 0.02, "", snr_mom, plotter=False)
        tscreatemask(smcube1, smnoise1 * snr_mask, smcube1+".mask")
        #
        # smooth2 cube mask
        smbeam = str(bmaj * 4.0) + "arcsec"
        imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube2)
        smnoise2 = noisehist(smcube2, 0.02, "", snr_mom, plotter=False)
        tscreatemask(smcube2, smnoise2 * snr_mask, smcube2+".mask")
        #
        # smooth3 cube mask
        smbeam = str(bmaj * 6.0) + "arcsec"
        imsmooth(imagename=imagename, targetres=True, major=smbeam, minor=smbeam, pa="0deg", outfile=smcube3)
        smnoise3 = noisehist(smcube3, 0.02, "", snr_mom, plotter=False)
        tscreatemask(smcube3, smnoise3 * snr_mask, smcube3+".mask")
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
    else:
        maskcube = maskcube
    #
    if maskimage!=None:
        maskcube_pre = maskcube
        maskcube = imagename+".mask2"
        immath(imagename=[maskcube_pre,maskimage], expr="IM0*IM1", outfile=maskcube)
    #
    #
    #
    ### nchan mom mask
    # measure noise
    noise = noisehist(imagename, 0.02, "", snr_mom, plotter=False)
    #
    # mask cube
    os.system("rm -rf " + imagename+".masked")
    immath(imagename=[imagename,maskcube], expr="iif(IM1>=1.0,IM0,0.0)", outfile=imagename+".masked")
    #
    nchanmask = imagename + ".nchanmask"
    os.system("rm -rf " + nchanmask + "*")
    immath(imagename=imagename+".masked", expr="iif(IM0>="+str(noise*snr_mom)+",1.0/10.,0.0)", outfile=nchanmask+"_tmp") # 10. is the channel width in km/s.
    immoments(imagename=nchanmask+"_tmp", moments=[0], outfile=nchanmask+"_tmp2")
    # make nchanmask
    tscreatemask(nchanmask+"_tmp2", nchan, nchanmask)
    #
    #
    #
    ### pbcorr
    os.system("rm -rf "+imagename+".pbcor")
    impbcor(imagename=imagename, pbimage=pbimage, outfile=imagename+".pbcor", cutoff=pblimit)
    #
    ### export mask
    outfile_mom0 = outputname+"_mom0.image"
    os.system("rm -rf " + outfile_mom0 + ".mask")
    os.system("rm -rf " + outfile_mom0 + "*")
    immoments(imagename=imagename+".pbcor", moments=[0], includepix=[0.,1e11], outfile=outfile_mom0+"_tmp")
    immath(imagename=[outfile_mom0+"_tmp",nchanmask], expr="IM0*IM1", outfile=outfile_mom0+"_tmp2")
    tscreatemask(outfile_mom0+"_tmp2", 0.000000001, outfile_mom0+".mask")
    #
    immath(imagename=[imagename+".masked",outfile_mom0+".mask"],expr="IM0*IM1",outfile=imagename+".masked2")
    #
    ### moments
    cube_for_moment = imagename+".masked2"
    # mom-0
    outfile_mom0 = outputname+"_mom0.image"
    #immoments(imagename=cube_for_moment, moments=[0], includepix=[0.,1e11], outfile=outfile_mom0+"_tmp")
    imagenames = [outfile_mom0+"_tmp",nchanmask]
    expr = "IM0*IM1"
    immath(imagename=imagenames, expr=expr, outfile=outfile_mom0, box=clipbox)
    #
    # mom-1
    outfile_mom1 = outputname+"_mom1.image"
    os.system("rm -rf " + outfile_mom1 + "*")
    immoments(imagename=cube_for_moment, moments=[1], includepix=[0.,1e11], outfile=outfile_mom1+"_tmp")
    imagenames = [outfile_mom1+"_tmp",nchanmask]
    expr = "IM0*IM1"
    immath(imagename=imagenames, expr=expr, outfile=outfile_mom1, box=clipbox)
    #
    # mom-2
    outfile_mom2 = outputname+"_mom2.image"
    os.system("rm -rf " + outfile_mom2 + "*")
    immoments(imagename=cube_for_moment, moments=[2], includepix=[0.,1e11], outfile=outfile_mom2+"_tmp")
    imagenames = [outfile_mom2+"_tmp",nchanmask]
    expr = "IM0*IM1"
    immath(imagename=imagenames, expr=expr, outfile=outfile_mom2, box=clipbox)
    #
    # mom-8
    outfile_mom8 = outputname+"_mom8.image"
    os.system("rm -rf " + outfile_mom8 + "*")
    immoments(imagename=cube_for_moment, moments=[8], includepix=[0.,1e11], outfile=outfile_mom8+"_tmp")
    imagenames = [outfile_mom8+"_tmp",nchanmask]
    expr = "IM0*IM1"
    immath(imagename=imagenames, expr=expr, outfile=outfile_mom8, box=clipbox)
    #
    # add header to mom0
    imhead(outfile_mom0, mode="put", hdkey="beammajor", hdvalue=str(bmaj)+"arcsec")
    imhead(outfile_mom0, mode="put", hdkey="beamminor", hdvalue=str(bmaj)+"arcsec")
    Jy2Kelvin(outfile_mom0, obsfreq_GHz, "K.km/s")
    #
    # add header to mom8
    imhead(outfile_mom8, mode="put", hdkey="beammajor", hdvalue=str(bmaj)+"arcsec")
    imhead(outfile_mom8, mode="put", hdkey="beamminor", hdvalue=str(bmaj)+"arcsec")
    Jy2Kelvin(outfile_mom8, obsfreq_GHz, "K")
    #
    # noise
    noise_mJy = str(np.round(noise*1000., 2))
    # cleanup
    os.system("rm -rf " + outfile_mom0 + "_tmp")
    os.system("rm -rf " + outfile_mom0 + "_tmp2")
    os.system("rm -rf " + outfile_mom1 + "_tmp")
    os.system("rm -rf " + outfile_mom2 + "_tmp")
    os.system("rm -rf " + outfile_mom8 + "_tmp")
    os.system("rm -rf " + imagename + ".pbcor") 
    os.system("rm -rf " + imagename + ".masked_tmp")
    os.system("rm -rf " + imagename + ".masked")
    os.system("rm -rf " + nchanmask + "*")
    os.system("rm -rf " + imagename + ".mask*")

    return outfile_mom0+".mask", noise_mJy


#####################
### Main Procedure
#####################
#
done = glob.glob(dir_co10)
if not done:
    os.mkdir(dir_co10)
#
done = glob.glob(dir_co21)
if not done:
    os.mkdir(dir_co21)
#
done = glob.glob(dir_cs21)
if not done:
    os.mkdir(dir_cs21)
#
done = glob.glob(dir_hcn10)
if not done:
    os.mkdir(dir_hcn10)
#
done = glob.glob(dir_hcop10)
if not done:
    os.mkdir(dir_hcop10)
#
co10mask, noise_co10_mJy = eazy_immoments(imagename=imageco10, pbimage=pbco10, outputname=dir_co10+"n6240_co10", snr_mom=snr_mom, obsfreq_GHz=115.27120/(1+redshift), pblimit=0.5, clipbox=clipbox)
_, noise_co21_mJy = eazy_immoments(imagename=imageco21, pbimage=pbco21, outputname=dir_co21+"n6240_co21", snr_mom=snr_mom, obsfreq_GHz=230.53800/(1+redshift), pblimit=0.3, clipbox=clipbox, maskimage=co10mask)
#_, noise_cs21_mJy = eazy_immoments(imagename=imagecs21, pbimage=pbcs21, outputname=dir_cs21+"n6240_cs21", snr_mom=snr_mom, obsfreq_GHz=230.53800/(1+redshift), pblimit=0.5, clipbox=clipbox)
#_, noise_hcn10_mJy = eazy_immoments(imagename=imagehcn10, pbimage=pbhcn10, outputname=dir_hcn10+"n6240_hcn10", snr_mom=snr_mom, obsfreq_GHz=230.53800/(1+redshift), pblimit=0.5, clipbox=clipbox)
#_, noise_hcop10_mJy = eazy_immoments(imagename=imagehcop10, pbimage=pbhcop10, outputname=dir_hcop10+"n6240_hcop10", snr_mom=snr_mom, obsfreq_GHz=230.53800/(1+redshift), pblimit=0.5, clipbox=clipbox)

#
print("### 1sigma of the input co10 datacube = " + noise_co10_mJy + " mJy/beam")
print("### 1sigma of the input co21 datacube = " + noise_co21_mJy + " mJy/beam")
#print("### 1sigma of the input cs21 datacube = " + noise_cs21_mJy + " mJy/beam")
#print("### 1sigma of the input hcn10 datacube = " + noise_hcn10_mJy + " mJy/beam")
#print("### 1sigma of the input hcop10 datacube = " + noise_hcop10_mJy + " mJy/beam")

os.system("rm -rf *.last")
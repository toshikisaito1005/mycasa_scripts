import os
import glob
import math
import scipy
import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
from scipy.optimize import curve_fit
plt.ioff()

# CASA imports
from taskinit import *
from importfits import importfits
from imregrid import imregrid
from imsmooth import imsmooth
from imval import imval
from immoments import immoments
from immath import immath
from makemask import makemask
from imhead import imhead
from imstat import imstat
from exportfits import exportfits
import analysisUtils as aU
mycl = aU.createCasaTool(cltool)
mycs = aU.createCasaTool(cstool)
myia = aU.createCasaTool(iatool)
myrg = aU.createCasaTool(rgtool)
myqa = aU.createCasaTool(qatool)


def tsimportfits(fitsimage,imagename):
    """
    myim01
    """
    os.system("rm -rf " + imagename)
    importfits(fitsimage = fitsimage,
               imagename = imagename,
               defaultaxes = True,
               defaultaxesvalues = ["RA","Dec","Frequency","Stokes"])

def tsroundbeam(imagename,outfile,common_beam,delete_imagename=True):
    """
    myim01
    """
    os.system("rm -rf " + outfile)
    imsmooth(imagename = imagename,
             targetres = True,
             major = common_beam,
             minor = common_beam,
             pa = "0deg",
             outfile = outfile)

    if delete_imagename==True:
        os.system("rm -rf " + imagename)

def tsimregrid(imagename,template,output,axes=[3]):
    """
    myim01
    """
    os.system("rm -rf " + output)
    imregrid(imagename=imagename,template=template,output=output,axes=axes)
    os.system("rm -rf " + imagename)

def tsbeam_area(imagename):
    """
    myim01, myim03
    """
    major = imhead(imagename=imagename,mode="get",hdkey="beammajor")["value"]
    minor = imhead(imagename=imagename,mode="get",hdkey="beamminor")["value"]
    pix = abs(imhead(imagename=imagename,mode="list")["cdelt1"])
    pixelsize = pix * 3600 * 180 / np.pi
    beamarea_arcsec = major * minor * np.pi/(4 * np.log(2))
    beamarea_pix = beamarea_arcsec / (pixelsize ** 2)
                   
    return beamarea_pix

def tsJy2Kelvin(imagename,outfile):
    """
    myim01
    """
    myunit = imhead(imagename,mode="list")["bunit"]
    if myunit=="Jy/beam":
        os.system("mv " + imagename + " " + outfile)
    else:
        headlist = imhead(imagename,mode="list")
        beamsize = headlist["beammajor"]["value"]
        restfreq = headlist["restfreq"][0]/1e9
        factor = 1.222e6 / beamsize / beamsize / restfreq / restfreq
        os.system("rm -rf " + outfile)
        immath(imagename = imagename,
               expr = "IM0/" + str(factor),
               outfile = outfile)
        imhead(outfile,mode="put",hdkey="bunit",hdvalue="Jy/beam")
        os.system("rm -rf " + imagename)

def stage_cubes(common_beam,co10_fits,co21_fits,co10_output,co21_output):
    """
    myim01
    """
    # importfits
    tsimportfits(co10_fits, co10_fits.replace(".fits",".image"))
    tsimportfits(co21_fits, co21_fits.replace(".fits",".image"))
    # round_beam co10
    if "ngc3627" in co10_fits:
        os.system("mv "+co10_fits.replace(".fits",".image")+" "+co10_output+"_tmp")
    elif "ngc4254" in co10_fits:
        os.system("mv "+co10_fits.replace(".fits",".image")+" "+co10_output+"_tmp")
    else:
        tsroundbeam(imagename = co10_fits.replace(".fits",".image"),
                    outfile = co10_output+"_tmp",
                    common_beam = common_beam)
    # round_beam co21
    tsroundbeam(imagename = co21_fits.replace(".fits",".image"),
                outfile = co21_output+"_tmp2",
                common_beam = common_beam)
    # regrid co21 to co10 (frequency-axis)
    tsimregrid(imagename = co21_output+"_tmp2",
               template = co10_output+"_tmp",
               output = co21_output+"_tmp")
    # Jansky/beam to Kelvin
    tsJy2Kelvin(co10_output+"_tmp",co10_output)
    tsJy2Kelvin(co21_output+"_tmp",co21_output)

def gridtemplate(imagename10,image_length,direction_ra,direction_dec):
    """
    myim02
    """
    # get native grid information
    num_x_pix = imhead(imagename10,mode="list")["shape"][0]
    num_y_pix = imhead(imagename10,mode="list")["shape"][1]
    pix_radian = imhead(imagename10,mode="list")["cdelt2"]
    obsfreq = 115.27120 # imhead(imagename10,mode="list")["restfreq"][0]/1e9
    pix_arcsec = round(pix_radian * 3600 * 180 / np.pi, 3)

    # create tempalte image
    blc_ra_tmp=imstat(imagename10)["blcf"].split(", ")[0]
    blc_dec_tmp=imstat(imagename10)["blcf"].split(", ")[1]
    blc_ra = blc_ra_tmp.replace(":","h",1).replace(":","m",1)+"s"
    blc_dec = blc_dec_tmp.replace(".","d",1).replace(".","m",1)+"s"
    beamsize=round(imhead(imagename10,"list")["beammajor"]["value"], 2)
    pix_size=round(beamsize/4.53, 2)
    size_x = int(image_length / pix_size)
    size_y = size_x
    c = SkyCoord(blc_ra, blc_dec)
    ra_dgr = str(c.ra.degree)
    dec_dgr = str(c.dec.degree)
    direction="J2000 "+direction_ra+" "+direction_dec
    mycl.done()
    mycl.addcomponent(dir=direction,
                      flux=1.0,
                      fluxunit="Jy",
                      freq="230.0GHz",
                      shape="Gaussian",
                      majoraxis="0.1arcmin",
                      minoraxis="0.05arcmin",
                      positionangle="45.0deg")

    myia.fromshape("template.im",[size_x,size_y,1,1],overwrite=True)
    mycs=myia.coordsys()
    mycs.setunits(["rad","rad","","Hz"])
    cell_rad=myqa.convert(myqa.quantity(str(pix_size)+"arcsec"),"rad")["value"]
    mycs.setincrement([-cell_rad,cell_rad],"direction")
    mycs.setreferencevalue([myqa.convert(direction_ra,"rad")["value"],
                            myqa.convert(direction_dec,"rad")["value"]],
                           type="direction")
    mycs.setreferencevalue(str(obsfreq)+"GHz","spectral")
    mycs.setincrement("1GHz","spectral")
    myia.setcoordsys(mycs.torecord())
    myia.setbrightnessunit("Jy/pixel")
    myia.modify(mycl.torecord(),subtract=False)
    exportfits(imagename="template.im",
               fitsimage="template.fits",
               overwrite=True)

    os.system("rm -rf template.image")
    importfits(fitsimage="template.fits",
               imagename="template.image")

    myia.close()
    mycl.close()

def tscreatemask(imagename,thres,outmask):
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
    return a*np.exp(-(x)**2/(2*c**2))

def noisehist(imagename,noises_byeye,output,snr,bins=200,thres=0.0001,logscale=True,plotter=True):
    """
    myim03
    """
    shape = imhead(imagename,mode="list")["shape"]
    box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
    data = imval(imagename,box=box)
    pixvalues = data["data"].flatten()
    pixvalues = pixvalues[abs(pixvalues)>thres]

    # plot
    histrange = [pixvalues.min()/1.5-0.02,-pixvalues.min()/1.5+0.02]
    plt.figure(figsize=(10,10))
    plt.rcParams["font.size"] = 22
    plt.subplots_adjust(bottom=0.10, left=0.19, right=0.99, top=0.90)
    histdata = plt.hist(pixvalues,
                        bins=bins,
                        range=histrange,
                        lw=0,
                        log=logscale,
                        color="blue",
                        alpha=0.3)
    plt.hist(pixvalues*-1,
                        bins=bins,
                        range=histrange,
                        lw=0,
                        log=logscale,
                        color="red",
                        alpha=0.3)

    popt, pcov = curve_fit(func1,
                           histdata[1][2:][histdata[1][2:]<noises_byeye],
                           histdata[0][1:][histdata[1][2:]<noises_byeye],
                           p0 = [np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]),
                                 noises_byeye],
                           maxfev = 10000)

    x = np.linspace(histdata[1][1], histdata[1][-1], 200)
    plt.plot(x, func1(x, popt[0], popt[1]), '-', c="black", lw=5)
    plt.plot([0,0],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '-',color='black',lw=2)
    plt.plot([popt[1],popt[1]],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '--',color='black',lw=2,
             label = "1 sigma = " + str(np.round(popt[1],3)) + " Jy beam$^{-1}$")
    plt.plot([popt[1]*snr,popt[1]*snr],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '--',color='black',lw=5,
             label = str(snr) + " sigma = " + str(np.round(popt[1]*snr,3)) + " Jy beam$^{-1}$")
    plt.plot([-popt[1],-popt[1]],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '--',color='black',lw=2)

    # percentile
    percentile = (0.5-scipy.special.erf(snr/np.sqrt(2))/2.) * 100.
    sigma_percentile = np.percentile(pixvalues,percentile) * -1

    plt.plot([sigma_percentile,sigma_percentile],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '-',color='black',lw=5,
             label = "|0.003%| = " + str(np.round(sigma_percentile,3)) + " Jy beam$^{-1}$")

    #plt.title(imagename.split("/")[-1])
    plt.xlim(0,histrange[1])
    plt.ylim([2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*1.2])#3.0])
    plt.xlabel("Pixel value (Jy beam$^{-1}$)")
    plt.ylabel("Number of pixels")
    plt.legend(loc = "upper right")
    if plotter==True:
      plt.savefig(output,dpi=100)

    return sigma_percentile/float(snr) # popt[1]

def noisehist_kelvin(imagename,jy2k,noises_byeye,output,snr,bins=200,thres=0.0000,logscale=True,plotter=True,title="test"):
    """
    myim03
    """
    shape = imhead(imagename,mode="list")["shape"]
    box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
    data = imval(imagename,box=box)
    pixvalues = data["data"].flatten() * jy2k
    pixvalues = pixvalues[abs(pixvalues)>thres]

    # plot
    histrange = [pixvalues.min()-0.02,-pixvalues.min()+0.02]
    plt.figure(figsize=(10,10))
    plt.rcParams["font.size"] = 22
    plt.subplots_adjust(bottom=0.10, left=0.19, right=0.99, top=0.90)
    histdata = plt.hist(pixvalues,
                        bins=bins,
                        range=histrange,
                        lw=0,
                        log=logscale,
                        color="blue",
                        alpha=0.3,
                        label="positive pixels")
    plt.hist(pixvalues*-1,
                        bins=bins,
                        range=histrange,
                        lw=0,
                        log=logscale,
                        color="red",
                        alpha=0.3,
                        label="negative pixels (reversed)")

    popt, pcov = curve_fit(func1,
                           histdata[1][2:][histdata[1][2:]<noises_byeye],
                           histdata[0][1:][histdata[1][2:]<noises_byeye],
                           p0 = [np.max(histdata[0][1:][histdata[1][2:]<noises_byeye]),
                                 noises_byeye],
                           maxfev = 10000)

    x = np.linspace(histdata[1][1], histdata[1][-1], 200)
    plt.plot(x, func1(x, popt[0], popt[1]), '-', c="black", lw=5)
    plt.plot([0,0],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '-',color='black',lw=2)
    plt.plot([popt[1],popt[1]],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '--',color='black',lw=2,
             label = "1 sigma = " + str(np.round(popt[1],3)) + " K")
    plt.plot([popt[1]*snr,popt[1]*snr],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '--',color='black',lw=5,
             label = str(snr) + " sigma = " + str(np.round(popt[1]*snr,3)) + " K")
    plt.plot([-popt[1],-popt[1]],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '--',color='black',lw=2)
    #
    # percentile
    percentile = (0.5-scipy.special.erf(snr/np.sqrt(2))/2.) * 100.
    sigma_percentile = np.percentile(pixvalues,percentile) * -1

    plt.plot([sigma_percentile,sigma_percentile],
             [2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*3.0],
             '-',color='black',lw=5, label=str(np.round(sigma_percentile,3))+" K")

    #plt.title(imagename.split("/")[-1])
    plt.xlim(0,histrange[1])
    plt.ylim([2e1,np.max(histdata[0][1:][histdata[1][2:]<noises_byeye])*1.2])#3.0])
    plt.xlabel("Pixel absolute value (K)")
    plt.ylabel("Number of pixels")
    plt.legend(loc = "upper right")
    plt.title(title)
    if plotter==True:
      plt.savefig(output,dpi=300)

def eazy_immoments(dir_proj,imagename,galname,noise,beamp,snr_mom,percent,nchan,
                   maskname=None,
                   myim="03"):
    """
    myim03, myim05
    use co10 mask for co10, co21 mask for co21
    This is be replace by eazy_immoments_r21.
    """
    if myim=="03":
        # prepare workinf directory e.g., ngc0628_co10
        name_line = imagename.split(galname+"_")[1].split("_")[0]
        dir_image = dir_proj+"../"+galname+"_"+name_line+"/"
        cubeimage = dir_image + name_line + "_cube.image"
        os.system("mkdir " + dir_image)
        os.system("cp -r " + imagename + " " + cubeimage)
    elif myim=="05":
        name_line = imagename.split(galname+"_")[1].split("/")[0]
        dir_image = dir_proj
        cubeimage = imagename
    
    print("### woking on " + galname + " " + name_line + " " + beamp)

    if maskname==None:
        os.system("rm -rf " + cubeimage+".masked")
        #os.system("rm -rf " + dir_image+"*.noise")
        os.system("rm -rf " + dir_image+"*.mask*")
    
        # imsmooth
        cubesmooth1 = cubeimage.replace(".image",".smooth1") # 4.0 mJy
        bmaj = imhead(cubeimage,"list")["beammajor"]["value"]
    	imsmooth(imagename = cubeimage,
                 targetres = True,
                 major = str(bmaj*3.0) + "arcsec",#1.2) + "arcsec",
                 minor = str(bmaj*3.0) + "arcsec",#1.2) + "arcsec",
                 pa = "0deg",
                 outfile = cubesmooth1)
        cubesmooth2 = cubeimage.replace(".image",".smooth2") # 10 mJy
        imsmooth(imagename = cubeimage,
                 targetres = True,
                 major = str(bmaj*5.0) + "arcsec",
                 minor = str(bmaj*5.0) + "arcsec",
                 pa = "0deg",
                 outfile = cubesmooth2)
        cubesmooth3 = cubeimage.replace(".image",".smooth3") # 10 mJy
        imsmooth(imagename = cubeimage,
                 targetres = True,
                 major = str(bmaj*7.0) + "arcsec",
                 minor = str(bmaj*7.0) + "arcsec",
                 pa = "0deg",
                 outfile = cubesmooth3)
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

def import_data(
    imagename,
    mode,
    index=0,
    ):
    """
    myim10
    """
    image_r = imhead(imagename,mode="list")["shape"][0] - 1
    image_t = imhead(imagename,mode="list")["shape"][1] - 1
    value = imval(imagename,box="0,0,"+str(image_r)+","+str(image_t))

    if mode=="coords":
        value_masked = value[mode][:,:,index] * 180 / np.pi
    else:
        value_masked = value[mode]

    value_masked_1d = value_masked.flatten()

    return value_masked_1d

def distance(x, y, pa, inc, ra_cnt, dec_cnt, scale):
    """
    myim10
    """
    tilt_cos = math.cos(math.radians(pa))
    tilt_sin = math.sin(math.radians(pa))
    
    x_tmp = x - ra_cnt
    y_tmp = y - dec_cnt
    
    x_new = (x_tmp*tilt_cos - y_tmp*tilt_sin)
    y_new = (x_tmp*tilt_sin + y_tmp*tilt_cos) * 1/math.sin(math.radians(inc))
    
    r = np.sqrt(x_new**2 + y_new**2) * 3600 * scale # arcsec * pc/arcsec
    
    return r

import os
import re
import sys
import glob
import scipy
import scipy.ndimage
import numpy as np
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.colors import LogNorm
from astropy.io import fits


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
myia = aU.createCasaTool(iatool)
myrg = aU.createCasaTool(rgtool)


####################################################################################
### Define Main Functions
####################################################################################
def cube_to_moments(pixelmin,
                    increment_mask,
                    thres_masking,
                    thres_mom,
                    pbcut,
                    dir_data,
                    galname,
                    chans,
                    suffix,
                    beam_size,
                    rms_co10,
                    rms_co21):
    """
    """
    print("###########################")
    print("### running cube_to_moments")
    print("###########################")
    
    os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*.moment*")
    os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*.mask")
    os.system("rm -rf "+dir_data+galname+"/*"+suffix+"*.cube")
    
    ### step 1/10: importfits
    print("### momentmaps 1/10: importfits")
    fitsimages = glob.glob(dir_data+"data/"+galname+"*.fits")
    for i in range(len(fitsimages)):
        eazy_importfits(fitsimages[i])

    # find imported images
    image_co10 = glob.glob(dir_data+"data/"+galname+"*co10*image*")[0]
    image_co21 = glob.glob(dir_data+"data/"+galname+"*co21*image*")[0]

    ### step 2/10: Kelvin to Jansky conversion
    print("### momentmaps 2/10: Kelvin to Jansky conversion")

    bunit = imhead(image_co10,"list")["bunit"]
    synsbeam10 = imhead(image_co10,"list")["beammajor"]["value"]
    if bunit == "K": # CO(1-0) conversion if bunit = K
        easy_K2Jy(image_co10,synsbeam10,115.27120)
        image_co10 = image_co10 + ".jy"
    else:
        print("# skip K2Jy for the CO(1-0) data")

    bunit = imhead(image_co21,"list")["bunit"]
    synsbeam21 = imhead(image_co21,"list")["beammajor"]["value"]
    if bunit == "K": # CO(2-1) conversion if bunit = K
        easy_K2Jy(image_co21,synsbeam21,230.53800)
        image_co21 = image_co21 + ".jy"
    else:
        print("# skip K2Jy for the CO(2-1) data")

    ### step 3/10: imregrid
    print("### momentmaps 3/10: imregrid")

    easy_imregrid(image_co10,image_co21) # co10
    image_co10 = image_co10 + ".regrid"

    pbimage = glob.glob(dir_data+"data/"+galname+"*.pb")[0]
    easy_imregrid(pbimage,image_co21,False) # pbimage
    pbimage = pbimage + ".regrid"

    ### step 4/10: imsmooth
    print("### momentmaps 4/10: imsmooth")

    beam_mask = beam_size * increment_mask # beam size for the masking
    easy_imsmooth(image_co10,beam_mask,False) # co10
    easy_imsmooth(image_co21,beam_mask,False) # co21

    ### mv the cubes to the working directory
    os.system("mkdir "+dir_data+galname)
    os.system("mv "+dir_data+"data/"+galname+"*10*smooth "\
              +dir_data+galname+"/"+galname+"_co10_"+suffix+".cube")
    os.system("mv "+dir_data+"data/"+galname+"*21*smooth "\
              +dir_data+galname+"/"+galname+"_co21_"+suffix+".cube")

    ### step 5/10: create CO(1-0) cube mask
    print("### momentmaps 5/10: create CO(1-0) cube mask")

    cube_co10 = glob.glob(dir_data+galname+"/"\
                          +galname+"*_co10_"+suffix+".cube")[0]
    thres_co10 = rms_co10 * increment_mask * thres_masking
    outmask_co10=cube_co10.replace(".cube",".mask")
    createmask(cube_co10,thres_co10,outmask_co10)

    ### step 6/10: create CO(2-1) cube mask
    print("### momentmaps 6/10: create CO(2-1) cube mask")

    cube_co21 = glob.glob(dir_data+galname+"/"\
                          +galname+"*_co21_"+suffix+".cube")[0]
    thres_co21 = rms_co21 * increment_mask * thres_masking
    outmask_co21=cube_co21.replace(".cube",".mask")
    createmask(cube_co21,thres_co21,outmask_co21)

    ### step 7/10: combine masks
    print("### momentmaps 7/10: combine masks")

    mask_combine = dir_data+galname+"/"+galname+"_combine_"+suffix+".mask"
    os.system("rm -rf " + mask_combine)
    immath(imagename = [outmask_co10, outmask_co21],
           mode = "evalexpr",
           expr = "IM0*IM1",
           outfile = mask_combine)

    beamarea = beam_area(image_co21,increment_mask)
    remove_smallmask(mask_combine,beamarea,pixelmin)

    ### step 8/10: imsmooth
    print("### step 8/10: imsmooth")

    easy_imsmooth(image_co10,beam_size,False) # co10
    easy_imsmooth(image_co21,beam_size,False) # co21

    # mv to working directory
    os.system("rm -rf "+cube_co10)
    os.system("rm -rf "+cube_co21)
    os.system("mv "+dir_data+"data/"+galname+"*10*smooth "+cube_co10)
    os.system("mv "+dir_data+"data/"+galname+"*21*smooth "+cube_co21)

    print("### step 9/10: immoments")
    moment_maps(cube_co10,chans,mask_combine,rms_co10*thres_mom)
    moment_maps(cube_co21,chans,mask_combine,rms_co21*thres_mom)

    ### pbmask
    print("### step 10/10: pb mask at " + str(pbcut))

    mask_pb = dir_data+galname+"/"+galname+"_pb_"+suffix+".mask"
    peak = imhead(pbimage,mode="list")["datamax"]
    createmask(pbimage,peak*pbcut,mask_pb)

    images_moment = glob.glob(cube_co10 + ".moment*")
    images_moment.extend(glob.glob(cube_co21+".moment*"))
    for i in range(len(images_moment)):
        outfile = images_moment[i].replace(".cube","")
        if galname == "ngc3110":
            os.system("mv " + images_moment[i] + " " \
                      + images_moment[i].replace(".cube",""))
        else:
            os.system("rm -rf " + outfile)
            immath(imagename = [images_moment[i],mask_pb],
                   mode = "evalexpr",
                   expr = "IM0*IM1",
                   outfile = outfile)
            os.system("rm -rf " + images_moment[i])

        """
        # exportfits
        os.system("rm -rf " + outfile + ".fits")
        exportfits(imagename = outfile,
                   fitsimage = outfile + ".fits",
                   velocity = True)
        """

def moments_to_ratio(dir_data,
                     galname,
                     suffix,
                     threesigma_co10,
                     threesigma_co21,
                     threesigma8_co10,
                     threesigma8_co21):
    """
    """
    print("###########################")
    print("### running moments_to_ratio")
    print("###########################")

    ### setup
    dir_data1 = dir_data+galname+"/"
    im_co10 = glob.glob(dir_data1+galname+"*co10*"+suffix+"*moment0")[0]
    im_co21 = glob.glob(dir_data1+galname+"*co21*"+suffix+"*moment0")[0]
    outmask_co10 = im_co10.replace(".moment0","_mom.mask")
    outmask_co21 = im_co21.replace(".moment0","_mom.mask")
    m8_co10 = glob.glob(dir_data1+galname+"*co10*"+suffix+"*moment8")[0]
    m8_co21 = glob.glob(dir_data1+galname+"*co21*"+suffix+"*moment8")[0]
    outmask8_co10 = m8_co10.replace(".moment8","_mom8.mask")
    outmask8_co21 = m8_co21.replace(".moment8","_mom8.mask")

    ### create a combined mask
    # mom-0
    peak = imstat(im_co10)["max"][0]
    createmask(im_co10,threesigma_co10,outmask_co10)
    peak = imstat(im_co21)["max"][0]
    createmask(im_co21,threesigma_co21,outmask_co21)

    outfile = dir_data1 + galname + "_r21_"+suffix+".mask"
    os.system("rm -rf " + outfile)
    immath(imagename = [outmask_co10, outmask_co21],
           mode = "evalexpr",
           expr = "IM0*IM1",
           outfile = outfile)

    makemask(mode = "copy",
             inpimage = outfile,
             inpmask = outfile,
             output = outfile + ":mask0",
             overwrite = True)

    #mom-8
    peak = imstat(m8_co10)["max"][0]
    createmask(m8_co10,threesigma8_co10,outmask8_co10)
    peak = imstat(im_co21)["max"][0]
    createmask(m8_co21,threesigma8_co21,outmask8_co21)

    outfile = dir_data1 + galname + "_r21_"+suffix+"_m8.mask"
    os.system("rm -rf " + outfile)
    immath(imagename = [outmask8_co10, outmask8_co21],
           mode = "evalexpr",
           expr = "IM0*IM1",
           outfile = outfile)

    makemask(mode = "copy",
             inpimage = outfile,
             inpmask = outfile,
             output = outfile + ":mask0",
             overwrite = True)

    ### create line ratio map
    #mom-0
    outfile = dir_data1 + galname + "_r21_"+suffix+".image"
    mask = dir_data1 + galname + "_r21_"+suffix+".mask"

    line_ratio(dir_data = "",
               im1 = im_co21,
               im2 = im_co10,
               outfile = outfile,
               diff = "4.",
               mask = mask)

    #mom-8
    outfile = dir_data1 + galname + "_r21_"+suffix+"_m8.image"
    mask = dir_data1 + galname + "_r21_"+suffix+"_m8.mask"

    line_ratio(dir_data = "",
               im1 = m8_co21,
               im2 = m8_co10,
               outfile = outfile,
               diff = "4.",
               mask = mask)

def sampling_co(dir_data,
                galname,
                chans,
                suffix,
                apertures,
                fov,
                beam_size,
                rms_co10,
                rms_co21,
                velres,
                sn_ratio,
                ra,
                decl,
                weight):
    """
    # 4arcsec to whatever
    """
    print("###########################")
    print("### running sampling_co")
    print("###########################")

    ### setup
    header_output = "#ra_dgr dec_dgr m0_co10 m0_co21 m2_co10 m2_co21 m8_co10 m8_co21 max_spmask mean_hamask"

    ch_end = int(chans.split("~")[1])
    ch_start = int(chans.split("~")[0])
    nchan = ch_end - ch_start + 1
    
    im_spmask = glob.glob(dir_data+"SpiralMasks/"+galname+"*_renamed.image")[0]
    im_hamask = glob.glob(dir_data+"galmasks/"+galname+"*.image")[0]
    dir_data = dir_data + galname + "/"
    image_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment0")[0]
    image_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment0")[0]
    mom2_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment2")[0]
    mom2_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment2")[0]
    mom8_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment8")[0]
    mom8_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment8")[0]

    c = SkyCoord(ra, decl)
    ra_dgr = c.ra.degree
    dec_dgr = c.dec.degree
    dec_dgr_org = dec_dgr

    dir_casa_region = dir_data + "casa_region/"
    done = glob.glob(dir_casa_region)
    if not done:
        os.mkdir(dir_casa_region)

    ### Nyquist sampling with varying aperture size
    for i in range(len(apertures)):
        print("##### sampling with aperture = " + str(apertures[i]) + ", " + weight)

        # define sampling grid at the given aperture size
        if galname == "ngc3627":
            stp_ra,stp_dec,rng_ra,rng_dec=def_step2(apertures[i],fov)
        else:
            stp_ra,stp_dec,rng_ra,rng_dec=def_step(apertures[i],fov)

        # rms calculation at the given aperture size
        Sa_co,Sb_co = def_area(image_co21,apertures[i],beam_size)
        rms_apt_co10 = rms_co10*velres*np.sqrt(nchan)/np.sqrt(Sa_co) #average
        rms_apt_co21 = rms_co21*velres*np.sqrt(nchan)/np.sqrt(Sa_co) #average

        # setup for imval txt output
        if type(apertures[i]) == int:
            name_size = "{0:02d}".format(apertures[i])
        elif type(apertures[i]) == float:
            name_size = str(apertures[i]).replace(".","p")

        product_file = dir_data+galname+"_flux_"+suffix+"_"\
                       +str(name_size)+"_"+weight+".txt"
        os.system("rm -rf "+product_file)
        f = open(product_file,"a")
        f.write(header_output+"\n")
        f.close()

        # sampling: unit = mom-0 = mean Jy/beam.km/s, mom-8 = mean Jy/beam
        images = [image_co10,
                  image_co21,
                  mom2_co10,
                  mom2_co21,
                  mom8_co10,
                  mom8_co21,
                  im_spmask,
                  im_hamask]
        thress = [rms_apt_co10*sn_ratio,
                  rms_apt_co21*sn_ratio,
                  0,
                  0,
                  rms_co10/np.sqrt(Sa_co)*sn_ratio,
                  rms_co21/np.sqrt(Sa_co)*sn_ratio,
                  0,
                  0]
        S_bms = [Sb_co, Sb_co, -1, -1, -1, -1, -1, -1]

        hexa_sampling(apertures[i],
                      images,
                      thress,
                      ra_dgr,
                      dec_dgr_org,
                      rng_ra,
                      rng_dec,
                      stp_ra,
                      stp_dec,
                      S_bms,
                      dir_casa_region,
                      product_file,
                      weight = weight)

def convolve_wise(dir_data,galname,wise_band,beam_native,targetbeam):
    """
    """
    print("###########################")
    print("### running convolve_wise")
    print("###########################")
    dir_galname = dir_data+galname+"/"
    dir_wise = dir_data+"wise/"
    imagename = glob.glob(dir_wise+galname+"_"+wise_band+"_gauss7p5.fits")[0]

    convert_str_to_beam(imagename,beam_native)
    easy_imsmooth(imagename.replace(".fits",".image")+".beam",
                  targetbeam,delete_original=False)
    os.system("mv "+imagename.replace(".fits",".image")+".beam.smooth "+dir_galname+galname+"_"+wise_band+"_"+str(targetbeam).replace(".","p")+".image")
    os.system("rm -rf "+imagename.replace(".fits",".image")+"*")

def sampling_co_wise(dir_data,
                     galname,
                     chans,
                     suffix,
                     apertures,
                     fov,
                     beam_size,
                     rms_co10,
                     rms_co21,
                     rms_w1,
                     rms_w2,
                     rms_w3,
                     velres,
                     sn_ratio,
                     ra,
                     decl,
                     weight):
    """
    # 7.5arcsec to whatever
    """
    print("###########################")
    print("### running sampling_co_wise")
    print("###########################")
    
    ### setup
    header_tmp1 = "#ra_dgr dec_dgr m0_co10 m0_co21 m2_co10 m2_co21 m8_co10 m8_co21"
    header_tmp2 = " wise1 wise2 wise3 max_spmask mean_hamask"
    header_output = header_tmp1 + header_tmp2
    
    ch_end = int(chans.split("~")[1])
    ch_start = int(chans.split("~")[0])
    nchan = ch_end - ch_start + 1
    
    im_spmask = glob.glob(dir_data+"SpiralMasks/"+galname+"*_renamed.image")[0]
    im_hamask = glob.glob(dir_data+"galmasks/"+galname+"*.image")[0]
    dir_data = dir_data + galname + "/"
    dir_wise = dir_data + "wise/"
    image_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment0")[0]
    image_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment0")[0]
    mom2_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment2")[0]
    mom2_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment2")[0]
    mom8_co10 = glob.glob(dir_data+galname+"_co10*"+suffix+"*moment8")[0]
    mom8_co21 = glob.glob(dir_data+galname+"_co21*"+suffix+"*moment8")[0]
    image_wise1 = glob.glob(dir_data+galname+"_w1_"+suffix+".image")[0]
    image_wise2 = glob.glob(dir_data+galname+"_w2_"+suffix+".image")[0]
    image_wise3 = glob.glob(dir_data+galname+"_w3_"+suffix+".image")[0]

    c = SkyCoord(ra, decl)
    ra_dgr = c.ra.degree
    dec_dgr = c.dec.degree
    dec_dgr_org = dec_dgr
    
    dir_casa_region = dir_data + "casa_region/"
    done = glob.glob(dir_casa_region)
    if not done:
        os.mkdir(dir_casa_region)

    ### Nyquist sampling with varying aperture size
    for i in range(len(apertures)):
        print("##### sampling with aperture = " + str(apertures[i]) + ", " + weight)
        
        # define sampling grid at the given aperture size
        if galname == "ngc3627":
            stp_ra,stp_dec,rng_ra,rng_dec=def_step2(apertures[i],fov)
        else:
            stp_ra,stp_dec,rng_ra,rng_dec=def_step(apertures[i],fov)

        # rms calculation at the given aperture size
        Sa_co,Sb_co = def_area(image_co21,apertures[i],beam_size)
        rms_apt_co10 = rms_co10*velres*np.sqrt(nchan)/np.sqrt(Sa_co) #average
        rms_apt_co21 = rms_co21*velres*np.sqrt(nchan)/np.sqrt(Sa_co) #average
        Sa_wise,Sb_wise = def_area(image_wise3,apertures[i],beam_size)
        rms_apt_w1 = rms_w1/np.sqrt(Sa_wise) #average
        rms_apt_w2 = rms_w2/np.sqrt(Sa_wise) #average
        rms_apt_w3 = rms_w3/np.sqrt(Sa_wise) #average

        # setup for imval txt output
        if type(apertures[i]) == int:
            name_size = "{0:02d}".format(apertures[i])
        elif type(apertures[i]) == float:
            name_size = str(apertures[i]).replace(".","p")

        product_file = dir_data+galname+"_flux_"+suffix+"_"\
                       +str(name_size)+"_"+weight+".txt"
        os.system("rm -rf "+product_file)
        f = open(product_file,"a")
        f.write(header_output+"\n")
        f.close()

        # sampling: unit = mom-0 = mean Jy/beam.km/s, mom-8 = mean Jy/beam
        images = [image_co10,
                  image_co21,
                  mom2_co10,
                  mom2_co21,
                  mom8_co10,
                  mom8_co21,
                  image_wise1,
                  image_wise2,
                  image_wise3,
                  im_spmask,
                  im_hamask]
        thress = [rms_apt_co10*sn_ratio,
                  rms_apt_co21*sn_ratio,
                  0,
                  0,
                  rms_co10/np.sqrt(Sa_co)*sn_ratio,
                  rms_co21/np.sqrt(Sa_co)*sn_ratio,
                  rms_apt_w1*sn_ratio,
                  rms_apt_w2*sn_ratio,
                  rms_apt_w3*sn_ratio,
                  0,
                  0]
        S_bms = [Sb_co, Sb_co, -1, -1, -1, -1, Sb_wise, Sb_wise, Sb_wise, -1, -1]

        hexa_sampling(apertures[i],
                      images,
                      thress,
                      ra_dgr,
                      dec_dgr_org,
                      rng_ra,
                      rng_dec,
                      stp_ra,
                      stp_dec,
                      S_bms,
                      dir_casa_region,
                      product_file,
                      weight = weight)


####################################################################################
### Define functions for moment map creation
####################################################################################
def eazy_importfits(fitsimage,defaultaxes=True):
    """
    for moment map creation
    """
    defaultaxesvalues = ['Right Ascension',
                         'Declination',
                         'Stokes',
                         'Frequency']
    imname = fitsimage.replace(".fits", ".image")
    os.system("rm -rf " + imname)
    importfits(fitsimage = fitsimage,
               imagename = imname,
               defaultaxes = defaultaxes,
               defaultaxesvalues = defaultaxesvalues)

def easy_K2Jy(imagename,synsbeam,freq):
    """
    for moment map creation
    """
    imhead(imagename = imagename,
           mode = "put",
           hdkey = "bunit",
           hdvalue = "Jy/beam")
    expr_coeff = synsbeam*synsbeam*freq*freq/1.222e6

    os.system("rm -rf " + imagename + ".jy")
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "IM0*" + str(expr_coeff),
           outfile = imagename + ".jy")
    os.system("rm -rf " + imagename)

def easy_imregrid(imagename,template,delete_original=True):
    """
    for moment map creation
    """
    os.system("rm -rf " + imagename + ".regrid")
    imregrid(imagename = imagename,
             template = template,
             output = imagename + ".regrid")

    if delete_original==True:
        os.system("rm -rf " + imagename)

def easy_imsmooth(imagename,targetbeam,delete_original=True):
    """
    for moment map creation
    """
    os.system("rm -rf " + imagename + ".smooth")
    imsmooth(imagename = imagename,
             kernel = "gauss",
             major = str(targetbeam) + "arcsec",
             minor = str(targetbeam) + "arcsec",
             pa = "0.0deg",
             targetres = True,
             outfile = imagename + ".smooth")

    if delete_original==True:
        os.system("rm -rf " + imagename)

def createmask(imagename,thres,outmask):
    """
    for moment map creation
    """
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)
        
    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")

def beam_area(imagename,increment_mask):
    """
    for moment map creation
    """
    major = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beammajor")["value"]
    minor = imhead(imagename = imagename,
                   mode = "get",
                   hdkey = "beamminor")["value"]
    pix = abs(imhead(imagename = imagename,
                     mode = "list")["cdelt1"])

    pixelsize = pix * 3600 * 180 / np.pi
    beamarea = (major * minor * np.pi/(4 * np.log(2))) \
                / (pixelsize ** 2) * increment_mask * increment_mask

    return beamarea

def remove_smallmask(outmask,beamarea,pixelmin):
    """
    for moment map creation
    """
    os.system("rm -rf " + outmask + ".all")
    os.system("cp -r " + outmask + " " + outmask + ".all")

    myia.open(outmask)
    mask = myia.getchunk()
    labeled, j = scipy.ndimage.label(mask)
    myhistogram = \
        scipy.ndimage.measurements.histogram(labeled,0,j+1,j+1)
    object_slices = scipy.ndimage.find_objects(labeled)
    threshold = beamarea * pixelmin

    for i in range(j):
        if myhistogram[i + 1] < threshold:
            mask[object_slices[i]] = 0
    myia.putchunk(mask)
    myia.done()

def moment_maps(imagename,
                chans,
                mask,
                thres,
                output_mom = [0,2,8]):
    """
    for moment map creation
    """
    # modify the header of the mask
    bmaj = imhead(imagename,"list")["beammajor"]["value"]
    bmin = imhead(imagename,"list")["beamminor"]["value"]
    bpa = imhead(imagename,"list")["beampa"]["value"]
    imhead(mask,"put","beammajor",str(bmaj)+"arcsec")
    imhead(mask,"put","beamminor",str(bmin)+"arcsec")
    imhead(mask,"put","beampa",str(bpa)+"deg")
    
    # create masked cube
    outfile = imagename + ".masked"
    os.system("rm -rf " + outfile)
    immath(imagename = [imagename, mask],
           mode = "evalexpr",
           expr = "iif(IM1 >= 1.0, IM0, 0.0)",
           outfile = outfile)

    #create moment maps using the masked cube
    for i in range(len(output_mom)):
        outfile = imagename + ".moment" + str(output_mom[i])
        os.system("rm -rf " + outfile)
        immoments(imagename = imagename + ".masked",
                  moments = [output_mom[i]],
                  chans = chans,
                  includepix = [thres, 1000000.],
                  outfile = outfile)


####################################################################################
### Define functions for line ratio map creation
####################################################################################
def line_ratio(dir_data,
               im1,
               im2,
               outfile,
               diff,
               mask = []):
    """
    """
    os.system("rm -rf " + dir_data + outfile)
    os.system("rm -rf " + dir_data + outfile + ".beforemask")
    if not mask:
        immath(imagename = [dir_data + im1, dir_data + im2],
               mode = "evalexpr",
               expr = "IM0/IM1/" + diff,
               outfile = dir_data + outfile)
    else:
        #modify the header of the mask
        maskname = dir_data + mask
        bmaj = imhead(imagename = dir_data + im1,
                      mode = "list")["beammajor"]["value"]
        bmin = imhead(imagename = dir_data + im1,
                      mode = "list")["beamminor"]["value"]
        bpa = imhead(imagename = dir_data + im1,
                     mode = "list")["beampa"]["value"]
        imhead(imagename = maskname,
               mode = "put",
               hdkey = "beammajor",
               hdvalue = str(bmaj) + "arcsec")
        imhead(imagename = maskname,
               mode = "put",
               hdkey = "beamminor",
               hdvalue = str(bmin) + "arcsec")
        imhead(imagename = maskname,
               mode = "put",
               hdkey = "beampa",
               hdvalue = str(bpa) + "deg")
        immath(imagename = [dir_data + im1, dir_data + im2],
               mode = "evalexpr",
               expr = "IM0/IM1/" + diff,
               outfile = dir_data + outfile + ".beforemask")
        immath(imagename = [dir_data + outfile + ".beforemask",
                            maskname],
               mode= "evalexpr",
               expr = "iif(IM1 >= 1.0, IM0, 0.0)",
               outfile = dir_data + outfile)
        os.system("rm -rf " + dir_data + outfile + ".beforemask")


####################################################################################
### Define functions for sampling
####################################################################################
def easy_imval(imagename,region_file,thres,S_bm):
    """
    sampling
    """
    value = imval(imagename = imagename,
                  region = region_file)
    value_masked = value["data"] * value["mask"]

    if "SpiralMasks" in imagename:
        data = value_masked.max(axis = (0, 1))
        data_mean = value_masked.mean(axis = (0, 1))

        if data_mean < data * 0.5:
            data = 0.0

    else:
        data = value_masked.mean(axis = (0, 1))
                  
        if data < thres:
            data = 0.0

    return data

def easy_imval_w(imagename,region_file,thres,S_bm):
    """
    sampling
    """
    value = imval(imagename = imagename,
                  region = region_file)
    value_masked = value["data"] * value["mask"]

    data_1d_tmp = value_masked.ravel()
    data_1d = []
    for i in range(len(data_1d_tmp)):
        if data_1d_tmp[i] > 0:
            data_1d.append(data_1d_tmp[i])

    array_1d = np.array(data_1d)

    if "SpiralMasks" in imagename:
        data = value_masked.max(axis = (0, 1))
        data_mean = value_masked.mean(axis = (0, 1))

        if data_mean < data * 0.5:
            data = 0.0

    else:
        # weighted stats
        if len(data_1d) > 1:
            data = np.average(array_1d, weights = array_1d)
        else:
            data = 0.0

        if data < thres:
            data = 0.0
    
    return data

def easy_imval_iw(imagename,region_file,thres,S_bm):
    """
    sampling
    """
    value = imval(imagename = imagename,
                  region = region_file)
    value_masked = value["data"] * value["mask"]

    data_1d_tmp = value_masked.ravel()
    data_1d = []
    for i in range(len(data_1d_tmp)):
        if data_1d_tmp[i] > 0:
            data_1d.append(data_1d_tmp[i])

    array_1d = np.array(data_1d)

    if "SpiralMasks" in imagename:
        data = value_masked.max(axis = (0, 1))
        data_mean = value_masked.mean(axis = (0, 1))
    
        if data_mean < data * 0.5:
            data = 0.0

    else:
        # weighted stats
        if len(data_1d) > 1:
            data = np.average(array_1d, weights = 1/array_1d)
        else:
            data = 0

        if data < thres:
            data = 0.0
    
    return data

def def_step(aperture,fov):
    """
    hexagonal Nyquist sampling
    """
    stp_ra = aperture / 60. / 60. # degree
    stp_dec = aperture / 60. / 60. * np.sqrt(3) # degree
    rng_ra = int(fov / aperture)
    rng_dec = int(fov / 2. / aperture)

    return stp_ra, stp_dec, rng_ra, rng_dec

def def_step2(aperture,fov):
    """
    hexagonal Nyquist sampling
    """
    stp_ra = aperture / 60. / 60. # degree
    stp_dec = aperture / 60. / 60. * np.sqrt(3) # degree
    rng_ra = int(fov / aperture)
    rng_dec = int(fov / 2. / aperture * 1.9)

    return stp_ra, stp_dec, rng_ra, rng_dec

def def_area(imagename,aperture,beam):
    """
    hexagonal Nyquist sampling
    """
    pixsize_tmp = imhead(imagename, mode="list")["cdelt1"]
    pixsize = round(abs(pixsize_tmp) * 3600 * 180 / np.pi, 2)
    S_ap = (aperture/2.) ** 2 * np.pi / pixsize ** 2 # aperture area
    S_bm = (beam/2.) ** 2 * np.pi / pixsize ** 2 # beam area

    return S_ap, S_bm

def next_ra(ra_dgr,stp_ra):
    ra_dgr = ra_dgr - stp_ra
    ra_dgr2 = ra_dgr - stp_ra / 2.

    return ra_dgr, ra_dgr2

def next_dec(dec_dgr,stp_dec):
    if dec_dgr > 0:
        dec_dgr = dec_dgr + stp_dec
        dec_dgr2 = dec_dgr + stp_dec/2.
    else:
        dec_dgr = dec_dgr - stp_dec
        dec_dgr2 = dec_dgr - stp_dec/2.

    return dec_dgr, dec_dgr2

def nyquist_photometry(product_file,
                       imagenames,
                       region_r,
                       region_h,
                       thress,
                       S_bms,
                       ra_dgr,
                       ra_dgr2,
                       dec_dgr,
                       dec_dgr2,
                       weight = "no"):
    """
    photometry and output
    """
    f = open(product_file, "a")
    R, H = [], []
    for k in range(len(imagenames)):
        if weight == "no":
           Rtmp=easy_imval(imagenames[k],region_r,thress[k],S_bms[k])
           Htmp=easy_imval(imagenames[k],region_h,thress[k],S_bms[k])
           R.append(str(Rtmp))
           H.append(str(Htmp))
        elif weight == "w":
           Rtmp=easy_imval_w(imagenames[k],region_r,thress[k],S_bms[k])
           Htmp=easy_imval_w(imagenames[k],region_h,thress[k],S_bms[k])
           R.append(str(Rtmp))
           H.append(str(Htmp))
        elif weight == "iw":
           Rtmp=easy_imval_iw(imagenames[k],region_r,thress[k],S_bms[k])
           Htmp=easy_imval_iw(imagenames[k],region_h,thress[k],S_bms[k])
           R.append(str(Rtmp))
           H.append(str(Htmp))

    f.write(str(ra_dgr)+" "+str(dec_dgr)+" "+str(" ".join(R))+"\n")
    f.write(str(ra_dgr2)+" "+str(dec_dgr2)+" "+str(" ".join(H))+"\n")
    f.close()

def write_region(region_file,ra_dgr,dec_dgr,aperture):
    """
    """
    f = open(region_file, "w")
    f.write("#CRTFv0\n")
    f.write("global coord=J2000\n")
    f.write("\n")
    f.write("circle[[" + str(round(ra_dgr, 5)) + "deg, " \
            + str(round(dec_dgr, 7)) + "deg], " \
            + str(round(aperture/2.)) + "arcsec]")
    f.write("")
    f.close()

def hexa_sampling(aperture,
                  imagenames,
                  thress,
                  ra_dgr,
                  dec_dgr_org,
                  rng_ra,
                  rng_dec,
                  stp_ra,
                  stp_dec,
                  S_bms,
                  dir_casa_region,
                  product_file,
                  weight):
    """
    """
    for i in range(rng_ra):
        ra_dgr, ra_dgr2 = next_ra(ra_dgr,stp_ra)
        dec_dgr = dec_dgr_org

        for j in range(rng_dec):
            dec_dgr, dec_dgr2 = next_dec(dec_dgr,stp_dec)
            # region R (full beam sampling)
            name_r = "R_"+str(i)+"_"+str(j)+".region"
            region_r = dir_casa_region + name_r
            write_region(region_r,ra_dgr,dec_dgr,aperture)

            # region H (full beam sampling sifted by aperture/2)
            name_h = "H_"+str(i)+"_"+str(j)+".region"
            region_h = dir_casa_region + name_h
            write_region(region_h,ra_dgr2,dec_dgr2,aperture)

            # output
            nyquist_photometry(product_file,
                               imagenames,
                               region_r,
                               region_h,
                               thress,
                               S_bms,
                               ra_dgr,
                               ra_dgr2,
                               dec_dgr,
                               dec_dgr2,
                               weight=weight)


####################################################################################
### Define functions for WISE
####################################################################################
def convert_str_to_beam(infile,beam):
    """
    round beam diameter in arcsec
    """
    ### import casa images
    if ".fits" in infile:
        done = glob.glob(infile.replace(".fits",".image"))
        if not done:
            eazy_importfits(infile,defaultaxes=False)

        imagename = infile.replace(".fits",".image")
    else:
        imagename = infile.replace(".fits",".image")

    ### str to beam
    beam = beam * u.arcsec # arcsec
    beamarea = (2*np.pi / (8*np.log(2))) * (beam**2).to(u.sr) # str

    os.system("rm -rf "+imagename+".beam")
    immath(imagename=imagename,
           outfile=imagename+".beam",
           expr = "IM0*1e6*"+str(beamarea.value))

    imhead(imagename=imagename+".beam",
           mode="put",
           hdkey="beammajor",
           hdvalue=str(beam.value)+"arcsec")

    imhead(imagename=imagename+".beam",
           mode="put",
           hdkey="beamminor",
           hdvalue=str(beam.value)+"arcsec")

    imhead(imagename=imagename+".beam",
           mode="put",
           hdkey="beampa",
           hdvalue="0.0deg")

    imhead(imagename=imagename+".beam",
           mode="put",
           hdkey="bunit",
           hdvalue="Jy/beam")

def convert_beam_to_str(infile,beam):
    ### str to beam
    beam = beam * u.arcsec # arcsec
    beamarea = (2*np.pi / (8*np.log(2))) * (beam**2).to(u.sr) # str

    os.system("rm -rf "+infile.replace(".beam", ".smooth"))
    immath(imagename=infile,
           outfile=infile.replace(".beam", ".smooth"),
           expr = "IM0*1e6*"+str(beamarea.value))



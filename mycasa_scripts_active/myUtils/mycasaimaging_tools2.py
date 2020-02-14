import os
import re
import sys
import glob
import numpy as np
import scipy.ndimage
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm
import matplotlib.patches as patches
from astropy.io import fits

# CASA imports
from taskinit import *
from importfits import importfits
from imregrid import imregrid
from imsmooth import imsmooth

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



#####################
### Main Procedure
#####################
def eazy_importfits(fitsimage,defaultaxes=True):
    """
    - 1
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
    - 2
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
    - 3
    """
    os.system("rm -rf " + imagename + ".regrid")
    imregrid(imagename = imagename,
             template = template,
             output = imagename + ".regrid")
 
    if delete_original==True:
        os.system("rm -rf " + imagename)



def easy_imsmooth(imagename,targetbeam,delete_original=True):
    """
    - 4
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
    - 5
    """
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)

    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")

    """
    makemask(mode = "copy",
             inpimage = outmask,
             inpmask = outmask,
             output = outmask + ":mask0",
             overwrite = True)
    """


def beam_area(imagename,increment_mask):
    """
    - 6
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
    - 7
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

    """
    makemask(mode = "copy",
             inpimage = outmask,
             inpmask = outmask,
             output = outmask + ":mask0",
             overwrite = True)
    """


def moment_maps(imagename,
                chans,
                mask,
                thres,
                output_mom = [0,1,2,8]):
    """
    - 8
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
                  includepix = [thres, 100000.],
                  outfile = outfile)


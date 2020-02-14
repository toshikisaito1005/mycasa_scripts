import os
import glob
import scipy
from astropy.io import fits
from astropy import units as u
from astropy.coordinates import SkyCoord

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


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/proj_jwu/"
image_co10 = dir_proj + "image_co10/co10.moment0"


#####################
### Functions
#####################
def createmask(imagename,thres,outmask):
    """
    for moment map creation
    """
    os.system("rm -rf " + outmask)
    immath(imagename = imagename,
           mode = "evalexpr",
           expr = "iif(IM0 >= " + str(thres) + ", 1.0, 0.0)",
           outfile = outmask)


#####################
### Main
#####################
os.system("rm -rf " + image_co10 + ".mask")
createmask(image_co10,0.1,image_co10 + ".mask")

os.system("rm -rf " + image_co10 + ".smooth")
imsmooth(imagename = image_co10 + ".mask",
         targetres = True,
         major = "2.1arcsec",
         minor = "2.1arcsec",
         pa = "0deg",
         outfile = image_co10 + ".smooth")

createmask(image_co10 + ".smooth",1.0,image_co10 + ".smooth.mask")
os.system("rm -rf " + image_co10 + ".mask")
os.system("rm -rf " + image_co10 + ".smooth")

imagenames = glob.glob(dir_proj + "*/*.moment0")
for i in range(len(imagenames)):
    immath(imagename = [imagenames[i],image_co10 + ".smooth.mask"],
           expr = "IM0*IM1",
           outfile = imagenames[i] + ".masked")



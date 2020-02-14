import os
import glob
import scipy
import numpy as np
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
dir_proj = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
image_catom = glob.glob(dir_proj + "image_ci10/ci10.moment0")[0]
image_co10 = glob.glob(dir_proj + "image_co10/co10.moment0")[0]
box = "103,115,180,192"

zspec = 0.01818
DL = 78.2 # Mpc
Tex = 21.3 # K
Tex2 = Tex + 10
beamarea = 22.382 # number of pixel


#####################
### definition
#####################
# CI(1-0) observed frequency
obsfreq = 492.16065100 / (1 + 0.01818)
obsfreq_co10 = 115.27120 / (1 + 0.01818)

# flux (Jy.km/s) to luminosity (K.km/spc^2)
eqn_flux2luminosity = 3.25e+7 / obsfreq**2 * DL**2 / (1 + zspec)**3
eqn_flux2luminosity_co10 = 3.25e+7 / obsfreq_co10**2 * DL**2 / (1 + zspec)**3


#####################
### Main
#####################
# CI luminosity
os.system("rm -rf " + image_catom + ".luminosity")
immath(imagename = image_catom,
       expr = "IM0/"+str(beamarea)+"*"+str(eqn_flux2luminosity),
       outfile = image_catom + ".luminosity")

# CO(1-0) luminosity
os.system("rm -rf " + image_co10 + ".luminosity")
immath(imagename = image_co10,
       expr = "IM0/"+str(beamarea)+"*"+str(eqn_flux2luminosity_co10),
       outfile = image_co10 + ".luminosity")

os.system("rm -rf *.last")

import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim
import mycasaimaging_tools2 as myim2
import mycasaimaging_Nyquist as Nyq
from astropy import units as u
from astropy.coordinates import SkyCoord



#####################
### Define Parameters
#####################
#multiplier_co10=0.01 # peak * multiplier
#multiplier_co21=0.005 # peak * multiplier



#####################
### Main Procedure
#####################
### setup
dir_data1 = dir_data + galname + "/"
im_co10=glob.glob(dir_data1+galname+"*co10*"+suffix+"*m*0.fits")[0]
im_co21=glob.glob(dir_data1+galname+"*co21*"+suffix+"*m*0.fits")[0]
outmask_co10 = im_co10.replace(".moment0.fits","_mom.mask")
outmask_co21 = im_co21.replace(".moment0.fits","_mom.mask")
m8_co10=glob.glob(dir_data1+galname+"*co10*"+suffix+"*m*8.fits")[0]
m8_co21=glob.glob(dir_data1+galname+"*co21*"+suffix+"*m*8.fits")[0]
outmask8_co10 = m8_co10.replace(".moment8.fits","_mom8.mask")
outmask8_co21 = m8_co21.replace(".moment8.fits","_mom8.mask")



### create mask for each moment map
# mom-0
peak = imstat(im_co10)["max"][0]
myim2.createmask(im_co10,threesigma_co10,outmask_co10)
peak = imstat(im_co21)["max"][0]
myim2.createmask(im_co21,threesigma_co21,outmask_co21)

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
myim2.createmask(m8_co10,threesigma8_co10,outmask8_co10)
peak = imstat(im_co21)["max"][0]
myim2.createmask(m8_co21,threesigma8_co21,outmask8_co21)

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

myim.line_ratio(dir_data = "",
                im1 = im_co21,
                im2 = im_co10,
                outfile = outfile,
                diff = "4.",
                mask = mask)

fitsimage = outfile.replace(".image", ".fits")
os.system("rm -rf " + fitsimage)
exportfits(imagename = outfile,
           fitsimage = fitsimage)

#mom-8
outfile = dir_data1 + galname + "_r21_"+suffix+"_m8.image"
mask = dir_data1 + galname + "_r21_"+suffix+"_m8.mask"

myim.line_ratio(dir_data = "",
                im1 = m8_co21,
                im2 = m8_co10,
                outfile = outfile,
                diff = "4.",
                mask = mask)

fitsimage = outfile.replace(".image", ".fits")
os.system("rm -rf " + fitsimage)
exportfits(imagename = outfile,
           fitsimage = fitsimage)

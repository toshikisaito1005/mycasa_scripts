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
def makeratio(im0,im1,name_im0,name_im1,cliplevel1,factor):
    os.system("rm -rf " + dir_proj + "image_ratio/ratio_"+name_im0+"_"+name_im1+".image_tmp")
    peak1 = imstat(im1)["max"][0]
    os.system("rm -rf " + im1 + ".complete")
    immath(imagename = im1,
           expr = "iif(IM0 >= " + str(peak1*cliplevel1) + ", IM0, 0.0)",
           outfile = im1 + ".complete")

    ratio_image = dir_proj + "image_ratio/ratio_"+name_im0+"_"+name_im1+".image"
    os.system("rm -rf " + ratio_image)
    immath(imagename = [im0,im1 + ".complete"],
           expr = "iif(IM0>=0,IM0/IM1/"+str(factor)+", 0.0)",
           outfile = ratio_image)

    os.system("rm -rf " + im1 + ".complete")


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/"
imagenames = glob.glob(dir_proj + "image_uvlim_*/*moment0")
imagenames.sort()

os.system("rm -rf " + dir_proj + "image_ratio/")
os.system("mkdir " + dir_proj + "image_ratio/")

m0_12co10 = imagenames[0]
m0_12co21 = imagenames[1]
m0_13co10 = imagenames[2]
m0_13co21 = imagenames[3]

cliplevel1 = [0.03,0.08,0.03,0.08]
factor = [4.0,4.0,230.53800000**2/220.39868420**2,115.27120180**2/110.20135430**2]
name_im0 = ["12co21","13co21","12co21","12co10"]
name_im1 = ["12co10","13co10","13co21","13co10"]
im0 = [m0_12co21,m0_13co21,m0_12co21,m0_12co10]
im1 = [m0_12co10,m0_13co10,m0_13co21,m0_13co10]

for i in range(len(im0)):
    makeratio(im0[i],im1[i],name_im0[i],name_im1[i],cliplevel1[i],factor[i])

### exportfits
imagenames = glob.glob(dir_proj + "image_ratio/ratio*.image")

for i in range(len(imagenames)):
    os.system("rm -rf " + imagenames[i].replace(".image",".fits"))
    exportfits(imagename = imagenames[i],
               fitsimage = imagenames[i].replace(".image",".fits"))

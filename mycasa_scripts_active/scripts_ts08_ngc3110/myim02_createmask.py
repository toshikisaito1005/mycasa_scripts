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
dir_proj = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/data/"
imagenames = glob.glob(dir_proj + "ngc3110_alma_12co10_l20_na.cube.regrid")
imagenames.reverse()
noises = [0.001]
pbcuts = [0.5]
snr_mom = 3.0
percent = 0.01

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
    imhead(imagename = outmask,
           mode = "del",
           hdkey = "beammajor")

def beam_area(imagename):
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
    beamarea_arcsec = major * minor * np.pi/(4 * np.log(2))
    beamarea_pix = beamarea_arcsec / (pixelsize ** 2)
                   
    return beamarea_pix


#####################
### Main
#####################
i = 0
# prepare workinf directory e.g., image_co10
name_line = imagenames[i].split("ngc3110_")[1].split("_")[1]
dir_image = dir_proj+"../image_"+name_line+"/"
pbimage = dir_image + name_line + "_cube.pb"
cubeimage = dir_image + name_line + "_cube.image"
os.system("rm -rf " + dir_image)
os.system("mkdir " + dir_image)
os.system("cp -r " + imagenames[i] + " " + cubeimage)
os.system("cp -r " + glob.glob(dir_proj+"*"+name_line+"*"+"*flux*")[0] + " " + pbimage)

print("### woking on " + name_line)
# imsmooth
cubesmooth1 = cubeimage.replace(".image",".smooth1") # 4.0 mJy
imsmooth(imagename = cubeimage,
         targetres = True,
         major = "3.0arcsec",
         minor = "3.0arcsec",
         pa = "0deg",
         outfile = cubesmooth1)

cubesmooth2 = cubeimage.replace(".image",".smooth2") # 10 mJy
imsmooth(imagename = cubeimage,
         targetres = True,
         major = "5.5arcsec",
         minor = "5.5arcsec",
         pa = "0deg",
         outfile = cubesmooth2)

# create mask
createmask(cubeimage,noises[i]*1.*2.5,dir_image+name_line+"_mask0.image")
createmask(cubesmooth1,noises[i]*2.*3.5,dir_image+name_line+"_mask1.image")
createmask(cubesmooth2,noises[i]*5.*5.5,dir_image+name_line+"_mask2.image")
    
immath(imagename = [dir_image+name_line+"_mask0.image",
                    dir_image+name_line+"_mask1.image",
                    dir_image+name_line+"_mask2.image"],
       expr = "iif(IM0+IM1+IM2 >= 2.0, 1.0, 0.0)",
       outfile = dir_image+name_line+"_mask_tmp.image")
        
immath(imagename = [dir_image+name_line+"_mask_tmp.image",
                    dir_image+name_line+"_cube.pb"],
       expr = "iif(IM1 >= "+str(pbcuts[i])+", IM0, 0.0)",
       outfile = "ngc3110_mask.cube")

os.system("rm -rf "+dir_image+name_line+"_cube.smooth1")
os.system("rm -rf "+dir_image+name_line+"_cube.smooth2")
os.system("rm -rf "+dir_image+name_line+"_mask0.image")
os.system("rm -rf "+dir_image+name_line+"_mask1.image")
os.system("rm -rf "+dir_image+name_line+"_mask2.image")
os.system("rm -rf "+dir_image+name_line+"_mask_tmp.image")
os.system("rm -rf *.last")

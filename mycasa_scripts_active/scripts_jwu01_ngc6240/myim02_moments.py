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
dir_proj = "/Users/saito/data/proj_jwu/data/"
imagenames = glob.glob(dir_proj + "*.smooth.regrid")
imagenames.sort()
noises = [0.0011,0.005,0.0006,0.0004,0.0004]
pbcuts = [0.75,0.35,0.9,0.9,0.9]

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


#####################
### Main
#####################
for i in range(len(imagenames)):
    # prepare workinf directory e.g., image_co10
    name_line = imagenames[i].split("ngc6240_")[1].split("_")[0]
    dir_image = dir_proj+"../image_"+name_line+"/"
    pbimage = dir_image + name_line + "_cube.pb"
    cubeimage = dir_image + name_line + "_cube.image"
    os.system("rm -rf " + dir_image)
    os.system("mkdir " + dir_image)
    os.system("cp -r " + imagenames[i] + " " + cubeimage)
    os.system("cp -r " + imagenames[i].replace("smooth","pb") + " " + pbimage)

    print("### woking on " + name_line)
    # noise histgrams


    # imsmooth
    cubesmooth1 = cubeimage.replace(".image",".smooth1") # 4.0 mJy
    imsmooth(imagename = cubeimage,
             targetres = True,
             major = "1.0arcsec",
             minor = "1.0arcsec",
             pa = "0deg",
             outfile = cubesmooth1)

    cubesmooth2 = cubeimage.replace(".image",".smooth2") # 10 mJy
    imsmooth(imagename = cubeimage,
             targetres = True,
             major = "3.5arcsec",
             minor = "3.5arcsec",
             pa = "0deg",
             outfile = cubesmooth2)

    # create mask
    createmask(cubeimage,noises[i]*1.*2.5,dir_image+"/"+name_line+"_mask0.image")
    createmask(cubesmooth1,noises[i]*2.*3.5,dir_image+"/"+name_line+"_mask1.image")
    createmask(cubesmooth2,noises[i]*5.*8.5,dir_image+"/"+name_line+"_mask2.image")
    
    immath(imagename = [dir_image+"/"+name_line+"_mask0.image",
                        dir_image+"/"+name_line+"_mask1.image",
                        dir_image+"/"+name_line+"_mask2.image",
                        dir_image+"/"+name_line+"_cube.pb"],
           expr = "iif(IM0+IM1+IM2 >= 2.0, 1.0, 0.0)",
           outfile = dir_image+"/"+name_line+"_mask_tmp.image")
        
    immath(imagename = [dir_image+"/"+name_line+"_mask_tmp.image",
                        dir_image+"/"+name_line+"_cube.pb"],
           expr = "iif(IM1 >= "+str(pbcuts[i])+", IM0, 0.0)",
           outfile = dir_image+"/"+name_line+"_mask.image")

    os.system("rm -rf "+dir_image+"/"+name_line+"_cube.smooth1")
    os.system("rm -rf "+dir_image+"/"+name_line+"_cube.smooth2")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask0.image")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask1.image")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask2.image")
    os.system("rm -rf "+dir_image+"/"+name_line+"_mask_tmp.image")
    
    impbcor(imagename = cubeimage,
            pbimage = pbimage,
            outfile = cubeimage+".pbcor")
            
    immath(imagename = [cubeimage+".pbcor",dir_image+"/"+name_line+"_mask.image"],
           expr = "IM0*IM1",
           outfile = cubeimage+".pbcor.masked")
    
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [0],
              includepix = [noises[i],100000.],
              outfile = dir_image+"/"+name_line+".moment0")
        
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [1],
              includepix = [noises[i],100000.],
              outfile = dir_image+"/"+name_line+".moment1")
              
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [8],
              includepix = [noises[i],100000.],
              outfile = dir_image+"/"+name_line+".moment8")



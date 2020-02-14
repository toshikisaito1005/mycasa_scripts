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
noises = [0.0010,0.0010,0.0013,0.0013,0.0011,0.0011,0.0008,0.0008,0.0005]
pbcuts = [0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25,0.25]
snr_mom = 3.0
percents = [0.01,0.01,0.01,0.01,0.06,0.06,0.02,0.02,0.02]


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
maskimage = "ngc3110_mask.cube"
imagenames = glob.glob(dir_proj + "*cube.uvlim.regrid")
imagenames.sort()

for i in range(len(imagenames)):
    # prepare working directory e.g., image_co10
    name_line = imagenames[i].split("ngc3110_")[1].split("_")[1]
    dir_image = dir_proj+"../image_uvlim_"+name_line+"/"
    pbimage = dir_image + name_line + "_cube.pb"
    cubeimage = dir_image + name_line + "_cube.image"
    os.system("rm -rf " + dir_image)
    os.system("mkdir " + dir_image)
    os.system("cp -r " + imagenames[i] + " " + cubeimage)
    os.system("cp -r " + glob.glob(dir_proj+"*"+name_line+"*"+"*flux*")[0] + " " + pbimage)

    print("### woking on " + name_line)
    
    if "13co21" in cubeimage:
        os.system("cp -r " + cubeimage + " " + cubeimage+".pbcor")
    else:
        impbcor(imagename = cubeimage,
                pbimage = pbimage,
                cutoff = pbcuts[i],
                outfile = cubeimage+".pbcor")

    immath(imagename = [cubeimage+".pbcor",maskimage],
           expr = "iif( IM0>=" + str(noises[i]*snr_mom) + ", IM0*IM1, 0.0)",
           outfile = cubeimage+".pbcor.masked")

    immath(imagename = cubeimage+".pbcor.masked",
           expr = "iif( IM0>0, 0.1, 0.0)", # 0.1 = 1/Vch
           outfile = cubeimage+".pbcor.maskedTF")

    immoments(imagename = cubeimage+".pbcor.maskedTF",
              moments = [0],
              outfile = dir_image+name_line+".moment0.noise_tmp") # Nch

    beamarea_pix = beam_area(dir_image+name_line+".moment0.noise_tmp")
    immath(dir_image+name_line+".moment0.noise_tmp",
           expr = "10*sqrt(IM0)*"+str(noises[i])+"/"+str(np.sqrt(beamarea_pix)),
           outfile = dir_image+name_line+".moment0.noise_Jykms")

    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [0],
              #includepix = [noises[i]*3.0,10000.],
              outfile = dir_image+name_line+".moment0_tmp")
        
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [1],
              #includepix = [noises[i]*3.0,10000.],
              outfile = dir_image+name_line+".moment1_tmp")
              
    immoments(imagename = cubeimage+".pbcor.masked",
              moments = [8],
              #includepix = [noises[i]*3.0,10000.],
              outfile = dir_image+name_line+".moment8_tmp")

    # masking
    peak = imstat(dir_image+name_line+".moment0_tmp")["max"][0]

    immath(imagename = [dir_image+name_line+".moment0_tmp",
                        dir_image+name_line+".moment0_tmp"],
           expr = "iif( IM0>=" + str(peak*percents[i]) + ", IM1, 0.0)",
           outfile = dir_image+name_line+".moment0")

    immath(imagename = [dir_image+name_line+".moment0_tmp",
                        dir_image+name_line+".moment1_tmp"],
           expr = "iif( IM0>=" + str(peak*percents[i]) + ", IM1, 0.0)",
           outfile = dir_image+name_line+".moment1")

    immath(imagename = [dir_image+name_line+".moment0_tmp",
                        dir_image+name_line+".moment8_tmp"],
           expr = "iif( IM0>=" + str(peak*percents[i]) + ", IM1, 0.0)",
           outfile = dir_image+name_line+".moment8")

    exportfits(imagename = dir_image+name_line+".moment0",
               fitsimage = dir_image+name_line+".moment0.fits")

    exportfits(imagename = dir_image+name_line+".moment1",
               fitsimage = dir_image+name_line+".moment1.fits")

    os.system("rm -rf " + cubeimage+".pbcor.maskedTF")
    os.system("rm -rf " + dir_image+name_line+".moment0.noise_tmp")
    os.system("rm -rf " + dir_image+name_line+".moment0_tmp")
    os.system("rm -rf " + dir_image+name_line+".moment1_tmp")
    os.system("rm -rf " + dir_image+name_line+".moment8_tmp")

os.system("rm -rf " + maskimage)
os.system("rm -rf *.last")

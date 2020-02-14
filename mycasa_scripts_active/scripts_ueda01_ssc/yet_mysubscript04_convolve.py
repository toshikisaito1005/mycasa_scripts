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
array = "12m7mtp" # "12m7mtp" or "12m7m" or "12m"
dir_proj = "/Users/saito/data/myproj_published/proj_ju01_ssc/am2038_"+array+"_na/"
imagename = glob.glob(dir_proj + "*.image")[0]
noise = 0.0025 # this is wrong when you convolve the datacube.
pbcut = 0.8
snr_mom = 2.5
percent = 0.05
beam = 6.0 # float

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
# imsmooth original
output_original = imagename.replace(".image",".smooth")
os.system("rm -rf " + output_original)
imsmooth(imagename = imagename,
         targetres = True,
         major = str(beam)+"arcsec",
         minor = str(beam)+"arcsec",
         pa = "0deg",
         outfile = output_original)
imagename = output_original

# imsmooth
cubesmooth1 = imagename.replace(".smooth",".smooth1")
os.system("rm -rf " + cubesmooth1)
imsmooth(imagename = imagename,
         targetres = True,
         major = "7.0arcsec",
         minor = "7.0arcsec",
         pa = "0deg",
         outfile = cubesmooth1)

cubesmooth2 = imagename.replace(".smooth",".smooth2")
os.system("rm -rf " + cubesmooth2)
imsmooth(imagename = imagename,
         targetres = True,
         major = "10.0arcsec",
         minor = "10.0arcsec",
         pa = "0deg",
         outfile = cubesmooth2)

# create mask
createmask(imagename,noise*snr_mom,
           imagename.replace(".smooth",".mask0.image"))
createmask(cubesmooth1,noise*snr_mom*beam/2.5,
           imagename.replace(".smooth",".mask1.image"))
createmask(cubesmooth2,noise*snr_mom*beam/1.5,
           imagename.replace(".smooth",".mask2.image"))

os.system("rm -rf " + imagename.replace(".smooth",".mask_tmp.image"))
immath(imagename = [imagename.replace(".smooth",".mask0.image"),
                    imagename.replace(".smooth",".mask1.image"),
                    imagename.replace(".smooth",".mask2.image")],
       expr = "iif(IM0+IM1+IM2 >= 2.0, 1.0, 0.0)",
       outfile = imagename.replace(".smooth",".mask_tmp.image"))

os.system("rm -rf " + imagename.replace(".smooth",".mask.image"))
os.system("rm -rf " + imagename.replace(".smooth",".mask_all.image"))
immath(imagename = [imagename.replace(".smooth",".mask_tmp.image"),
                    imagename.replace(".smooth",".pb")],
       expr = "iif(IM1 >= "+str(pbcut)+", IM0, 0.0)",
       outfile = imagename.replace(".smooth",".mask.image"))

os.system("rm -rf "+imagename.replace(".smooth",".smooth1"))
os.system("rm -rf "+imagename.replace(".smooth",".smooth2"))
os.system("rm -rf "+imagename.replace(".smooth",".mask0.image"))
os.system("rm -rf "+imagename.replace(".smooth",".mask1.image"))
os.system("rm -rf "+imagename.replace(".smooth",".mask2.image"))
os.system("rm -rf "+imagename.replace(".smooth",".mask_tmp.image"))

os.system("rm -rf " + imagename+".pbcor")
impbcor(imagename = imagename,
        pbimage = imagename.replace(".smooth",".pb"),
        cutoff = pbcut,
        outfile = imagename+".pbcor")

mask_use_here = imagename.replace(".smooth",".mask.image")

os.system("rm -rf " + imagename+".pbcor.masked")
immath(imagename = [imagename+".pbcor",mask_use_here],
       expr = "iif( IM0>=" + str(noise*snr_mom) + ", IM0*IM1, 0.0)",
       outfile = imagename+".pbcor.masked")

"""
immath(imagename = imagename+".pbcor.masked",
       expr = "iif( IM0>0, 0.1, 0.0)", # 0.1 = 1/Vch
       outfile = imagename+".pbcor.maskedTF")

immoments(imagename = cubeimage+".pbcor.maskedTF",
          moments = [0],
          outfile = dir_image+name_line+".moment0.noise_tmp") # Nch

beamarea_pix = beam_area(dir_image+name_line+".moment0.noise_tmp")
immath(dir_image+name_line+".moment0.noise_tmp",
       expr = "10*sqrt(IM0)*"+str(noise)+"/"+str(np.sqrt(beamarea_pix)),
       outfile = dir_image+name_line+".moment0.noise_Jykms")
"""

beamstr = str(beam).replace(".","p")
os.system("rm -rf "+imagename.replace(".smooth","_"+beamstr+".moment*"))
immoments(imagename = imagename+".pbcor.masked",
          moments = [0],
          includepix = [noise*2.5,1000000.],
          outfile = imagename.replace(".smooth","_"+beamstr+".moment0"))
        
immoments(imagename = imagename+".pbcor.masked",
          moments = [1],
          includepix = [noise*2.5,1000000.],
          outfile = imagename.replace(".smooth","_"+beamstr+".moment1"))
              
immoments(imagename = imagename+".pbcor.masked",
          moments = [8],
          includepix = [noise*2.5,1000000.],
          outfile = imagename.replace(".smooth","_"+beamstr+".moment8"))

os.system("rm -rf *.last")

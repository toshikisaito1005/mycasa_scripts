import os
import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord


#####################
### set keys
#####################
dir_project = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628","ngc3627","ngc4321"]
outputs = ["env_all_04p0.mask.image",
           "env_all_08p0.mask.image",
           "env_all_04p0.mask.image"]

#####################
### Main Procedure
#####################
for i in range(len(gals)):
  galname = gals[i]
  output = outputs[i]
  #
  fits_arm = glob.glob(dir_project + galname + "_r21/env_*arm*.fits")
  fits_bulge = glob.glob(dir_project + galname + "_r21/env_*bulge*.fits")
  fits_bar = glob.glob(dir_project + galname + "_r21/env_*bar_*.fits")
  fits_barend = glob.glob(dir_project + galname + "_r21/env_*barend_*.fits")
  fitsimages = np.r_[fits_arm, fits_bulge, fits_bar, fits_barend]
  #
  if galname=="ngc0628":
    os.system("rm -rf " + output)
    immath(imagename = fitsimages,
      expr = "iif(IM1>0, IM1*2, IM0)",
      outfile = output)
  elif galname=="ngc4321":
    os.system("rm -rf " + output + "_tmp")
    immath(imagename = fitsimages,
      expr = "iif(IM2>0, IM2*3, IM0)",
      outfile = output + "_tmp")
    #
    os.system("rm -rf " + output)
    immath(imagename = [output + "_tmp", fits_bulge[0]],
      expr = "iif(IM1>0, IM1*2, IM0)",
      outfile = output)
    #
    os.system("rm -rf " + output + "_tmp*")
    #
  elif galname=="ngc3627":
    os.system("rm -rf " + output + "_tmp")
    immath(imagename = fitsimages,
      expr = "iif(IM1>0, IM1*2, IM0)",
      outfile = output + "_tmp")
    #
    os.system("rm -rf " + output + "_tmp2")
    immath(imagename = [output + "_tmp", fits_bar[0]],
      expr = "iif(IM1>0, IM1*3, IM0)",
      outfile = output + "_tmp2")
    #
    os.system("rm -rf " + output)
    immath(imagename = [output + "_tmp2", fits_barend[0]],
      expr = "iif(IM1>0, IM1*3, IM0)", # or IM1*4 if bar-end is needed.
      outfile = output)
    #
    os.system("rm -rf " + output + "_tmp*")
    #
  os.system("rm -rf " + dir_project + galname + "_r21/" + output.replace(".image",".fits"))
  exportfits(imagename = output,
    fitsimage = dir_project + galname + "_r21/" + output.replace(".image",".fits"))
  os.system("rm -rf " + output)


os.system("rm -rf *.last")

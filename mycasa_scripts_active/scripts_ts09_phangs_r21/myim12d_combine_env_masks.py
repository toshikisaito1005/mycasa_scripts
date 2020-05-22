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
exprs = ["IM0 + IM1*2", "iif()"
         "IM0 + IM1*2 + IM2*3 + IM3*4",
         "IM0 + IM1*2"]
outputs = ["env_all_04p0.mask.image",
           "env_all_08p0.mask.image",
           "env_all_04p0.mask.image"]

#####################
### Main Procedure
#####################
for i in range(len(gals)):
  galname = gals[i]
  expr = exprs[i]
  output = outputs[i]
  #
  fits_arm = glob.glob(dir_project + galname + "_r21/env_*arm*.fits")
  fits_bulge = glob.glob(dir_project + galname + "_r21/env_*bulge*.fits")
  fits_bar = glob.glob(dir_project + galname + "_r21/env_*bar_*.fits")
  fits_barend = glob.glob(dir_project + galname + "_r21/env_*barend_*.fits")
  fitsimages = np.r_[fits_arm, fits_bulge, fits_bar, fits_barend]
  #
  os.system("rm -rf " + output)
  immath(imagename = fitsimages,
    expr = expr,
    outfile = output)

  os.system("rm -rf " + output.replace(".image",".fits"))
  exportfits(imagename = output,
    fitsimage = dir_project + galname + "_r21/" + output.replace(".image",".fits"))
  os.system("rm -rf " + output)


os.system("rm -rf *.last")

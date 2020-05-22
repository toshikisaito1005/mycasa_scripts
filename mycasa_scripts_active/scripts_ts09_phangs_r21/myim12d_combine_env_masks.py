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


#####################
### Main Procedure
#####################
galname = gals[i]
fitsimages = glob.glob(dir_project + galname + "_r21/env_*.fits")



os.system("rm -rf *.last")

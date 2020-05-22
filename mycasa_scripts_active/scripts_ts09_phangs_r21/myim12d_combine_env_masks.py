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
fits_arm = glob.glob(dir_project + galname + "_r21/env_*arm*.fits")
fits_bulge = glob.glob(dir_project + galname + "_r21/env_*bulge*.fits")
fits_bar = glob.glob(dir_project + galname + "_r21/env_*bar_*.fits")
fits_barend = glob.glob(dir_project + galname + "_r21/env_*barend_*.fits")
fitsimages = np.r_[fits_arm, fits_bulge, fits_bar, fits_barend]
#


os.system("rm -rf *.last")

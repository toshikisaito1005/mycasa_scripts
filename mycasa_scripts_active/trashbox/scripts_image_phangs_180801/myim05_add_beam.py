import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt
sys.path.append(os.getcwd() + "/../")
import mycasaanalysis_tools as myana

#####################
### Main Procedure
#####################
dir_data = "../../phangs/co_ratio/photmetry/"

fitsimages = glob.glob(dir_data + "*.fits")

for i in range(len(fitsimages)):
    imagename = fitsimages[i].replace(".fits", ".image")
    os.system("rm -rf " + imagename)
    importfits(fitsimage = fitsimages[i],
               imagename = imagename)
    imhead(imagename = imagename,
           mode = "add",
           hdkey = "beammajor",
           hdvalue = "5.0arcsec")
    imhead(imagename = imagename,
           mode = "add",
           hdkey = "beamminor",
           hdvalue = "5.0arcsec")
    exportfits(imagename = imagename,
               fitsimage = fitsimages[i],
               overwrite = True)
    os.system("rm -rf " + imagename)

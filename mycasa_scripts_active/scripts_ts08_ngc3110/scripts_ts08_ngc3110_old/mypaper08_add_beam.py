import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt
sys.path.append(os.getcwd() + "/../")
import mycasaanalysis_tools3 as myana

#####################
### Main Procedure
#####################
dir_data = "../../ngc3110/ana/data_nyquist/"
plt.rcParams["font.size"] = 14

fitsimages = glob.glob(dir_data + "*.fits")

for i in range(len(fitsimages)):
    imagename = fitsimages[i].replace(".fits", ".image")
    os.system("rm -rf " + imagename)
    importfits(fitsimage = fitsimages[i],
               imagename = imagename)
    imhead(imagename = imagename,
           mode = "add",
           hdkey = "beammajor",
           hdvalue = "3.0arcsec")
    imhead(imagename = imagename,
           mode = "add",
           hdkey = "beamminor",
           hdvalue = "3.0arcsec")
    exportfits(imagename = imagename,
               fitsimage = fitsimages[i],
               overwrite = True)
    os.system("rm -rf " + imagename)

import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data = "../../ngc3110/ana/data_nyquist/"

#####################
### Main Procedure
#####################
imagenames = [[dir_data + "nyquist_co21_m0_uvlim.fits",
               dir_data + "nyquist_co10_m0_uvlim.fits"],
              [dir_data + "nyquist_13co21_m0_uvlim.fits",
               dir_data + "nyquist_13co10_m0_uvlim.fits"],
              [dir_data + "nyquist_co10_m0_uvlim.fits",
               dir_data + "nyquist_13co10_m0_uvlim.fits"],
              [dir_data + "nyquist_co21_m0_uvlim.fits",
               dir_data + "nyquist_13co21_m0_uvlim.fits"]]
ratioimages = [dir_data + "nyquist_R_co21_co10.image",
               dir_data + "nyquist_R_13co21_13co10.image",
               dir_data + "nyquist_R_co10_13co10.image",
               dir_data + "nyquist_R_co21_13co21.image"]

for i in range(len(imagenames)):
    os.system("rm -rf " + ratioimages[i])
    immath(imagename = imagenames[i],
           mode = "evalexpr",
           expr = "IM0/IM1",
           outfile = ratioimages[i])
    fitsimage = ratioimages[i].replace("image", "fits")
    os.system("rm -rf " + fitsimage)
    exportfits(imagename = ratioimages[i],
               fitsimage = fitsimage)
    os.system("rm -rf " + ratioimages[i])


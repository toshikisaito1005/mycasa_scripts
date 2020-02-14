import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_fits = "../../ALMA_ACA_co10/fits/"
dir_data = "../../ALMA_ACA_co10/fits/data_aca/"

imagenames = glob.glob(dir_data + "*.moment*")

for i in range(len(imagenames)):
    fitsimage = dir_fits \
        + imagenames[i].split("/")[5].replace(".image", "") \
        + ".fits"
    os.system("rm -rf " + fitsimage)
    exportfits(imagename = imagenames[i],
        velocity = True,
        fitsimage = fitsimage)
    print(fitsimage)


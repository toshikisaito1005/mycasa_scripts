import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_fits = "../../proposal/alma_cycle6/"
dir_data = "../../proposal/alma_cycle6/"

imagenames = glob.glob(dir_data + "*.moment*")

for i in range(len(imagenames)):
    fitsimage = dir_fits \
        + imagenames[i].split("/")[4].replace(".image", "") \
        + ".fits"
    os.system("rm -rf " + fitsimage)
    exportfits(imagename = imagenames[i],
        velocity = True,
        fitsimage = fitsimage)
    print(fitsimage)


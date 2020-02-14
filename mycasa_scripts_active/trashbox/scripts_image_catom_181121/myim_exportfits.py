import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim




dir_data = ["../../iras18293/products/line/",
            "../../iras18293/products/line_uvlim/"]


for i in range(len(dir_data)):
    imagenames = glob.glob(dir_data[i] + "*.moment*")
    imagenames2 = glob.glob(dir_data[i] + "R_*.image")
    imagenames.extend(imagenames2)
    for j in range(len(imagenames)):
        fitsimage = dir_data[i] \
            + imagenames[j].split("/")[5].replace(".image", "") \
            + ".fits"
        os.system("rm -rf " + fitsimage)
        exportfits(imagename = imagenames[j],
            velocity = True,
            fitsimage = fitsimage)
        print(fitsimage)
        os.system("rm -rf " + imagenames[j])


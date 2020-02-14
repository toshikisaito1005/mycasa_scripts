import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


done = glob.glob("../../ngc3110/ana/product/")
if not done:
    os.mkdir("../../ngc3110/ana/product/")


dir_fits = "../../ngc3110/ana/product/fits/"
done = glob.glob(dir_fits)
if not done:
    os.mkdir(dir_fits)


dir_data = ["../../ngc3110/ana/datacube_line/",
            "../../ngc3110/ana/datacube_line_uv_smooth/"]


for i in range(len(dir_data)):
    imagenames = glob.glob(dir_data[i] + "*.image")
    for j in range(len(imagenames)):
        fitsimage = dir_fits \
            + imagenames[j].split("/")[5].replace(".image", ".fits")
        os.system("rm -rf " + fitsimage)
        exportfits(imagename = imagenames[j],
            velocity = True,
            fitsimage = fitsimage)


for i in range(len(dir_data)):
    imagenames = glob.glob(dir_data[i] + "*.moment*")
    for j in range(len(imagenames)):
        fitsimage = dir_fits \
            + imagenames[j].split("/")[5].replace(".image", "") \
            + ".fits"
        os.system("rm -rf " + fitsimage)
        exportfits(imagename = imagenames[j],
            velocity = True,
            fitsimage = fitsimage)
        print(imagenames[j])
        print(fitsimage)


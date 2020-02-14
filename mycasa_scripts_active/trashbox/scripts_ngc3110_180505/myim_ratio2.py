import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/datacube_LTE_uv_smooth/"
im_12co10 = "line_12co10_contsub_clean20_nat_uv_smooth.image.moment0"
im_12co21 = "line_12co21_contsub_clean20_nat_smooth.image.moment0"
im_13co10 = "line_13co10_contsub_clean20_nat_uv_smooth.image.moment0"
im_13co21 = "line_13co21_contsub_clean20_nat_smooth.image.moment0"

#####################
### Main Procedure
#####################
### create cube mask
imagenames = glob.glob(dir_data + "*.image")
myim.createmask(dir_data = dir_data,
                imagename = imagenames[0].split("/")[-1],
                thres = -1.0)


### create momement maps
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "14~40",
                 mask = "mask1.image",
                 thres = -1.0)
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "12~41",
                 mask = "mask1.image",
                 thres = -1.0)
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[2],
                 chans = "17~38",
                 mask = "mask1.image",
                 thres = -1.0)
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[3],
                 chans = "16~40",
                 mask = "mask1.image",
                 thres = -1.0)


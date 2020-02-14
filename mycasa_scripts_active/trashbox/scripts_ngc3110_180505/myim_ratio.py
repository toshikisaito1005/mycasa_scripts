import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/datacube_line_uv_smooth/"
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
                thres = 0.0022)


### create momement maps
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[0],
                 chans = "14~40",
                 mask = "mask1.image",
                 thres = 0.0033)
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[1],
                 chans = "12~41",
                 mask = "mask1.image",
                 thres = 0.0021)
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[2],
                 chans = "17~38",
                 mask = "mask1.image",
                 thres = 0.0027)
myim.moment_maps(dir_data = dir_data,
                 imagename = imagenames[3],
                 chans = "16~40",
                 mask = "mask1.image",
                 thres = 0.0021)


### create mask for each moment map
peak = imstat(dir_data + im_12co21)["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_12co21,
                thres = 0.03 * peak,
                outmask = "12co21.mask")
peak = imstat(dir_data + im_12co10)["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_12co10,
                thres = 0.03 * peak,
                outmask = "12co10.mask")
peak = imstat(dir_data + im_13co10)["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_13co10,
                thres = 0.08 * peak,
                outmask = "13co10.mask")
peak = imstat(dir_data + im_13co21)["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_13co21,
                thres = 0.03 * peak,
                outmask = "13co21.mask")


### create mask for line ratio map
outfile = dir_data + "R_12co21_12co10.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "12co21.mask",
                    dir_data + "12co10.mask"],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)
outfile = dir_data + "R_13co21_13co10.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "13co21.mask",
                    dir_data + "13co10.mask"],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)
outfile = dir_data + "R_12co10_13co10.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "12co10.mask",
                    dir_data + "13co10.mask"],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)
outfile = dir_data + "R_12co21_13co21.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "12co21.mask",
                    dir_data + "13co21.mask"],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)


imagenames = glob.glob(dir_data + "R_*.mask")
for i in range(len(imagenames)):
    makemask(mode = "copy",
             inpimage = imagenames[i],
             inpmask = imagenames[i],
             output = imagenames[i] + ":mask0",
             overwrite = True)


### create line ratio map
myim.line_ratio(dir_data = dir_data,
                im1 = im_12co21,
                im2 = im_12co10,
                outfile = "R_12co21_12co10.image",
                diff = "4.",
                mask = "R_12co21_12co10.mask")
myim.line_ratio(dir_data = dir_data,
                im1 = im_13co21,
                im2 = im_13co10,
                outfile = "R_13co21_13co10.image",
                diff = "4.",
                mask = "R_13co21_13co10.mask")
myim.line_ratio(dir_data = dir_data,
                im1 = im_12co21,
                im2 = im_13co21,
                outfile = "R_12co21_13co21.image",
                diff = "1.",
                mask = "R_12co21_13co21.mask")
myim.line_ratio(dir_data = dir_data,
                im1 = im_12co10,
                im2 = im_13co10,
                outfile = "R_12co10_13co10.image",
                diff = "1.",
                mask = "R_12co10_13co10.mask")


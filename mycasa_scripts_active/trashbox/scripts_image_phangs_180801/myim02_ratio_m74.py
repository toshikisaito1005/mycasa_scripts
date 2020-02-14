import os
import re
import sys
import glob
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data = "../../phangs/co_ratio/"
im_12co10 = "m74co10_12m+7m+TP_feathered_robust_6kms_wmask_wmodel_pbcor.image.smooth.moment0"
im_12co21 = "m74co21_12m+7m+TP_feathered_2kms_robust_wmask_wmodel.image.regrid.smooth.moment0"

#####################
### Main Procedure
#####################
### create mask for each moment map
peak = imstat(dir_data + im_12co21)["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_12co21,
                thres = 0.05 * peak,
                outmask = "mom_12co21.mask")
peak = imstat(dir_data + im_12co10)["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_12co10,
                thres = 0.05 * peak,
                outmask = "mom_12co10.mask")

### create mask for line ratio map
outfile = dir_data + "R_12co21_12co10.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "mom_12co21.mask",
                    dir_data + "mom_12co10.mask"],
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


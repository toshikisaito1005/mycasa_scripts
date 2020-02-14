import os
import re
import sys
import glob
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


#####################
### Main Procedure
#####################
dir_data = "../../iras18293/products/line_uvlim/"
images_cube = glob.glob(dir_data + "*pbcor.image")

beams = []
for i in range(len(images_cube)):
    beam = imhead(images_cube[i])["restoringbeam"]["major"]["value"]
    beams.append(beam)

beam_max =  round(np.max(beams) + 0.1, 1)

### smoothing datacubes
# co data
default(imsmooth)
for i in range(2):
    os.system("rm -rf " + images_cube[i] + ".smooth")
    imsmooth(imagename = images_cube[i],
             kernel = "gauss",
             targetres = True,
             major = str(beam_max) + "arcsec",
             minor = str(beam_max) + "arcsec",
             pa = "0deg",
             box = "118,118,393,393",
             outfile = images_cube[i] + ".smooth")

# cI data
rms_12co10 = 0.003
i = 2
images_cube2 = images_cube[i] + ".masked_for_imsmooth"
os.system("rm -rf " + images_cube2)
immath(imagename = [images_cube[i], images_cube[0]],
       mode = "evalexpr",
       expr = "iif(IM1 >= " + str(0.003 * 5.) + ", IM0, 0.0)",
       outfile = images_cube2)

os.system("rm -rf " + images_cube[i] + ".smooth")
imsmooth(imagename = images_cube2,
         kernel = "gauss",
         targetres = True,
         major = str(beam_max) + "arcsec",
         minor = str(beam_max) + "arcsec",
         pa = "0deg",
         box = "118,118,393,393",
         outfile = images_cube[i] + ".smooth")


images_cube = glob.glob(dir_data + "*.image.smooth")
im_12co10 = images_cube[0]
im_12co21 = images_cube[1]
im_ci10 = images_cube[2]

rms_12co10 = 0.003
rms_12co21 = 0.0015
rms_ci10 = 0.007


### create mask for each moment map
myim.createmask(dir_data = dir_data,
                imagename = im_12co10.split("/")[-1],
                thres = rms_12co10 * 4.,
                outmask = "12co10.mask")
myim.moment_maps(dir_data = dir_data,
                 imagename = im_12co10,
                 chans = "18~75",
                 mask = "12co10.mask",
                 thres = rms_12co10 * 4.)

myim.createmask(dir_data = dir_data,
                imagename = im_12co21.split("/")[-1],
                thres = rms_12co21 * 4.,
                outmask = "12co21.mask")
myim.moment_maps(dir_data = dir_data,
                 imagename = im_12co21,
                 chans = "18~75",
                 mask = "12co21.mask",
                 thres = rms_12co21 * 4.)

myim.createmask(dir_data = dir_data,
                imagename = im_ci10.split("/")[-1],
                thres = rms_ci10 * 4.,
                outmask = "ci10.mask")

myim.moment_maps(dir_data = dir_data,
                 imagename = im_ci10,
                 chans = "18~75",
                 mask = "ci10.mask",
                 thres = rms_ci10 * 4.)


### create mask for line ratio map
peak = imstat(im_12co10 + ".moment0")["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_12co10.split("/")[-1] + ".moment0",
                thres = peak * 0.1,
                outmask = "12co10_mom0.mask")

peak = imstat(im_12co21 + ".moment0")["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_12co21.split("/")[-1] + ".moment0",
                thres = peak * 0.1,
                outmask = "12co21_mom0.mask")

peak = imstat(im_ci10 + ".moment0")["max"][0]
myim.createmask(dir_data = dir_data,
                imagename = im_ci10.split("/")[-1] + ".moment0",
                thres = peak * 0.1,
                outmask = "ci10_mom0.mask")


outfile = dir_data + "R_ci_12co10_mom0.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "12co10_mom0.mask",
                    dir_data + "ci10_mom0.mask"],
       mode = "evalexpr",
       expr = "IM0 * IM1",
       outfile = outfile)

outfile = dir_data + "R_12co21_12co10_mom0.mask"
os.system("rm -rf " + outfile)
immath(imagename = [dir_data + "12co21_mom0.mask",
                    dir_data + "12co10_mom0.mask"],
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
                im1 = im_ci10.split("/")[-1] + ".moment0",
                im2 = im_12co10.split("/")[-1] + ".moment0",
                outfile = "R_ci_12co10.image",
                diff = "18.23",
                mask = "R_ci_12co10_mom0.mask")

myim.line_ratio(dir_data = dir_data,
                im1 = im_12co21.split("/")[-1] + ".moment0",
                im2 = im_12co10.split("/")[-1] + ".moment0",
                outfile = "R_12co21_12co10.image",
                diff = "4.",
                mask = "R_12co21_12co10_mom0.mask")

os.system("rm -rf " + dir_data + "*.mask")

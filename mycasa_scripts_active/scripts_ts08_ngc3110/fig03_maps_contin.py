import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/"
ra_center = "10:04:02.220"
dec_center = "-6.28.29.604"
xlim = [-26, 26]
ylim = [30, -22]
value = None

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

im_m0s = glob.glob(dir_data + "data/*contin_*")
for i in range(len(im_m0s)):
    os.system("rm -rf " + im_m0s[i].replace("contin","continmJy"))
    immath(imagename = im_m0s[i],
           expr = "IM0*1000.",
           outfile = im_m0s[i].replace("contin","continmJy"))
    os.system("rm -rf " + im_m0s[i].replace("contin","continmJy") + ".fits")
    exportfits(imagename = im_m0s[i].replace("contin","continmJy"),
               fitsimage = im_m0s[i].replace("contin","continmJy") + ".fits")
    os.system("rm -rf " + im_m0s[i].replace("contin","continmJy"))


#####################
### Main Procedure
#####################
### Band 3 continuum
imagename_contour = "data/" + im_m0s[0].split("/")[-1].replace("contin","continmJy") + ".fits"
imagename_color = "data/" + im_m0s[0].split("/")[-1].replace("contin","continmJy") + ".fits"
contour = [0.16, 0.32, 0.64, 0.96]
title = "2.9 mm Continuum"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(mJy beam$^{-1}$)"
output = "eps/fig03a_b3_contin.eps"
myim.fits2eps(dir_data = dir_data,
              imagename_color = imagename_color,
              imagename_contour = imagename_contour,
              ra_center = ra_center,
              dec_center = dec_center,
              title = title,
              colorbar_label = colorbar_label,
              output = output,
              colorscale = colorscale,
              colorlog = colorlog,
              color_contour = color_contour,
              color_beam = color_beam,
              colorbar = colorbar,
              value = value,
              contour = contour,
              xlim = xlim,
              ylim = ylim)

### Band 6 continuum
imagename_contour = "data/" + im_m0s[1].split("/")[-1].replace("contin","continmJy") + ".fits"
imagename_color = "data/" + im_m0s[1].split("/")[-1].replace("contin","continmJy") + ".fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "1.3 mm Continuum"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(mJy beam$^{-1}$)"
output = "eps/fig03b_b6_contin.eps"
myim.fits2eps(dir_data = dir_data,
              imagename_color = imagename_color,
              imagename_contour = imagename_contour,
              ra_center = ra_center,
              dec_center = dec_center,
              title = title,
              colorbar_label = colorbar_label,
              output = output,
              colorscale = colorscale,
              colorlog = colorlog,
              color_contour = color_contour,
              color_beam = color_beam,
              colorbar = colorbar,
              value = value,
              contour = contour,
              xlim = xlim,
              ylim = ylim)

import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
ra_center = "18:32:40.935"
dec_center = "-34.11.27.281"
xlim = [-10, 10]
ylim = [10, -10]
value = None

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data + "image_b8contin/")
os.system("mkdir " + dir_data + "image_b8contin/")

imagename  = glob.glob(dir_data+"data/*b8_contin*")[0]
pbimage = glob.glob(dir_data+"data/*b8_contin*")[1]
outfile = dir_data + "image_b8contin/b8contin.flux"
impbcor(imagename=imagename,pbimage=pbimage,outfile=outfile,cutoff=0.5)
immath(imagename = dir_data + "image_b8contin/b8contin.flux",
       expr = "IM0 * 1000.",
       outfile = dir_data + "image_b8contin/b8contin.moment0")


imagenames = glob.glob(dir_data + "image_*/*.moment0")
for i in range(len(imagenames)):
    os.system("rm -rf " + imagenames[i] + ".fits")
    exportfits(imagename = imagenames[i],
               fitsimage = imagenames[i] + ".fits")

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "image_co10/co10.moment0.fits"
imagename_color = "image_co10/co10.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
contour = [0.025, 0.05, 0.10, 0.2, 0.4, 0.8, 0.95]
title = "(a) $^{12}$CO $J$ = 1-0 Integrated Intensity"
colorscale = "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "eps/iras18293_12co10_m0.png"
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

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "image_co10/co10.moment0.fits"
imagename_color = "image_ci10/ci10.moment0.fits"
contour = [0.025, 0.05, 0.10, 0.2, 0.4, 0.8, 0.95]
title = "(b) [CI] $J$ = 1-0 Integrated Intensity"
colorscale = "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "eps/iras18293_ci10_m0.png"
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

###Dust
# moment 0 color + moment 0 contour
imagename_contour = "image_co10/co10.moment0.fits"
imagename_color = "image_b8contin/b8contin.moment0.fits"
contour = [0.025, 0.05, 0.10, 0.2, 0.4, 0.8, 0.95]
title = "(c) 609$\mu$m Continuum"
colorscale = "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(mJy beam$^{-1}$)"
output = "eps/iras18293_b8contin.png"
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
              ylim = ylim,
              clim = [0,42])

os.system("rm -rf *.last")

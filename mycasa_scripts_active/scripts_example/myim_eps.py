import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../data/"
ra_center = "10:04:02.090" # image center
dec_center = "-6.28.29.604" # image center
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96] # contour * peak
xlim = [-30, 30] # image area (arcsec) from the image center
ylim = [30, -30] # image area (arcsec) from the image center
value = None


#####################
### Main Procedure
#####################
### moment 0 color + moment 0 contour
imagename_contour = "moment0.fits"
imagename_color = "moment0.fits"
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "r" # black
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "12co10_m0.eps"

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


### moment 1 color + moment 0 contour
imagename_contour = "moment0.fits"
imagename_color = "moment1.fits"
colorscale = "rainbow"
color_contour = "k" # black
color_beam = "black"
colorlog = False
colorbar = True
clim = [-300, 300]
title = "$^{12}$CO (1-0) Velocity Field"
colorbar_label = "(km s$^{-1}$)"
output = "12co10_m1.eps"
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
              clim = clim)


### moment 2 color + moment 0 contour
imagename_contour = "moment0.fits"
imagename_color = "moment2.fits"
colorscale = "rainbow"
color_contour = "k" # black
color_beam = "black"
colorlog = False
colorbar = True
clim = [0, 100]
title = "$^{12}$CO (1-0) Velocity Dispersion"
colorbar_label = "(km s$^{-1}$)"
output = "12co10_m2.eps"
myim.fits2eps(dir_data = dir_data,
              imagename_color = imagename_color,
              imagename_contour = imagename_contour,
              ra_center = ra_center,
              dec_center = dec_center,
              title = title,
              colorbar_label = colorbar_label,
              output = output,
              colorscale = colorscale,
              color_contour = color_contour,
              color_beam = color_beam,
              colorlog = colorlog,
              colorbar = colorbar,
              value = value,
              contour = contour,
              xlim = xlim,
              ylim = ylim,
              clim = clim)

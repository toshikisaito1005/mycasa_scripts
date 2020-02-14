import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/data_vv114/"
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
colorbar = True
value = None


done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")


#####################
### Main Procedure
#####################
### VV 114
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
ra_center = "01:07:47.230"
dec_center = "-17.30.25.627"
xlim = [-3, 16]
ylim = [11, -6]
clim = [5600, 6200]
imagename_contour = "VV114_AL0-2B7_12co32_l10_na.image.imsmooth.moment0.fits"
imagename_color = "VV114_AL0-2B7_12co32_l10_na.image.imsmooth.moment1.fits"
title = "VV 114 CO (3-2) [80 pc x 80 pc]"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = False
colorbar_label = "(km s$^{-1}$)"
output = "../eps/vv114_co10.eps"
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


import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../iras18293/products/line_uvlim/"
ra_center = "18:32:41.285"
dec_center = "-34.11.27.170"
xlim = [-11, 11]
ylim = [11, -11]
value = None


done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")


#####################
### Main Procedure
#####################

### R_12co21_12co10
imagename_contour = "iras18293_AL3B3_co10_l10_na_uvlim_pbcor.smooth.moment0.fits"
imagename_color = "R_12co21_12co10.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO ($J$ = 2-1) / $^{12}$CO ($J$ = 1-0) Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
clim = [0.8, 1.2]
colorbar_label = "Ratio"
output = "../eps/R_12co21_12co10.eps"
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

### R_ci_12co10
imagename_contour = "iras18293_AL3B3_co10_l10_na_uvlim_pbcor.smooth.moment0.fits"
imagename_color = "R_ci_12co10.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "[CI] ($J$ = 1-0) / $^{12}$CO ($J$ = 1-0) Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
clim = [.04, .12]
colorbar_label = "Ratio"
output = "../eps/R_ci_12co10.eps"
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



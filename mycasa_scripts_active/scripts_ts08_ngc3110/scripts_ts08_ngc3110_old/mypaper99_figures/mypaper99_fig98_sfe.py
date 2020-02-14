import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim


dir_data = "../../../ngc3110/ana/data_nyquist/"
ra_center = "10:04:02.090"
dec_center = "-6.28.29.604"
xlim = [-30, 30]
ylim = [30, -30]
value = None


done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")


#####################
### Main Procedure
#####################
### SFE
# color + contour
imagename_contour = "nyquist_co10_m0.fits"
imagename_color = "nyquist_sfe.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = ""
colorscale = "rainbow" # "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
clim = [0, 1.03325e-08]
title = "SFE"
colorbar_label = "(yr$^{-1}$)"
output = "../eps/nyquist_SFE.eps"
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

import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim


dir_data = "../../../ngc3110/ana/data_continuum/"

# casa2fits
imagenames = glob.glob(dir_data + "*.image.regrid")
for i in range(len(imagenames)):
    fitsimage = imagenames[i].replace(".image", "") + ".fits"
    os.system("rm -rf " + fitsimage)
    exportfits(imagename = imagenames[i],
               fitsimage = fitsimage)

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

### band3 continuum
# color + contour
imagename_contour = "continuum_band3_12co10_13co10_clean.regrid.fits"
imagename_color = "continuum_band3_12co10_13co10_clean.regrid.fits"
contour = [0.16, 0.32, 0.64, 0.96]
title = "2.9 mm Continuum"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$)"
output = "../eps/band3_continuum.eps"
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

### band6 continuum
# color + contour
imagename_contour = "continuum_band6_12co21_13co21_clean.regrid.fits"
imagename_color = "continuum_band6_12co21_13co21_clean.regrid.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "1.3 mm Continuum"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$)"
output = "../eps/band6_continuum.eps"
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

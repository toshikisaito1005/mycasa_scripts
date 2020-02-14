import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../../")
import mycasaimaging_tools as myim


dir_data = "../../../ngc3110/ana/product/fits/"
ra_center = "10:04:02.090"
dec_center = "-6.28.29.604"
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
xlim = [-30, 30]
ylim = [30, -30]
value = None


done = glob.glob(dir_data + "../../eps/")
if not done:
    os.mkdir(dir_data + "../../eps/")


#####################
### Main Procedure
#####################

# line ratios
imagename_contour = "line_12co10_contsub_clean20_nat.regrid.immath.moment0.fits"
imagename_color = "R_12co21_12co10.image.regrid.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0.4, 1.]
title = "$^{12}$CO (2-1) / $^{12}$CO (1-0) Ratio"
colorbar_label = "Ratio"
output = "../../eps/R_12co21_12co10.eps"
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

imagename_contour = "line_12co10_contsub_clean20_nat.regrid.immath.moment0.fits"
imagename_color = "R_13co21_13co10.image.regrid.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0.4, 1.]
title = "$^{13}$CO (2-1) / $^{13}$CO (1-0) Ratio"
colorbar_label = "Ratio"
output = "../../eps/R_13co21_13co10.eps"
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


imagename_contour = "line_12co10_contsub_clean20_nat.regrid.immath.moment0.fits"
imagename_color = "R_12co10_13co10.image.regrid.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [10., 30.]
title = "$^{12}$CO (1-0) / $^{13}$CO (1-0) Ratio"
colorbar_label = "Ratio"
output = "../../eps/R_12co10_13co10.eps"
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


imagename_contour = "line_12co10_contsub_clean20_nat.regrid.immath.moment0.fits"
imagename_color = "R_12co21_13co21.image.regrid.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [10., 30.]
title = "$^{12}$CO (2-1) / $^{13}$CO (2-1) Ratio"
colorbar_label = "Ratio"
output = "../../eps/R_12co21_13co21.eps"
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


import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ALMA_ACA_co10/fits/"
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
colorbar = True
value = None


done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")


#####################
### Main Procedure
#####################
### NGC 1614
ra_center = "04:34:00.027"
dec_center = "-08.34.45.028"
xlim = [-12, 12]
ylim = [12, -12]
clim = [4480, 4840]
imagename_contour = "ngc1614_AL+ACAB3_co10_l10_na.moment0.fits"
imagename_color = "ngc1614_AL+ACAB3_co10_l10_na.moment1.fits"
title = "NGC 1614 CO (1-0) [330 pc x 180 pc]"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = False
colorbar_label = "(km s$^{-1}$)"
output = "../eps/ngc1614_co10.eps"
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


### NGC 5257
ra_center = "13:39:52.922"
dec_center = "+00.50.24.393"
xlim = [-25, 25]
ylim = [25, -25]
clim = [6420, 6920]
imagename_contour = "ngc5257_AL3B3_co10_l20_na.moment0.fits"
imagename_color = "ngc5257_AL3B3_co10_l20_na.moment1.fits"
title = "NGC 5257 CO (1-0) [800 pc x 640 pc]"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = False
colorbar_label = "(km s$^{-1}$)"
output = "../eps/ngc5257_co10.eps"
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


### NGC 5258
ra_center = "13:39:57.737"
dec_center = "+00.49.50.792"
xlim = [-30, 30]
ylim = [30, -30]
clim = [6400, 6900]
imagename_contour = "ngc5258_AL3B3_co10_l20_na.moment0.fits"
imagename_color = "ngc5258_AL3B3_co10_l20_na.moment1.fits"
title = "NGC 5258 CO (1-0) [800 pc x 640 pc]"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = False
colorbar_label = "(km s$^{-1}$)"
output = "../eps/ngc5258_co10.eps"
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


### NGC 6240
contour = [0.0025, 0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
ra_center = "16:52:58.894"
dec_center = "+02.24.03.949"
xlim = [-15, 15]
ylim = [15, -15]
clim = [6700, 7300]
imagename_contour = "ngc6240_AL4B6_co10_l20_na.moment0.fits"
imagename_color = "ngc6240_AL4B6_co10_l20_na.moment1.fits"
title = "NGC 6240 CO (1-0) [310 pc x 260 pc]"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = False
colorbar_label = "(km s$^{-1}$)"
output = "../eps/ngc6240_co10.eps"
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


### VV 114
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
ra_center = "01:07:47.230"
dec_center = "-17.30.25.627"
xlim = [-25, 25]
ylim = [25, -25]
clim = [5600, 6200]
imagename_contour = "vv114_AL+ACAB3_co10_l10_na.trans.moment0.fits"
imagename_color = "vv114_AL+ACAB3_co10_l10_na.trans.moment1.fits"
title = "VV 114 CO (1-0) [1120 pc x 680 pc]"
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


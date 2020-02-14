import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../iras18293/products/line/"
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

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "iras18293_AL3B3_co10_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B3_co10_l10_na.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO ($J$ = 1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/12co10_m0.eps"
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


# moment 1 color + moment 0 contour
imagename_contour = "iras18293_AL3B3_co10_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B3_co10_l10_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [5200, 5600]
title = "$^{12}$CO ($J$ = 1-0) Velocity Field"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/12co10_m1.eps"
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


# moment 2 color + moment 0 contour
imagename_contour = "iras18293_AL3B3_co10_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B3_co10_l10_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO ($J$ = 1-0) Velocity Dispersion"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/12co10_m2.eps"
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

###12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "iras18293_AL3B6_co21_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B6_co21_l10_na.moment0.fits"
contour = contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO ($J$ = 2-1) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/12co21_m0.eps"
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


# moment 1 color + moment 0 contour
imagename_contour = "iras18293_AL3B6_co21_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B6_co21_l10_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [5200, 5600]
title = "$^{12}$CO ($J$ = 2-1) Velocity Field"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/12co21_m1.eps"
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


# moment 2 color + moment 0 contour
imagename_contour = "iras18293_AL3B6_co21_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B6_co21_l10_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "$^{12}$CO ($J$ = 2-1) Velocity Dispersion"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/12co21_m2.eps"
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


###CI(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "iras18293_AL3B8_cI10_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B8_cI10_l10_na.moment0.fits"
contour = contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "[CI] ($J$ = 1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ci10_m0.eps"
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


# moment 1 color + moment 0 contour
imagename_contour = "iras18293_AL3B8_cI10_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B8_cI10_l10_na.moment1.fits"
contour = contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [5200, 5600]
title = "[CI] ($J$ = 1-0) Velocity Field"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/ci10_m1.eps"
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


# moment 2 color + moment 0 contour
imagename_contour = "iras18293_AL3B8_cI10_l10_na.moment0.fits"
imagename_color = "iras18293_AL3B8_cI10_l10_na.moment2.fits"
contour = contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "[CI] ($J$ = 1-0) Velocity Dispersion"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/ci10_m2.eps"
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



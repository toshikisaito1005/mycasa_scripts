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
### R_b6_b3_contin
# color + contour
imagename_contour = "nyquist_co10_m0.fits"
imagename_color = "nyquist_R_b6_b3_contin.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = ""
colorscale = "rainbow" # "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
clim = [0., 4.]
title = "Spectral Index"
colorbar_label = ""
output = "../eps/nyquist_R_b6_b3_contin.eps"
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


### alpha_ISM
# color + contour
imagename_contour = "nyquist_co10_m0.fits"
imagename_color = "nyquist_alpha_co.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = ""
colorscale = "rainbow" # "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
clim = [0., 4.]
title = "$M_{ISM}$/$L'_{CO(1-0)}$"
colorbar_label = "($M_{\odot}$ (K km s$^{-1}$ pc$^2$)$^{-1}$)"
output = "../eps/nyquist_alpha_co.eps"
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

### corr_SFR
# color + contour
imagename_contour = "nyquist_co10_m0.fits"
imagename_color = "nyquist_corr_sfr.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = ""
colorscale = "rainbow" # "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
clim = [0., 2.5]
title = "Extinction-corrected SFR Density"
colorbar_label = "($M_{\odot}$ kpc$^{-2}$ yr$^{-1}$)"
output = "../eps/nyquist_corr_sfr.eps"
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

### SSC
# color + contour
imagename_contour = "nyquist_co10_m0.fits"
imagename_color = "nyquist_ssc_gauss.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = ""
colorscale = "rainbow" # "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
#clim = [0, 8]
title = "SSC Number Density"
colorbar_label = "(kpc$^{-2}$)"
output = "../eps/nyquist_SSC.eps"
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

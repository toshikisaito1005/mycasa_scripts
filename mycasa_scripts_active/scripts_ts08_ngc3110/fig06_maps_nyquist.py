import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/"
ra_center = "10:04:02.220"
dec_center = "-6.28.29.604"
xlim = [-26, 26]
ylim = [30, -22]
value = None

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

fitsimages = glob.glob(dir_data + "image_nyquist/*.fits")
fitsimages.sort()


#####################
### Main Procedure
#####################
### common
imagename_contour = "image_nyquist/ngc3110_nyquist_co10_luminosity.fits"
contour = contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]

### spectral index
imagename_color = "image_nyquist/ngc3110_nyquist_index.fits"
title = "Spectral Index"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = ""
output = "eps/fig06c_index.eps"
clim = [0, 2]
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

### SFE
imagename_color = "image_nyquist/ngc3110_nyquist_sfe.fits"
title = "SFE"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(Gyr$^{-1}$)"
output = "eps/fig06f_sfe.eps"
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

### SFR density
imagename_color = "image_nyquist/ngc3110_nyquist_sfr_density.fits"
title = "Extinction-corrected SFR Surface Density"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "($M_{\odot}$ kpc$^{-2}$ yr$^{-1}$)"
output = "eps/fig06d_sfr.eps"
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

### SSC density
imagename_color = "image_nyquist/ngc3110_nyquist_ssc_density.fits"
title = "SSC Surface Density"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(kpc$^{-2}$)"
output = "eps/fig06e_ssc.eps"
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

### Tkin
imagename_color = "image_nyquist/ngc3110_nyquist_Tkin.fits"
title = "Kinetic Temperature"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(K)"
output = "eps/fig06a_Tkin.eps"
clim = [0,100]
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

### nH2
imagename_color = "image_nyquist/ngc3110_nyquist_nH2.fits"
title = "H$_2$ Volume Density"
colorscale = "rainbow"
color_contour = "black"
color_beam = "white"
colorlog = True
colorbar = True
colorbar_label = "(K km s$^{-1}$ pc$^2$)"
output = "eps/fig06b_nH2.eps"
clim = [10**2, 10**5]
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


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
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
xlim = [-26, 26]
ylim = [30, -22]
value = None

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

im_m0s = glob.glob(dir_data + "image_*/*.moment0.fits")
im_ratios = glob.glob(dir_data + "image_ratio/*.fits")


#####################
### Main Procedure
#####################
### $^{12}$CO (2-1) / $^{12}$CO (1-0) Ratio
imagename_contour = "image_12co10/" + im_m0s[0].split("/")[-1]
imagename_color = "image_ratio/" + im_ratios[1].split("/")[-1]
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) / $^{12}$CO (1-0) Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/fig04a_12co21_12co10.eps"
clim = [0.4,1.0]
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

### $^{13}$CO (2-1) / $^{13}$CO (1-0) Ratio
imagename_contour = "image_12co10/" + im_m0s[0].split("/")[-1]
imagename_color = "image_ratio/" + im_ratios[3].split("/")[-1]
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{13}$CO (2-1) / $^{13}$CO (1-0) Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/fig04b_13co21_13co10.eps"
clim = [0.4,1.0]
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

### $^{12}$CO (2-1) / $^{13}$CO (2-1) Ratio
imagename_contour = "image_12co10/" + im_m0s[0].split("/")[-1]
imagename_color = "image_ratio/" + im_ratios[2].split("/")[-1]
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) / $^{13}$CO (2-1) Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/fig04c_12co21_13co21.eps"
clim = [5,30]
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

### $^{12}$CO (1-0) / $^{13}$CO (1-0) Ratio
imagename_contour = "image_12co10/" + im_m0s[0].split("/")[-1]
imagename_color = "image_ratio/" + im_ratios[0].split("/")[-1]
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) / $^{13}$CO (1-0) Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/fig04d_12co10_13co10.eps"
clim = [5,30]
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

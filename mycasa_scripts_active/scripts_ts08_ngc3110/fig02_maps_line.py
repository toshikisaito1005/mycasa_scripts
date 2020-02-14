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
im_m1s = glob.glob(dir_data + "image_*/*.moment1.fits")


#####################
### Main Procedure
#####################
###12CO(1-0)
imagename_contour = "image_12co10/" + im_m0s[0].split("/")[-1]
imagename_color = "image_12co10/" + im_m1s[0].split("/")[-1]
contour = contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Velocity Field"
colorscale = "bwr"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(km s$^{-1}$)"
output = "eps/fig02a_12co10.eps"
clim = [-300, 300]
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
imagename_contour = "image_12co21/" + im_m0s[1].split("/")[-1]
imagename_color = "image_12co21/" + im_m1s[1].split("/")[-1]
contour = contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Velocity Field"
colorscale = "bwr"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(km s$^{-1}$)"
output = "eps/fig02b_12co21.eps"
clim = [-300, 300]
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

###13CO(1-0)
imagename_contour = "image_13co10/" + im_m0s[2].split("/")[-1]
imagename_color = "image_13co10/" + im_m1s[2].split("/")[-1]
contour = contour = [0.06, 0.12, 0.24, 0.48, 0.96]
title = "$^{13}$CO (1-0) Velocity Field"
colorscale = "bwr"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(km s$^{-1}$)"
output = "eps/fig02c_13co10.eps"
clim = [-300, 300]
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

###13CO(2-1)
imagename_contour = "image_13co21/" + im_m0s[3].split("/")[-1]
imagename_color = "image_13co21/" + im_m1s[3].split("/")[-1]
contour = contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{13}$CO (2-1) Velocity Field"
colorscale = "bwr"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(km s$^{-1}$)"
output = "eps/fig02d_13co21.eps"
clim = [-300, 300]
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

###C18O(2-1)
imagename_contour = "image_c18o21/" + im_m0s[4].split("/")[-1]
imagename_color = "image_c18o21/" + im_m1s[4].split("/")[-1]
contour = contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "C$^{18}$O (2-1) Velocity Field"
colorscale = "bwr"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(km s$^{-1}$)"
output = "eps/fig02e_c18o21.eps"
clim = [-300, 300]
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

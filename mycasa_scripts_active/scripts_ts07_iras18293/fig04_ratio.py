import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/myproj_published/proj_ts07_iras18293/"
ra_center = "18:32:40.935"
dec_center = "-34.11.27.281"
xlim = [-10, 10]
ylim = [10, -10]
value = None
clip = 0.10027554936773037 # 10**6.0
freq_factor = 115.27120*115.27120/492.16065100/492.16065100

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

#####################
### Main Procedure
#####################
# ci co ratio
ci = dir_data + "image_ci10/ci10.moment0"
co = dir_data + "image_co10/co10.moment0"
cliplevel = clip * imstat(co)["max"][0] * 100000.

os.system("rm -rf " + co + ".complete")
immath(imagename = co,
       expr = "iif(IM0 <= " + str(cliplevel) + ", IM0, 0.0)",
       outfile = co + ".complete")

os.system("rm -rf " + dir_data + "image_ci10/ratio.moment0")
immath(imagename = [ci,co + ".complete"],
       expr = "iif(IM0 >= 0, IM0/IM1*"+str(freq_factor)+", 0.0)",
       outfile = dir_data + "image_ci10/ratio.moment0")

imagenames = glob.glob(dir_data + "image_*/*.moment0")
for i in range(len(imagenames)):
    os.system("rm -rf " + imagenames[i] + ".fits")
    exportfits(imagename = imagenames[i],
               fitsimage = imagenames[i] + ".fits")


# ci dust ratio
ci = dir_data + "image_ci10/ci10.moment0"
dust = dir_data + "image_co10/co10.moment0"
cliplevel = clip * imstat(co)["max"][0] * 100000.

os.system("rm -rf " + co + ".complete")
immath(imagename = co,
       expr = "iif(IM0 <= " + str(cliplevel) + ", IM0, 0.0)",
       outfile = co + ".complete")

os.system("rm -rf " + dir_data + "image_ci10/ratio.moment0")
immath(imagename = [ci,co + ".complete"],
       expr = "iif(IM0 >= 0, IM0/IM1*"+str(freq_factor)+", 0.0)",
       outfile = dir_data + "image_ci10/ratio.moment0")


###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "image_co10/co10.moment0.fits"
imagename_color = "image_ci10/ratio.moment0.fits"
contour = [0.025, 0.05, 0.10, 0.2, 0.4, 0.8, 0.95]
title = "[CI]/$^{12}$CO Line Luminosity Ratio"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/iras18293_ratio_m0.png"
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
              clim = [0.0,0.26])# [0,0.26])


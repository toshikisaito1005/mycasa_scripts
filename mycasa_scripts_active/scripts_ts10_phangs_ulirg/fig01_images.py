
import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)

dir_data = "/Users/saito/data/myproj_active/proj_ts10_phangs_ulirgs/"

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

#####################
### Main Procedure
#####################

ra_center = "12:14:12.823"
dec_center = "-47.13.42.928"
xlim = [-10, 10]
ylim = [10, -10]
value = None
imagename_contour = "data/eso267_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "ESO 267-G030"
colorscale = "PuBu"
color_contour = "black"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(K km s$^{-1}$)"
output = "eps/eso267_m0.png"
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


os.system("rm -rf *.last")

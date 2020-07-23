
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
# eso267
ra_center = "12:14:12.923"
dec_center = "-47.13.43.85"
xlim = [-10, 10]
ylim = [10, -10]
value = None
imagename_contour = "data/eso267_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "ESO 267-G030"
colorscale = "gnuplot"
color_contour = "white"
color_beam = "black"
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

# eso297g011
ra_center = "01:36:23.415"
dec_center = "-37.19.17.6"
xlim = [-10, 10]
ylim = [10, -10]
value = None
imagename_contour = "data/eso297g011_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "ESO 297-G011"
colorscale = "gnuplot"
color_contour = "white"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(K km s$^{-1}$)"
output = "eps/eso297g011_m0.png"
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

# eso297g012
ra_center = "01:36:24.185"
dec_center = "-37.20.25.45"
xlim = [-5, 5]
ylim = [5, -5]
value = None
imagename_contour = "data/eso297g012_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "ESO 297-G012"
colorscale = "gnuplot"
color_contour = "white"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(K km s$^{-1}$)"
output = "eps/eso297g012_m0.png"
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

# eso297g012
ra_center = "01:36:24.185"
dec_center = "-37.20.25.45"
xlim = [-5, 5]
ylim = [5, -5]
value = None
imagename_contour = "data/eso507_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0"
imagename_color = imagename_contour
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "ESO 507-G070"
colorscale = "gnuplot"
color_contour = "white"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(K km s$^{-1}$)"
output = "eps/eso507_m0.png"
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

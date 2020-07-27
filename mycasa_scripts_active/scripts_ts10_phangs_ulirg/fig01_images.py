
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
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
value = None
colorscale = "gnuplot"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(K km s$^{-1}$)"

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")

#####################
### Main Procedure
#####################
"""
# eso267
ra_center = "12:14:12.923"
dec_center = "-47.13.43.85"
xlim = [-13.68*1.25, 13.68*1.25] #5kpc*1.25 # [-9.5, 9.5]
ylim = [13.68*1.25, -13.68*1.25] # [9.5, -9.5]
imagename_contour = "data/eso267_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "ESO 267-G030"
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
xlim = [-14.46*1.25, 14.46*1.25] # [-9.5, 9.5]
ylim = [14.46*1.25, -14.46*1.25] # [9.5, -9.5]
value = None
imagename_contour = "data/eso297g011_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "ESO 297-G011"
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
xlim = [-14.46*1.25, 14.46*1.25] # [-4.7, 4.7]
ylim = [14.46*1.25, -14.46*1.25] # [4.7, -4.7]
value = None
imagename_contour = "data/eso297g012_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "ESO 297-G012"
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

# eso507
ra_center = "13:02:52.337"
dec_center = "-23.55.18.5"
xlim = [-11.76*1.25, 11.76*1.25] # [-5.1, 5.1]
ylim = [11.76*1.25, -11.76*1.25] # [5.1, -5.1]
value = None
imagename_contour = "data/eso507_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "ESO 507-G070"
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

# eso557
ra_center = "06:31:47.245"
dec_center = "-17.37.17.45"
xlim = [-11.76*1.25, 11.76*1.25] # [-6, 6]
ylim = [11.76*1.25, -11.76*1.25] # [6, -6]
value = None
imagename_contour = "data/eso557_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "ESO 557-G002"
output = "eps/eso557_m0.png"
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

# ic4518e
ra_center = "14:57:44.462"
dec_center = "-43.07.52.879"
xlim = [-16.35*1.25, 16.35*1.25] # [-13, 13]
ylim = [16.35*1.25, -16.35*1.25] # [13, -13]
value = None
imagename_contour = "data/ic4518e_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "IC4518E"
output = "eps/ic4518e_m0.png"
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

# ic4518w
ra_center = "14:57:41.222"
dec_center = "-43.07.56.0"
xlim = [-16.35*1.25, 16.35*1.25] # [-9.2, 9.2]
ylim = [16.35*1.25, -16.35*1.25] # [9.2, -9.2]
value = None
imagename_contour = "data/ic4518w_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "IC4518W"
output = "eps/ic4518w_m0.png"
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

# ic5179
ra_center = "22:16:09.07"
dec_center = "-36.50.38.2"
xlim = [-22.2*1.25, 22.2*1.25] # [-14, 14]
ylim = [22.2*1.25, -22.2*1.25] # [14, -14]
value = None
imagename_contour = "data/ic5179_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "IC5179"
output = "eps/ic5179_m0.png"
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

# iras06592
ra_center = "06:59:40.245"
dec_center = "-63.17.52.70"
xlim = [-11.25*1.25, 11.25*1.25] # [-6, 6]
ylim = [11.25*1.25, -11.25*1.25] # [6, -6]
value = None
imagename_contour = "data/iras06592_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "IRAS 06592-6313"
output = "eps/iras06592_m0.png"
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

# irasf10409
ra_center = "10:43:07.677"
dec_center = "-46.12.44.3"
xlim = [-11.76*1.25, 11.76*1.25] # [-12, 12]
ylim = [11.76*1.25, -11.76*1.25] # [12, -12]
value = None
imagename_contour = "data/irasf10409_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "IRAS F10409-4556"
output = "eps/irasf10409_m0.png"
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

# irasf17138
ra_center = "17:16:35.791"
dec_center = "-10.20.37.885"
xlim = [-14.46*1.25, 14.46*1.25] # [-11, 11]
ylim = [14.46*1.25, -14.46*1.25] # [11, -11]
value = None
imagename_contour = "data/irasf17138_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "IRAS F17138-1017"
output = "eps/irasf17138_m0.png"
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

# mcg02
ra_center = "13:02:20.717"
dec_center = "-15.46.01.729"
xlim = [-16.35*1.25, 16.35*1.25] # [-16, 16]
ylim = [16.35*1.25, -16.35*1.25] # [16, -16]
value = None
imagename_contour = "data/mcg02-33-098_12m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "MCG-02-33-098"
output = "eps/mcg02_m0.png"
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

# ngc1614
ra_center = "04:34:00.47"
dec_center = "-8.34.44.0"
xlim = [-16.38*1.25, 16.38*1.25] # [-12, 12]
ylim = [16.38*1.25, -16.38*1.25] # [12, -12]
value = None
imagename_contour = "data/ngc1614_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "NGC 1614"
output = "eps/ngc1614_m0.png"
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

# ngc2369
ra_center = "07:16:37.76"
dec_center = "-62.20.38.35"
xlim = [-24.39*1.25, 24.39*1.25] # [-14.5, 14.5]
ylim = [24.39*1.25, -24.39*1.25] # [14.5, -14.5]
value = None
imagename_contour = "data/ngc2369_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "NGC 2369"
output = "eps/ngc2369_m0.png"
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

# ngc3110
ra_center = "10:04:02.135"
dec_center = "-6.28.28.75"
xlim = [-15.36*1.25, 15.36*1.25] # [-18, 18]
ylim = [15.36*1.25, -15.36*1.25] # [18, -18]
value = None
imagename_contour = "data/ngc3110_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "NGC 3110"
output = "eps/ngc3110_m0.png"
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

# ngc3256
ra_center = "10:27:51.3"
dec_center = "-43.54.16.732"
xlim = [-27.06*1.25, 27.06*1.25] # [-24, 24]
ylim = [27.06*1.25, -27.06*1.25] # [24, -24]
value = None
imagename_contour = "data/ngc3256_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "NGC 3256"
output = "eps/ngc3256_m0.png"
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

# ngc5257
ra_center = "13:39:52.91"
dec_center = "0.50.25.2"
xlim = [-11.25*1.25, 11.25*1.25] # [-14, 14]
ylim = [11.25*1.25, -11.25*1.25] # [14, -14]
value = None
imagename_contour = "data/ngc5257_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "NGC 5257"
output = "eps/ngc5257_m0.png"
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

# ngc6240
ra_center = "16:52:58.85"
dec_center = "2.24.02.6"
xlim = [-10.35*1.25, 10.35*1.25] # [-7, 7]
ylim = [10.35*1.25, -10.35*1.25] # [7, -7]
value = None
imagename_contour = "data/ngc6240_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "NGC 6240"
output = "eps/ngc6240_m0.png"
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

# eso319
ra_center = "11:27:54.079"
dec_center = "-41.36.52.788"
xlim = [] # [-5, 5]
ylim = [] # [5, -5]
value = None
imagename_contour = "data/eso319_12m+7m_co21_pbcorr_trimmed_k_res150pc_strict_mom0.fits"
imagename_color = imagename_contour
title = "ESO 319-G022"
output = "eps/eso319_m0.png"
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
"""

os.system("rm -rf *.last")

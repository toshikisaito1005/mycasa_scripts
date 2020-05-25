import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)

dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/data_old/"
galname = "ngc0628"


done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")


#####################
### Main Procedure
#####################
### common
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-150, 150]
ylim = [150, -150]
value = None


### model
#
imagename_contour = galname + "/sim_ngc0628_skymodel.smooth.fits"
imagename_color = galname + "/sim_ngc0628_skymodel.smooth.fits"
imagemax = imstat(dir_data + imagename_contour)["max"]
#
contour = np.array([0.15, 0.35, 0.55, 0.75, 0.95])
title = "7m-only"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc0628_skymodel.png"
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


### 7m-only
#
imagename_contour = galname + "/sim_ngc0628_skymodel.smooth.fits"
imagename_color = galname + "/sim_ngc0628_7m_br.smooth.pbcor.clip.fits"
imagemax = imstat(dir_data + imagename_contour)["max"]
#
contour = np.array([0.15, 0.35, 0.55, 0.75, 0.95])
title = "7m-only"
colorscale = "rainbow"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc0628_7m.png"
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


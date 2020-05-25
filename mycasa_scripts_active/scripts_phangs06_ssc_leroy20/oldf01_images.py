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
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-120, 120]
ylim = [120, -120]
value = None
#
imagename_contour = galname + "/sim_ngc0628_skymodel.smooth.fits"
imagename_color = galname + "/sim_ngc0628_7m_br.smooth.pbcor.clip.fits"
imagemax = imstat(dir_data + imagename_contour)["max"]
#
contour = np.array([0.04, 0.08, 0.16, 0.32, 0.64, 0.96])
title = "7m-only"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
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


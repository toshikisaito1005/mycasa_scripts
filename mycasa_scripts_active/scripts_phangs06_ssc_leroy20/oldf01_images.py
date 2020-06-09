import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)


dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/sim_ngc0628/"
galname = "ngc0628"


done = glob.glob(dir_data + "../../eps/")
if not done:
    os.mkdir(dir_data + "../../eps/")


imagenames = glob.glob(dir_data + "*.image")
for i in range(len(imagenames)):


#####################
### Main Procedure
#####################
### common
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-150, 150]
ylim = [150, -150]
clim = [0, 3.93731]
clim_diff = [-1.0, 0.3]
value = None
color_contour = "black"
color_beam = "white"
colorbar = True
colorlog = False
colorscale = "rainbow"
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
contour = np.array([0.15, 0.35, 0.55, 0.75, 0.95])
imagename_contour = "sim_ngc0628_skymodel.smooth.fits"


### model
#
imagename_color = galname + "/sim_ngc0628_skymodel.smooth.fits"
title = "Convolved Model"
output = "../eps/ngc0628_skymodel.png"
#
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


### 7m-only
#
imagename_color = galname + "/sim_ngc0628_7m_br.smooth.pbcor.clip.fits"
title = "Convolved 7m-only"
output = "../eps/ngc0628_7m.png"
#
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
#
imagename_color = galname + "/sim_ngc0628_7m_br.smooth.pbcor.difference.fits"
title = "7m-only - Model"
output = "../eps/ngc0628_diff_7m.png"
#
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
              clim = clim_diff)


### CAF
#
imagename_color = galname + "/sim_ngc0628_caf_br.smooth.pbcor.clip.fits"
title = "Convolved Feather"
output = "../eps/ngc0628_feather.png"
#
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
#
imagename_color = galname + "/sim_ngc0628_caf_br.smooth.pbcor.difference.fits"
title = "Feather - Model"
output = "../eps/ngc0628_diff_feather.png"
#
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
              clim = clim_diff)


### CBF
#
imagename_color = galname + "/sim_ngc0628_cbf_br.smooth.pbcor.clip.fits"
title = "Convolved tp2vis"
output = "../eps/ngc0628_tp2vis.png"
#
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
#
imagename_color = galname + "/sim_ngc0628_cbf_br.smooth.pbcor.difference.fits"
title = "tp2vis - Model"
output = "../eps/ngc0628_diff_tp2vis.png"
#
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
              clim = clim_diff)


### CDF
#
imagename_color = galname + "/sim_ngc0628_cdf_br.smooth.pbcor.clip.fits"
title = "Convolved TPmodel"
output = "../eps/ngc0628_tpmodel.png"
#
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
#
imagename_color = galname + "/sim_ngc0628_cdf_br.smooth.pbcor.difference.fits"
title = "TPmodel - Model"
output = "../eps/ngc0628_diff_tpmodel.png"
#
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
              clim = clim_diff)


os.system("rm -rf *.last")

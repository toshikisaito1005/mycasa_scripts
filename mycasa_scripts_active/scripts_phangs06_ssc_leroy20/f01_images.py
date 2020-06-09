import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)


galname = "ngc1097" # "ngc0628" "ngc1097"
dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/sim_" + galname + "/"


done = glob.glob(dir_data + "../../eps/")
if not done:
    os.mkdir(dir_data + "../../eps/")


imagenames = glob.glob(dir_data + "*.smooth")
for i in range(len(imagenames)):
	done = glob.glob(imagenames[i].replace(".smooth",".smooth.fits"))
	if not done:
		exportfits(imagename = imagenames[i],
			fitsimage = imagenames[i].replace(".smooth",".smooth.fits"))


#####################
### Main Procedure
#####################
### common
"""
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
clim = [0, 3.93731]
contour = np.array([0.15, 0.35, 0.55, 0.75, 0.95])
xlim = [-150, 150]
ylim = [150, -150]
"""
ra_center = "02:46:19.088"
dec_center = "-30.16.30.099"
clim = [0, 10]
contour = np.array([0.02,0.04,0.08,0.16,0.32,0.64,0.96])
xlim = [-135, 135]
ylim = [135, -135]
###
value = None
color_contour = "black"
color_beam = "white"
colorbar = True
colorlog = False
colorscale = "rainbow"
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
imagename_contour = "sim_"+galname+"_skymodel_regrid.smooth.fits"


### model
#
imagename_color = "sim_"+galname+"_skymodel_regrid.smooth.fits"
title = "Convolved Model"
output = "../../eps/"+galname+"_skymodel.png"
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
imagename_color = "sim_"+galname+"_7m_br.smooth.fits"
title = "Convolved 7m-only"
output = "../../eps/"+galname+"_7m.png"
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


### CAF
#
imagename_color = "sim_"+galname+"_feather_br.smooth.fits"
title = "Convolved Feather"
output = "../../eps/"+galname+"_feather.png"
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


### CBF
#
imagename_color = "sim_"+galname+"_tp2vis_br.smooth.fits"
title = "Convolved tp2vis"
output = "../../eps/"+galname+"_tp2vis.png"
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


### CDF
#
imagename_color = "sim_"+galname+"_tpmodel_br.smooth.fits"
title = "Convolved tpmodel"
output = "../../eps/"+galname+"_tpmodel.png"
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


os.system("rm -rf *.last")

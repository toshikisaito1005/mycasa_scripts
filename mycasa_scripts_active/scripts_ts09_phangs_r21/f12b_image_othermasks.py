import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)

dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
data_image = glob.glob(dir_data + "*/*_04p0*moment0")
data_image.extend(glob.glob(dir_data + "*/*_04p0*moment8"))
data2_image = glob.glob(dir_data + "*/*_08p0*moment0")
data2_image.extend(glob.glob(dir_data + "*/*_08p0*moment0"))
data_image = np.r_[data_image, data2_image]
data_image.sort()

for i in range(len(data_image)):
    done = glob.glob(data_image[i])
    if not done:
      print("### processing " + data_image[i])
      os.system("rm -rf " + data_image[i].replace(".image","") + ".fits")
      exportfits(imagename = data_image[i],
                 fitsimage = data_image[i].replace(".image","") + ".fits")

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")


#####################
### Main Procedure
#####################
# common
clim = [0,1]
color_contour = "white" # "grey"

# ngc0628
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-120, 120]
ylim = [120, -120]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
color_beam = "grey"
imagename_contour = "ngc0628_co21/co21_04p0.moment0.fits"
imagename_color = "ngc0628_r21/cprops_04p0.mask.fits"
contour = [0.036,0.04,0.44]#[0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 0628 Cloud Mask"
colorscale = "bwr"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc0628_cloud_mask.png"
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
              clim = clim,
              showbeam = False)


### ngc4321
ra_center = "12:22:54.931"
dec_center = "15.49.20.369"
xlim = [-100, 100]
ylim = [100, -100]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
color_beam = "grey"
imagename_contour = "ngc4321_co21/co21_04p0.moment0.fits"
imagename_color = "ngc4321_r21/cprops_04p0.mask.fits"
contour = [0.0095,0.010,0.0105]#[0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 4321 Cloud Mask"
colorscale = "bwr"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc4321_cloud_mask.png"
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
              clim = clim,
              showbeam = False)


### ngc3627
ra_center = "11:20:15.35"
dec_center = "12.58.87.0"
xlim = [-135, 135]
ylim = [160, -110]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc3627_co21/co21_08p0.moment0.fits"
imagename_color = "ngc3627_r21/cprops_08p0.mask.fits"
contour = [0.0197,0.020,0.0203]#[0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 3627 Cloud Mask"
colorscale = "bwr"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc3627_cloud_mask.png"
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
              clim = clim,
              showbeam = False)


# common
clim = [0,4]

# ngc0628
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-120, 120]
ylim = [120, -120]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
color_beam = "grey"
imagename_contour = "ngc0628_co21/co21_04p0.moment0.fits"
imagename_color = "ngc0628_r21/env_all_04p0.mask.fits"
contour = [0.036,0.04,0.44]#[0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 0628 Environmental Mask"
colorscale = "gnuplot"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc0628_env_mask.png"
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
              clim = clim,
              showbeam = False)


### ngc4321
ra_center = "12:22:54.931"
dec_center = "15.49.20.369"
xlim = [-100, 100]
ylim = [100, -100]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
color_beam = "grey"
imagename_contour = "ngc4321_co21/co21_04p0.moment0.fits"
imagename_color = "ngc4321_r21/env_all_04p0.mask.fits"
contour = [0.0095,0.010,0.0105]#[0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 4321 Environmental Mask"
colorscale = "gnuplot"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc4321_env_mask.png"
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
              clim = clim,
              showbeam = False)


### ngc3627
ra_center = "11:20:15.35"
dec_center = "12.58.87.0"
xlim = [-135, 135]
ylim = [160, -110]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc3627_co21/co21_08p0.moment0.fits"
imagename_color = "ngc3627_r21/env_all_08p0.mask.fits"
contour = [0.0197,0.020,0.0203]#[0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 3627 Environmental Mask"
colorscale = "gnuplot"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc3627_env_mask.png"
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
              clim = clim,
              showbeam = False)


# common
clim = [0,1]

# ngc0628
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-120, 120]
ylim = [120, -120]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
color_beam = "grey"
imagename_contour = "ngc0628_co21/co21_04p0.moment0.fits"
imagename_color = "ngc0628_r21/piechart_04p0.mask.fits"
contour = [0.036,0.04,0.44]#[0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 0628 HII Region Mask"
colorscale = "PiYG"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc0628_piechart_mask.png"
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
              clim = clim,
              showbeam = False)


### ngc4321
ra_center = "12:22:54.931"
dec_center = "15.49.20.369"
xlim = [-100, 100]
ylim = [100, -100]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
color_beam = "grey"
imagename_contour = "ngc4321_co21/co21_04p0.moment0.fits"
imagename_color = "ngc4321_r21/piechart_04p0.mask.fits"
contour = [0.0095,0.010,0.0105]#[0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 4321 HII Region Mask"
colorscale = "PiYG"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc4321_piechart_mask.png"
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
              clim = clim,
              showbeam = False)


### ngc3627
ra_center = "11:20:15.35"
dec_center = "12.58.87.0"
xlim = [-135, 135]
ylim = [160, -110]
value = None

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc3627_co21/co21_08p0.moment0.fits"
imagename_color = "ngc3627_r21/piechart_08p0.mask.fits"
contour = [0.0197,0.020,0.0203]#[0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "NGC 3627 HII Region Mask"
colorscale = "PiYG"
colorlog = False
colorbar = False
colorbar_label = ""
output = "eps/ngc3627_piechart_mask.png"
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
              clim = clim,
              showbeam = False)

os.system("rm -rf *.last")

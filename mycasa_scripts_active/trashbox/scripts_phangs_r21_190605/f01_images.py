import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/phangs/co_ratio/ngc0628/"
ra_center = "01:36:41.694"
dec_center = "15.46.56.797"
xlim = [-120, 120]
ylim = [120, -120]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

#####################
### Main Procedure
#####################
"""
###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc0628_co10_4p0.moment0.fits"
imagename_color = "ngc0628_co10_4p0.moment0.fits"
contour = [0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc0628_12co10_m0.png"
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


### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc0628_co21_4p0.moment0.fits"
imagename_color = "ngc0628_co21_4p0.moment0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc0628_12co21_m0.png"
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

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc0628_co21_4p0.moment0.fits"
imagename_color = "ngc0628_r21_4p0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "../eps/ngc0628_r21.png"
clim = [0, 1.2]
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
"""


### ngc4321
dir_data = "/Users/saito/data/phangs/co_ratio/"
data_image = glob.glob(dir_data + "ngc4321_co/*_4p0*moment0")
data_r21 = glob.glob(dir_data + "ngc4321_co/*r21_4p0*")
data_image = np.r_[data_image, data_r21]

for i in range(len(data_image)):
    os.system("rm -rf " + data_image[i].replace(".image","") + ".fits")
    exportfits(imagename = data_image[i],
               fitsimage = data_image[i].replace(".image","") + ".fits")

dir_data = "/Users/saito/data/phangs/co_ratio/ngc4321_co/"
ra_center = "12:22:54.931"
dec_center = "15.49.20.369"
xlim = [-100, 100]
ylim = [100, -100]
value = None

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co10_4p0.moment0.fits"
imagename_color = "ngc4321_co10_4p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co10_m0.png"
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


### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co21_4p0.moment0.fits"
imagename_color = "ngc4321_co21_4p0.moment0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co21_m0.png"
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

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4321_co21_4p0.moment0.fits"
imagename_color = "ngc4321_r21_4p0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
color_contour = "black"
color_beam = "black"
colorbar_label = "Ratio"
output = "../eps/ngc4321_r21.png"
clim = [0, 1.]
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


### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4321_co21_4p0.moment0.fits"
imagename_color = "ngc4321_r21_4p0_m8.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Peak Temperature Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
color_contour = "black"
color_beam = "black"
colorbar_label = "Ratio"
output = "../eps/ngc4321_r21_m8.png"
clim = [0, 1.]
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


"""
### ngc3627
dir_data = "/Users/saito/data/phangs/co_ratio/ngc3627_co/"
ra_center = "11:20:14.973"
dec_center = "12.58.17.194"
xlim = [-160, 160]
ylim = [160, -160]
value = None

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc3627_co10_8p0.moment0.fits"
imagename_color = "ngc3627_co10_8p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc3627_12co10_m0.png"
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


### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc3627_co21_8p0.moment0.fits"
imagename_color = "ngc3627_co21_8p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc3627_12co21_m0.png"
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

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc3627_co21_8p0.moment0.fits"
imagename_color = "ngc3627_r21_8p0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1)/$^{12}$CO (1-0) Line Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "../eps/ngc3627_r21.png"
clim = [0, 1.2]
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


### ngc3351
dir_data = "/Users/saito/data/phangs/co_ratio/ngc3351/"
ra_center = "10:43:56.300"
dec_center = "11.42.12.909"
xlim = [-80, 80]
ylim = [80, -80]
value = None

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc3351_co10_8p0.moment0.fits"
imagename_color = "ngc3351_co10_8p0.moment0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc3351_12co10_m0.png"
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

### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc3351_co21_8p0.moment0.fits"
imagename_color = "ngc3351_co21_8p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc3351_12co21_m0.png"
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

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc3351_co21_8p0.moment0.fits"
imagename_color = "ngc3351_r21_8p0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1)/$^{12}$CO (1-0) Line Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "../eps/ngc3351_r21.png"
clim = [0, 1.2]
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


### ngc4254
dir_data = "/Users/saito/data/phangs/co_ratio/ngc4254_co/"
ra_center = "12:18:49.682"
dec_center = "14.25.42.531"
xlim = [-120, 120]
ylim = [120, -120]
value = None

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4254_co10_8p0.moment0.fits"
imagename_color = "ngc4254_co10_8p0.moment0.fits"
contour = [0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4254_12co10_m0.png"
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

### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4254_co21_8p0.moment0.fits"
imagename_color = "ngc4254_co21_8p0.moment0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4254_12co21_m0.png"
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

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4254_co21_8p0.moment0.fits"
imagename_color = "ngc4254_r21_8p0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1)/$^{12}$CO (1-0) Line Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "../eps/ngc4254_r21.png"
clim = [0, 1]
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
"""


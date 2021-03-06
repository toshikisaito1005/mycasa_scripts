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
data_image = glob.glob(dir_data + "*/*_04p0*moment0_Kelvin")
data_image.extend(glob.glob(dir_data + "*/*_04p0*moment8_Kelvin"))
data2_image = glob.glob(dir_data + "*/*_08p0*moment0_Kelvin")
data2_image.extend(glob.glob(dir_data + "*/*_08p0*moment0"))
data3_image =  glob.glob(dir_data + "*_r21/*_04p0*moment0")
data3_image.extend(glob.glob(dir_data + "*_r21/*_08p0*moment0"))
data_image = np.r_[data_image, data2_image, data3_image]
data_image.sort()


for i in range(len(data_image)):
    os.system("rm -rf " + data_image[i].replace(".image","") + ".fits")
    exportfits(imagename = data_image[i],
               fitsimage = data_image[i].replace(".image","") + ".fits")

done = glob.glob(dir_data + "eps/")
if not done:
    os.mkdir(dir_data + "eps/")


#####################
### Main Procedure
#####################
ra_center = "01:36:41.8"
dec_center = "15.47.0.0"
xlim = [-120, 120]
ylim = [120, -120]
value = None

###12CO(1-0)
co10max = imstat(dir_data+"ngc0628_co10/co10_04p0.moment0_Kelvin")["max"][0]
co21max = imstat(dir_data+"ngc0628_co21/co21_04p0.moment0_Kelvin")["max"][0]
# moment 0 color + moment 0 contour
imagename_contour = "ngc0628_co10/co10_04p0.moment0_Kelvin.fits"
imagename_color = "ngc0628_co10/co10_04p0.moment0_Kelvin.fits"
contour = np.array([0.04, 0.08, 0.16, 0.32, 0.64, 0.96]) / co10max * co21max
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc0628_12co10_m0.png"
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
              nucleus = 50)


### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc0628_co21/co21_04p0.moment0_Kelvin.fits"
imagename_color = "ngc0628_co21/co21_04p0.moment0_Kelvin.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc0628_12co21_m0.png"
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
              nucleus = 50)

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc0628_co21/co21_04p0.moment0_Kelvin.fits"
imagename_color = "ngc0628_r21/r21_04p0.moment0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "eps/ngc0628_r21.png"
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
              clim = clim,
              nucleus = 50)


### ngc4321
ra_center = "12:22:54.931"
dec_center = "15.49.20.369"
xlim = [-100, 100]
ylim = [100, -100]
value = None

###12CO(1-0)
co10max = imstat(dir_data+"ngc4321_co10/co10_04p0.moment0_Kelvin")["max"][0]
co21max = imstat(dir_data+"ngc4321_co21/co21_04p0.moment0_Kelvin")["max"][0]
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co10/co10_04p0.moment0_Kelvin.fits"
imagename_color = "ngc4321_co10/co10_04p0.moment0_Kelvin.fits"
contour = np.array([0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]) / co10max * co21max
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc4321_12co10_m0.png"
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
              nucleus = 30)

### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co21/co21_04p0.moment0_Kelvin.fits"
imagename_color = "ngc4321_co21/co21_04p0.moment0_Kelvin.fits"
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc4321_12co21_m0.png"
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
              nucleus = 30)

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4321_co21/co21_04p0.moment0_Kelvin.fits"
imagename_color = "ngc4321_r21/r21_04p0.moment0.fits"
contour = [0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Integrated Intensity Ratio"
colorscale = "jet" #"jet"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/ngc4321_r21.png"
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
              clim = clim,
              nucleus = 30)

"""
### R21
# R21 color + CO(2-1) moment 0 contour
color_contour = "grey"
color_beam = "grey"
imagename_contour = "ngc4321_co21/co21_04p0.moment0.fits"
imagename_color = "ngc4321_r21/r21_04p0.moment8.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Peak Temperature Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Ratio"
output = "eps/ngc4321_r21_m8.png"
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
ra_center = "11:20:15.35"
dec_center = "12.58.87.0"
xlim = [-135, 135]
ylim = [160, -110]
value = None

###12CO(1-0)
co10max = imstat(dir_data+"ngc3627_co10/co10_08p0.moment0_Kelvin")["max"][0]
co21max = imstat(dir_data+"ngc3627_co21/co21_08p0.moment0_Kelvin")["max"][0]
# moment 0 color + moment 0 contour
imagename_contour = "ngc3627_co10/co10_08p0.moment0_Kelvin.fits"
imagename_color = "ngc3627_co10/co10_08p0.moment0_Kelvin.fits"
contour = np.array([0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]) / co10max * co21max
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc3627_12co10_m0.png"
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
              nucleus = 50)


### 12CO(2-1)
# moment 0 color + moment 0 contour
imagename_contour = "ngc3627_co21/co21_08p0.moment0_Kelvin.fits"
imagename_color = "ngc3627_co21/co21_08p0.moment0_Kelvin.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc3627_12co21_m0.png"
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
              nucleus = 50)

### R21
# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc3627_co21/co21_08p0.moment0_Kelvin.fits"
imagename_color = "ngc3627_r21/r21_08p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1)/$^{12}$CO (1-0) Line Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "eps/ngc3627_r21.png"
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
              clim = clim,
              nucleus = 50)



### ngc4254
"""
ra_center = "12:18:49.3"
dec_center = "14.25.01.0"
xlim = [-120, 120]
ylim = [120, -120]
value = None

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4254_co10/co10_08p0.moment0.fits"
imagename_color = "ngc4254_co10/co10_08p0.moment0.fits"
contour = [0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc4254_12co10_m0.png"
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
imagename_contour = "ngc4254_co21/co21_08p0.moment0.fits"
imagename_color = "ngc4254_co21/co21_08p0.moment0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "eps/ngc4254_12co21_m0.png"
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
imagename_contour = "ngc4254_co21/co21_08p0.moment0.fits"
imagename_color = "ngc4254_r21/r21_08p0.moment0.fits"
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1)/$^{12}$CO (1-0) Line Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
colorbar_label = "Line Ratio"
output = "eps/ngc4254_r21.png"
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

os.system("rm -rf *.last")


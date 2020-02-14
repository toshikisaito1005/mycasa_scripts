import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

dir_data = "/Users/saito/data/phangs/co_ratio/"
data_image = glob.glob(dir_data + "*_co/*_*p0*moment0")
data_r21 = glob.glob(dir_data + "*_co/*r21_*p0*image")
data_image = np.r_[data_image, data_r21]

for i in range(len(data_image)):
    done = glob.glob(data_image[i].replace(".image","") + ".fits")
    if not done:
        exportfits(imagename = data_image[i],
                   fitsimage = data_image[i].replace(".image","") + ".fits")

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

#####################
### Main Procedure
#####################
### ngc4321
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
output = "../eps/ngc4321_12co10_m0_4p0.png"
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

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co10_8p0.moment0.fits"
imagename_color = "ngc4321_co10_8p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co10_m0_8p0.png"
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

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co10_12p0.moment0.fits"
imagename_color = "ngc4321_co10_12p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co10_m0_12p0.png"
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

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co10_16p0.moment0.fits"
imagename_color = "ngc4321_co10_16p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co10_m0_16p0.png"
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

###12CO(1-0)
# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co10_20p0.moment0.fits"
imagename_color = "ngc4321_co10_20p0.moment0.fits"
contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (1-0) Integrated Intensity"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co10_m0_20p0.png"
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
output = "../eps/ngc4321_12co21_m0_4p0.png"
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

# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co21_8p0.moment0.fits"
imagename_color = "ngc4321_co21_8p0.moment0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co21_m0_8p0.png"
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

# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co21_12p0.moment0.fits"
imagename_color = "ngc4321_co21_12p0.moment0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co21_m0_12p0.png"
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

# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co21_16p0.moment0.fits"
imagename_color = "ngc4321_co21_16p0.moment0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co21_m0_16p0.png"
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

# moment 0 color + moment 0 contour
imagename_contour = "ngc4321_co21_20p0.moment0.fits"
imagename_color = "ngc4321_co21_20p0.moment0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO (2-1) Integrated Intensity"
colorscale = "OrRd"
colorlog = True
colorbar = False
colorbar_label = "(Jy km s$^{-1}$)"
output = "../eps/ngc4321_12co21_m0_20p0.png"
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
output = "../eps/ngc4321_r21_4p0.png"
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

# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4321_co21_8p0.moment0.fits"
imagename_color = "ngc4321_r21_8p0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
color_contour = "black"
color_beam = "black"
colorbar_label = "Ratio"
output = "../eps/ngc4321_r21_8p0.png"
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

# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4321_co21_12p0.moment0.fits"
imagename_color = "ngc4321_r21_12p0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
color_contour = "black"
color_beam = "black"
colorbar_label = "Ratio"
output = "../eps/ngc4321_r21_12p0.png"
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

# R21 color + CO(2-1) moment 0 contour
imagename_contour = "ngc4321_co21_16p0.moment0.fits"
imagename_color = "ngc4321_r21_16p0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
color_contour = "black"
color_beam = "black"
colorbar_label = "Ratio"
output = "../eps/ngc4321_r21_16p0.png"
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

imagename_contour = "ngc4321_co21_20p0.moment0.fits"
imagename_color = "ngc4321_r21_20p0.fits"
contour = [0.005, 0.01, 0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]
title = "$^{12}$CO Integrated Intensity Ratio"
colorscale = "jet"
colorlog = False
colorbar = True
color_contour = "black"
color_beam = "black"
colorbar_label = "Ratio"
output = "../eps/ngc4321_r21_20p0.png"
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

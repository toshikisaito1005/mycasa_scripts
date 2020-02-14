import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


contour = [0.02, 0.04, 0.08, 0.16, 0.32, 0.64, 0.96]

#####################
### Main Procedure
#####################

### eso148
dir_data = "../../hcn_ulirgs/hcn_eso148/"
ra_center = "23:15:46.793"
dec_center = "-59.03.13.839"
xlim = [-5, 5]
ylim = [5, -5]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

### eso148 hcn43
# moment 0 color + moment 0 contour
imagename_contour = "ESO_148_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "ESO_148_AL3B7_hcn43_l20_na.moment0.fits"
title = "ESO 148-IG002: HCN (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/eso148_hcn_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "ESO_148_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "ESO_148_AL3B7_hcn43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12640, 12960]
title = "ESO 148-IG002: HCN (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso148_hcn_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "ESO_148_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "ESO_148_AL3B7_hcn43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "ESO 148-IG002: HCN (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso148_hcn_m2.eps"
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


### eso148 hco_plus43
# moment 0 color + moment 0 contour
imagename_contour = "ESO_148_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "ESO_148_AL3B7_hco_plus43_l20_na.moment0.fits"
title = "ESO 148-IG002: HCO$^{+}$ (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/eso148_hco_plus_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "ESO_148_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "ESO_148_AL3B7_hco_plus43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12640, 12960]
title = "ESO 148-IG002: HCO$^{+}$ (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso148_hco_plus_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "ESO_148_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "ESO_148_AL3B7_hco_plus43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "ESO 148-IG002: HCO$^{+}$ (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso148_hco_plus_m2.eps"
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


### eso286
dir_data = "../../hcn_ulirgs/hcn_eso286/"
ra_center = "20:58:26.799"
dec_center = "-42.39.00.9"
xlim = [-5, 5]
ylim = [5, -5]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

### eso148 hcn43
# moment 0 color + moment 0 contour
imagename_contour = "ESO_286_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "ESO_286_AL3B7_hcn43_l20_na.moment0.fits"
title = "ESO 286-IG019: HCN (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/eso286_hcn_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "ESO_286_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "ESO_286_AL3B7_hcn43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12160, 12520]
title = "ESO 286-IG019: HCN (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso286_hcn_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "ESO_286_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "ESO_286_AL3B7_hcn43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "ESO 286-IG019: HCN (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso286_hcn_m2.eps"
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


### eso148 hco_plus43
# moment 0 color + moment 0 contour
imagename_contour = "ESO_286_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "ESO_286_AL3B7_hco_plus43_l20_na.moment0.fits"
title = "ESO 286-IG019: HCO$^{+}$ (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/eso286_hco_plus_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "ESO_286_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "ESO_286_AL3B7_hco_plus43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12160, 12520]
title = "ESO 286-IG019: HCO$^{+}$ (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso286_hco_plus_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "ESO_286_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "ESO_286_AL3B7_hco_plus43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "ESO 286-IG019: HCO$^{+}$ (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/eso286_hco_plus_m2.eps"
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


### iras05189
dir_data = "../../hcn_ulirgs/hcn_iras05189/"
ra_center = "05:21:01.335"
dec_center = "-25.21.45.9"
xlim = [-3, 3]
ylim = [3, -3]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

### eso148 hcn43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_F05189_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F05189_AL3B7_hcn43_l20_na.moment0.fits"
title = "IRAS F05189-2524: HCN (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/iras05189_hcn_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_F05189_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F05189_AL3B7_hcn43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12200, 12360]
title = "IRAS F05189-2524: HCN (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras05189_hcn_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_F05189_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F05189_AL3B7_hcn43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "IRAS F05189-2524: HCN (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras05189_hcn_m2.eps"
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


### eso148 hco_plus43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_F05189_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F05189_AL3B7_hco_plus43_l20_na.moment0.fits"
title = "IRAS F05189-2524: HCO$^{+}$ (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/iras05189_hco_plus_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_F05189_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F05189_AL3B7_hco_plus43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12200, 12360]
title = "IRAS F05189-2524: HCO$^{+}$ (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras05189_hco_plus_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_F05189_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F05189_AL3B7_hco_plus43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "IRAS F05189-2524: HCO$^{+}$ (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras05189_hco_plus_m2.eps"
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


### iras13120
dir_data = "../../hcn_ulirgs/hcn_iras13120/"
ra_center = "13:15:06.359"
dec_center = "-55.09.23.779"
xlim = [-3, 3]
ylim = [3, -3]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

### iras13120 hcn43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_13120_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_13120_AL3B7_hcn43_l20_na.moment0.fits"
title = "IRAS 13120-5453: HCN (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/iras13120_hcn_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_13120_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_13120_AL3B7_hcn43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [8840, 9280]
title = "IRAS 13120-5453: HCN (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras13120_hcn_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_13120_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_13120_AL3B7_hcn43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "IRAS 13120-5453: HCN (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras13120_hcn_m2.eps"
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


### eso148 hco_plus43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_13120_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_13120_AL3B7_hco_plus43_l20_na.moment0.fits"
title = "IRAS 13120-5453: HCO$^{+}$ (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/iras13120_hco_plus_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_13120_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_13120_AL3B7_hco_plus43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [8840, 9280]
title = "IRAS 13120-5453: HCO$^{+}$ (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras13120_hco_plus_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_13120_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_13120_AL3B7_hco_plus43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 100]
title = "IRAS 13120-5453: HCO$^{+}$ (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/iras13120_hco_plus_m2.eps"
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


### irasf12112
dir_data = "../../hcn_ulirgs/hcn_irasf12112/"
ra_center = "12:13:46.140"
dec_center = "02.48.40.498"
xlim = [-3, 3]
ylim = [3, -3]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

### iras13120 hcn43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_F12112_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F12112_AL3B7_hcn43_l20_na.moment0.fits"
title = "IRAS F12112+0305: HCN (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/irasf12112_hcn_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_F12112_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F12112_AL3B7_hcn43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [20090, 20600]
title = "IRAS F12112+0305: HCN (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf12112_hcn_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_F12112_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F12112_AL3B7_hcn43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 200]
title = "IRAS F12112+0305: HCN (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf12112_hcn_m2.eps"
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


### eso148 hco_plus43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_F12112_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F12112_AL3B7_hco_plus43_l20_na.moment0.fits"
title = "IRAS F12112+0305: HCO$^{+}$ (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/irasf12112_hco_plus_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_F12112_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F12112_AL3B7_hco_plus43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [20090, 20600]
title = "IRAS F12112+0305: HCO$^{+}$ (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf12112_hco_plus_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_F12112_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F12112_AL3B7_hco_plus43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 200]
title = "IRAS F12112+0305: HCO$^{+}$ (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf12112_hco_plus_m2.eps"
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


### irasf17207
dir_data = "../../hcn_ulirgs/hcn_irasf17207/"
ra_center = "17:23:21.927"
dec_center = "-00.17.01.842"
xlim = [-2, 2]
ylim = [2, -2]
value = None

done = glob.glob(dir_data + "../eps/")
if not done:
    os.mkdir(dir_data + "../eps/")

### iras13120 hcn43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_F17207_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F17207_AL3B7_hcn43_l20_na.moment0.fits"
title = "IRAS F17207-0014: HCN (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/irasf17207_hcn_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_F17207_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F17207_AL3B7_hcn43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12030, 12620]
title = "IRAS F17207-0014: HCN (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf17207_hcn_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_F17207_AL3B7_hcn43_l20_na.moment0.fits"
imagename_color = "IRAS_F17207_AL3B7_hcn43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 200]
title = "IRAS F17207-0014: HCN (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf17207_hcn_m2.eps"
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


### eso148 hco_plus43
# moment 0 color + moment 0 contour
imagename_contour = "IRAS_F17207_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F17207_AL3B7_hco_plus43_l20_na.moment0.fits"
title = "IRAS F17207-0014: HCO$^{+}$ (4-3) Moment-0"
colorscale = "PuBu"
color_contour = "black"
color_beam = "black"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$ km s$^{-1}$)"
output = "../eps/irasf17207_hco_plus_m0.eps"
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

# moment 1 color + moment 0 contour
imagename_contour = "IRAS_F17207_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F17207_AL3B7_hco_plus43_l20_na.moment1.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [12030, 12620]
title = "IRAS F17207-0014: HCO$^{+}$ (4-3) Moment-1"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf17207_hco_plus_m1.eps"
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

# moment 2 color + moment 0 contour
imagename_contour = "IRAS_F17207_AL3B7_hco_plus43_l20_na.moment0.fits"
imagename_color = "IRAS_F17207_AL3B7_hco_plus43_l20_na.moment2.fits"
colorscale = "rainbow"
colorlog = False
colorbar = True
clim = [0, 200]
title = "IRAS F17207-0014: HCO$^{+}$ (4-3) Moment-2"
colorbar_label = "(km s$^{-1}$)"
output = "../eps/irasf17207_hco_plus_m2.eps"
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
### dust continuum
contour = [0.04, 0.08, 0.16, 0.32, 0.64, 0.96]

# eso148
dir_data = "../../hcn_ulirgs/hcn_eso148/"
ra_center = "23:15:46.793"
dec_center = "-59.03.10.839"
xlim = [-5, 5]
ylim = [5, -5]
value = None
imagename_contour = "ESO_148-IG002_AL2B6_contin_na.fits"
imagename_color = "ESO_148-IG002_AL2B6_contin_na.fits"
title = "ESO 148-IG002: Band 7 Continuum"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$)"
output = "../eps/eso148_contin.eps"
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

# eso286
dir_data = "../../hcn_ulirgs/hcn_eso286/"
ra_center = "20:58:26.799"
dec_center = "-42.39.00.9"
xlim = [-5, 5]
ylim = [5, -5]
value = None
imagename_contour = "ESO_286-IG019_AL2B6_contin_na.fits"
imagename_color = "ESO_286-IG019_AL2B6_contin_na.fits"
title = "ESO 286-IG019: Band 7 Continuum"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$)"
output = "../eps/eso286_contin.eps"
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

# iras13120
dir_data = "../../hcn_ulirgs/hcn_iras13120/"
ra_center = "13:15:06.359"
dec_center = "-55.09.23.779"
xlim = [-3, 3]
ylim = [3, -3]
value = None
imagename_contour = "IRAS_13120-5453_AL2B6_contin_na.fits"
imagename_color = "IRAS_13120-5453_AL2B6_contin_na.fits"
title = "IRAS 13120-5453: Band 7 Continuum"
colorscale = "rainbow"
color_contour = "white"
color_beam = "white"
colorlog = False
colorbar = True
colorbar_label = "(Jy beam$^{-1}$)"
output = "../eps/iras13120_contin.eps"
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


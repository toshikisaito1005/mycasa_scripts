import os
import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord


#####################
### set keys
#####################
dir_fits = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_other/env_masks/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
spiral_fits = ["NGC0628_mask_v5_sp_arms.image",    # >0
				       "NGC3627_mask_large_barends.image", # 5
				       "NGC4321_mask_v5_sp_arms.image"]    # >0
mom0_fits = ["../../ngc0628_r21/r21_04p0.moment0",
			 "../../ngc3627_r21/r21_08p0.moment0",
			 "../../ngc4321_r21/r21_04p0.moment0"]
output = ["../../ngc0628_r21/env_04p0.mask.fits",
		  "../../ngc3627_r21/env_08p0.mask.fits",
		  "../../ngc4321_r21/env_04p0.mask.fits"]
expr = ["iif(IM0>0,1,0)",
        "iif(IM0=5,1,0)",
        "iif(IM0>0,1,0)"]
# output = "ngc1365_cprops_mask_1p38.fits"
snr = 5.0 # peak signal-to-noise ratio threshold to identify clouds
scales = [44/1.0,52/1.3,103/1.4] # parsec / arcsec
image_ra_cnt = ["01:36:41.790",
				"11:20:15.181",
				"12:22:54.961"]
image_decl_cnt = ["15.46.58.400",
				  "12.59.28.137",
				  "15.49.20.263"]
convolution_scale = [np.sqrt((44/1.0*4.0)**2-120**2),
					 np.sqrt((52/1.3*8.0)**2-120**2),
					 np.sqrt((103/1.4*4.0)**2-120**2),
					 ]

i=0


#####################
### Main Procedure
#####################
expr = expr[i]
spiral_fits = dir_fits + spiral_fits[i]
mom0_fits = dir_fits + mom0_fits[i]
output = dir_fits + output[i]
image_ra_cnt = image_ra_cnt[i]
image_decl_cnt = image_decl_cnt[i]
scale = scales[i]
convolution_scale = convolution_scale[i]


#
os.system("rm -rf " + spiral_fits.replace(".image",".mask"))
immath(imagename = spiral_fits,
  expr = expr,
  outfile = spiral_fits.replace(".image",".mask"))

done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

imregrid(imagename = spiral_fits.replace(".image",".mask"),
  template = mom0_fits,
  output = output.replace(".fits",".image"))

exportfits(imgaename = output.replace(".fits",".image"),
  fitsimage = output)

os.system("rm -rf *.last")

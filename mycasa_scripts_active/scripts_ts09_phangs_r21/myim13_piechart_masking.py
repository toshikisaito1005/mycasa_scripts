import os
import glob
import numpy as np
from astropy.io import fits
from astropy.table import Table
from astropy.coordinates import SkyCoord


#####################
### set keys
#####################
dir_fits = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data_other/mask_piechart/"
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"
spiral_fits = ["ngc0628_HASUB_astro_sqr_HII.SNHoopes_commonfov_04arcsec_clipped.image",
               "ngc3627_HASUB_astro_sqr_HII.SNHoopes_commonfov_08arcsec_clipped.image",
               "ngc4321_HASUB_astro_sqr_HII.SNHoopes_commonfov_04arcsec_clipped.image",
               "ngc0628_HASUB_astro_sqr_HII.SNHoopes_commonfov_20arcsec_clipped.image",
               "ngc3627_HASUB_astro_sqr_HII.SNHoopes_commonfov_24arcsec_clipped.image",
               "ngc4321_HASUB_astro_sqr_HII.SNHoopes_commonfov_20arcsec_clipped.image"]
mom0_fits = ["../../ngc0628_r21/r21_04p0.moment0",
       "../../ngc3627_r21/r21_08p0.moment0",
       "../../ngc4321_r21/r21_04p0.moment0",
       "../../ngc0628_r21/r21_20p0.moment0",
       "../../ngc3627_r21/r21_24p0.moment0",
       "../../ngc4321_r21/r21_20p0.moment0"]
output = ["../../ngc0628_r21/piechart_04p0.mask.fits",
      "../../ngc3627_r21/piechart_08p0.mask.fits",
      "../../ngc4321_r21/piechart_04p0.mask.fits",
      "../../ngc0628_r21/piechart_20p0.mask.fits",
      "../../ngc3627_r21/piechart_24p0.mask.fits",
      "../../ngc4321_r21/piechart_20p0.mask.fits"]
expr = ["iif(IM0>0,1,0)",
        "iif(IM0>0,1,0)",
        "iif(IM0>0,1,0)",
        "iif(IM0>0,1,0)",
        "iif(IM0>0,1,0)",
        "iif(IM0>0,1,0)"]


#####################
### Main Procedure
#####################
for i in range(len(spiral_fits)):
  this_expr = expr[i]
  this_spiral_fits = dir_fits + spiral_fits[i]
  this_mom0_fits = dir_fits + mom0_fits[i]
  this_output = dir_fits + output[i]
  print("### processing " + this_spiral_fits)
  #
  os.system("rm -rf " + this_spiral_fits.replace(".image",".mask"))
  immath(imagename = this_spiral_fits,
    expr = this_expr,
    outfile = this_spiral_fits.replace(".image",".mask"))

  done = glob.glob(dir_product)
  if not done:
      os.mkdir(dir_product)

  os.system("rm -rf " + this_output.replace(".fits",".image"))
  imregrid(imagename = this_spiral_fits.replace(".image",".mask"),
    template = this_mom0_fits,
    output = this_output.replace(".fits",".image"))

  immath(imagename = this_output.replace(".fits",".image"),
    expr = "iif(IM0>0,1,0)",
    outfile = this_output.replace(".fits",".image2"))

  os.system("rm -rf " + this_output)
  exportfits(imagename = this_output.replace(".fits",".image2"),
    fitsimage = this_output)

  os.system("rm -rf " + this_output.replace(".fits",".image"))
  importfits(fitsimage = this_output,
             imagename = this_output.replace(".fits",".image"),
             defaultaxes = True,
             defaultaxesvalues = ["RA","Dec","1GHz","Stokes"])

  os.system("rm -rf " + this_output)
  exportfits(imagename = this_output.replace(".fits",".image"),
    fitsimage = this_output)

  os.system("rm -rf " + this_output.replace(".fits",".image*"))


os.system("rm -rf *.last")

import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/datacube_line/"
pa = "40deg"
blc = [128,  10, 0,  1]
trc = [148, 269, 0, 49]


#####################
### Main Procedure
#####################
imagename = "line_12co10_contsub_clean20_nat.image.regrid.immath.masked"


output = dir_data + imagename + ".rotated"
os.system("rm -rf " + output)
ia.open(dir_data + imagename)
ia.rotate(pa = pa, outfile = output)
ia.close()


mybox = rg.box(blc = blc, trc = trc)
output = dir_data + imagename + ".pv"
os.system("rm -rf " + output)
ia.open(dir_data + imagename + ".rotated")
rebin_bin = [1, trc[1] - blc[1] + 1, 1, 1]
ia.rebin(region = mybox,
               outfile = output,
               bin = rebin_bin,
               dropdeg = True,
               overwrite = True,
               crop = True)
ia.close()



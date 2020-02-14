import os
import re
import sys
import glob
sys.path.append(os.getcwd())
import mycasaimaging_tools as myim


dir_data = "../../ngc3110/ana/data_continuum/"
major = "1.8arcsec"
minor = "1.8arcsec"

#####################
### Main Procedure
#####################
template = "../../ngc3110/ana/datacube_line/line_12co10_contsub_clean20_nat.image.regrid.immath.moment0"


imagenames = glob.glob(dir_data + "*.image")

for i in range(len(imagenames)):
    outfile_smooth = imagenames[i] + ".smooth"
    os.system("rm -rf " + outfile_smooth)
    imsmooth(imagename = imagenames[i],
        kernel = "gauss",
        targetres = True,
        major = major,
        minor = major,
        pa = "0.0deg",
        outfile = outfile_smooth)
    outfile_regrid = imagenames[i] + ".regrid"
    os.system("rm -rf " + outfile_regrid)
    imregrid(imagename = outfile_smooth,
        template = template,
        output = outfile_regrid)
    os.system("rm -rf " + outfile_smooth)


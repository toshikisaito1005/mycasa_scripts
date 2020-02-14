import os
import re
import sys
import glob
import scipy
sys.path.append(os.getcwd() + "/..")
import mycasaimaging_tools as myim


#####################
### Main Procedure
#####################
dir_data = ["../../hcn_ulirgs/hcn_eso148/",
            "../../hcn_ulirgs/hcn_eso286/",
            "../../hcn_ulirgs/hcn_iras05189/",
            "../../hcn_ulirgs/hcn_iras13120/",
            "../../hcn_ulirgs/hcn_irasf12112/",
            "../../hcn_ulirgs/hcn_irasf17207/"]

fitsimage = ["ESO_148-IG002_AL2B6_contin_na.fits",
             "ESO_286-IG019_AL2B6_contin_na.fits",
             "IRAS_F05189-2524_AL2B6_contin_na.fits",
             "IRAS_13120-5453_AL2B6_contin_na.fits",
             "IRAS_F12112+0305_AL2B6_contin_na.fits",
             "IRAS_F17207-0014_AL2B6_contin_na.fits"]

for i in range(len(dir_data)):
    output = dir_data[i] + fitsimage[i].replace(".fits", "_j2000.image")
    os.system("rm -rf " + output)
    imregrid(imagename = dir_data[i] + fitsimage[i],
             template = "J2000",
             output = output)
    outfits = output.replace(".image", ".fits")
    os.system("rm -rf " + outfits)
    exportfits(imagename = output,
               fitsimage = outfits)
    os.system("rm -rf " + output)

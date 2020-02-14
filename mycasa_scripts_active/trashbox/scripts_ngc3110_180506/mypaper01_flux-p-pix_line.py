import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data1 = "../../ngc3110/ana/other/"
dir_data2 = "../../ngc3110/ana/datacube_line/"
ra_blc = "10h04m05.152s" #blc
decl_blc = "-06.29.14.082" #blc
ra_trc = "10h03m59.126s" #trc
decl_trc = "-06.27.44.270" #trc

#####################
### Main Procedure
#####################
dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)

dir_product = dir_data1 + "photmetry/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

product_file = dir_product + "ngc3110_flux.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y h-alpha co10 co21 13co10 13co21\n")
f.close()

region_file = dir_casa_region + "box.region"
f = open(region_file, "w")
f.write("#CRTFv0\n")
f.write("global coord=J2000\n")
f.write("\n")
f.write("box[[" + ra_blc + ", " + decl_blc + "], [" + ra_trc + ", " + decl_trc + "]]")
f.write("")
f.close()

#h-alpha
value = imval(imagename = dir_data1 + "n3110.ha-new.fits",
              region = region_file)
value_haplha = value["data"]

#co10
beta = 1.226 * 10 ** 6. / 1.813 / 1.434 / 115.27120 ** 2

value = imval(imagename = dir_data2 + "line_12co10_contsub_clean20_nat.image.regrid.immath.moment0",
              region = region_file)
value_co10 = value["data"] * beta

#co21
value = imval(imagename = dir_data2 + "line_12co21_contsub_clean20_nat.image.regrid.immath.moment0",
              region = region_file)
value_co21 = value["data"]  * beta

#13co10
value = imval(imagename = dir_data2 + "line_13co10_contsub_clean20_nat.image.regrid.immath.moment0",
              region = region_file)
value_13co10 = value["data"]  * beta

#13co21
value = imval(imagename = dir_data2 + "line_13co21_contsub_clean20_nat.image.regrid.immath.moment0",
              region = region_file)
value_13co21 = value["data"]  * beta

# writing
f = open(product_file, "a")
for i in range(len(value_haplha[0])):
    for j in range(len(value_haplha[1])):
        f.write(str(i) + " " + str(j) \
                + " " + str(value_haplha[i,j]) \
                + " " + str(value_co10[i,j]) \
                + " " + str(value_co21[i,j]) \
                + " " + str(value_13co10[i,j]) \
                + " " + str(value_13co21[i,j]) \
                + "\n")
f.close()


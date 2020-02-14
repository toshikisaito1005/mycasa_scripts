import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data1 = "../../../ngc3110/ana/other/"
dir_data2 = "../../../ngc3110/ana/data_continuum/"
ra = "10h04m03.181s" #blc
decl = "-06d29m01.279s" #blc

#####################
### Main Procedure
#####################
### H-alpha
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60
ra_deg = ra_hh + ra_mm + ra_ss
decl_deg = decl_hh - decl_mm - decl_ss

step_ra = 1.5 / 60 / 60
step_decl = 1.5 / 60 / 60 * sqrt(3)
ra_deg = ra_deg + step_ra
decl_deg = decl_deg - step_decl

dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)

dir_product = dir_data1 + "photmetry/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

product_file = dir_product + "ngc3110_flux_contin.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y h-alpha band3 band6\n")
f.close()

for i in range(25):
    ra_deg = ra_deg - step_ra
    ra_deg2 = ra_deg - step_ra / 2. ################
    decl_deg = decl_hh - decl_mm - decl_ss
    for j in range(25):
        decl_deg = decl_deg + step_decl
        # region R
        region_file = dir_casa_region + "R_" + str(i) + "_" + str(j) + ".region"
        f = open(region_file, "w")
        f.write("#CRTFv0\n")
        f.write("global coord=J2000\n")
        f.write("\n")
        f.write("circle[[" + str(round(ra_deg, 5)) + "deg, " + str(round(decl_deg, 7)) + "deg], 1.5arcsec]")
        f.write("")
        f.close()
        # region H
        region_file2 = dir_casa_region + "H_" + str(i) + "_" + str(j) + ".region"
        decl_deg2 = decl_deg + step_decl / 2.
        f = open(region_file2, "w")
        f.write("#CRTFv0\n")
        f.write("global coord=J2000\n")
        f.write("\n")
        f.write("circle[[" + str(round(ra_deg2, 5)) + "deg, " + str(round(decl_deg2, 7)) + "deg], 1.5arcsec]")
        f.write("")
        f.close()
        #h-alpha: R
        value = imval(imagename = dir_data1 + "n3110.ha-new.fits",
                      region = region_file)
        value_masked_haplha = value["data"] * value["mask"]
        data_halpha = value_masked_haplha.sum(axis = (0, 1))
        #h-alpha: H
        value = imval(imagename = dir_data1 + "n3110.ha-new.fits",
                      region = region_file2)
        value_masked_haplha2 = value["data"] * value["mask"]
        data_halpha2 = value_masked_haplha.sum(axis = (0, 1))
        #band 3 continuum 104.024625: R
        value = imval(imagename = dir_data2 + "continuum_band3_12co10_13co10_clean.image.regrid",
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        data_co10 = value_masked_co10.sum(axis = (0, 1))
        if data_co10 < 3.890841e-05 * sqrt(113) * 3.0:
            data_co10 = 0.0
        #band 3 continuum 104.024625: H
        value = imval(imagename = dir_data2 + "continuum_band3_12co10_13co10_clean.image.regrid",
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        data_co102 = value_masked_co102.sum(axis = (0, 1))
        if data_co102 < 3.890841e-05 * sqrt(113) * 3.0:
            data_co102 = 0.0
        #band 6 continuum #234.6075: R
        value = imval(imagename = dir_data2 + "continuum_band6_12co21_13co21_clean.image.regrid",
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        data_co21 = value_masked_co21.sum(axis = (0, 1))
        if data_co21 < 5.480585e-05 * sqrt(113) * 3.0:
            data_co21 = 0.0
        #band 6 continuum #234.6075: H
        value = imval(imagename = dir_data2 + "continuum_band6_12co21_13co21_clean.image.regrid",
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        data_co212 = value_masked_co212.sum(axis = (0, 1))
        if data_co212 < 5.480585e-05 * sqrt(113) * 3.0:
            data_co212 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(ra_deg) + " " + str(decl_deg)  + " " + str(data_halpha) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(ra_deg2) + " " + str(decl_deg2)  + " " + str(data_halpha2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


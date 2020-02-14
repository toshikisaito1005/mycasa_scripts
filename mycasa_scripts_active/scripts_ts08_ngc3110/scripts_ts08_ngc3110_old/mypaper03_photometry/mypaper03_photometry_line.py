import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data1 = "../../../ngc3110/ana/other/"
dir_data2 = "../../../ngc3110/ana/datacube_aperture/"
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

product_file = dir_product + "ngc3110_flux.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y h-alpha co10 co21 13co10 13co21\n")
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
        #co10: R
        value = imval(imagename = dir_data2 + "line_12co10_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.813 / 1.434 / 115.27120 ** 2
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta / 113.
        if data_co10 < 0.0011 * 20 * sqrt(27) * beta * 3.:
            data_co10 = 0.0
        #co10: H
        value = imval(imagename = dir_data2 + "line_12co10_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.813 / 1.434 / 115.27120 ** 2
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta / 113.
        if data_co102 < 0.0011 * 20 * sqrt(27) * beta * 3.:
            data_co102 = 0.0
        #co21: R
        value = imval(imagename = dir_data2 + "line_12co21_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.676 / 0.927 / 230.53800 ** 2
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta / 113.
        if data_co21 < 0.0011 * 20 * sqrt(30) * beta * 3.:
            data_co21 = 0.0
        #co21: H
        value = imval(imagename = dir_data2 + "line_12co21_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.676 / 0.927 / 230.53800 ** 2
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta / 113.
        if data_co212 < 0.0011 * 20 * sqrt(30) * beta * 3.:
            data_co212 = 0.0
        #13co10: R
        value = imval(imagename = dir_data2 + "line_13co10_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file)
        value_masked_13co10 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.161 / 1.141 / 110.20135430 ** 2
        data_13co10 = value_masked_13co10.sum(axis = (0, 1)) * beta / 113.
        if data_13co10 < 0.0009 * 20 * sqrt(22) * beta * 2.:
            data_13co10 = 0.0
        #13co10: H
        value = imval(imagename = dir_data2 + "line_13co10_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file2)
        value_masked_13co102 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.161 / 1.141 / 110.20135430 ** 2
        data_13co102 = value_masked_13co102.sum(axis = (0, 1)) * beta / 113.
        if data_13co102 < 0.0009 * 20 * sqrt(22) * beta * 2.:
            data_13co102 = 0.0
        #13co21: R
        value = imval(imagename = dir_data2 + "line_13co21_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file)
        value_masked_13co21 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.589 / 0.928 / 220.39868420 ** 2
        data_13co21 = value_masked_13co21.sum(axis = (0, 1)) * beta / 113.
        if data_13co21 < 0.0007 * 20 * sqrt(25) * beta * 2.5:
            data_13co21 = 0.0
        #13co21: H
        value = imval(imagename = dir_data2 + "line_13co21_contsub_clean20_nat.image.regrid.immath.moment0",
                      region = region_file2)
        value_masked_13co212 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 1.589 / 0.928 / 220.39868420 ** 2
        data_13co212 = value_masked_13co212.sum(axis = (0, 1)) * beta / 113.
        if data_13co212 < 0.0007 * 20 * sqrt(25) * beta * 2.5:
            data_13co212 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(ra_deg) + " " + str(decl_deg)  + " " + str(data_halpha) + " " + str(data_co10) + " " + str(data_co21) + " " + str(data_13co10) + " " + str(data_13co21) + "\n")
        f.write(str(ra_deg2) + " " + str(decl_deg2)  + " " + str(data_halpha2) + " " + str(data_co102) + " " + str(data_co212) + " " + str(data_13co102) + " " + str(data_13co212) + "\n")
        f.close()


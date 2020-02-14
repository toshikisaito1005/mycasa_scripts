import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data1 = "../../phangs/co_ratio/"
ra = "01h36m43.737s" #blc
decl = "15d44m06.766s" #blc
theta = 45.

#####################
### Main Procedure
#####################
### M74
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60
ra_deg = ra_hh + ra_mm + ra_ss
decl_deg = decl_hh + decl_mm + decl_ss
ra_orig = ra_deg
decl_orig = decl_deg

step_ra = 2.5 / 60 / 60
step_decl = 2.5 / 60 / 60 * sqrt(3)
ra_deg = ra_deg - step_ra
decl_deg = decl_deg + step_decl

dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)

dir_product = dir_data1 + "photmetry/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

product_file = dir_product + "m74_flux_0.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21\n")
f.close()

for i in range(80):
    ra_deg = ra_deg - step_ra
    ra_deg2 = ra_deg - step_ra / 2.
    decl_deg = decl_hh + decl_mm + decl_ss
    for j in range(60):
        decl_deg = decl_deg + step_decl
        ### create CASA region format
        # region R
        region_file = dir_casa_region + "R_" + str(i) + "_" + str(j) + ".region"
        f = open(region_file, "w")
        f.write("#CRTFv0\n")
        f.write("global coord=J2000\n")
        f.write("\n")
        x = ra_orig + (- ra_deg + ra_orig) * np.cos(theta*np.pi/180.) - (decl_deg - decl_orig) * np.sin(theta*np.pi/180.)
        y = decl_orig + (- ra_deg + ra_orig) * np.sin(theta*np.pi/180.) + (decl_deg - decl_orig) * np.cos(theta*np.pi/180.)
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], 2.5arcsec]")
        f.write("")
        f.close()
        # region H
        region_file2 = dir_casa_region + "H_" + str(i) + "_" + str(j) + ".region"
        decl_deg2 = decl_deg + step_decl / 2.
        f = open(region_file2, "w")
        f.write("#CRTFv0\n")
        f.write("global coord=J2000\n")
        f.write("\n")
        x2 = ra_orig + (- ra_deg2 + ra_orig) * np.cos(theta*np.pi/180.) - (decl_deg2 - decl_orig) * np.sin(theta*np.pi/180.)
        y2 = decl_orig + (- ra_deg2 + ra_orig) * np.sin(theta*np.pi/180.) + (decl_deg2 - decl_orig) * np.cos(theta*np.pi/180.)
        f.write("circle[[" + str(round(x2, 7)) + "deg, " + str(round(y2, 7)) + "deg], 2.5arcsec]")
        f.write("")
        f.close()
        ### imval co21
        #grid R
        value = imval(imagename = dir_data1 + "m74co21_12m+7m+TP_feathered_2kms_robust_wmask_wmodel.image.regrid.smooth.moment0",
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 3.2 / 3.2 / 230.53800 ** 2
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta / 80.
        if data_co21 < 0.03 * 6 * sqrt(17) * beta * 3.:
            data_co21 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + "m74co21_12m+7m+TP_feathered_2kms_robust_wmask_wmodel.image.regrid.smooth.moment0",
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 3.2 / 3.2 / 230.53800 ** 2
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta / 80.
        if data_co212 < 0.03 * 6 * sqrt(17) * beta * 3.:
            data_co212 = 0.0
        ### imval co10
        #grid R
        value = imval(imagename = dir_data1 + "m74co10_12m+7m+TP_feathered_robust_6kms_wmask_wmodel_pbcor.image.smooth.moment0",
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 3.2 / 3.2 / 115.27120 ** 2
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta / 80.
        if data_co10 < 0.01 * 6 * sqrt(17) * beta * 3.:
            data_co10 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + "m74co10_12m+7m+TP_feathered_robust_6kms_wmask_wmodel_pbcor.image.smooth.moment0",
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        beta = 1.226 * 10 ** 6. / 3.2 / 3.2 / 115.27120 ** 2
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta / 80.
        if data_co102 < 0.01 * 6 * sqrt(17) * beta * 3.:
            data_co102 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(x) + " " + str(y) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(x2) + " " + str(y2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


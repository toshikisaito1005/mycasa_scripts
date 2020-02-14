import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data1 = "../../../ngc3110/ana/other/"
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

product_file = dir_product + "ngc3110_flux_sfr.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y h-alpha vla1.45GHz\n")
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
        #vla: R # Jy/beam
        value = imval(imagename = dir_data1 + "vla_1.45GHz.fits",
                      region = region_file)
        value_masked_vla = value["data"] * value["mask"]
        data_vla = value_masked_vla.sum(axis = (0, 1))
        if data_vla < 1.127606e-04 * sqrt(68) * 3.:
            data_vla = 0
        #vla: H
        value = imval(imagename = dir_data1 + "vla_1.45GHz.fits",
                      region = region_file2)
        value_masked_vla2 = value["data"] * value["mask"]
        data_vla2 = value_masked_vla.sum(axis = (0, 1))
        if data_vla2 < 1.127606e-04 * sqrt(68) * 3.:
            data_vla2 = 0
        # writing
        f = open(product_file, "a")
        f.write(str(ra_deg) + " " + str(decl_deg)  + " " + str(data_halpha) + " " + str(data_vla) + "\n")
        f.write(str(ra_deg2) + " " + str(decl_deg2)  + " " + str(data_halpha2) + " " + str(data_vla2) + "\n")
        f.close()


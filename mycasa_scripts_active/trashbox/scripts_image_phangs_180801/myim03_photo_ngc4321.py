import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim

dir_data1 = "../../phangs/co_ratio/"
ra = "12h23m00.574s" #blc
decl = "15d47m50.480s" #blc
theta = 0
beam_orig = 4.06
beam = beam_orig
beta10 = 1.226 * 10 ** 6. / beam / beam / 115.27120 ** 2
beta21 = 1.226 * 10 ** 6. / beam / beam / 230.53800 ** 2
rms10 = 0.012 * 5 * sqrt(53) * beta10 * 2.5
rms21 = 0.020 * 5 * sqrt(53) * beta21 * 2.5
beamarea = 51
fits_co10 = "ngc4321_co10_12m+7m+tp_k.image.smooth.moment0"
fits_co21 = "ngc4321_co21_12m+7m+tp_pbcorr_round_k.image.regrid.smooth.moment0"
galaxy_name = "ngc4321"
num_aperture_ra = 96
num_aperture_decl = 48

#####################
### Main Procedure
#####################
### ngc4321
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


## 300 pc resolution
beam = beam_orig
step_ra = beam/2. / 60 / 60
step_decl = beam/2. / 60 / 60 * sqrt(3)
ra_deg = ra_orig - step_ra
decl_deg = decl_orig + step_decl

dir_casa_region = dir_data1 + "casa_region/"
done = glob.glob(dir_casa_region)
if not done:
    os.mkdir(dir_casa_region)

dir_product = dir_data1 + "photmetry/"
done = glob.glob(dir_product)
if not done:
    os.mkdir(dir_product)

product_file = dir_product + galaxy_name + "_flux_300pc.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21\n")
f.close()

for i in range(num_aperture_ra):
    ra_deg = ra_deg + step_ra
    ra_deg2 = ra_deg + step_ra / 2.
    decl_deg = decl_hh + decl_mm + decl_ss
    for j in range(num_aperture_decl):
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
        f.write("")
        f.close()
        ### imval co21
        #grid R
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co21 < rms21:
            data_co21 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co212 < rms21:
            data_co212 = 0.0
        ### imval co10
        #grid R
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co10 < rms10:
            data_co10 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co102 < rms10:
            data_co102 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(x) + " " + str(y) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(x2) + " " + str(y2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


## 600 pc resolution
beam = beam_orig * 2
step_ra = beam/2. / 60 / 60
step_decl = beam/2. / 60 / 60 * sqrt(3)
ra_deg = ra_orig - step_ra * 1
decl_deg = decl_orig + step_decl * 1

product_file = dir_product + galaxy_name + "_flux_600pc.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21\n")
f.close()

for i in range(int(num_aperture_ra/2.)):
    ra_deg = ra_deg + step_ra
    ra_deg2 = ra_deg + step_ra / 2.
    decl_deg = decl_hh + decl_mm + decl_ss
    for j in range(int(num_aperture_decl/2)):
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
        f.write("")
        f.close()
        ### imval co21
        #grid R
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co21 < rms21:
            data_co21 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co212 < rms21:
            data_co212 = 0.0
        ### imval co10
        #grid R
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co10 < rms10:
            data_co10 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co102 < rms10:
            data_co102 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(x) + " " + str(y) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(x2) + " " + str(y2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


## 900 pc resolution
beam = beam_orig * 3
step_ra = beam/2. / 60 / 60
step_decl = beam/2. / 60 / 60 * sqrt(3)
ra_deg = ra_orig - step_ra * 1
decl_deg = decl_orig + step_decl * 1

product_file = dir_product + galaxy_name + "_flux_900pc.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21\n")
f.close()

for i in range(int(num_aperture_ra/3.)):
    ra_deg = ra_deg + step_ra
    ra_deg2 = ra_deg + step_ra / 2.
    decl_deg = decl_hh + decl_mm + decl_ss
    for j in range(int(num_aperture_decl/3.)):
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
        f.write("")
        f.close()
        ### imval co21
        #grid R
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co21 < rms21:
            data_co21 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co212 < rms21:
            data_co212 = 0.0
        ### imval co10
        #grid R
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co10 < rms10:
            data_co10 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co102 < rms10:
            data_co102 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(x) + " " + str(y) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(x2) + " " + str(y2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


## 1200 pc resolution
beam = beam_orig * 4
step_ra = beam/2. / 60 / 60
step_decl = beam/2. / 60 / 60 * sqrt(3)
ra_deg = ra_orig - step_ra * 1
decl_deg = decl_orig + step_decl * 1

product_file = dir_product + galaxy_name + "_flux_1200pc.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21\n")
f.close()

for i in range(int(num_aperture_ra/4.)):
    ra_deg = ra_deg + step_ra
    ra_deg2 = ra_deg + step_ra / 2.
    decl_deg = decl_hh + decl_mm + decl_ss
    for j in range(int(num_aperture_decl/4.)):
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
        f.write("")
        f.close()
        ### imval co21
        #grid R
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co21 < rms21:
            data_co21 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co212 < rms21:
            data_co212 = 0.0
        ### imval co10
        #grid R
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co10 < rms10:
            data_co10 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co102 < rms10:
            data_co102 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(x) + " " + str(y) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(x2) + " " + str(y2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


## 1500 pc resolution
beam = beam_orig * 5
step_ra = beam/2. / 60 / 60
step_decl = beam/2. / 60 / 60 * sqrt(3)
ra_deg = ra_orig - step_ra * 1
decl_deg = decl_orig + step_decl * 1

product_file = dir_product + galaxy_name + "_flux_1500pc.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21\n")
f.close()

for i in range(int(num_aperture_ra/5.)):
    ra_deg = ra_deg + step_ra
    ra_deg2 = ra_deg + step_ra / 2.
    decl_deg = decl_hh + decl_mm + decl_ss
    for j in range(int(num_aperture_decl/5.)):
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
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
        f.write("circle[[" + str(round(x, 7)) + "deg, " + str(round(y, 7)) + "deg], " + str(beam/2.) + "arcsec]")
        f.write("")
        f.close()
        ### imval co21
        #grid R
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file)
        value_masked_co21 = value["data"] * value["mask"]
        data_co21 = value_masked_co21.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co21 < rms21:
            data_co21 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co21,
                      region = region_file2)
        value_masked_co212 = value["data"] * value["mask"]
        data_co212 = value_masked_co212.sum(axis = (0, 1)) * beta21 / beamarea
        if data_co212 < rms21:
            data_co212 = 0.0
        ### imval co10
        #grid R
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file)
        value_masked_co10 = value["data"] * value["mask"]
        data_co10 = value_masked_co10.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co10 < rms10:
            data_co10 = 0.0
        #grid H
        value = imval(imagename = dir_data1 + fits_co10,
                      region = region_file2)
        value_masked_co102 = value["data"] * value["mask"]
        data_co102 = value_masked_co102.sum(axis = (0, 1)) * beta10 / beamarea
        if data_co102 < rms10:
            data_co102 = 0.0
        # writing
        f = open(product_file, "a")
        f.write(str(x) + " " + str(y) + " " + str(data_co10) + " " + str(data_co21) + "\n")
        f.write(str(x2) + " " + str(y2) + " " + str(data_co102) + " " + str(data_co212) + "\n")
        f.close()


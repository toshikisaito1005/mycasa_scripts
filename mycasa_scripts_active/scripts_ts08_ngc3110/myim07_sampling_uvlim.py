import os
import re
import sys
import glob
import scipy
import numpy as np
sys.path.append(os.getcwd() + "/../")
import mycasaimaging_tools as myim


dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/"
ra = "10h04m03.181s" #blc
decl = "-06d29m01.279s" #blc
ra_blc = 151.01325416666666 #blc
decl_blc = -6.483688611111111 #blc
step = 1.5 # arcsec
aperture_radius = "1.5" # arcsecs
numx = 23 # number of apertures in x-axis
numy = 23 # number of apertures in y-axis


#####################
### Function
#####################
def create_casa_apertures(ra_blc,decl_blc,numx,numy,aperture_radius,step):
    step_ra = step / 60 / 60
    step_decl = step / 60 / 60 * sqrt(3)
    ra_deg = ra_blc + step_ra
    decl_deg = decl_blc - step_decl
    for i in range(numx):
        ra_deg = ra_deg - step_ra
        ra_deg2 = ra_deg - step_ra / 2.
        decl_deg = decl_blc
        for j in range(numy):
            decl_deg = decl_deg + step_decl
            region_name = "_"+str(i).zfill(2)+"_"+str(j).zfill(2)+".region"
            # region A
            region_file = dir_casa_region + "A" + region_name
            f = open(region_file, "w")
            f.write("#CRTFv0\n")
            f.write("global coord=J2000\n")
            f.write("\n")
            f.write("circle[[" + str(round(ra_deg, 5)) + "deg, " + str(round(decl_deg, 7)) + "deg], "+aperture_radius+"arcsec]")
            f.write("")
            f.close()
            # region B
            region_file2 = dir_casa_region + "B" + region_name
            decl_deg2 = decl_deg + step_decl / 2.
            f = open(region_file2, "w")
            f.write("#CRTFv0\n")
            f.write("global coord=J2000\n")
            f.write("\n")
            f.write("circle[[" + str(round(ra_deg2, 5)) + "deg, " + str(round(decl_deg2, 7)) + "deg], "+aperture_radius+"arcsec]")
            f.write("")
            f.close()

def casa2radec(casa_aperture):
    # import ra and dec
    f = open(casa_aperture)
    lines = f.readlines()
    f.close()
    str_xy = lines[3].replace("circle[[","").replace("deg","").replace("]","")
    data_ra = str_xy.split(",")[0]
    data_dec = str_xy.split(",")[1].replace(" ", "")

    return data_ra, data_dec

def eazy_imval(imagename,casa_aperture):
    value = imval(imagename=imagename,region=casa_aperture)
    value_masked = value["data"] * value["mask"]
    data = value_masked.sum(axis = (0, 1))
    data_1d = value_masked.flatten()
    num_all = float(len(data_1d))
    num_detect = len(data_1d[data_1d>0])
    
    if num_detect/num_all < 0.5:
        data = 0.0

    return data

#####################
### Main Procedure
#####################
# directories
done = glob.glob(dir_data + "image_nyquist/")
if not done:
    os.mkdir(dir_data + "image_nyquist/")

dir_casa_region = dir_data + "casa_region/"
os.system("rm -rf " + dir_casa_region)
os.mkdir(dir_casa_region)

# create casa regions
create_casa_apertures(ra_blc,decl_blc,numx,numy,aperture_radius,step)
casa_apertures = glob.glob(dir_casa_region + "*.region")
casa_apertures.sort()

# import images
imagenames = glob.glob(dir_data + "image_uvlim_*/*.moment0")
imagenames.sort()

product_file = dir_data + "image_nyquist/ngc3110_uvlim_sum.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y co10 co21 13co10 13co21\n")
f.close()
for i in range(len(casa_apertures)):
    # measure fluxes and positions
    data_ra, data_dec = casa2radec(casa_apertures[i])
    data_co10 = np.round(eazy_imval(imagenames[0],casa_apertures[i]),3)
    data_co21 = np.round(eazy_imval(imagenames[1],casa_apertures[i]),3)
    data_13co10 = np.round(eazy_imval(imagenames[2],casa_apertures[i]),3)
    data_13co21 = np.round(eazy_imval(imagenames[3],casa_apertures[i]),3)
    # export to txt file
    f = open(product_file, "a")
    data1 = str(data_ra) + " " + str(data_dec)  + " "
    data2 = data1 + str(data_co10) + " " + str(data_co21) + " "
    data3 = data2 + str(data_13co10) + " " + str(data_13co21)
    f.write(data3 + "\n")
    f.close()

os.system("cp " + product_file + " ngc3110_uvlim_sum.txt")
os.system("rm -rf *.last")
os.system("rm -rf " + dir_casa_region)


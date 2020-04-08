import os
import glob
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628","ngc3627","ngc4321"]
beams = ["04p0","08p0","04p0"]


#####################
### Main
#####################
for i in range(len(gals)):
    galname = gals[i]
    dir_co10 = dir_proj + galname + "_co10/"
    dir_co21 = dir_proj + galname + "_co21/"
    co10image = dir_co10 + "co10_" + beams[i] + ".moment0"
    co21image = dir_co21 + "co21_" + beams[i] + ".moment0"

    # header
    co10header = imhead(co10image, mode="list")
    co10beamwsize = co10header["beammajor"]["value"]
    co21header = imhead(co21image, mode="list")
    co21beamwsize = co21header["beammajor"]["value"]

    # J2K factor
    J2K_co10 = 1.222e6 / co10beamwsize**2 / 115.27120**2
    J2K_co21 = 1.222e6 / co21beamwsize**2 / 230.53800**2

    # apply
    os.system("rm -rf " + co10image + "_Kelvin")
    immath(imagename = co10image,
    	expr = "IM0*" + str(J2K_co10),
    	outfile = co10image + "_Kelvin")

    os.system("rm -rf " + co21image + "_Kelvin")
    immath(imagename = co21image,
    	expr = "IM0*" + str(J2K_co21),
    	outfile = co21image + "_Kelvin")

os.system("rm -rf *.last")

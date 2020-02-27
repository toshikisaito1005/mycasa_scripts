import os
import glob
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628","ngc3627","nngc4321"]
beams = ["04p0","08p0","04p0"]


#####################
### Main
#####################
for i in range(len(gals)):
    galname = gals[i]
    dir_co10 = dir_proj + galname + "_co10/"
    dir_co21 = dir_proj + galname + "_co21/"
    co10image = dir_co10 + "co10_" + beams[i] + ".moment0"


os.system("rm -rf *.last")

import os
import glob
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galaxy = ["ngc0628",
          "ngc4321",
          #"ngc4254",
          "ngc3627"]


#####################
### Main
#####################
i=0
galname = galaxy[i]
dir_co10 = dir_proj + galname + "_co10/"
dir_co21 = dir_proj + galname + "_co21/"
co10image = glob.glob(dir_co10 + "co10_cube*.image")[0]
co21image = glob.glob(dir_co21 + "co21_cube*.image")[0]


os.system("rm -rf *.last")

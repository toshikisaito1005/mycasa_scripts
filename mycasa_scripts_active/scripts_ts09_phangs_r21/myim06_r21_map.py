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
percent = 0.01


#####################
### Main
#####################
for i in range(len(galaxy)):
    # import data for r21 map
    galname = galaxy[i]
    co10images = glob.glob(dir_proj + galname + "_*/co10*.moment0")
    co10images.extend(glob.glob(dir_proj + galname + "_*/co10*.moment8"))
    co10images.sort()
    co21images = glob.glob(dir_proj + galname + "_*/co21*.moment0")
    co21images.extend(glob.glob(dir_proj + galname + "_*/co21*.moment8"))
    co21images.sort()

    # mkdir
    dir_ratio = dir_proj + galname + "_r21/"
    os.system("rm -rf " + dir_ratio)
    os.mkdir(dir_ratio)

    # immath
    for j in range(len(co10images)):
        outfile = dir_ratio + co10images[j].split("/")[-1].replace("co10","r21")
        os.system("rm -rf " + outfile + "_tmp")
        immath(imagename = [co21images[j],
                            co10images[j]],
               expr = "iif(IM0>0,IM0/IM1/4.0,0)",
               outfile = outfile + "_tmp")

        makemask(mode = "copy",
                 inpimage = outfile + "_tmp",
                 inpmask = outfile + "_tmp",
                 output = outfile,# + "_tmp_mask:mask0",
                 overwrite = True)
        """
        makemask(mode = "copy",
                 inpimage = outfile + "_tmp_mask",
                 inpmask = outfile + "_tmp_mask:mask0",
                 output = "",
                 overwrite = True)
        
        immath(imagename = [outfile + "_tmp",
                            outfile + "_tmp_mask"],
               expr = "iif(IM1>=1,IM0,0)",
               outfile = outfile)
        """
        os.system("rm -rf " + outfile + "_tmp")
        os.system("rm -rf " + outfile + "_tmp_mask")

os.system("rm -rf *.last")

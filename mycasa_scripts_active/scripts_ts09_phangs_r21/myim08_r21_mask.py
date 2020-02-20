import os
import glob
import numpy as np
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
galaxy = ["ngc0628", "ngc4321", "ngc4254", "ngc3627"]


#####################
### Main
#####################
for i in range(len(galaxy)):
    # import data for r21 map
    galname = galaxy[i]
    r21images = glob.glob(dir_proj + galname + "_r21/r21*.moment0")
    r21images.sort()
    r21image = r21images[0]

    shape = imhead(r21image,mode="list")["shape"]
    box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
    data = imval(r21image,box=box)
    pixvalues = data["data"].flatten()
    pixvalues = pixvalues[abs(pixvalues)!=0]
    median = np.median(pixvalues)

    outfile = r21image + ".highlowmask"
    os.system("rm -rf " + outfile + "_tmp")
    immath(imagename = r21image,
           expr = "iif(IM0>"+str(median)+",1.0,-1.0)",
           outfile = outfile + "_tmp")

    os.system("rm -rf " + outfile)
    immath(imagename = [r21image, outfile+"_tmp"],
           expr = "iif(IM0>0.0,IM1,0)",
           outfile = outfile)
    os.system("rm -rf " + outfile + "_tmp")

os.system("rm -rf *.last")

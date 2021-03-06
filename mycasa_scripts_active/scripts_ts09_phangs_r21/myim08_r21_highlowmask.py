import os
import glob
import numpy as np
import scripts_phangs_r21 as r21


#####################
### Parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628", "ngc3627", "ngc4321"]
#beam = [4.0, 8.0, 4.0]
#beam = [13.6, 15.0, 8.5]


#####################
### Main
#####################
for i in range(len(gals)):
    # import data for r21 map
    galname = gals[i]
    beamp = str(beam[i]).replace(".","p").zfill(4)
    r21image = glob.glob(dir_proj + galname + "_r21/r21_"+beamp+".moment0")[0]

    shape = imhead(r21image,mode="list")["shape"]
    box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
    data = imval(r21image,box=box)
    pixvalues = data["data"].flatten()
    pixvalues[np.isinf(pixvalues)]=0
    pixvalues = pixvalues[abs(pixvalues)!=0]
    median = np.median(pixvalues)
    pupp = np.percentile(pixvalues,66.6666665)
    plow = np.percentile(pixvalues,33.3333335)

    outfile = r21image + ".highlowmask"
    os.system("rm -rf " + outfile + "_tmp")
    immath(imagename = r21image,
           expr = "iif(IM0>"+str(pupp)+",1.0,0.0)",
           outfile = outfile + "_tmp")

    os.system("rm -rf " + outfile)
    immath(imagename = [r21image, outfile+"_tmp"],
           expr = "iif(IM0<"+str(plow)+",-1.0,IM1)",
           outfile = outfile)
    os.system("rm -rf " + outfile + "_tmp")

    os.system("rm -rf " + outfile + ".fits")
    exportfits(imagename = outfile,
               fitsimage = outfile + ".fits")

os.system("rm -rf *.last")

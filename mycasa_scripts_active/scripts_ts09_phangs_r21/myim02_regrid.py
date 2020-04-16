import os
import glob
import numpy as np
import scripts_phangs_r21 as r21

dir_data = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/data/"
galnames = ["ngc0628","ngc4321","ngc3627"]
image_lengths = [280.,230.,280.] # arcsec
direction_ras = ["24.174deg","185.729deg","170.063deg"]
direction_decs = ["15.783deg","15.8223deg","12.9914deg"]
chanss = ["14~36","","25~74"]


#####################
### Main Procedure
#####################
os.system("rm -rf " + dir_data.replace("r21/data/","r21/data_ready"))
os.system("mkdir " + dir_data.replace("r21/data/","r21/data_ready"))

for i in range(len(galnames)):
    imagenames = glob.glob(dir_data + galnames[i] + "*co*.image*")
    imagenames.sort()
    r21.gridtemplate(imagenames[0],
                     image_lengths[i],
                     direction_ras[i],
                     direction_decs[i])

    for j in range(len(imagenames)):
        output_tmp = imagenames[j].replace("r21/data","r21/data_ready")
        output = output_tmp.replace(".image",".regrid").replace("_pbcor","")
        os.system("rm -rf "+output)
        imregrid(imagename=imagenames[j],
                 template="template.image",
                 output=output,
                 axes=[0,1])

        outfile = output.replace(".regrid",".image")
        os.system("rm -rf "+outfile)
        immath(imagename = output,
               expr = "IM0",
               chans = chanss[i],
               outfile = outfile)

        os.system("rm -rf " + output)

        # pbmasking
        imagename = outfile
        pbmask = outfile.replace(".image",".pbmask")
        os.system("rm -rf " + pbmask + "_tmp")
        immath(imagename = imagename,
               expr = "iif( IM0 >=-100000000., 1.0, 0.0)",
               outfile = pbmask + "_tmp")
        #
        imsmooth(imagename = pbmask + "_tmp",
                 major = "55.0arcsec",
                 minor = "55.0arcsec",
                 pa = "0deg",
                 outfile = pbmask + "_tmp2")
        os.system("rm -rf " + pbmask + "_tmp")
        #
        os.system("rm -rf " + pbmask)
        maxval = imstat(pbmask + "_tmp2")["max"][0]
        immath(imagename = pbmask + "_tmp2",
               expr = "iif( IM0 >=" + str(maxval*0.6) + ", 1.0, 0.0)",
               outfile = pbmask)
        os.system("rm -rf " + pbmask + "_tmp2")

    os.system("rm -rf template.*")

os.system("rm -rf *.last")
#os.system("rm -rf " + dir_data)

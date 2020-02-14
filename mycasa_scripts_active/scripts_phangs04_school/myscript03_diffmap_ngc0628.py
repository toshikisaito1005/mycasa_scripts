import os
import glob
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()


dir_data = "../../myproj_published/proj_phangs04_school/data/"
galaxy = ["ngc0628"]
alpha_co = 4.3

#####################
### Main Procedure
#####################
dir_working = dir_data + "../products/"

for i in range(len(galaxy)):
    galname = galaxy[i]
    imagenames_12m7mtp = glob.glob(dir_data + galname + "*12m7mtp_*.image")
    imagenames_12m7m = glob.glob(dir_data + galname + "*12m7m_*.image")
    imagenames_12m7mtp.sort()
    imagenames_12m7m.sort()

    for j in range(len(imagenames_12m7mtp)):
        imagenames_12m7mtp_regrid = imagenames_12m7mtp[j] + ".regrid"
        os.system("rm -rf " + imagenames_12m7mtp_regrid)
        imregrid(imagename = imagenames_12m7mtp[j],
                 output = imagenames_12m7mtp_regrid,
                 template = imagenames_12m7m[j])
        
        imagename = [imagenames_12m7mtp_regrid, imagenames_12m7m[j]]
        outfile = dir_data + imagenames_12m7mtp[j].split("/")[-1].replace("12m7mtp","diff")
        os.system("rm -rf " + outfile)
        immath(imagename = imagename,
               expr = "IM0 - IM1",
               outfile = outfile)

        os.system("rm -rf " + imagenames_12m7mtp[j])
        os.system("mv " + imagenames_12m7mtp_regrid + " " + imagenames_12m7mtp[j])

os.system("rm -rf *.last")

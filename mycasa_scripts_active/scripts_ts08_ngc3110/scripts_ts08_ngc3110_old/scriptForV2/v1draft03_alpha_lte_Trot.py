import os
import sys
import re
import glob
import numpy as np
import scipy
sys.path.append(os.getcwd() + "/../../")
import mycasaanalysis_tools3 as myana


#####################
### Main Procedure
#####################
"""
# center
ra = "10h04m02.090s"
decl = "-6d28m29.604s"
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60
"""


# main
dir_data = "../../../ngc3110/ana/other/"
txt_data = "photmetry/ngc3110_flux.txt"
product_data = "photmetry/ngc3110_alpha_lte_Trot.txt"
data = np.loadtxt(dir_data + txt_data, usecols = (0,1,2,3,4,5,6))
d_ra, d_decl = data[:,0], data[:,1]
fl_12co10 = data[:,3]
fl_13co10 = data[:,5]
fl_13co21 = data[:,6]


"""
# distance
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325
"""


# main
os.system("rm -rf " + dir_data + product_data)
f = open(dir_data + product_data, "w")
f.write("#x y distance alpha_lte err_alpha_lte\n")
f.close()


#tco_h2 = 1.4e-06 #  70, 1e-4
#tco_h2 = 5.0e-07 # 200, 1e-4
tco_h2 = 4.3e-06 #  70, 3e-4
#tco_h2 = 1.5e-06 # 200, 3e-4


for i in range(len(fl_13co21)):
    log_Ntot_1, Qrot_1 = myana.rot0_13co(10.0, fl_13co21[i])
    log_Ntot_2, Qrot_2 = myana.rot0_13co(15.0, fl_13co21[i])
    log_Ntot_3, Qrot_3 = myana.rot0_13co(25.0, fl_13co21[i])
    dist = str(value[i]) # kpc

    if fl_12co10[i] > 0:
        # case 1
        NH2_1 = 10 ** log_Ntot_1 / tco_h2
        X_co_1 = NH2_1 / fl_12co10[i]
        alpha_co_1 = 4.3 * X_co_1 / 2e+20
        # case 2
        NH2_2 = 10 ** log_Ntot_2 / tco_h2
        X_co_2 = NH2_2 / fl_12co10[i]
        alpha_co_2 = 4.3 * X_co_2 / 2e+20
        # case 3
        NH2_3 = 10 ** log_Ntot_3 / tco_h2
        X_co_3 = NH2_3 / fl_12co10[i]
        alpha_co_3 = 4.3 * X_co_3 / 2e+20
    else:
        alpha_co_1 = 0
        alpha_co_2 = 0
        alpha_co_3 = 0

    mean_alpha_co = (alpha_co_1 + alpha_co_2 + alpha_co_3) /3.
    err_alpha_co = max([alpha_co_1, alpha_co_2, alpha_co_3]) - mean_alpha_co

    f = open(dir_data + product_data, "a")
    f.write(str(d_ra[i])+" "+str(d_decl[i])+" "+dist+" "\
            +str(mean_alpha_co)+" "+str(err_alpha_co)+"\n")
    f.close()


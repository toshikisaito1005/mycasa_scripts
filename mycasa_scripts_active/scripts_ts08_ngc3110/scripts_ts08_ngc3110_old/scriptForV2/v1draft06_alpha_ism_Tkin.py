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
# center
ra = "10h04m02.090s"
decl = "-6d28m29.604s"
ra_hh = float(ra.split("h")[0])*15
ra_mm = float(ra.split("h")[1].split("m")[0])*15/60
ra_ss = float(ra.split("h")[1].split("m")[1].rstrip("s"))*15/60/60
decl_hh = float(decl.split("d")[0])
decl_mm = float(decl.split("d")[1].split("m")[0])/60
decl_ss = float(decl.split("d")[1].split("m")[1].rstrip("s"))/60/60


# main
dir_data = "../../../ngc3110/ana/other/"
txt_data = "photmetry/ngc3110_flux.txt"
txt_data2 = "photmetry/ngc3110_flux_contin.txt"

txt_data3 = "photmetry/ngc3110_radex_map_22.0.txt"
txt_data4 = "photmetry/ngc3110_radex_map_22.1.txt"
txt_data5 = "photmetry/ngc3110_radex_map_22.2.txt"
txt_data6 = "photmetry/ngc3110_radex_map_22.3.txt"
txt_data7 = "photmetry/ngc3110_radex_map_22.4.txt"

product_data = "photmetry/ngc3110_alpha_ism_Tkin.txt"
data = np.loadtxt(dir_data + txt_data, usecols = (0,1,2,3,4,5,6))
data2 = np.loadtxt(dir_data + txt_data2, usecols = (0,1,2,3,4))
d_ra, d_decl = data[:,0], data[:,1]
fl_12co10 = data[:,3]
fl_13co10 = data[:,5]
fl_13co21 = data[:,6]
fl_band6 = data2[:,4]

d_kin_1 = np.loadtxt(dir_data + txt_data3, usecols = (0,1,2))[:,2]
d_kin_2 = np.loadtxt(dir_data + txt_data4, usecols = (0,1,2))[:,2]
d_kin_3 = np.loadtxt(dir_data + txt_data5, usecols = (0,1,2))[:,2]
d_kin_4 = np.loadtxt(dir_data + txt_data6, usecols = (0,1,2))[:,2]
d_kin_5 = np.loadtxt(dir_data + txt_data7, usecols = (0,1,2))[:,2]


# distance
ra_cent_deg = [(ra_hh + ra_mm + ra_ss)] * len(d_ra)
decl_cent_deg = [(decl_hh - decl_mm - decl_ss)] * len(d_decl)

x1 = d_ra - ra_cent_deg
y1 = d_decl - decl_cent_deg

x2 = (x1 * cos(171*np.pi/180.) - y1 * sin(171*np.pi/180.)) / np.cos(65.*np.pi/180.)
y2 = x1 * sin(171*np.pi/180.) + y1 * cos(171*np.pi/180.)

value = np.sqrt(x2 ** 2 + y2 ** 2) * 3600. * 0.325


# 10, 15, 25 K
def factor_b2m(Td):
    """
    """
    z = 0.016858
    h = 6.626e-27 # erg.s
    k = 1.38e-16 # erg/K
    nu_obs = 234.6075e+9 / (1 + z) #GHz
    alpha_850 = 6.7e+19

    factor = h * nu_obs * (1+z) / (k * Td)
    factor_0 = h * 352.6970094e+9 * (1+0) / (k * Td)
    gamma_rj = factor / (np.exp(factor) - 1)
    gamma_0 = factor_0 / (np.exp(factor_0) - 1)
    factor_b2m_tmp1 = 1.78 * (1+z)**4.8 * (352.6970094/234.6075)**3.8
    factor_b2m_tmp2 = (69.4/1000.)**2 * 10.e+10
    factor_b2m_tmp3 = factor_b2m_tmp1 * factor_b2m_tmp2
    factor_b2m = factor_b2m_tmp3 * (6.7e+19/alpha_850) * gamma_0/gamma_rj

    return factor_b2m

#
beta = 1.226 * 10 ** 6. / 1.813 / 1.434 / 115.27120 ** 2
jy_co10 = fl_12co10 / beta * 113. / 47.115

nu_obs = 115.27120 / (1 + 0.016858)


# main
os.system("rm -rf " + dir_data + product_data)
f = open(dir_data + product_data, "w")
f.write("#x y distance alpha_ism err_alpha_ism\n")
f.close()


for i in range(len(fl_band6)):
    dist = str(value[i]) # kpc
    factor_b2m_2 = factor_b2m(d_kin_2[i])
    factor_b2m_3 = factor_b2m(d_kin_3[i])
    factor_b2m_4 = factor_b2m(d_kin_4[i])
    
    Mism_2 = factor_b2m_2 * fl_band6[i]
    Mism_3 = factor_b2m_3 * fl_band6[i]
    Mism_4 = factor_b2m_4 * fl_band6[i]
    
    l_co = 3.25e+7 * jy_co10[i] / nu_obs**2 * 69.4**2 / (1 + 0.016858)**2

    if fl_band6[i] > 0:
        if l_co > 0:
            alpha_ism_2 = Mism_2 / l_co
            alpha_ism_3 = Mism_3 / l_co
            alpha_ism_4 = Mism_4 / l_co
        else:
            alpha_ism_2 = 0
            alpha_ism_3 = 0
            alpha_ism_4 = 0
    else:
        alpha_ism_2 = 0
        alpha_ism_3 = 0
        alpha_ism_4 = 0

    mean_alpha_co = (alpha_ism_2 + alpha_ism_3 + alpha_ism_4) /3.
    err_alpha_co = max([alpha_ism_2, alpha_ism_3, alpha_ism_4]) - mean_alpha_co

    f = open(dir_data + product_data, "a")
    f.write(str(d_ra[i])+" "+str(d_decl[i])+" "+dist+" "\
            +str(mean_alpha_co)+" "+str(err_alpha_co)+" "+str(d_kin_3[i])+"\n")
    f.close()


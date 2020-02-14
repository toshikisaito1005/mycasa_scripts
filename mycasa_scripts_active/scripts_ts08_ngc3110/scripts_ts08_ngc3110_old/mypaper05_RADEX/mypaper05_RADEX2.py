import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt
sys.path.append(os.getcwd() + "/../../")
import mycasaanalysis_tools as myana

#####################
### Main Procedure
#####################
dir_data = "/Users/saito/data/ngc3110/ana/other/photmetry/"
dir_data2 = "/Users/saito/data/myradex_scripts/radex_ngc3110/"
plt.rcParams["font.size"] = 14

### import line ratio
txt_data = "ngc3110_flux_uvlim.txt"
data = np.loadtxt(dir_data + txt_data, usecols = (0,1,2,3,4,5,6))
fl_12co10 = data[:,3]
fl_12co21 = data[:,4]
fl_13co10 = data[:,5]
fl_13co21 = data[:,6]

ratio1 = fl_12co21/fl_12co10
for i in range(len(ratio1)):
    if fl_12co10[i] == 0.:
        ratio1[i] = 0.

ratio2 = fl_12co21/fl_13co21
for i in range(len(ratio2)):
    if fl_13co21[i] == 0.:
        ratio2[i] = 0.

### import column density
txt_data2 = "ngc3110_H2mass.txt"
data = np.loadtxt(dir_data + txt_data2, usecols = (0,1,2))
ra, decl = data[:,0], data[:,1]
area = (3 * 325 / 2. * 3.086e+18) ** 2 * np.pi
NH2 = data[:,2]*1.9884e33*6.0e23/(1.36*2.*area)

#####
txt_data2 = "ngc3110_sfr.txt"
data = np.loadtxt(dir_data + txt_data2, usecols = (0,1,2))
ra_sfr, decl_sfr, sfr = data[:,0], data[:,1], data[:,2]

for i in range(len(NH2)):
    if NH2[i] == 0.:
        NH2[i] = 1

logNH2 = np.round(np.log10(NH2), 1)

for i in range(len(logNH2)):
    logNH2[i] = 22.4

### RADEX
product_file = dir_data + "ngc3110_radex_map.txt"
os.system("rm -rf " + product_file)
f = open(product_file, "a")
f.write("#x y Tkin nH2\n")

for i in range(len(logNH2)):
    radex_model = glob.glob(dir_data2 + "out_" + str(logNH2[i]) + ".txt")
    if radex_model:
        data = np.loadtxt(radex_model[0])
        Tkin, nH2 = data[:,0], data[:,1]
        ratio1_r, ratio2_r = data[:,2], data[:,3]
        x =  ratio1_r - ratio1[i]
        y =  ratio2_r - ratio2[i]
        location = np.argmin(np.sqrt(abs(x ** 2 - y ** 2)))
        out_T, out_n = Tkin[location], nH2[location]
        if logNH2[i] < 21.9:
            out_n = 10
        if ratio2[i] == 0:
            out_T = 0
            out_n = 10
        #####
        f = open(product_file, "a")
        f.write(str(ra[i]) + " " + str(decl[i]) + " " + str(out_T) + " " + str(out_n) + " \n")
f.close()


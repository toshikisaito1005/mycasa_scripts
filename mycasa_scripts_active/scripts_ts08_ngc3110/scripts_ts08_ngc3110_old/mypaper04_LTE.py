import os
import sys
import re
import glob
import numpy as np
import scipy
sys.path.append(os.getcwd() + "/../")
import mycasaanalysis_tools as myana

#####################
### Main Procedure
#####################
dir_data = "../../ngc3110/ana/other/"
txt_data = "photmetry/ngc3110_flux.txt"
data = np.loadtxt(dir_data + txt_data, usecols = (0,1,2,3,4,5,6))
fl_12co10 = data[:,3]
fl_13co10 = data[:,5]
fl_13co21 = data[:,6]

fl_13co10b = fl_13co10[fl_13co10 > 0]
fl_13co21b = fl_13co21[fl_13co10 > 0]
fl_12co10b = fl_12co10[fl_13co10 > 0]
fl_13co10c =  fl_13co10b[fl_12co10b > 0]
fl_13co21c =  fl_13co21b[fl_12co10b > 0]
fl_12co10c =  fl_12co10b[fl_12co10b > 0]
fl_13co10d =  fl_13co10c[fl_13co21c > 0]
fl_13co21d =  fl_13co21c[fl_13co21c > 0]
fl_12co10d =  fl_12co10c[fl_13co21c > 0]


os.system("rm -rf " + dir_data + \
          "../product/txt/rotation_diagram_13co.txt")
f = open(dir_data + "../product/txt/rotation_diagram_13co.txt", "w")
f.write("#Trot  log N(13co)  log N(H2)\n")
f.close()

#tco_h2 = 1.4e-06 #  70, 1e-4
#tco_h2 = 5.0e-07 # 200, 1e-4
tco_h2 = 4.3e-06 #  70, 3e-4
#tco_h2 = 1.5e-06 # 200, 3e-4


for i in range(len(fl_13co10d)):
    Trot, log_Ntot, Qrot = myana.rot1_13co(fl_13co10d[i], fl_13co21d[i])
    log_NH2 = round(np.log10(10**(log_Ntot)/tco_h2), 2)
    f = open(dir_data + "../product/txt/rotation_diagram_13co.txt",
             "a")
    f.write(str(Trot) + "  " + str(log_Ntot) + "  " + str(log_NH2) + "\n")
    f.close()

data = np.loadtxt(dir_data \
                  + "../product/txt/rotation_diagram_13co.txt",
                  usecols = (0,1,2))

Tkin, logN13co, logNH2 = data[:,0], data[:,1], data[:,2]

area = (3 / 2. * 325 * 3.086e+18) ** 2 * np.pi
MH2 = 1.36 * 2.0/ 6.0e23 / 1.9884e33 * 10 ** logNH2 * area
#alpha_co = MH2 / (23.5 * (3./2. ** 2 * np.pi) * 69.4 ** 2 * fl_12co10d)
X_co = 10 ** logNH2 / fl_12co10d
alpha_co = 4.3 * X_co / 2e+20

print(Tkin)
print(logN13co)
print(logNH2)
print(np.log10(MH2))

print(round(np.mean(Tkin), 1), round(np.median(Tkin), 1))
print(round(np.mean(logN13co), 1), round(np.median(logN13co), 1))
print(round(np.mean(logNH2), 1), round(np.median(logNH2), 1))

print("mean alpha_CO = " + str(round(np.mean(alpha_co), 1)))
print("median alpha_CO = " + str(round(np.median(alpha_co), 1)))
print("mean log X_CO = " + str(round(np.mean(X_co), 1)))
print("median log X_CO = " + str(round(np.median(X_co), 1)))

Mradex1 = 1.36 * 2.0/ 6.0e23 / 1.9884e33 * 10 ** 21.5 * area
Mradex2 = 1.36 * 2.0/ 6.0e23 / 1.9884e33 * 10 ** 22.0 * area

os.system("rm -rf " + dir_data + "gasmass_lte.txt")
np.savetxt(dir_data + "gasmass_lte.txt",
           np.c_[fl_12co10d, MH2],
           delimiter=" ")


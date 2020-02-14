import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt

#####################
### Main Procedure
#####################
dir_data = "/Users/saito/data/myproj_published/proj_ts08_ngc3110/image_nyquist/"
txt_data = "ngc3110_uvlim_sum.txt"
data = np.loadtxt(dir_data + txt_data)
data_ra = data[:,0]
data_dec = data[:,1]
data_12co10 = data[:,2] # Jy/beam.km/s
data_12co21 = data[:,3] # Jy/beam.km/s
data_13co10 = data[:,4] # Jy/beam.km/s
data_13co21 = data[:,5] # Jy/beam.km/s

r21 = data_12co21/data_12co10 / (230.53800000/115.27120180)**2 # K.km/s / K.km/s
for i in range(len(r21)):
    if data_12co10[i] == 0.:
        r21[i] = 0.

r13 = data_12co21/data_13co21 / (230.53800000/220.39868420)**2 # K.km/s / K.km/s
for i in range(len(r13)):
    if data_13co21[i] == 0.:
        r13[i] = 0.

### RADEX
radex_grids = glob.glob(dir_data + "../data_others/radex_*.txt")
radex_grids.sort()

product_nH2 = dir_data + "ngc3110_radex_nH2.txt"
os.system("rm -rf " + product_nH2)
f = open(product_nH2, "a")
f.write("#x y 22.0 22.1 22.2 22.3 22.4 22.5 \n")
for i in range(len(r21)):
    nH2s = []
    for j in range(len(radex_grids)):
        data = np.loadtxt(radex_grids[j])
        nH2= data[:,1]
        radex_r21, radex_r13 = data[:,2], data[:,3]
        diff_r21 = radex_r21 - r21[i]
        diff_r13 = radex_r13 - r13[i]
        index = np.argmin(np.sqrt(abs(diff_r21**2 - diff_r13**2)))
        best_nH2 = nH2[index]
        if r13[i] == 0.:
            best_nH2 = 0.
        if r21[i] == 0.:
            best_nH2 = 0.
        nH2s.append(best_nH2)

    # export
    data1 = str(nH2s[0])+" "+str(nH2s[1])+" "+str(nH2s[2])+" "
    data2 = data1 + str(nH2s[3])+" "+str(nH2s[4])
    f = open(product_nH2, "a")
    f.write(str(data_ra[i])+" "+str(data_dec[i])+" "+data2+"\n")

f.close()

import os
import re
import sys
import glob
import scipy
import numpy as np
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)


#####
dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
dir_gals = glob.glob(dir_data + "sim_*/")
dir_gals.sort()


list_area = []
list_fidelity_7m = []
list_fidelity_feather = []
list_fidelity_tp2vis = []
list_fidelity_tpmodel = []
for i in range(len(dir_gals)):
       print("# processing " + dir_gals[i].split("/")[-2] + " " + str(i) + "/" + str(len(dir_gals)))
       #
       fidelity_7m = glob.glob(dir_gals[i] + "*7m*.fidelity")[0]
       fidelity_feather = glob.glob(dir_gals[i] + "*feather*.fidelity")[0]
       fidelity_tp2vis = glob.glob(dir_gals[i] + "*tp2vis*.fidelity")[0]
       fidelity_tpmodel = glob.glob(dir_gals[i] + "*tpmodel*.fidelity")[0]
       #
       image_7m = glob.glob(dir_gals[i] + "*7m*.fidelity")[0]
       image_feather = glob.glob(dir_gals[i] + "*feather*.fidelity")[0]
       image_tp2vis = glob.glob(dir_gals[i] + "*tp2vis*.fidelity")[0]
       image_tpmodel = glob.glob(dir_gals[i] + "*tpmodel*.fidelity")[0]
       image_model = glob.glob(dir_gals[i] + "*skymodel_regrid.smooth")[0]
       #
       shape = imhead(fidelity_7m,mode="list")["shape"]
       box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
       pixsize = abs(imhead(fidelity_7m,mode="list")["cdelt1"])*180/np.pi*3600
       pixarea = pixsize**2
       #
       fidelity_7m = imval(fidelity_7m,box=box)["data"].flatten()
       fidelity_7m[np.isnan(fidelity_7m)] = 0
       median_fidelity_7m = np.median(fidelity_7m[fidelity_7m>0])
       #
       area = np.sqrt(pixarea * len(fidelity_7m[fidelity_7m>0]) / np.pi)
       #
       fidelity_feather = imval(fidelity_feather,box=box)["data"].flatten()
       fidelity_feather[np.isnan(fidelity_feather)] = 0
       median_fidelity_feather = np.median(fidelity_feather[fidelity_feather>0])
       #
       fidelity_tp2vis = imval(fidelity_tp2vis,box=box)["data"].flatten()
       fidelity_tp2vis[np.isnan(fidelity_tp2vis)] = 0
       median_fidelity_tp2vis = np.median(fidelity_tp2vis[fidelity_tp2vis>0])
       #
       fidelity_tpmodel = imval(fidelity_tpmodel,box=box)["data"].flatten()
       fidelity_tpmodel[np.isnan(fidelity_tpmodel)] = 0
       median_fidelity_tpmodel = np.median(fidelity_tpmodel[fidelity_tpmodel>0])
       #
       list_area.append(area)
       list_fidelity_7m.append(median_fidelity_7m)
       list_fidelity_feather.append(median_fidelity_feather)
       list_fidelity_tp2vis.append(median_fidelity_tp2vis)
       list_fidelity_tpmodel.append(median_fidelity_tpmodel)

list_median = np.c_[list_area,list_fidelity_7m,list_fidelity_feather,list_fidelity_tp2vis,list_fidelity_tpmodel]
np.savetxt("list_median.txt",list_median,header="area 7m feather tp2vis tpmodel",fmt="%.3f")

os.system("rm -rf *.last")

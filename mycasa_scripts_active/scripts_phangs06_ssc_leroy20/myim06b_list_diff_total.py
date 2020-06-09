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
list_7m = []
list_feather = []
list_tp2vis = []
list_tpmodel = []
for i in range(len(dir_gals)):
       print("# processing " + dir_gals[i].split("/")[-2] + " " + str(i) + "/" + str(len(dir_gals)))
       #
       image_7m = glob.glob(dir_gals[i] + "*7m*.smooth")[0]
       image_feather = glob.glob(dir_gals[i] + "*feather*.smooth")[0]
       image_tp2vis = glob.glob(dir_gals[i] + "*tp2vis*.smooth")[0]
       image_tpmodel = glob.glob(dir_gals[i] + "*tpmodel*.smooth")[0]
       image_model = glob.glob(dir_gals[i] + "*skymodel_regrid.smooth")[0]
       #
       shape = imhead(image_7m,mode="list")["shape"]
       box = "0,0,"+str(shape[0]-1)+","+str(shape[1]-1)
       pixsize = abs(imhead(image_7m,mode="list")["cdelt1"])*180/np.pi*3600
       pixarea = pixsize**2
       #
       image_model = imval(image_model,box=box)["data"].flatten()
       image_model[np.isnan(image_model)] = 0
       diff_total_model = np.sum(image_model[image_model>0])
       #
       area = np.sqrt(pixarea * len(image_model[image_model>0]) / np.pi)
       #
       image_7m = imval(image_7m,box=box)["data"].flatten()
       image_7m[np.isnan(image_7m)] = 0
       diff_total_7m = (diff_total_model - np.sum(image_7m[image_7m>0])) / diff_total_model
       #
       image_feather = imval(image_feather,box=box)["data"].flatten()
       image_feather[np.isnan(image_feather)] = 0
       diff_total_feather = (diff_total_model - np.sum(image_feather[image_feather>0])) / diff_total_model
       #
       image_tp2vis = imval(image_tp2vis,box=box)["data"].flatten()
       image_tp2vis[np.isnan(image_tp2vis)] = 0
       diff_total_tp2vis = (diff_total_model - np.sum(image_tp2vis[image_tp2vis>0])) / diff_total_model
       #
       image_tpmodel = imval(image_tpmodel,box=box)["data"].flatten()
       image_tpmodel[np.isnan(image_tpmodel)] = 0
       diff_total_tpmodel = (diff_total_model - np.sum(image_tpmodel[image_tpmodel>0])) / diff_total_model
       #
       list_area.append(area)
       list_7m.append(diff_total_7m)
       list_feather.append(diff_total_feather)
       list_tp2vis.append(diff_total_tp2vis)
       list_tpmodel.append(diff_total_tpmodel)

list_median = np.c_[list_area,list_7m,list_feather,list_tp2vis,list_tpmodel]
np.savetxt("list_diff_total.txt",list_median,header="area 7m feather tp2vis tpmodel",fmt="%.3f")

os.system("rm -rf *.last")

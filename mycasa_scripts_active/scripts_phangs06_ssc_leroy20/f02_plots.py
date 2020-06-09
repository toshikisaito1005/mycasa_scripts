import os
import re
import sys
import glob
import scipy
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)


#####
dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
dir_gals = glob.glob(dir_data + "sim_*/")
dir_gals.sort()


for i in range(len(dir_gals)):
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
       #
       fidelity_7m = imval(fidelity_7m,box=box)
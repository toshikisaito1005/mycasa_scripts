import os
import sys
import glob
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
plt.ioff()


#####
dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/sim_phangs/"
dir_gals = glob.glob(dir_data + "sim_*/")
dir_gals.sort()


imagenames = glob.glob(dir_gals[i] + "*_br.smooth")
skymodel = glob.glob(dir_gals[i] + "*_skymodel_regrid.smooth")[0]
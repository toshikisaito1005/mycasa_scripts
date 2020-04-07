import os
import sys
import glob
import math
import numpy as np
import matplotlib.pyplot as plt
plt.ioff()

#####################
### parameters
#####################
dir_product = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/eps/"


#####################
### Main Procedure
#####################
data = np.loadtxt("ngc0628_stats_600pc.txt")
stats_n0628_no = data[0:5]
stats_n0628_wco10 = data[5:10]
stats_n0628_wco21 = data[10:15]


import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import matplotlib.ticker as ticker
plt.ioff()


#####################
### parameters
#####################
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/eps/"
galaxy = ["ngc0628","ngc3627","ngc4321"]


#####################
### functions
#####################



#####################
### Main Procedure
#####################
txtfiles = glob.glob(dir_data + "*_parameter_600pc.txt")



plt.figure(figsize=(10,0))
plt.rcParams["font.size"] = 14
gs = gridspec.GridSpec(nrows=5, ncols=15)
ax1 = plt.subplot(gs[0:5,0:5])
ax2 = plt.subplot(gs[0:5,5:10])
ax3 = plt.subplot(gs[0:5,10:15])


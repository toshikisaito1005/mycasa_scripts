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
dir_data = "/Users/saito/data/mycasa_scripts_active/scripts_ts09_phangs_r21/"


#####################
### functions
#####################



#####################
### Main Procedure
#####################
plt.figure(figsize=(10,0))
plt.rcParams["font.size"] = 14
gs = gridspec.GridSpec(nrows=9, ncols=16)
ax1 = plt.subplot(gs[1:7,0:4])
ax2 = plt.subplot(gs[1:7,4:8])
ax3 = plt.subplot(gs[1:7,8:12])
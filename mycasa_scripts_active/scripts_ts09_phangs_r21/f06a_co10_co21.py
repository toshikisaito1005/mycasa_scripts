import os
import sys
import glob
import math
import numpy as np
import scipy.optimize
from scipy.optimize import curve_fit
import matplotlib as mpl
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import matplotlib.patches as pat
import matplotlib.gridspec as gridspec
plt.ioff()


#####################
### parameters
#####################
dir_proj = "/Users/saito/data/myproj_active/proj_ts09_phangs_r21/"
gals = ["ngc0628",
        "ngc3627",
        "ngc4321"]
beam = [[4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0],
        [8.0,10.0,12.0,14.0,16.0,18.0,20.0,22.0,24.0],
        [4.0,6.0,8.0,10.0,12.0,14.0,16.0,18.0,20.0]]


#####################
### functions
#####################



#####################
### Main Procedure
#####################
i = 0
dir_co10 = dir_proj + gals[i]




### plot
plt.figure(figsize=(8,5))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(left=0.15, right=0.90, bottom=0.15, top=0.90)
ax1 = plt.subplot(1,1,1)


import os
import re
import sys
import glob
import scipy
import numpy as np
import matplotlib.cm as cm
import mycasaimaging_tools as myim
import matplotlib.pyplot as plt
plt.ioff()

reload(myim)


dir_data = "/Users/saito/data/myproj_active/proj_phangs06_ssc/eps/"


done = glob.glob(dir_data + "../../eps/")
if not done:
    os.mkdir(dir_data + "../../eps/")


#####################
### Main Procedure
#####################
data = np.loadtxt("list_median.txt")

fig = plt.figure(figsize=(12,4))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom=0.15, left=0.07, right=0.95, top=0.95)

median_7m, disp_7m = np.round(np.median(data[:,1]),1), np.round(np.std(data[:,1]),1)
label_7m = "7m-only (" + str(median_7m) + " $\pm$ " + str(disp_7m) + ")"

plt.scatter(data[:,0],
            data[:,1],
            color=cm.gnuplot(0/3.5), s=50, alpha=0.7, lw=1, label=label_7m)
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
### def
#####################
def plotter(
       txtdata,):

#####################
### Main Procedure
#####################
data = np.loadtxt("list_median.txt")
#
fig = plt.figure(figsize=(12,4))
plt.rcParams["font.size"] = 16
plt.subplots_adjust(bottom=0.15, left=0.07, right=0.95, top=0.95)
#
median_7m, disp_7m = np.round(np.median(data[:,1]),1), np.round(np.std(data[:,1]),1)
median_feather, disp_feather = np.round(np.median(data[:,2]),1), np.round(np.std(data[:,2]),1)
median_tp2vis, disp_tp2vis = np.round(np.median(data[:,3]),1), np.round(np.std(data[:,3]),1)
median_tpmodel, disp_tpmodel = np.round(np.median(data[:,4]),1), np.round(np.std(data[:,4]),1)
#
label_7m = "7m-only (" + str(median_7m) + " $\pm$ " + str(disp_7m) + ")"
label_feather = "feather (" + str(median_feather) + " $\pm$ " + str(disp_feather) + ")"
label_tp2vis = "tp2vis (" + str(median_tp2vis) + " $\pm$ " + str(disp_tp2vis) + ")"
label_tpmodel = "tpmodel (" + str(median_tpmodel) + " $\pm$ " + str(disp_tpmodel) + ")"
#
plt.scatter(data[:,0], data[:,1], color=cm.gnuplot(0/3.5), s=50, alpha=0.7, lw=1, label=label_7m)
plt.scatter(data[:,0], data[:,2], color=cm.gnuplot(1/3.5), s=50, alpha=0.7, lw=1, label=label_feather)
plt.scatter(data[:,0], data[:,3], color=cm.gnuplot(2/3.5), s=50, alpha=0.7, lw=1, label=label_tp2vis)
plt.scatter(data[:,0], data[:,4], color=cm.gnuplot(3/3.5), s=50, alpha=0.7, lw=1, label=label_tpmodel)
#
plt.savefig(dir_data + "fig_fidelity_vs_circ_diameter.png")

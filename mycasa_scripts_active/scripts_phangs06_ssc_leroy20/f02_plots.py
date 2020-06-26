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
       txtdata,
       output,
       ylim,
       ylabel,
       npround=2,
       ):
       data = np.loadtxt(txtdata)
       #
       fig = plt.figure(figsize=(15,4))
       plt.rcParams["font.size"] = 16
       plt.subplots_adjust(bottom=0.15, left=0.07, right=0.95, top=0.95)
       #
       median_7m, disp_7m = np.round(np.median(data[:,1]),npround), np.round(np.std(data[:,1]),npround)
       median_feather, disp_feather = np.round(np.mean(data[:,2]),npround), np.round(np.std(data[:,2]),npround)
       median_tp2vis, disp_tp2vis = np.round(np.mean(data[:,3]),npround), np.round(np.std(data[:,3]),npround)
       median_tpmodel, disp_tpmodel = np.round(np.mean(data[:,4]),npround), np.round(np.std(data[:,4]),npround)
       #
       plt.plot([0,300],[median_7m,median_7m],"--",c=cm.gnuplot(0/3.5),lw=2)
       plt.plot([0,300],[median_feather,median_feather],"--",c=cm.gnuplot(1/3.5),lw=2)
       plt.plot([0,300],[median_tp2vis,median_tp2vis],"--",c=cm.gnuplot(2/3.5),lw=2)
       plt.plot([0,300],[median_tpmodel,median_tpmodel],"--",c=cm.gnuplot(3/3.5),lw=2)
       #
       label_7m = "7m-only (" + str(median_7m) + " $\pm$ " + str(disp_7m) + ")"
       label_feather = "feather (" + str(median_feather) + " $\pm$ " + str(disp_feather) + ")"
       label_tp2vis = "tp2vis (" + str(median_tp2vis) + " $\pm$ " + str(disp_tp2vis) + ")"
       label_tpmodel = "tpmodel (" + str(median_tpmodel) + " $\pm$ " + str(disp_tpmodel) + ")"
       #
       plt.scatter(data[:,0]*2, data[:,1], color=cm.gnuplot(0/3.5), s=40, alpha=0.7, lw=1, marker="o", label=label_7m)
       plt.scatter(data[:,0]*2, data[:,2], color=cm.gnuplot(1/3.5), s=40, alpha=0.7, lw=1, marker="v", label=label_feather)
       plt.scatter(data[:,0]*2, data[:,3], color=cm.gnuplot(2/3.5), s=40, alpha=0.7, lw=1, marker="s", label=label_tp2vis)
       plt.scatter(data[:,0]*2, data[:,4], color=cm.gnuplot(3/3.5), s=40, alpha=0.7, lw=1, marker="D", label=label_tpmodel)
       #
       plt.xlabel("CO Size Diameter (arcsec)")
       plt.ylabel(ylabel)
       plt.xlim([0,300])
       plt.ylim(ylim)
       plt.legend(ncol=2)
       #plt.grid(axis="both")
       plt.savefig(output)


#####################
### Main Procedure
#####################
plotter("list_median.txt", dir_data+"ssc_fidelity_vs_size.png", [0.001,55], "Fidelity Median", 1)
plotter("list_diff_total.txt", dir_data+"ssc_diff_total_vs_size.png", [-0.3,1.7], "Total Flux Difference")
plotter("list_diff_peak.txt", dir_data+"ssc_diff_vs_size.png", [-0.3,1.7], "Peak Flux Difference")

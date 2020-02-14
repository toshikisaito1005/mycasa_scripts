import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt
sys.path.append(os.getcwd() + "/../../")
import mycasaanalysis_tools as myana

#####################
### Main Procedure
#####################
dir_data = "/Users/saito/data/ngc3110/ana/other/photmetry/"
plt.rcParams["font.size"] = 14


txt_data = "ngc3110_flux_uvlim.txt"
data = np.loadtxt(dir_data + txt_data, usecols = (0,1,2,3,4,5,6))
fl_12co10 = data[:,3]
fl_12co21 = data[:,4]
fl_13co10 = data[:,5]
fl_13co21 = data[:,6]

fl_13co10b = fl_13co10[fl_13co10 > 9.2] #Jy.km/s
fl_13co21b = fl_13co21[fl_13co10 > 9.2] #Jy.km/s
fl_12co10b = fl_12co10[fl_13co10 > 9.2] #Jy.km/s
fl_12co21b = fl_12co21[fl_13co10 > 9.2] #Jy.km/s

fl_13co10c =  fl_13co10b[fl_12co10b > 8.4] #Jy.km/s
fl_13co21c =  fl_13co21b[fl_12co10b > 8.4] #Jy.km/s
fl_12co10c =  fl_12co10b[fl_12co10b > 8.4] #Jy.km/s
fl_12co21c =  fl_12co21b[fl_12co10b > 8.4] #Jy.km/s

fl_13co10d =  fl_13co10c[fl_13co21c > 2.3] #Jy.km/s
fl_13co21d =  fl_13co21c[fl_13co21c > 2.3] #Jy.km/s
fl_12co10d =  fl_12co10c[fl_13co21c > 2.3] #Jy.km/s
fl_12co21d =  fl_12co21c[fl_13co21c > 2.3] #Jy.km/s

# Radex grids with NGC 3110 data points (21.5)
logNH2 = "21.5"
dir_eps = "../../ngc3110/ana/product/"
data1 = np.loadtxt("../scripts_radex/12co_1-0_2-1_21.5.dat",
                   usecols = (0, 1, 2))
data2 = np.loadtxt("../scripts_radex/13co_1-0_2-1_21.5.dat",
                   usecols = (0, 1, 2))
plt.figure()
plt.plot(data1[:,2][np.where(data1[:,0] == 5.)],
         data2[:,2][np.where(data1[:,0] == 5.)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 10.62)],
         data2[:,2][np.where(data1[:,0] == 10.62)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 14.35)],
         data2[:,2][np.where(data1[:,0] == 14.35)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 24.30)],
         data2[:,2][np.where(data1[:,0] == 24.30)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 64.66)],
         data2[:,2][np.where(data1[:,0] == 64.66)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 200.)],
         data2[:,2][np.where(data1[:,0] == 200.)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 2.)],
         data2[:,2][np.where(data1[:,1] == 2.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 3.)],
         data2[:,2][np.where(data1[:,1] == 3.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 3.5)],
         data2[:,2][np.where(data1[:,1] == 3.5)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 4.)],
         data2[:,2][np.where(data1[:,1] == 4.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 5.)],
         data2[:,2][np.where(data1[:,1] == 5.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(fl_12co21d/fl_12co10d,
         fl_13co21d/fl_13co10d, 'ro', markersize=12)
plt.text(0.5, 0.07, "$T_{kin}$ = 5 K")
plt.text(0.7, 0.15, "11 K")
plt.text(0.8, 0.23, "14 K")
plt.text(0.9, 0.31, "24 K")
plt.text(1.0, 0.4, "65 K")
plt.text(1.0, 1.0, "200 K")
plt.text(0.47, 0.2, "10$^{2.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.3, "10$^{3.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.4, "10$^{3.5}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.5, "10$^{4.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.6, "10$^{5.0}$ cm$^{-2}$", color="grey")
plt.xlim([0.45,1.1])
plt.ylim([0.,1.5])
plt.title("RADEX Grid @ log($N_{H_2}$/cm$^{-2}$) = " + logNH2)
plt.xlabel("$^{12}$CO(2-1)/$^{12}$CO(1-0) Ratio")
plt.ylabel("$^{13}$CO(2-1)/$^{13}$CO(1-0) Ratio")
plt.savefig(dir_eps + "plot_radex_" + logNH2 + ".eps", dpi=30)



# Radex grids with NGC 3110 data points (22.5)
logNH2 = "22.5"
dir_eps = "../../ngc3110/ana/product/"
data1 = np.loadtxt("../scripts_radex/12co_1-0_2-1_" + logNH2 + ".dat",
                   usecols = (0, 1, 2))
data2 = np.loadtxt("../scripts_radex/13co_1-0_2-1_" + logNH2 + ".dat",
                   usecols = (0, 1, 2))
plt.figure()
plt.plot(data1[:,2][np.where(data1[:,0] == 5.)],
         data2[:,2][np.where(data1[:,0] == 5.)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 10.62)],
         data2[:,2][np.where(data1[:,0] == 10.62)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 14.35)],
         data2[:,2][np.where(data1[:,0] == 14.35)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 24.30)],
         data2[:,2][np.where(data1[:,0] == 24.30)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 64.66)],
         data2[:,2][np.where(data1[:,0] == 64.66)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 200.)],
         data2[:,2][np.where(data1[:,0] == 200.)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 2.)],
         data2[:,2][np.where(data1[:,1] == 2.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 3.)],
         data2[:,2][np.where(data1[:,1] == 3.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 3.5)],
         data2[:,2][np.where(data1[:,1] == 3.5)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 4.)],
         data2[:,2][np.where(data1[:,1] == 4.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 5.)],
         data2[:,2][np.where(data1[:,1] == 5.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(fl_12co21d/fl_12co10d,
         fl_13co21d/fl_13co10d, 'ro', markersize=12)
plt.text(0.56, 0.2, "$T_{kin}$ = 5 K")
plt.text(0.78, 0.35, "11 K")
plt.text(0.85, 0.38, "14 K")
plt.text(0.92, 0.42, "24 K")
plt.text(1.03, 0.56, "65 K")
plt.text(0.6, 1.2, "200 K")
plt.text(0.47, 0.3, "10$^{2.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.4, "10$^{3.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.5, "10$^{3.5}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.6, "10$^{4.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.7, "10$^{5.0}$ cm$^{-2}$", color="grey")
plt.xlim([0.45,1.1])
plt.ylim([0.,1.5])
plt.title("RADEX Grid @ log($N_{H_2}$/cm$^{-2}$) = " + logNH2)
plt.xlabel("$^{12}$CO(2-1)/$^{12}$CO(1-0) Ratio")
plt.ylabel("$^{13}$CO(2-1)/$^{13}$CO(1-0) Ratio")
plt.savefig(dir_eps + "plot_radex_" + logNH2 + ".eps", dpi=30)



# Radex grids with NGC 3110 data points (22.0)
logNH2 = "22.0"
dir_eps = "../../ngc3110/ana/product/"
data1 = np.loadtxt("../scripts_radex/12co_1-0_2-1_" + logNH2 + ".dat",
                   usecols = (0, 1, 2))
data2 = np.loadtxt("../scripts_radex/13co_1-0_2-1_" + logNH2 + ".dat",
                   usecols = (0, 1, 2))
plt.figure()
plt.plot(data1[:,2][np.where(data1[:,0] == 5.)],
         data2[:,2][np.where(data1[:,0] == 5.)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 10.62)],
         data2[:,2][np.where(data1[:,0] == 10.62)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 14.35)],
         data2[:,2][np.where(data1[:,0] == 14.35)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 24.30)],
         data2[:,2][np.where(data1[:,0] == 24.30)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 64.66)],
         data2[:,2][np.where(data1[:,0] == 64.66)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,0] == 200.)],
         data2[:,2][np.where(data1[:,0] == 200.)],
         "-", c="black", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 2.)],
         data2[:,2][np.where(data1[:,1] == 2.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 3.)],
         data2[:,2][np.where(data1[:,1] == 3.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 3.5)],
         data2[:,2][np.where(data1[:,1] == 3.5)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 4.)],
         data2[:,2][np.where(data1[:,1] == 4.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(data1[:,2][np.where(data1[:,1] == 5.)],
         data2[:,2][np.where(data1[:,1] == 5.)],
         linestyle="dashed", c="grey", linewidth = 2.)
plt.plot(fl_12co21d/fl_12co10d,
         fl_13co21d/fl_13co10d, 'ro', markersize=12)
plt.text(0.56, 0.1, "$T_{kin}$ = 5 K")
plt.text(0.78, 0.25, "11 K")
plt.text(0.85, 0.28, "14 K")
plt.text(0.92, 0.32, "24 K")
plt.text(1.03, 0.46, "65 K")
plt.text(1.03, 1.3, "200 K")
plt.text(0.47, 0.2, "10$^{2.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.3, "10$^{3.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.4, "10$^{3.5}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.5, "10$^{4.0}$ cm$^{-2}$", color="grey")
plt.text(0.49, 0.6, "10$^{5.0}$ cm$^{-2}$", color="grey")
plt.xlim([0.45,1.1])
plt.ylim([0.,1.5])
plt.title("RADEX Grid @ log($N_{H_2}$/cm$^{-2}$) = " + logNH2)
plt.xlabel("$^{12}$CO(2-1)/$^{12}$CO(1-0) Ratio")
plt.ylabel("$^{13}$CO(2-1)/$^{13}$CO(1-0) Ratio")
plt.savefig(dir_eps + "plot_radex_" + logNH2 + ".eps", dpi=30)


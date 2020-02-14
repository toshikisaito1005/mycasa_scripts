import os
import sys
import re
import glob
import numpy as np
import scipy
import matplotlib.pyplot as plt
sys.path.append(os.getcwd() + "/../")
import mycasaanalysis_tools as myana

#####################
### Main Procedure
#####################
dir_data = "/Users/saito/data/ngc3110/ana/other/photmetry/"
plt.rcParams["font.size"] = 14


"""
# gas mass
txt_data = "rotation_diagram_gasmass.txt"
data = np.loadtxt(dir_data  + txt_data, usecols = (0,1,2))
plt.figure()
plt.legend()
plt.xlabel("Region")
plt.ylabel("$M_{H_2}$ (10$^{7}$ $M_{sun}$)")
plt.errorbar(data[:,0], data[:,1], yerr=data[:,2], linewidth=2)
plt.plot(data[:,0], data[:,1], 'bo')
plt.xlim([0,36])
plt.legend()
plt.savefig(dir_data + "../plot_gasmass.eps", dpi=300)


# SSC
txt_data = "number_SSC.txt"
data = np.loadtxt(dir_data  + txt_data, usecols = (0,1))
plt.figure()
plt.legend()
plt.xlabel("Region")
plt.ylabel("Number of SSC")
plt.plot(data[:,0], data[:,1], 'bo-')
plt.xlim([0,24])
plt.legend()
plt.savefig(dir_data + "../plot_SSC.eps", dpi=300)



#2-1/1-0
txt_data = "line_ratios.txt"
data = np.loadtxt(dir_data + txt_data, usecols = (0,1,2,3,4,5,6,7,8))
plt.figure()
plt.xlabel("Region")
plt.ylabel("$J$ = 2-1/$J$ = 1-0 Ratio")
plt.errorbar(data[:,0], data[:,1], linewidth = 2, yerr=data[:,2])
plt.plot(data[:,0], data[:,1], 'bo', label = "$^{12}$CO")
plt.errorbar(data[:,0], data[:,3], linewidth = 2, yerr=data[:,4],
             c = "r")
plt.plot(data[:,0], data[:,3], 'wo')
plt.plot(data[:,0][data[:,4] > 0.0],
         data[:,3][data[:,4] > 0.0], 'ro',label = "$^{13}$CO")
for i in range(len(data[:,4])):
    if data[:,4][i] == 0.0:
        plt.quiver(data[:,0][i], data[:,3][i], 0, 0.15,
                   color = "r",
                   width = 0.003,
                   angles = "xy",
                   scale_units= "xy",
                   scale = 1)
plt.legend()
plt.savefig(dir_data + "../plot_ratio_2110.eps", dpi=300)



#12/13
txt_data = "line_ratios.txt"
plt.figure()
plt.xlabel("Region")
plt.ylabel("$^{12}$CO/$^{13}$CO Ratio")
plt.errorbar(data[:,0], data[:,5], yerr=data[:,6], linewidth = 2)
plt.plot(data[:,0], data[:,5], 'wo')
plt.plot(data[:,0][data[:,6] > 0.0],
         data[:,5][data[:,6] > 0.0], 'bo', label = "$J$ = 1-0")
for i in range(len(data[:,6])):
    if data[:,6][i] == 0.0:
        plt.quiver(data[:,0][i], data[:,5][i], 0, 3.28125,
                   color = "b",
                   width = 0.003,
                   angles = "xy",
                   scale_units= "xy",
                   scale = 1)
plt.errorbar(data[:,0], data[:,7], linewidth = 2, yerr=data[:,8],
             c = "r")
plt.plot(data[:,0], data[:,7], 'wo')
plt.plot(data[:,0][data[:,8] > 0.0],
         data[:,7][data[:,8] > 0.0], 'ro', label = "$J$ = 2-1")
for i in range(len(data[:,8])):
    if data[:,8][i] == 0.0:
        plt.quiver(data[:,0][i], data[:,7][i], 0, 3.28125,
                   color = "r",
                   width = 0.003,
                   angles = "xy",
                   scale_units= "xy",
                   scale = 1)
plt.legend()
plt.savefig(dir_data + "../plot_ratio_12co13co.eps", dpi=300)
"""

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


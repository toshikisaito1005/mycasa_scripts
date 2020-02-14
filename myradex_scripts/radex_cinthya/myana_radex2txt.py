import os
import sys
import re
import glob
import numpy as np
import scipy
from pylab import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

#####################
### Main Procedure
#####################
logNH2 = ["22.26","21.95"]

for i in range(len(logNH2)):
    dir_eps = "/Users/saito/data/myradex_scripts/radex_cinthya/"
    data = np.loadtxt("/Users/saito/data/myradex_scripts/radex_cinthya/out_" + logNH2[i] + ".txt",
                      usecols = (0, 1, 2, 3, 4, 5, 6))
    #
    x, y, z1, z2 = data[:,0], data[:,1], data[:,2], data[:,3]
    z3, z4 = data[:,4], data[:,5]
    z5 = data[:,6]
    X = x.reshape(40, 40)
    Y = y.reshape(40, 40)
    Z1 = z1.reshape(40, 40) # CO(2-1)/CO(1-0) = 0.69 +/- 0.1
    Z2 = z2.reshape(40, 40) # CO(1-0)/13CO(1-0) = 7.2 +/- 1.0
    Z3 = z3.reshape(40, 40) # HCN(1-0)/13CO(1-0) = 0.2 +/- 0.03
    Z4 = z4.reshape(40, 40) # HCN(1-0)/HCO+(1-0) = 1.0 +/- 0.21
    Z5 = z5.reshape(40, 40) # HCN(1-0)/CO(2-1) = 0.04 +/- 0.008
    #
    fig = plt.figure()
    plt.rcParams["font.size"] = 12
    plt.subplots_adjust(bottom = 0.15)
    plt.gca().set_aspect('equal', adjustable='box')
    ax = plt.axes()
    plt.xscale('log')
    plt.title("RADEX Grid @ log($N_{H_2}$/cm$^{-2}$) = " + logNH2[i])
    plt.ylabel("$T_{kin}$ (K)")
    plt.xlabel("n$_{H_2}$ (cm$^{-3}$)")
    plt.ylim([0,120]) #plt.xlim([-10,280])
    # chi_square
    chi_1 = (0.69 - Z1) ** 2. / 0.1 ** 2.
    chi_2 = (7.2 - Z2) ** 2. / 1.0 ** 2.
    chi_3 = (0.2 - Z3) ** 2. / 0.03 ** 2.
    chi_4 = (1.0 - Z4) ** 2. / 0.21 ** 2.
    chi_5 = (0.04 - Z5) ** 2. / 0.008 ** 2.
    chi_low = chi_1 + chi_2
    chi_high = chi_3 + chi_4
    chi_old = chi_4 + chi_5
    chi_final = chi_5 + chi_3 + chi_2
    #cont = plt.contourf(Y, X, chi_final, levels=[.0,5.99146], colors="skyblue", linewidths = 1.)
    #cont = plt.contourf(Y, X, chi_high, levels=[.0,3.84], colors="pink", linewidths = 1.)
    #cont = plt.contourf(Y, X, chi_old, levels=[.0,3.84], colors="pink", linewidths = 1.)
    plt.plot(Y[np.where(chi_final==chi_final.min())[0],np.where(chi_final==chi_final.min())[1]], X[np.where(chi_final==chi_final.min())[0],np.where(chi_final==chi_final.min())[1]], "D",
             markersize=15, color="grey")
    #plt.plot(Y[np.where(chi_high==chi_high.min())[0],np.where(chi_high==chi_high.min())[1]], X[np.where(chi_high==chi_high.min())[0],np.where(chi_high==chi_high.min())[1]], "D",
    #         markersize=10, color="red")
    #plt.plot(Y[np.where(chi_old==chi_old.min())[0],np.where(chi_old==chi_old.min())[1]], X[np.where(chi_old==chi_old.min())[0],np.where(chi_old==chi_old.min())[1]], "D",
    #         markersize=10, color="red")
    ### CO(2-1)/CO(1-0)
    #cont = plt.contour(Y, X, Z1, levels=[0.69], colors="blue")
    #cont.clabel(fmt='%1.2f', fontsize=14)
    #cont = plt.contour(Y, X, Z1, levels=[0.69-0.1,0.69+0.1],
    #                   colors="blue",
    #                   linewidths = 0.5, linestyles = "dashed")
    ### CO(1-0)/13CO(1-0)
    cont = plt.contour(Y, X, Z2, levels=[7.2], colors="green")
    cont.clabel(fmt='%1.2f', fontsize=12, inline=True)
    cont = plt.contour(Y, X, Z2, levels=[7.2-1.0,7.2+1.0],
                       colors="green",
                       linewidths = 0.5, linestyles = "dashed")
    ### HCN(1-0)/13CO(1-0)
    cont = plt.contour(Y, X, Z3, levels=[0.2], colors="blue")
    cont.clabel(fmt='%1.2f', fontsize=12, inline=True)
    cont = plt.contour(Y, X, Z3, levels=[0.2-0.03,0.2+0.03],
                       colors="blue",
                       linewidths = 0.5, linestyles = "dashed")
    ### HCN(1-0)/HCO+(1-0)
    #cont = plt.contour(Y, X, Z4, levels=[1.0], colors="red")
    #cont.clabel(fmt='%1.2f', fontsize=14)
    #cont = plt.contour(Y, X, Z4, levels=[1.0-0.21,1.0+0.21],
    #                   colors="red",
    #                   linewidths = 0.5, linestyles = "dashed")
    ### HCN(1-0)/CO(2-1)
    cont = plt.contour(Y, X, Z5, levels=[0.04], colors="red")
    cont.clabel(fmt='%1.2f', fontsize=12, inline=True)
    cont = plt.contour(Y, X, Z5, levels=[0.04-0.008,0.04+0.008],
                       colors="red",
                       linewidths = 0.5, linestyles = "dashed")

    # label
    #red_patch = mpatches.Patch(color="red",
    #                           label="HCN(1-0)/HCO$^+$(1-0)")
    grey_patch = mpatches.Patch(color="red",
                                label="HCN(1-0)/CO(2-1)")
    black_patch = mpatches.Patch(color="blue",
                                 label="HCN(1-0)/$^{13}$CO(1-0)")
    green_patch = mpatches.Patch(color="green",
                                 label="CO(1-0)/$^{13}$CO(1-0)")
    #blue_patch = mpatches.Patch(color="blue",
    #                            label="CO(2-1)/CO(1-0)")
    plt.legend(handles=[grey_patch,black_patch,
                        green_patch],
               loc="upper right")
    
    plt.savefig(dir_eps + "plot_radex_" + logNH2[i] + ".eps", dpi=300)
    print(Y[np.where(chi_high==chi_high.min())[0],np.where(chi_high==chi_high.min())[1]], X[np.where(chi_high==chi_high.min())[0],np.where(chi_high==chi_high.min())[1]])
